import { NameEntry } from "./types";
import { lookup, lookupAr } from "./lookupIndices";

/**
 * Split on whitespace, but merge an adjacent pair into one lemma when
 * the book has it as a two-word compound (e.g. kunya "Abu X").
 *
 * A handful of book entries are legitimately two words (roughly 800
 * "Abu X" kunya/family lemmas plus a few compound given names). A blind
 * whitespace split treats them as two meaningless fragments, breaking
 * gender/religion detection and split() on names that contain one.
 * Greedy pairwise lookahead, same approach tashkeel() already uses for
 * "عبد الرحمن"-style pairs.
 */
export function compoundTokens(fullName: string): Array<[string, NameEntry | undefined]> {
  const raw = fullName.trim().split(/\s+/).filter(Boolean);
  const out: Array<[string, NameEntry | undefined]> = [];
  const n = raw.length;
  let i = 0;
  while (i < n) {
    if (i < n - 1) {
      const pair = `${raw[i]} ${raw[i + 1]}`;
      const pairEntry = lookupAr(pair) || lookupAr(`${raw[i]}${raw[i + 1]}`);
      if (pairEntry !== undefined) {
        out.push([pair, pairEntry]);
        i += 2;
        continue;
      }
    }
    out.push([raw[i], lookup(raw[i])]);
    i += 1;
  }
  return out;
}
