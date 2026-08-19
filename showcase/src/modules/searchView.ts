import { EgyptianNames } from "../engine";
import { DICTIONARY } from "../i18n/translations";
import { getLang } from "../main";

let activeSearchRerun: (() => void) | null = null;

export function rerunSearch(): void {
  activeSearchRerun?.();
}

export function initSearchView(engine: EgyptianNames, showToast: (msg: string) => void): void {
  const queryInput = document.getElementById("search-query") as HTMLInputElement;
  const startsWithInput = document.getElementById("search-prefix") as HTMLInputElement;
  const roleSelect = document.getElementById("search-role") as HTMLSelectElement;
  const genderSelect = document.getElementById("search-gender") as HTMLSelectElement;
  const religionSelect = document.getElementById("search-religion") as HTMLSelectElement;
  const freqSelect = document.getElementById("search-freq") as HTMLSelectElement;
  const resultsTableBody = document.getElementById("search-results-tbody") as HTMLElement;
  const resultCountBadge = document.getElementById("search-count-badge") as HTMLElement;

  const runSearch = () => {
    const lang = getLang();
    const dict = DICTIONARY[lang];

    const contains = queryInput?.value?.trim() || undefined;
    const startsWith = startsWithInput?.value?.trim() || undefined;
    const role = roleSelect?.value !== "all" ? roleSelect?.value : undefined;
    const gender = genderSelect?.value !== "all" ? genderSelect?.value : undefined;
    const religion = religionSelect?.value !== "all" ? religionSelect?.value : undefined;
    const frequency = freqSelect?.value !== "all" ? freqSelect?.value : undefined;

    const results = engine.search({
      contains,
      startsWith,
      role,
      gender,
      religion,
      frequency,
      maxResults: 60,
    });

    if (resultCountBadge) {
      resultCountBadge.textContent = dict.terms.resultsCount(results.length);
    }

    if (resultsTableBody) {
      resultsTableBody.innerHTML = "";
      if (results.length === 0) {
        resultsTableBody.innerHTML = `
          <tr>
            <td colspan="6" style="text-align: center; color: var(--text-muted); padding: 2rem;">
              ${lang === "ar" ? "لم يتم العثور على نتائج مطابقة." : "No matching names found."}
            </td>
          </tr>
        `;
        return;
      }

      results.forEach((r, idx) => {
        const religionLabel =
          r.religion === "muslim"
            ? dict.terms.muslim
            : r.religion === "christian"
            ? dict.terms.christian
            : dict.terms.neutral;

        const genderLabel =
          r.gender === "male"
            ? dict.terms.male
            : r.gender === "female"
            ? dict.terms.female
            : dict.terms.unisex;

        const roleLabel =
          r.role === "family" ? dict.terms.family : dict.terms.given;

        const row = document.createElement("tr");
        row.style.borderBottom = "1px solid var(--border-color)";
        row.innerHTML = `
          <td style="padding: 0.55rem 0.75rem; color: var(--text-muted); font-size: 0.75rem;">#${idx + 1}</td>
          <td style="padding: 0.55rem 0.75rem; font-family: var(--font-arabic); font-size: 1.05rem; font-weight: 600; color: var(--text-primary);">${r.tashkeel || r.ar}</td>
          <td style="padding: 0.55rem 0.75rem; color: var(--text-secondary); font-size: 0.82rem;">${r.en}</td>
          <td style="padding: 0.55rem 0.75rem;">
            <span class="badge">${genderLabel}</span>
          </td>
          <td style="padding: 0.55rem 0.75rem;">
            <span class="badge">${religionLabel}</span>
          </td>
          <td style="padding: 0.55rem 0.75rem;">
            <span class="badge">${roleLabel}</span>
          </td>
        `;
        resultsTableBody.appendChild(row);
      });
    }
  };

  activeSearchRerun = runSearch;

  queryInput?.addEventListener("input", runSearch);
  startsWithInput?.addEventListener("input", runSearch);
  roleSelect?.addEventListener("change", runSearch);
  genderSelect?.addEventListener("change", runSearch);
  religionSelect?.addEventListener("change", runSearch);
  freqSelect?.addEventListener("change", runSearch);

  // Initial
  runSearch();
}
