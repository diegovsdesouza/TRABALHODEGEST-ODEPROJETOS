// Carrega dados/tratados como se viessem do Supabase (nomes sem o número, campos vazios = null, números convertidos).
import fs from 'fs'; import path from 'path';
function parseCSV(txt) {
  const rows = []; let row = [], f = '', q = false;
  for (let i = 0; i < txt.length; i++) { const ch = txt[i];
    if (q) { if (ch === '"') { if (txt[i + 1] === '"') { f += '"'; i++; } else q = false; } else f += ch; }
    else if (ch === '"') q = true; else if (ch === ',') { row.push(f); f = ''; }
    else if (ch === '\n') { row.push(f); rows.push(row); row = []; f = ''; } else if (ch !== '\r') f += ch; }
  if (f || row.length) { row.push(f); rows.push(row); }
  return rows;
}
const TEXTO = new Set(['codigo_eap', 'codigo_pai', 'valor', 'versao', 'vinculo_ids', 'predecessoras', 'sucessoras', 'combinavel_com']);
export function carregar(dir) {
  const db = {};
  for (const f of fs.readdirSync(dir).filter((x) => x.endsWith('.csv'))) {
    const [cab, ...ls] = parseCSV(fs.readFileSync(path.join(dir, f), 'utf8')).filter((r) => r.length > 1 || r[0]);
    db[f.slice(3, -4)] = ls.map((l) => Object.fromEntries(cab.map((c, i) => { const v = l[i];
      if (v === '' || v === undefined) return [c, null];
      if (!TEXTO.has(c) && /^-?\d+(\.\d+)?$/.test(v)) return [c, Number(v)]; return [c, v]; })));
  }
  return db;
}
