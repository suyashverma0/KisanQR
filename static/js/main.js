// ================= MOBILE NAVBAR TOGGLE =================

const navToggle = document.getElementById("navToggle");
const navLinks = document.getElementById("navLinks");

if (navToggle && navLinks) {
    navToggle.addEventListener("click", function () {
        navLinks.classList.toggle("open");
    });
}

// ================= AUTO-DISMISS FLASH MESSAGES =================

document.querySelectorAll(".alert").forEach(function (alertBox) {
    setTimeout(function () {
        alertBox.style.transition = "opacity 0.4s ease";
        alertBox.style.opacity = "0";
        setTimeout(function () {
            alertBox.remove();
        }, 400);
    }, 6000);
});
