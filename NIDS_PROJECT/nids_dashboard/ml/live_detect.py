import pyshark
import numpy as np
from predict import detect_attack

# Choose your network interface
INTERFACE = "Wi-Fi"  # change to your interface name

# Function to extract features from a packet
def extract_features(packet):
    """
    Extract numeric features from live packet.
    Adjust features according to your trained model.
    """
    try:
        length = int(packet.length)
        tcp_syn = int(packet.tcp.flags_syn) if hasattr(packet, "tcp") else 0
        tcp_ack = int(packet.tcp.flags_ack) if hasattr(packet, "tcp") else 0
        udp_flag = int(packet.highest_layer == "UDP")
        # Add more features as per your model
        return [length, tcp_syn, tcp_ack, udp_flag]
    except:
        # Skip packets that can't be processed
        return None

# Start live capture
capture = pyshark.LiveCapture(interface=INTERFACE)

print(f"Listening on {INTERFACE}... Press Ctrl+C to stop.")

for packet in capture.sniff_continuously():
    features = extract_features(packet)
    if features is None:
        continue

    label, confidence = detect_attack(features)
    if label == "Attack":
        print(f"⚠️ Attack detected! Confidence: {confidence:.2f}")
    else:
        print(f"Normal packet detected. Confidence: {confidence:.2f}")
