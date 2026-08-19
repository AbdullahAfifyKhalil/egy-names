import { EgyptianNames } from "../engine";
import { NameInfo } from "../engine/types";
import { DICTIONARY } from "../i18n/translations";
import { getLang } from "../main";

let activeInspectorRerun: (() => void) | null = null;

export function rerunInspector(): void {
  activeInspectorRerun?.();
}

export function initInspectorView(engine: EgyptianNames, showToast: (msg: string) => void): void {
  const input = document.getElementById("inspect-input") as HTMLInputElement;
  const resultCard = document.getElementById("inspect-result-card") as HTMLElement;

  const runInspect = () => {
    const lang = getLang();
    const dict = DICTIONARY[lang];
    const text = input?.value?.trim() || "";

    if (!text) {
      if (resultCard) {
        resultCard.innerHTML = `<p style="color: var(--text-muted); text-align: center; padding: 2rem;">${dict.inspectEmptyPrompt}</p>`;
      }
      return;
    }

    const info = engine.annotate(text);
    const singleInfo: NameInfo | null = Array.isArray(info) ? info[0] : info;
    const rankInfo = engine.rank(text);
    const meaning = engine.meaning(text);

    if (!singleInfo) {
      if (resultCard) {
        resultCard.innerHTML = `
          <div style="text-align: center; padding: 2rem;">
            <p style="color: var(--text-primary); font-weight: 600; font-size: 1rem;">
              ${lang === "ar" ? `الاسم "${text}" غير موجود في قاعدة الأسماء` : `Name "${text}" not found in database`}
            </p>
            <p style="color: var(--text-secondary); font-size: 0.85rem; margin-top: 0.35rem;">
              ${lang === "ar" ? "جرّب البحث عن أسماء شائعة مثل: محمد، فاطمة، مينا، الشناوي" : "Try searching common names like: Mohamed, Fatima, Mina, Elshazly"}
            </p>
          </div>
        `;
      }
      return;
    }

    const slotLabels = [
      dict.terms.slot1,
      dict.terms.slot2,
      dict.terms.slot3,
      dict.terms.slot4,
      dict.terms.slot5,
      dict.terms.slot6,
      dict.terms.slot7,
      dict.terms.slot8,
    ];

    const religionLabel =
      singleInfo.religion === "muslim"
        ? dict.terms.muslim
        : singleInfo.religion === "christian"
        ? dict.terms.christian
        : dict.terms.neutral;

    const genderLabel =
      singleInfo.gender === "male"
        ? dict.terms.male
        : singleInfo.gender === "female"
        ? dict.terms.female
        : dict.terms.unisex;

    const roleLabel =
      singleInfo.role === "family" ? dict.terms.family : dict.terms.given;

    const freqLabel =
      singleInfo.frequencyClass === "common"
        ? dict.terms.common
        : singleInfo.frequencyClass === "rare"
        ? dict.terms.rare
        : dict.terms.normal;

    if (resultCard) {
      resultCard.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 1px solid var(--border-color); padding-bottom: 1rem; margin-bottom: 1.25rem;">
          <div>
            <div style="font-family: var(--font-arabic); font-size: 1.75rem; font-weight: 700; color: var(--text-primary); line-height: 1.2;">
              ${singleInfo.tashkeel || singleInfo.ar}
            </div>
            <div style="font-size: 1rem; color: var(--text-secondary); font-weight: 500; margin-top: 0.2rem;">
              ${singleInfo.en}
            </div>
          </div>
          <div style="display: flex; flex-direction: column; align-items: flex-end; gap: 0.35rem;">
            <div style="display: flex; gap: 0.3rem;">
              <span class="badge">${religionLabel}</span>
              <span class="badge">${genderLabel}</span>
              <span class="badge">${roleLabel}</span>
            </div>
            <div style="font-size: 0.75rem; color: var(--text-secondary); font-weight: 500;">
              ${freqLabel}
            </div>
          </div>
        </div>

        <!-- Meaning Section -->
        <div style="background: var(--bg-surface); border: 1px solid var(--border-color); border-radius: var(--radius-sm); padding: 1rem; margin-bottom: 1.25rem;">
          <div style="font-size: 0.72rem; font-weight: 600; color: var(--text-muted); text-transform: uppercase; margin-bottom: 0.35rem;">
            ${dict.etymologyHeader}
          </div>
          <div style="font-family: var(--font-arabic); font-size: 1rem; color: var(--text-primary); direction: rtl; margin-bottom: 0.35rem; line-height: 1.5;">
            ${meaning?.ar || singleInfo.meaningAr || (lang === "ar" ? "لم يتم تسجيل معنى نصي مفصل لهذا الاسم." : "No extended textual meaning recorded.")}
          </div>
          ${meaning?.en || singleInfo.meaningEn ? `<div style="font-size: 0.85rem; color: var(--text-secondary);">${meaning?.en || singleInfo.meaningEn}</div>` : ''}
        </div>

        <!-- National Corpus Rank -->
        ${rankInfo ? `
          <div style="background: var(--bg-surface); border: 1px solid var(--border-color); border-radius: var(--radius-sm); padding: 1rem; margin-bottom: 1.25rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <div>
                <div style="font-size: 0.72rem; font-weight: 600; color: var(--text-muted); text-transform: uppercase;">${dict.nationalRankHeader}</div>
                <div style="font-size: 1.25rem; font-weight: 700; color: var(--text-primary); margin-top: 0.15rem;">#${rankInfo.rank}</div>
                <div style="font-size: 0.8rem; color: var(--text-secondary);">${lang === "ar" ? rankInfo.description.replace("Top", "أعلى").replace("Extremely Common", "شائع جداً") : rankInfo.description}</div>
              </div>
              <div style="text-align: ${lang === 'ar' ? 'left' : 'right'};">
                <div style="font-size: 1.25rem; font-weight: 700; color: var(--text-primary);">${rankInfo.percentile}%</div>
                <div style="font-size: 0.72rem; color: var(--text-muted);">${dict.percentileRankLabel}</div>
                <div style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 0.15rem;">${dict.corpusShareLabel}: ${rankInfo.corpusShare}</div>
              </div>
            </div>
          </div>
        ` : ''}

        <!-- Slot Distribution -->
        <div style="margin-bottom: 1.25rem;">
          <div style="font-size: 0.72rem; font-weight: 600; color: var(--text-muted); text-transform: uppercase; margin-bottom: 0.5rem;">
            ${dict.slotProbHeader}
          </div>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(95px, 1fr)); gap: 0.35rem;">
            ${singleInfo.slotDistribution.map((pct, idx) => `
              <div style="background: var(--bg-surface); border: 1px solid var(--border-color); border-radius: var(--radius-xs); padding: 0.5rem; text-align: center;">
                <div style="font-size: 0.68rem; color: var(--text-muted);">${slotLabels[idx] || `${dict.terms.slot} ${idx + 1}`}</div>
                <div style="font-size: 0.95rem; font-weight: 600; color: var(--text-primary); margin-top: 0.1rem;">
                  ${(pct * 100).toFixed(1)}%
                </div>
              </div>
            `).join('')}
          </div>
        </div>

        <!-- Variants -->
        <div>
          <div style="font-size: 0.72rem; font-weight: 600; color: var(--text-muted); text-transform: uppercase; margin-bottom: 0.35rem;">
            ${dict.variantsHeader}
          </div>
          <div style="display: flex; flex-wrap: wrap; gap: 0.3rem;">
            ${singleInfo.enVariants.map((v) => `
              <span class="badge">
                ${v}
              </span>
            `).join('')}
          </div>
        </div>
      `;
    }
  };

  activeInspectorRerun = runInspect;

  input?.addEventListener("input", runInspect);

  const presetBtns = document.querySelectorAll<HTMLButtonElement>(".inspect-preset-btn");
  presetBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      const sample = btn.dataset.sample;
      if (sample && input) {
        input.value = sample;
        runInspect();
      }
    });
  });

  // Initial
  runInspect();
}
