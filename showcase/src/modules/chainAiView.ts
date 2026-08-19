import { EgyptianNames } from "../engine";
import { DICTIONARY } from "../i18n/translations";
import { getLang } from "../main";

let activeChainRerun: (() => void) | null = null;

export function rerunChainAi(): void {
  activeChainRerun?.();
}

export function initChainAiView(engine: EgyptianNames, showToast: (msg: string) => void): void {
  const input = document.getElementById("chain-input") as HTMLInputElement;
  const chainPartsContainer = document.getElementById("chain-parts-container") as HTMLElement;
  const genderMeterVal = document.getElementById("ai-gender-val") as HTMLElement;
  const genderMeterFill = document.getElementById("ai-gender-fill") as HTMLElement;
  const religionMeterVal = document.getElementById("ai-religion-val") as HTMLElement;
  const religionMeterFill = document.getElementById("ai-religion-fill") as HTMLElement;
  const uniquenessVal = document.getElementById("ai-uniqueness-val") as HTMLElement;
  const uniquenessNote = document.getElementById("ai-uniqueness-note") as HTMLElement;
  const uniquenessFill = document.getElementById("ai-uniqueness-fill") as HTMLElement;

  const runChainAnalysis = () => {
    const lang = getLang();
    const dict = DICTIONARY[lang];
    const text = input?.value || "";

    if (!text.trim()) {
      if (chainPartsContainer) {
        chainPartsContainer.innerHTML = `<p style="color: var(--text-muted); padding: 1rem 0;">${dict.inspectEmptyPrompt}</p>`;
      }
      return;
    }

    const parts = engine.analyzeChain(text);
    const genderDet = engine.detectGender(text);
    const religionDet = engine.detectReligion(text);
    const uniqueDet = engine.uniqueness(text);

    // Render generational chain
    if (chainPartsContainer) {
      chainPartsContainer.innerHTML = "";
      parts.forEach((p) => {
        let roleName = dict.terms.given;
        if (p.role === "father") roleName = dict.terms.father;
        else if (p.role === "grandfather") roleName = dict.terms.grandfather;
        else if (p.role === "great_grandfather") roleName = dict.terms.great_grandfather;
        else if (p.role === "family") roleName = dict.terms.family;

        const item = document.createElement("div");
        item.className = "token-chip";
        item.style.minWidth = "120px";
        item.style.textAlign = "center";
        item.innerHTML = `
          <div style="font-size: 0.72rem; color: var(--text-muted); font-weight: 600;">${dict.terms.slot} ${p.slot}</div>
          <span class="token-chip-text">${p.name}</span>
          <span class="badge" style="margin-top: 0.25rem;">${roleName}</span>
        `;
        chainPartsContainer.appendChild(item);
      });
    }

    // Update Gender Inference
    if (genderMeterVal && genderMeterFill) {
      const confPct = Math.round(genderDet.confidence * 100);
      const genderName =
        genderDet.gender === "male"
          ? dict.terms.male
          : genderDet.gender === "female"
          ? dict.terms.female
          : dict.terms.unisex;
      genderMeterVal.textContent = `${genderName} (${confPct}%)`;
      genderMeterFill.style.width = `${confPct}%`;
    }

    // Update Religion Inference
    if (religionMeterVal && religionMeterFill) {
      const confPct = Math.round(religionDet.confidence * 100);
      const religionName =
        religionDet.religion === "muslim"
          ? dict.terms.muslim
          : religionDet.religion === "christian"
          ? dict.terms.christian
          : dict.terms.neutral;
      religionMeterVal.textContent = `${religionName} (${confPct}%)`;
      religionMeterFill.style.width = `${confPct}%`;
    }

    // Update Uniqueness Score
    if (uniquenessVal && uniquenessNote && uniquenessFill) {
      const scorePct = Math.round(uniqueDet.score * 100);
      uniquenessVal.textContent = `${(uniqueDet.score * 10).toFixed(1)} / 10`;
      uniquenessNote.textContent =
        lang === "ar"
          ? "معدل محسوب وفق تكرارات مكونات الاسم في المدونة الوطنية."
          : uniqueDet.note;
      uniquenessFill.style.width = `${scorePct}%`;
    }
  };

  activeChainRerun = runChainAnalysis;

  input?.addEventListener("input", runChainAnalysis);

  const presetBtns = document.querySelectorAll<HTMLButtonElement>(".chain-preset-btn");
  presetBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      const sample = btn.dataset.sample;
      if (sample && input) {
        input.value = sample;
        runChainAnalysis();
      }
    });
  });

  // Initial
  runChainAnalysis();
}
