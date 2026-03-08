import csv
import io
import random

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count
from django.utils.timezone import now, timedelta

from .models import DetectionResult, PasswordResetOTP
from .alerts import send_otp_email, send_attack_alert_bulk


# ================= AUTH =================

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        if user:
            login(request, user)
            return redirect('dashboard')

        messages.error(request, "Invalid username or password")

    return render(request, 'auth/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')

        if password != confirm:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'auth/register.html')


# ================= DASHBOARD =================

@login_required
def dashboard(request):
    detections = DetectionResult.objects.filter(user=request.user)

    attack_stats = detections.values('attack_type').annotate(total=Count('id'))

    normal_count = detections.filter(attack_type__iexact="normal").count()
    attack_count = detections.exclude(attack_type__iexact="normal").count()

    total_records = detections.count()
    sensitivity = attack_count / total_records if total_records > 0 else 0

    return render(request, "nids_dashboard/dashboard.html", {
        "detections": detections,
        "attack_stats": attack_stats,
        "normal_count": normal_count,
        "attack_count": attack_count,
        "sensitivity": round(sensitivity, 2)
    })


# ================= CSV UPLOAD =================

@login_required
def upload_csv(request):
    from .ml.predict import detect_attack

    if request.method == "POST":
        csv_file = request.FILES.get("csv_file")

        if not csv_file or not csv_file.name.endswith(".csv"):
            messages.error(request, "Please upload a valid CSV file")
            return redirect("upload")

        try:
            text_file = io.TextIOWrapper(csv_file.file, encoding="utf-8", errors="ignore")
            reader = csv.reader(text_file)

            next(reader, None)  # ✅ Skip header row

            total = 0
            attacks = []
            TP = 0
            FN = 0

            for row in reader:
                if not row:
                    continue

                # Expect 10 features + 1 label
                if len(row) != 11:
                    print("Skipping invalid row:", row)
                    continue

                total += 1

                actual_label = row[-1].strip().lower()

                # Only first 10 columns to model
                result = detect_attack(row[:10])

                attack_type = result.get("attack", "Normal")
                severity = result.get("severity", "Low")
                confidence = float(result.get("confidence", 0.0))

                DetectionResult.objects.create(
                    user=request.user,
                    attack_type=attack_type,
                    severity=severity,
                    confidence=confidence
                )

                if attack_type.lower() != "normal":
                    attacks.append(attack_type)

                # Sensitivity calculation
                if actual_label != "normal" and attack_type.lower() != "normal":
                    TP += 1
                elif actual_label != "normal" and attack_type.lower() == "normal":
                    FN += 1

            sensitivity = TP / (TP + FN) if (TP + FN) > 0 else 0

            # Send alert only if attacks found
            if attacks:
                send_attack_alert(f"""
🚨 NIDS ALERT 🚨
User: {request.user.username}
Total Records: {total}
Attack Count: {len(attacks)}
Attack Types: {list(set(attacks))}
Sensitivity: {sensitivity:.2f}
Time: {now()}
""")

            messages.success(
                request,
                f"CSV processed successfully | Total: {total} | Attacks: {len(attacks)} | Sensitivity: {sensitivity:.2f}"
            )

        except Exception as e:
            print("CSV Processing Error:", e)
            messages.error(request, "Error processing CSV file")

        return redirect("dashboard")

    return render(request, "nids_dashboard/upload.html")


# ================= ATTACK LOGS =================

@login_required
def attack_logs(request):
    results = DetectionResult.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'nids_dashboard/attack_logs.html', {'results': results})


@login_required
def attack_stats(request):
    stats = DetectionResult.objects.filter(user=request.user) \
        .values('attack_type') \
        .annotate(total=Count('id'))
    return render(request, 'nids_dashboard/attack_stats.html', {'stats': stats})


@login_required
def about_page(request):
    return render(request, 'nids_dashboard/about.html')


# ================= DELETE DETECTION =================

@login_required
def delete_detection(request, id):
    detection = get_object_or_404(DetectionResult, id=id, user=request.user)
    detection.delete()
    messages.success(request, "Detection record deleted successfully")
    return redirect('dashboard')


# ================= PASSWORD RESET OTP =================

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if not user:
            messages.error(request, "Email not registered")
            return redirect('forgot')

        PasswordResetOTP.objects.filter(user=user).delete()

        otp = str(random.randint(100000, 999999))
        PasswordResetOTP.objects.create(user=user, otp=otp)

        send_otp_email(user, otp)

        request.session['reset_user'] = user.id
        return redirect('verify_otp')

    return render(request, 'auth/forgot.html')


def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        user_id = request.session.get('reset_user')

        record = PasswordResetOTP.objects.filter(
            user_id=user_id,
            otp=otp,
            created_at__gte=now() - timedelta(minutes=5)
        ).first()

        if record:
            request.session['otp_verified'] = True
            return redirect('reset_password')

        messages.error(request, "Invalid or expired OTP")

    return render(request, 'auth/verify_otp.html')


def reset_password(request):
    if not request.session.get('otp_verified'):
        return redirect('login')

    if request.method == 'POST':
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')

        if password != confirm:
            messages.error(request, "Passwords do not match")
            return redirect('reset_password')

        user_id = request.session.get('reset_user')
        user = User.objects.get(id=user_id)
        user.set_password(password)
        user.save()

        request.session.flush()

        messages.success(request, "Password reset successful")
        return redirect('login')

    return render(request, 'auth/reset_password.html')