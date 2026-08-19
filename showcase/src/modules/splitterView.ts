import { EgyptianNames } from "../engine";
import { DICTIONARY } from "../i18n/translations";
import { getLang } from "../main";

let activeSplitterRerun: (() => void) | null = null;

export function rerunSplitter(): void {
  activeSplitterRerun?.();
}

export function initSplitterView(engine: EgyptianNames, showToast: (msg: string) => void): void {
  const input = document.getElementById("split-input") as HTMLInputElement;
  const resultsContainer = document.getElementById("split-tokens-container") as HTMLElement;
  const copyBtn = document.getElementById("btn-copy-split") as HTMLButtonElement;

  const runSplit = () => {
    const lang = getLang();
    const dict = DICTIONARY[lang];
    const text = input?.value || "";

    if (!text.trim()) {
      if (resultsContainer) {
        resultsContainer.innerHTML = `<p style="color: var(--text-muted); padding: 1rem 0;">${dict.inspectEmptyPrompt}</p>`;
      }
      return;
    }

    const tokens = engine.split(text);

    if (resultsContainer) {
      resultsContainer.innerHTML = "";
      tokens.forEach((token, idx) => {
        const info = engine.annotate(token);
        const singleInfo = Array.isArray(info) ? info[0] : info;
        
        let roleLabel = dict.terms.given;
        if (singleInfo) {
          if (singleInfo.role === "family") roleLabel = dict.terms.family;
          else if (singleInfo.role === "given") roleLabel = dict.terms.given;
        }

        let freqLabel = dict.terms.normal;
        if (singleInfo) {
          if (singleInfo.frequencyClass === "common") freqLabel = dict.terms.common;
          else if (singleInfo.frequencyClass === "rare") freqLabel = dict.terms.rare;
        }

        const en = engine.translate(token, "en");

        const chip = document.createElement("div");
        chip.className = "token-chip";
        chip.style.minWidth = "110px";
        chip.innerHTML = `
          <div style="font-size: 0.72rem; color: var(--text-muted); font-weight: 600;">#${idx + 1}</div>
          <span class="token-chip-text">${token}</span>
          <span style="font-size: 0.78rem; color: var(--text-secondary);">${en}</span>
          <div style="display: flex; gap: 0.25rem; margin-top: 0.35rem;">
            <span class="badge">${roleLabel}</span>
            <span class="badge">${freqLabel}</span>
          </div>
        `;
        resultsContainer.appendChild(chip);
      });
    }
  };

  activeSplitterRerun = runSplit;

  input?.addEventListener("input", runSplit);

  copyBtn?.addEventListener("click", () => {
    const text = input?.value || "";
    if (text.trim()) {
      const tokens = engine.split(text);
      const joined = tokens.join(" ");
      navigator.clipboard.writeText(joined);
      const dict = DICTIONARY[getLang()];
      showToast(dict.terms.copied + joined);
    }
  });

  const sampleBtns = document.querySelectorAll<HTMLButtonElement>(".split-preset-btn");
  sampleBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      const sample = btn.dataset.sample;
      if (sample && input) {
        input.value = sample;
        runSplit();
      }
    });
  });

  // Initial
  runSplit();
}
