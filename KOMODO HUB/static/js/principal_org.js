document.getElementById("code").onclick = async function () {
    const accessCode = generateCode();

    try {
        const response = await fetch('/save_access_code', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ access_code: accessCode })
        });

        const data = await response.json();
        alert(data.message); // Show Flask response as alert
        window.location.reload();
    } catch (error) {
        console.error("Error sending access code:", error);
        alert("Failed to send access code.");
    }
};

function generateCode() {
    const characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    let accessCode = "";
    for (let i = 0; i < 5; i++) {
        accessCode += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    return accessCode;
}