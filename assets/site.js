(() => {
  const form = document.querySelector("[data-conversation-filters]");
  if (form) {
    const cards = [...document.querySelectorAll("#conversation-results .conversation-card")];
    const count = document.querySelector("[data-conversation-count]");
    const update = () => {
      const query = form.elements.query.value.trim().toLowerCase();
      const theme = form.elements.theme.value;
      const environment = form.elements.environment.value;
      const geography = form.elements.geography.value;
      const kind = form.elements.kind.value;
      const since = form.elements.since.value;
      let shown = 0;
      cards.forEach((card) => {
        const matches = (!query || card.textContent.toLowerCase().includes(query)) &&
          (!theme || (theme === "__unclassified__" ? !card.dataset.theme : card.dataset.theme.split(" ").includes(theme))) &&
          (!environment || card.dataset.environment.split(" ").includes(environment)) &&
          (!geography || card.dataset.geography.split(" ").includes(geography)) &&
          (!kind || card.dataset.kind === kind) && (!since || card.dataset.date >= since);
        card.hidden = !matches;
        if (matches) shown += 1;
      });
      count.textContent = `${shown} entr${shown === 1 ? "y" : "ies"} shown`;
    };
    form.addEventListener("input", update);
    form.addEventListener("reset", () => setTimeout(update));
    update();
  }

  const publicationForm = document.querySelector("[data-publication-filters]");
  if (!publicationForm) return;
  const entries = [...document.querySelectorAll(".bibliography-entry")];
  const publicationCount = document.querySelector("[data-publication-count]");
  const updatePublications = () => {
    const query = publicationForm.elements.query.value.trim().toLowerCase();
    const type = publicationForm.elements.type.value;
    let shown = 0;
    entries.forEach((entry) => {
      const matches = (!query || entry.textContent.toLowerCase().includes(query)) && (!type || entry.dataset.type === type);
      entry.hidden = !matches;
      if (matches) shown += 1;
    });
    publicationCount.textContent = `${shown} record${shown === 1 ? "" : "s"} shown`;
  };
  publicationForm.addEventListener("input", updatePublications);
  publicationForm.addEventListener("reset", () => setTimeout(updatePublications));
  updatePublications();
})();
