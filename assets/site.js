(() => {
  const form = document.querySelector("[data-watch-filters]");
  if (!form) return;
  const cards = [...document.querySelectorAll("#watch-results .watch-card")];
  const count = document.querySelector("[data-watch-count]");
  const update = () => {
    const query = form.elements.query.value.trim().toLowerCase();
    const theme = form.elements.theme.value;
    const source = form.elements.source.value;
    let shown = 0;
    cards.forEach((card) => {
      const matches = (!query || card.textContent.toLowerCase().includes(query)) &&
        (!theme || card.dataset.theme.split(" ").includes(theme)) &&
        (!source || card.dataset.source === source);
      card.hidden = !matches;
      if (matches) shown += 1;
    });
    count.textContent = `${shown} item${shown === 1 ? "" : "s"} shown`;
  };
  form.addEventListener("input", update);
  form.addEventListener("reset", () => setTimeout(update));
  update();
})();
