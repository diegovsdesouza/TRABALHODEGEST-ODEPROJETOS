// R16 · Simulador de cenários (convenções 21 a 23): novo término, custo, VPL e resultado de C1 a C6 e das combinações.
import Chart from 'chart.js/auto';
import { dados, fmt, htmlTabela, dataCorte } from './db.js';
import * as K from './calc.js';

let grafico = null;
export async function paginaCenarios(alvo) {
  const db = await dados(); const d = dataCorte();
  const cen = db.cenarios.slice().sort((a, b) => a.id_cenario.localeCompare(b.id_cenario));
  const comb = (id) => (cen.find((c) => c.id_cenario === id)?.combinavel_com || '').split(';').filter(Boolean);
  const res = cen.map((c) => ({ ...K.cenario(db, [c.id_cenario], d), nome: c.nome_cenario, quem: c.id_proponente, desc: c.descricao, id: c.id_cenario }));
  const ref = res[0];
  alvo.innerHTML = `<h2>Simulador de cenários · data de status ${fmt.data(d)}</h2>
  <p class="nota">Cada cenário parte da previsão pela rede na data de status (convenção 11), aplica as mudanças das tabelas 44 a 46 (convenção 21), soma os custos (convenção 22) e refaz o caso de negócio com TMA de 14% a.a. (convenção 23). Resultado = VPL − custo do atraso (R$ 50.100 por dia útil além de 07/05/2027).</p>
  <div class="cartao">${htmlTabela(res, [
    { campo: 'id', titulo: 'Cenário', t: 1, f: (v, l) => `<b>${v}</b> ${l.nome}` },
    { campo: 'termino', titulo: 'Término previsto', f: fmt.data }, { campo: 'duAlemContrato', titulo: 'du além do contrato', cor: (v) => (v > 0 ? 'neg' : 'pos') },
    { campo: 'meses', titulo: 'Meses de atraso', f: (v) => fmt.n(v, 2) }, { campo: 'ent', titulo: 'ENT (R$)', f: fmt.rs },
    { campo: 'vpl', titulo: 'VPL (R$)', f: fmt.rs }, { campo: 'payback', titulo: 'Payback (anos)', f: (v) => fmt.n(v, 2) },
    { campo: 'custoAtraso', titulo: 'Custo do atraso (R$)', f: fmt.rs }, { campo: 'resultado', titulo: 'Resultado (R$)', f: fmt.rs, cor: (v) => (v >= ref.resultado ? 'pos' : 'neg') },
    { campo: 'resultado', titulo: 'vs. C1', f: (v) => (v === ref.resultado ? '—' : (v > ref.resultado ? '+' : '') + fmt.rs(v - ref.resultado)) }],
    { classeLinha: (l) => (l.resultado === Math.max(...res.map((x) => x.resultado)) ? 'total' : '') })}
    <p class="fonte">Linha em destaque = maior resultado. ENT do cenário = ENT atual (ONT ÷ IDC) + custos da tabela 44 + (pontos incluídos − excluídos) × custo real por ponto (${fmt.rs(ref.custoPonto)}) + reforço da tabela 46 + investimento da tabela 43.</p></div>
  <div class="grade" style="margin-top:12px">
    <div class="cartao"><h3>Testar uma combinação</h3><p class="nota">Marque os cenários. Só aparecem combinações permitidas pela coluna "combinável com" da tabela 43.</p>
      <div id="marcar" class="linha">${cen.filter((c) => c.id_cenario !== 'C1').map((c) => `<label style="flex-direction:row;gap:4px"><input type="checkbox" value="${c.id_cenario}"> ${c.id_cenario} ${c.nome_cenario}</label>`).join('')}</div>
      <div id="combo" style="margin-top:8px"></div></div>
    <div class="cartao"><h3>Fluxo de caixa acumulado (R$ mil)</h3><canvas id="gF" class="grafico"></canvas><p class="fonte">Folha M7: C1, C3 e C4. Convenção 16 (payback com interpolação).</p></div>
  </div>
  <div class="cartao" style="margin-top:12px"><h3>O que cada cenário muda</h3>${htmlTabela(res, [
    { campo: 'id', titulo: 'Cenário', t: 1 }, { campo: 'quem', titulo: 'Quem defende', t: 1, f: (v) => db.partes_interessadas.find((p) => p.id_parte === v)?.parte_interessada || v },
    { campo: 'desc', titulo: 'O que propõe', t: 1 }, { campo: 'custoAtiv', titulo: 'Custo nas atividades', f: fmt.rs }, { campo: 'pts', titulo: 'Pontos ±' },
    { campo: 'recursos', titulo: 'Reforço', f: fmt.rs }, { campo: 'varBen', titulo: 'Benefício', f: (v) => fmt.n(v, 1) + '%' }, { campo: 'varOp', titulo: 'Custo op./ano', f: fmt.rs },
    { campo: 'releases', titulo: 'R2 / R3', f: (v) => `${fmt.data(v.R2.data)} / ${fmt.data(v.R3.data)}` }])}</div>`;

  const desenharFluxo = (lista) => {
    if (grafico) grafico.destroy();
    grafico = new Chart(alvo.querySelector('#gF'), { type: 'line', data: { labels: ref.anos.map((a) => 'ano ' + a.ano),
      datasets: lista.map((r, i) => ({ label: r.ids.join('+'), data: r.anos.map((a) => a.acumulado / 1000), borderColor: ['#2f75b5', '#c00000', '#2e7d32', '#ed7d31', '#7030a0', '#6b7785', '#000'][i % 7] })) },
      options: { plugins: { legend: { position: 'bottom' } } } });
  };
  desenharFluxo(res.filter((r) => ['C1', 'C3', 'C4'].includes(r.id)));
  alvo.querySelectorAll('#marcar input').forEach((cb) => (cb.onchange = () => {
    const sel = [...alvo.querySelectorAll('#marcar input:checked')].map((x) => x.value);
    const box = alvo.querySelector('#combo');
    if (sel.length < 2) { box.innerHTML = '<p class="nota">Marque pelo menos dois cenários.</p>'; desenharFluxo(res.filter((r) => ['C1', 'C3', 'C4'].includes(r.id))); return; }
    const invalido = sel.find((a) => sel.some((b) => a !== b && !comb(a).includes(b)));
    if (invalido) { box.innerHTML = `<div class="alerta">Combinação não permitida pela tabela 43: ${sel.join(' + ')}. ${sel.map((s) => `${s} combina com ${comb(s).join(', ') || 'nenhum'}`).join('; ')}.</div>`; return; }
    const r = K.cenario(db, sel, d);
    box.innerHTML = htmlTabela([r], [{ campo: 'ids', titulo: 'Combinação', t: 1, f: (v) => v.join(' + ') }, { campo: 'termino', titulo: 'Término', f: fmt.data },
      { campo: 'duAlemContrato', titulo: 'du além' }, { campo: 'ent', titulo: 'ENT', f: fmt.rs }, { campo: 'vpl', titulo: 'VPL', f: fmt.rs },
      { campo: 'resultado', titulo: 'Resultado', f: fmt.rs }, { campo: 'resultado', titulo: 'vs. C1', f: (v) => fmt.rs(v - ref.resultado) }]);
    desenharFluxo([ref, r]);
  }));
}
