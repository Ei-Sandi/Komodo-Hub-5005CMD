document.addEventListener("DOMContentLoaded", function () {
    // Search functionality
    function searchReports() {
        let input = document.getElementById('search').value.toLowerCase();
        let reports = document.getElementsByClassName('report');

        for (let i = 0; i < reports.length; i++) {
            let reportText = reports[i].innerText.toLowerCase();
            reports[i].style.display = reportText.includes(input) ? "flex" : "none";
        }
    }
    document.getElementById('search').addEventListener("keyup", searchReports);

    // Expand/Collapse Report Details
    document.querySelectorAll(".toggle-details").forEach(button => {
        button.addEventListener("click", function () {
            let extraDetails = this.previousElementSibling;
            if (extraDetails.style.display === "block") {
                extraDetails.style.display = "none";
                this.textContent = "Show More";
            } else {
                extraDetails.style.display = "block";
                this.textContent = "Show Less";
            }
        });
    });

    // Modal Functionality
    let modal = document.getElementById("modal");
    document.getElementById("loginBtn").addEventListener("click", () => modal.style.display = "block");
    document.getElementById("registerBtn").addEventListener("click", () => modal.style.display = "block");
    document.querySelector(".close").addEventListener("click", () => modal.style.display = "none");

    // Dark Mode Toggle
    let darkModeButton = document.getElementById("darkModeToggle");
    darkModeButton.addEventListener("click", function () {
        document.body.classList.toggle("dark-mode");
    });

    // Active Navigation Highlight
    document.querySelectorAll(".nav-link").forEach(link => {
        link.addEventListener("click", function () {
            document.querySelectorAll(".nav-link").forEach(l => l.classList.remove("active"));
            this.classList.add("active");
        });
    });
});
