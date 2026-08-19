import { EgyptianNames } from "../engine";

export function initCorrectorView(engine: EgyptianNames, showToast: (msg: string) => void): void {
  const input = document.getElementById("correct-input") as HTMLInputElement;
  const correctedOutput = document.getElementById("correct-output") as HTMLElement;
  const tashkeelOutput = document.getElementById("tashkeel-output") as HTMLElement;
  const copyCorrectBtn = document.getElementById("btn-copy-correct") as HTMLButtonElement;
  const copyTashkeelBtn = document.getElementById("btn-copy-tashkeel") as HTMLButtonElement;

  const runCorrection = () => {
    const text = input?.value || "";
    if (!text.trim()) {
      if (correctedOutput) correctedOutput.textContent = "الاسم المصحح سيظهر هنا...";
      if (tashkeelOutput) tashkeelOutput.textContent = "الاسم المشكول سيظهر هنا...";
      return;
    }

    const corrected = engine.correct(text);
    const diacritized = engine.tashkeel(corrected);

    if (correctedOutput) correctedOutput.textContent = corrected;
    if (tashkeelOutput) tashkeelOutput.textContent = diacritized;
  };

  input?.addEventListener("input", runCorrection);

  copyCorrectBtn?.addEventListener("click", () => {
    const text = correctedOutput?.textContent;
    if (text && text !== "الاسم المصحح سيظهر هنا...") {
      navigator.clipboard.writeText(text);
      showToast("Copied corrected name: " + text);
    }
  });

  copyTashkeelBtn?.addEventListener("click", () => {
    const text = tashkeelOutput?.textContent;
    if (text && text !== "الاسم المشكول سيظهر هنا...") {
      navigator.clipboard.writeText(text);
      showToast("Copied tashkeel name: " + text);
    }
  });

  const presetBtns = document.querySelectorAll<HTMLButtonElement>(".correct-preset-btn");
  presetBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      const sample = btn.dataset.sample;
      if (sample && input) {
        input.value = sample;
        runCorrection();
      }
    });
  });

  // Initial
  runCorrection();
}
