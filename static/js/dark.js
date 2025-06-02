
  const toggleBtn = document.getElementById("themeToggle");
  const darkTheme = document.getElementById("darkTheme");
  const icon = toggleBtn.querySelector("i");

  toggleBtn.addEventListener("click", () => {
    const isDark = !darkTheme.disabled;
    darkTheme.disabled = isDark;

    // Update icon
    icon.className = isDark ? "bi bi-moon-stars-fill fs-5" : "bi bi-sun-fill fs-5";

    // Optionally: save preference
    localStorage.setItem("theme", isDark ? "light" : "dark");
  });

  // Load saved theme preference on page load
  window.addEventListener("DOMContentLoaded", () => {
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme === "dark") {
      darkTheme.disabled = false;
      icon.className = "bi bi-sun-fill fs-5";
    }
  });

