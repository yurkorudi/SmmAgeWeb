const DEFAULT_LANGUAGE = "uk";
const LANGUAGE_STORAGE_KEY = "smmage-language";
const sourceTexts = new Map();
let translationCache = {};

const menuToggle = document.querySelector(".menu-toggle");
const navPanel = document.querySelector(".nav-panel");

menuToggle?.addEventListener("click", () => {
  const isOpen = navPanel.classList.toggle("open");
  menuToggle.setAttribute("aria-expanded", String(isOpen));
});

function collectSourceTexts() {
  document.querySelectorAll("[data-i18n]").forEach(element => {
    if (!sourceTexts.has(element.dataset.i18n)) {
      sourceTexts.set(element.dataset.i18n, element.textContent.trim());
    }
  });
}

async function loadTranslations(lang) {
  if (lang === DEFAULT_LANGUAGE) {
    return {};
  }

  if (!translationCache[lang]) {
    const response = await fetch(`/static/i18n/${lang}.json`, { cache: "no-cache" });
    translationCache[lang] = response.ok ? await response.json() : {};
  }

  return translationCache[lang];
}

async function setLanguage(lang) {
  const selectedLang = lang || DEFAULT_LANGUAGE;
  const dictionary = await loadTranslations(selectedLang);
  document.documentElement.lang = selectedLang;

  document.querySelectorAll("[data-i18n]").forEach(element => {
    const key = element.dataset.i18n;
    element.textContent = dictionary[key] || sourceTexts.get(key) || element.textContent;
  });

  document.querySelectorAll(".lang-btn").forEach(button => {
    button.classList.toggle("active", button.dataset.lang === selectedLang);
  });

  localStorage.setItem(LANGUAGE_STORAGE_KEY, selectedLang);
  window.dispatchEvent(new CustomEvent("languagechange", { detail: { lang: selectedLang } }));
}

document.querySelectorAll(".lang-btn").forEach(button => {
  button.addEventListener("click", () => setLanguage(button.dataset.lang));
});

collectSourceTexts();
setLanguage(localStorage.getItem(LANGUAGE_STORAGE_KEY) || DEFAULT_LANGUAGE);
