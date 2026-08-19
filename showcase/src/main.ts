import { EgyNames } from "./engine";
import { DICTIONARY, Lang } from "./i18n/translations";
import { initChainAiView, rerunChainAi } from "./modules/chainAiView";
import { initCodePlayground } from "./modules/codePlayground";
import { initCorrectorView } from "./modules/correctorView";
import { initGeneratorView } from "./modules/generatorView";
import { initInspectorView, rerunInspector } from "./modules/inspectorView";
import { initSearchView, rerunSearch } from "./modules/searchView";
import { initSplitterView, rerunSplitter } from "./modules/splitterView";
import { initTranslatorView } from "./modules/translatorView";
import "./styles/animations.css";
import "./styles/components.css";
import "./styles/main.css";

const engine = new EgyNames();
let currentLang: Lang = (localStorage.getItem("egy_names_lang") as Lang) || "en";
let currentTheme: "dark" | "light" =
  (localStorage.getItem("egy_names_theme") as "dark" | "light") || "dark";

export function getLang(): Lang {
  return currentLang;
}

export function showToast(message: string): void {
  const toast = document.getElementById("app-toast");
  if (!toast) return;
  toast.textContent = message;
  toast.classList.add("show");
  setTimeout(() => {
    toast.classList.remove("show");
  }, 2400);
}

function applyTheme(theme: "dark" | "light") {
  currentTheme = theme;
  document.documentElement.setAttribute("data-theme", theme);
  localStorage.setItem("egy_names_theme", theme);

  const themeLabel = document.getElementById("theme-label");
  const themeSvg = document.getElementById("theme-icon-svg");

  if (themeLabel) {
    if (theme === "dark") {
      themeLabel.textContent = currentLang === "ar" ? "فاتح" : "Light";
      if (themeSvg) {
        themeSvg.innerHTML = `<circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/>`;
      }
    } else {
      themeLabel.textContent = currentLang === "ar" ? "داكن" : "Dark";
      if (themeSvg) {
        themeSvg.innerHTML = `<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>`;
      }
    }
  }
}

function applyLanguage(lang: Lang) {
  currentLang = lang;
  document.documentElement.lang = lang;
  document.documentElement.dir = lang === "ar" ? "rtl" : "ltr";
  localStorage.setItem("egy_names_lang", lang);

  const dict = DICTIONARY[lang];

  // Update all data-i18n elements
  const elements = document.querySelectorAll<HTMLElement>("[data-i18n]");
  elements.forEach((el) => {
    const key = el.dataset.i18n as keyof typeof dict;
    if (key && dict[key] && typeof dict[key] === "string") {
      el.textContent = dict[key] as string;
    }
  });

  // Update Language button label
  const langLabel = document.getElementById("lang-label");
  if (langLabel) {
    langLabel.textContent = lang === "ar" ? "English" : "العربية";
  }

  // Update Theme toggle button text for current lang
  applyTheme(currentTheme);

  // Update Placeholders
  const arTransInput = document.getElementById("trans-ar-input") as HTMLInputElement;
  if (arTransInput) arTransInput.placeholder = dict.arInputPlaceholder;

  const enTransInput = document.getElementById("trans-en-input") as HTMLInputElement;
  if (enTransInput) enTransInput.placeholder = dict.enInputPlaceholder;

  const splitInput = document.getElementById("split-input") as HTMLInputElement;
  if (splitInput) splitInput.placeholder = dict.splitPlaceholder;

  const inspectInput = document.getElementById("inspect-input") as HTMLInputElement;
  if (inspectInput) inspectInput.placeholder = dict.inspectPlaceholder;

  const correctInput = document.getElementById("correct-input") as HTMLInputElement;
  if (correctInput) correctInput.placeholder = dict.correctPlaceholder;

  const chainInput = document.getElementById("chain-input") as HTMLInputElement;
  if (chainInput) chainInput.placeholder = dict.chainPlaceholder;

  // Rerun active views for dynamic translations
  rerunSplitter();
  rerunChainAi();
  rerunInspector();
  rerunSearch();
}

async function bootstrap() {
  const loader = document.getElementById("app-loader");
  const loaderSub = document.getElementById("loader-sub");

  // Apply initial theme & language
  applyTheme(currentTheme);
  applyLanguage(currentLang);

  // Bind Theme Toggle
  const themeBtn = document.getElementById("btn-theme-toggle");
  themeBtn?.addEventListener("click", () => {
    applyTheme(currentTheme === "dark" ? "light" : "dark");
  });

  // Bind Language Toggle
  const langBtn = document.getElementById("btn-lang-toggle");
  langBtn?.addEventListener("click", () => {
    applyLanguage(currentLang === "en" ? "ar" : "en");
  });

  try {
    if (loaderSub) loaderSub.textContent = "Loading 33,117 verified lemmas from dataset...";
    await engine.init("/names.json.gz");

    // Populate Hero Stats
    const stats = engine.stats();
    const statNames = document.getElementById("stat-total-names");
    const statTokens = document.getElementById("stat-total-tokens");
    const statStudents = document.getElementById("stat-total-students");
    const statKeys = document.getElementById("stat-total-keys");

    if (statNames) statNames.textContent = stats.total_names.toLocaleString();
    if (statTokens) statTokens.textContent = (stats.corpus_tokens / 1000000).toFixed(1) + "M+";
    if (statStudents) statStudents.textContent = (stats.corpus_students / 1000000).toFixed(2) + "M";
    if (statKeys) statKeys.textContent = "134,000+";

    // Setup Tab Navigation
    const tabBtns = document.querySelectorAll<HTMLButtonElement>(".tab-btn");
    const tabPanels = document.querySelectorAll<HTMLElement>(".tab-panel");

    tabBtns.forEach((btn) => {
      btn.addEventListener("click", () => {
        const targetTab = btn.dataset.tab;
        tabBtns.forEach((b) => b.classList.remove("active"));
        tabPanels.forEach((p) => p.classList.remove("active"));

        btn.classList.add("active");
        const panel = document.getElementById(targetTab || "");
        if (panel) {
          panel.classList.add("active");
        }
      });
    });

    // Setup Install Button Copy
    const installBtn = document.getElementById("btn-install-cmd");
    if (installBtn) {
      installBtn.addEventListener("click", () => {
        navigator.clipboard.writeText("pip install egy-names # or npm install egy-names");
        showToast(DICTIONARY[currentLang].installCopied);
      });
    }

    // Initialize all interactive views
    initGeneratorView(engine, showToast);
    initTranslatorView(engine, showToast);
    initSplitterView(engine, showToast);
    initInspectorView(engine, showToast);
    initCorrectorView(engine, showToast);
    initChainAiView(engine, showToast);
    initSearchView(engine, showToast);
    initCodePlayground(showToast);

    // Apply language again after views are initialized to populate dynamic elements
    applyLanguage(currentLang);

    // Hide loader
    if (loader) {
      loader.style.opacity = "0";
      setTimeout(() => {
        loader.style.display = "none";
      }, 200);
    }
  } catch (err: any) {
    console.error("Initialization error:", err);
    if (loaderSub) {
      loaderSub.textContent = "Failed to load database: " + err.message;
      loaderSub.style.color = "#e11d48";
    }
  }
}

document.addEventListener("DOMContentLoaded", bootstrap);
