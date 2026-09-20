const revealItems = document.querySelectorAll(".reveal");

if ("IntersectionObserver" in window) {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.14 });

  revealItems.forEach(item => observer.observe(item));
} else {
  revealItems.forEach(item => item.classList.add("is-visible"));
}

document.querySelectorAll(".contact-form").forEach(form => {
  form.addEventListener("submit", () => {
    const button = form.querySelector("button[type='submit']");
    if (!button || !form.checkValidity()) return;
    button.disabled = true;
    button.textContent = "Надсилаємо…";
    button.setAttribute("aria-busy", "true");
  });
});

const mobilePreviewWidth = 390;
const mobilePreviewHeight = 844;

function resizeWebsitePreviews() {
  document.querySelectorAll(".phone-screen").forEach(screen => {
    const viewport = screen.querySelector(".website-viewport");
    const iframe = screen.querySelector(".website-iframe");
    if (!viewport || !iframe) return;

    const availableWidth = screen.clientWidth;
    const availableHeight = screen.clientHeight;
    if (!availableWidth || !availableHeight) return;

    const scaleX = availableWidth / mobilePreviewWidth;
    const scaleY = availableHeight / mobilePreviewHeight;
    const scale = Math.min(scaleX, scaleY);

    iframe.style.setProperty("--scale", scale);
    viewport.style.width = `${mobilePreviewWidth * scale}px`;
    viewport.style.height = `${mobilePreviewHeight * scale}px`;
  });
}

resizeWebsitePreviews();
window.addEventListener("load", resizeWebsitePreviews);
window.addEventListener("resize", resizeWebsitePreviews);

if ("ResizeObserver" in window) {
  const websitePreviewObserver = new ResizeObserver(resizeWebsitePreviews);
  document.querySelectorAll(".phone-screen").forEach(screen => {
    websitePreviewObserver.observe(screen);
  });
}
