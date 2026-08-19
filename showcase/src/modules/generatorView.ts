import { EgyptianNames } from "../engine";
import { FrequencyClass, Gender, GeneratedName, Religion } from "../engine/types";

export function initGeneratorView(engine: EgyptianNames, showToast: (msg: string) => void): void {
  const countSlider = document.getElementById("gen-count") as HTMLInputElement;
  const countVal = document.getElementById("gen-count-val") as HTMLElement;
  const lenSlider = document.getElementById("gen-len") as HTMLInputElement;
  const lenVal = document.getElementById("gen-len-val") as HTMLElement;
  const familyToggle = document.getElementById("gen-family") as HTMLInputElement;
  const generateBtn = document.getElementById("btn-generate") as HTMLButtonElement;
  const resultsContainer = document.getElementById("generator-results") as HTMLElement;

  let currentGender: Gender | undefined = undefined;
  let currentReligion: Religion | undefined = undefined;
  let currentFrequency: FrequencyClass | undefined = undefined;

  // Setup pill selectors
  const setupPills = (
    containerId: string,
    onSelect: (val: string | undefined) => void
  ) => {
    const container = document.getElementById(containerId);
    if (!container) return;
    const btns = container.querySelectorAll<HTMLButtonElement>(".pill-btn");
    btns.forEach((btn) => {
      btn.addEventListener("click", () => {
        btns.forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        const val = btn.dataset.val;
        onSelect(val === "all" ? undefined : val);
        runGenerate();
      });
    });
  };

  setupPills("gen-gender-pills", (val) => (currentGender = val as Gender));
  setupPills("gen-religion-pills", (val) => (currentReligion = val as Religion));
  setupPills("gen-freq-pills", (val) => (currentFrequency = val as FrequencyClass));

  if (countSlider && countVal) {
    countSlider.addEventListener("input", () => {
      countVal.textContent = countSlider.value;
    });
  }

  if (lenSlider && lenVal) {
    lenSlider.addEventListener("input", () => {
      lenVal.textContent = lenSlider.value === "0" ? "Auto" : lenSlider.value;
    });
  }

  const runGenerate = () => {
    const count = parseInt(countSlider?.value || "5", 10);
    const lengthVal = parseInt(lenSlider?.value || "0", 10);
    const length = lengthVal > 0 ? lengthVal : undefined;
    const familyName = familyToggle?.checked !== false;

    const names: GeneratedName[] = engine.generate({
      count,
      gender: currentGender,
      religion: currentReligion,
      length,
      familyName,
      frequency: currentFrequency,
    });

    renderResults(names);
  };

  const renderResults = (names: GeneratedName[]) => {
    if (!resultsContainer) return;
    resultsContainer.innerHTML = "";

    names.forEach((n) => {
      const card = document.createElement("div");
      card.className = "name-result-card";
      card.innerHTML = `
        <div class="name-result-info">
          <div class="name-result-ar">${n.ar}</div>
          <div class="name-result-en">${n.en}</div>
        </div>
        <div class="card-action-btns">
          <button class="action-icon-btn copy-btn" title="Copy name">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
          </button>
          <button class="action-icon-btn inspect-btn" title="Inspect lemma">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          </button>
        </div>
      `;

      const copyBtn = card.querySelector(".copy-btn");
      copyBtn?.addEventListener("click", () => {
        navigator.clipboard.writeText(`${n.ar} (${n.en})`);
        showToast("Copied: " + n.ar);
      });

      const inspectBtn = card.querySelector(".inspect-btn");
      inspectBtn?.addEventListener("click", () => {
        const inspectInput = document.getElementById("inspect-input") as HTMLInputElement;
        const inspectTabBtn = document.querySelector('[data-tab="tab-inspector"]') as HTMLButtonElement;
        if (inspectInput && inspectTabBtn) {
          inspectInput.value = n.partsAr[0];
          inspectTabBtn.click();
          inspectInput.dispatchEvent(new Event("input"));
        }
      });

      resultsContainer.appendChild(card);
    });
  };

  generateBtn?.addEventListener("click", runGenerate);
  familyToggle?.addEventListener("change", runGenerate);

  // Initial generation
  runGenerate();
}
