function showAlert(message, type = "info") {
    let alertBox = document.createElement("div");
    alertBox.className = `alert alert-${type} position-fixed top-0 end-0 m-3`;
    alertBox.innerText = message;

    document.body.appendChild(alertBox);

    setTimeout(() => alertBox.remove(), 4000);
}

function showAlert(message, type = "info") {
    let alertBox = document.createElement("div");
    alertBox.className = `alert alert-${type} position-fixed top-0 end-0 m-3 shadow`;
    alertBox.style.zIndex = "9999";
    alertBox.innerText = message;

    document.body.appendChild(alertBox);

    setTimeout(() => alertBox.remove(), 5000);
}

// Attack popup
function attackPopup(attack, severity) {
    let type = "info";
    if (severity === "HIGH") type = "danger";
    else if (severity === "MEDIUM") type = "warning";
    else type = "success";

    showAlert(`⚠️ ${attack} attack detected (${severity})`, type);
}