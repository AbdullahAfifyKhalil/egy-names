import { lookup } from "./lookupIndices";
import { NameInfo, toNameInfo } from "./types";

export function annotateSingle(name: string): NameInfo | null {
  const entry = lookup(name);
  if (!entry) return null;
  return toNameInfo(entry);
}

export function annotate(name: string): NameInfo | null | (NameInfo | null)[] {
  if (!name || !name.trim()) return null;

  const tokens = name.trim().split(/\s+/);
  if (tokens.length === 1) {
    return annotateSingle(tokens[0]);
  }

  return tokens.map((t) => annotateSingle(t));
}
