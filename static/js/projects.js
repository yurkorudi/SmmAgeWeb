document.querySelectorAll(".project-filters button").forEach(button => {
  button.addEventListener("click", () => {
    document.querySelectorAll(".project-filters button").forEach(item => item.classList.toggle("active", item === button));
    document.querySelectorAll(".project-catalog .project-card").forEach(card => {
      card.hidden = card.dataset.category !== button.dataset.filter;
    });
  });
});
