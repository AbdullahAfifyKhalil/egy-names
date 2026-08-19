import { EgyptianNames } from "../engine";

export function initTranslatorView(engine: EgyptianNames, showToast: (msg: string) => void): void {
  const arInput = document.getElementById("trans-ar-input") as HTMLInputElement;
  const enOutput = document.getElementById("trans-en-output") as HTMLElement;
  const enInput = document.getElementById("trans-en-input") as HTMLInputElement;
  const arOutput = document.getElementById("trans-ar-output") as HTMLElement;
  const tokenBadgesContainer = document.getElementById("trans-tokens-container") as HTMLElement;
  const copyEnBtn = document.getElementById("btn-copy-trans-en") as HTMLButtonElement;
  const copyArBtn = document.getElementById("btn-copy-trans-ar") as HTMLButtonElement;

  const updateArToEn = () => {
    const text = arInput?.value || "";
    if (!text.trim()) {
      if (enOutput) enOutput.textContent = "Translation will appear here...";
      if (tokenBadgesContainer) tokenBadgesContainer.innerHTML = "";
      return;
    }

    const translated = engine.translate(text, "en");
    if (enOutput) enOutput.textContent = translated;

    // Render token badges
    const tokens = text.trim().split(/\s+/);
    if (tokenBadgesContainer) {
      tokenBadgesContainer.innerHTML = "";
      tokens.forEach((t) => {
        const transT = engine.translate(t, "en");
        const chip = document.createElement("div");
        chip.className = "token-chip";
        chip.innerHTML = `
          <span class="token-chip-text">${t}</span>
          <span class="token-chip-tag">${transT}</span>
        `;
        tokenBadgesContainer.appendChild(chip);
      });
    }
  };

  const updateEnToAr = () => {
    const text = enInput?.value || "";
    if (!text.trim()) {
      if (arOutput) arOutput.textContent = "الترجمة ستظهر هنا...";
      return;
    }
    const translated = engine.translate(text, "ar");
    if (arOutput) arOutput.textContent = translated;
  };

  arInput?.addEventListener("input", updateArToEn);
  enInput?.addEventListener("input", updateEnToAr);

  copyEnBtn?.addEventListener("click", () => {
    const text = enOutput?.textContent;
    if (text && text !== "Translation will appear here...") {
      navigator.clipboard.writeText(text);
      showToast("Copied English translation: " + text);
    }
  });

  copyArBtn?.addEventListener("click", () => {
    const text = arOutput?.textContent;
    if (text && text !== "الترجمة ستظهر هنا...") {
      navigator.clipboard.writeText(text);
      showToast("Copied Arabic translation: " + text);
    }
  });

  // Preset buttons
  const presetBtns = document.querySelectorAll<HTMLButtonElement>(".trans-preset-btn");
  presetBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      const sample = btn.dataset.sample;
      if (sample && arInput) {
        arInput.value = sample;
        updateArToEn();
      }
    });
  });

  // Initial run
  updateArToEn();
}
