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
