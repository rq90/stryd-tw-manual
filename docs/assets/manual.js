// The complete manual stays readable as one document when scripts are disabled.
const home = document.getElementById("home");
const reading = document.querySelector(".reading");
const chapters = [...document.querySelectorAll(".chapter")];
const menu = document.querySelector(".mobile-menu");
const chapterLinks = [...document.querySelectorAll("aside nav a")];
const rows = [...document.querySelectorAll("#watch tbody tr")];
const select = document.getElementById("brand-select");
for (const row of rows) {
  const brand = row.querySelector("th a");
  if (![...select.options].some((option) => option.value === brand.hash)) {
    select.add(new Option(brand.textContent, brand.hash));
  }
}
select.addEventListener("change", () => {
  for (const row of rows) {
    row.hidden = Boolean(select.value && row.querySelector("th a").hash !== select.value);
  }
  document.getElementById("filter-status").textContent = "顯示 " + rows.filter(row => !row.hidden).length + " 組錶款";
});
document.getElementById("watch-filter").hidden = false;

function showPage(focusHeading) {
  const target = document.getElementById(location.hash.slice(1));
  const chapter = target?.closest(".chapter");
  home.hidden = Boolean(chapter);
  reading.hidden = !chapter;
  for (const page of chapters) page.hidden = page !== chapter;
  for (const link of chapterLinks) {
    if (chapter && link.hash === "#" + chapter.id) link.setAttribute("aria-current", "page");
    else link.removeAttribute("aria-current");
  }
  menu.open = false;
  const heading = chapter?.querySelector("h2") ?? document.getElementById("home-title");
  const innerTarget = chapter && target !== chapter ? target : null;
  const detail = innerTarget?.closest("details");
  if (detail) detail.open = true;
  document.title = chapter ? heading.textContent + "｜Stryd 台灣手冊" : "Stryd 台灣｜安裝與使用手冊";
  if (innerTarget) {
    const focusTarget = innerTarget.matches("details") ? innerTarget.querySelector("summary") : innerTarget;
    if (focusHeading) {
      if (!focusTarget.hasAttribute("tabindex")) focusTarget.tabIndex = -1;
      focusTarget.focus({preventScroll: true});
    }
    innerTarget.scrollIntoView();
  } else {
    if (focusHeading) heading.focus({preventScroll: true});
    window.scrollTo(0, 0);
  }
}
window.addEventListener("hashchange", () => showPage(true));
document.addEventListener("click", (event) => {
  const link = event.target.closest("a");
  if (link?.getAttribute("href") === "#main") {
    event.preventDefault();
    document.getElementById("main").focus();
  } else if (link?.getAttribute("href")?.startsWith("#") && link.hash === location.hash) {
    event.preventDefault();
    showPage(true);
  }
});
showPage(false);
