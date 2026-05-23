document.querySelectorAll('a[href*="#"]').forEach(anchor => {
  anchor.addEventListener("click", function(e) {
    const url = new URL(this.getAttribute("href"), window.location.href);
    const samePage = url.pathname === window.location.pathname;

    if (!samePage || !url.hash) return;

    e.preventDefault();

    const target = document.querySelector(url.hash);
    if (!target) return;

    target.scrollIntoView({ behavior: "smooth" });

    const navPanel = document.querySelector(".nav-panel");
    const menuToggle = document.querySelector(".menu-toggle");
    navPanel?.classList.remove("open");
    menuToggle?.setAttribute("aria-expanded", "false");
  });
});
