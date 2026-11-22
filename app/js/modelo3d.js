// R12 · Modelo 3D da obra (Three.js), montado em etapas ligadas às atividades (tabela 38), com controle de data.
// Até a data de status, o avanço é o real (tabela 17); depois dela, segue a previsão pela rede (convenção 11).
// Elemento ligado a atividades: avanço médio ponderado pelo orçamento. Ligado a épico: pontos concluídos ÷ pontos do épico.
// Ligado a releases: releases entregues ÷ 3. Altura e cor sobem com o avanço; vermelho = cadeia que define o término e atrasada.
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { dados, fmt, htmlTabela, dataCorte } from './db.js';
import * as K from './calc.js';

let renderer = null, frame = null;

function sextas(ini, fim) { const out = []; const d = new Date(ini + 'T12:00:00Z'); while (d.toISOString().slice(0, 10) <= fim) { out.push(d.toISOString().slice(0, 10)); d.setUTCDate(d.getUTCDate() + 7); } return out; }

export function avancoElementos(db, data, ctx) {
  const { lb, pv, orc, status } = ctx; const u = K.ultimoAvanco(db.avanco_semanal, data <= status ? data : status);
  const C = lb.C; const du = C.duAte(data);
  const avAtv = (i) => {
    if (data <= status) return u[i] ? Number(u[i].avanco_acumulado_pct) / 100 : 0;
    const a = pv.ativ[i]; if (!a) return 0; if (a.situacao === 'CONCLUIDA') return 1;
    const ini = a.situacao === 'EM_ANDAMENTO' ? C.duAte(status) : a.ES - 1; const base = a.situacao === 'EM_ANDAMENTO' ? a.avanco / 100 : 0;
    return Math.min(1, Math.max(base, base + (1 - base) * (du - ini) / Math.max(1, a.EF - ini)));
  };
  const relData = (r) => pv.agil.releases[r].real || pv.agil.releases[r].data;
  return db.elementos_3d.map((e) => {
    const ids = (e.vinculo_ids || '').split(';').filter(Boolean); let av = null, det = [];
    if (e.vinculo_tipo === 'ATIVIDADE') {
      const pesos = ids.map((i) => orc[i] || 1); const tot = pesos.reduce((s, x) => s + x, 0);
      det = ids.map((i) => ({ id: i, nome: db.atividades.find((a) => a.id_atividade === i)?.nome_atividade, avanco: avAtv(i), critica: pv.cadeia.includes(i) }));
      av = det.reduce((s, x, k) => s + x.avanco * pesos[k], 0) / tot;
    } else if (e.vinculo_tipo === 'RELEASE') {
      det = ids.map((r) => ({ id: r, nome: db.releases.find((x) => x.id_release === r)?.nome_release, avanco: relData(r) <= data ? 1 : 0 }));
      av = det.reduce((s, x) => s + x.avanco, 0) / det.length;
    } else if (e.vinculo_tipo === 'EPICO') {
      const its = db.backlog_itens.filter((b) => ids.includes(b.id_epico) && b.prioridade_moscow !== 'WONT');
      const tot = its.reduce((s, b) => s + Number(b.pontos), 0);
      const ate = data <= status ? data : status;
      let conc = its.filter((b) => b.status === 'CONCLUIDO' && b.data_conclusao && b.data_conclusao <= ate).reduce((s, b) => s + Number(b.pontos), 0) / (tot || 1);
      const rel = db.epicos.find((x) => x.id_epico === ids[0])?.id_release_planejada;
      if (data > status && rel && relData(rel) <= data) conc = 1;
      av = conc; det = [{ id: ids[0], nome: db.epicos.find((x) => x.id_epico === ids[0])?.nome_epico, avanco: conc }];
    }
    const etapa = e.vinculo_tipo === 'ATIVIDADE' ? Math.min(...ids.map((i) => lb.ativ[i]?.ES ?? 999)) : e.vinculo_tipo === 'NENHUM' ? 0 : 900;
    return { ...e, avanco: av, det, atrasoCritico: det.some((x) => x.critica && pv.ativ[x.id]?.desvio > 0 && x.avanco < 1), etapaDu: etapa };
  });
}

export async function paginaModelo3D(alvo) {
  if (renderer) { cancelAnimationFrame(frame); renderer.dispose(); renderer = null; }
  const db = await dados(); const status = '2026-11-13'; const lb = K.linhaDeBase(db); const pv = K.previsao(db, status, lb);
  const orc = {}; db.orcamento_linha_de_base.forEach((o) => (orc[o.id_atividade] = (orc[o.id_atividade] || 0) + Number(o.valor_orcado_rs)));
  const ctx = { lb, pv, orc, status };
  const datas = sextas('2026-01-30', '2027-06-25'); const corte = dataCorte();
  let idx = datas.findIndex((d) => d >= corte); if (idx < 0) idx = datas.length - 1;
  const etapas = avancoElementos(db, status, ctx).filter((e) => e.vinculo_tipo !== 'NENHUM').sort((a, b) => a.etapaDu - b.etapaDu || a.id_elemento.localeCompare(b.id_elemento));
  alvo.innerHTML = `<h2>Modelo 3D da linha de injeção e pintura</h2>
    <div class="cartao">
      <div class="linha" style="align-items:center"><label style="flex:1">Data: <b id="lblData"></b> <span id="lblFase" class="chip"></span>
        <input type="range" id="slider" min="0" max="${datas.length - 1}" value="${idx}" style="width:100%"></label>
        <button class="sec" id="play">▶ Animar a obra</button></div>
      <div class="legenda3d"><i style="background:hsl(29,75%,50%)"></i>0% <i style="background:hsl(60,75%,50%)"></i>50% <i style="background:hsl(119,60%,42%)"></i>100%
        <i style="background:#d32f2f"></i>na cadeia do término e atrasado <i style="background:#9aa3ad"></i>existente · a altura sobe com o avanço; elemento não iniciado aparece só em contorno</div>
      <div id="cena3d"><div class="painelZona" id="painel"></div></div>
      <p class="fonte">Geometria: tabela 38 (x, y, z, largura, comprimento, altura em metros). Até 13/11/2026 o avanço é o real (tabela 17); depois, a previsão pela rede. Mouse/dedo: girar, arrastar e aproximar. Toque num elemento para ver as atividades.</p>
    </div>
    <div class="cartao" style="margin-top:12px"><h3>Etapas de implantação (ordem pela data de início da linha de base)</h3>${htmlTabela(etapas.map((e, i) => ({ ...e, ordem: i + 1 })), [
      { campo: 'ordem', titulo: 'Etapa' }, { campo: 'id_elemento', titulo: 'Elemento', t: 1 }, { campo: 'nome_elemento', titulo: 'Nome', t: 1 },
      { campo: 'vinculo_ids', titulo: 'Ligado a', t: 1 }, { campo: 'etapaDu', titulo: 'Início LB', f: (v) => (v < 900 ? fmt.data(lb.C.data(v)) : 'trilha ágil') },
      { campo: 'avanco', titulo: 'Avanço em 13/11', f: (v) => fmt.pct(v, 0) }])}</div>`;
  const box = alvo.querySelector('#cena3d'); const painel = alvo.querySelector('#painel');
  const cena = new THREE.Scene(); cena.background = new THREE.Color('#dfe8f1');
  const cam = new THREE.PerspectiveCamera(45, box.clientWidth / box.clientHeight, 1, 3000); cam.position.set(80, 120, 170);
  renderer = new THREE.WebGLRenderer({ antialias: true }); renderer.setSize(box.clientWidth, box.clientHeight); box.prepend(renderer.domElement);
  const ctl = new OrbitControls(cam, renderer.domElement); ctl.target.set(80, 0, -35); ctl.update();
  cena.add(new THREE.AmbientLight(0xffffff, 0.75)); const sol = new THREE.DirectionalLight(0xffffff, 0.8); sol.position.set(60, 200, 120); cena.add(sol);

  const malhas = {};
  const caixa = (w, h, d, cor, op = 1) => new THREE.Mesh(new THREE.BoxGeometry(w, h, d), new THREE.MeshLambertMaterial({ color: cor, transparent: op < 1, opacity: op }));
  for (const e of db.elementos_3d) {
    const W = Number(e.largura), D = Number(e.comprimento), H = Math.max(0.2, Number(e.altura));
    const g = new THREE.Group(); g.position.set(Number(e.x) + W / 2, Number(e.z), -(Number(e.y) + D / 2));
    let corpo;
    if (e.id_elemento === 'EL02') { corpo = caixa(W, H, D, '#5c6bc0', 0.08); corpo.position.y = H / 2; g.add(new THREE.LineSegments(new THREE.EdgesGeometry(corpo.geometry), new THREE.LineBasicMaterial({ color: 0x3949ab }))); g.children.at(-1).position.y = H / 2; }
    else { corpo = caixa(W, 1, D, '#b0b8c1'); }
    g.add(corpo);
    if (e.tipo_elemento === 'EQUIPAMENTO' && e.id_elemento === 'EL09') { const fun = new THREE.Mesh(new THREE.CylinderGeometry(1.2, 0.6, 2.5, 16), new THREE.MeshLambertMaterial({ color: '#455a64' })); fun.position.set(-W / 2 + 6, H + 1.2, 0); fun.userData.det = 1; g.add(fun); }
    if (e.id_elemento === 'EL11') for (let k = -1; k <= 1; k++) { const rb = new THREE.Mesh(new THREE.CylinderGeometry(0.6, 0.9, 3, 12), new THREE.MeshLambertMaterial({ color: '#ff8f00' })); rb.position.set(k * 9, H + 1.5, 0); rb.userData.det = 1; g.add(rb); }
    g.add(new THREE.LineSegments(new THREE.EdgesGeometry(corpo.geometry), new THREE.LineBasicMaterial({ color: 0x37474f })));
    g.userData = { e, corpo, H, borda: g.children.at(-1) };
    cena.add(g); malhas[e.id_elemento] = g;
  }
  const aplicar = (d) => {
    const els = avancoElementos(db, d, ctx);
    for (const e of els) {
      const g = malhas[e.id_elemento]; const { corpo, H, borda } = g.userData; g.userData.atual = e;
      if (e.id_elemento === 'EL02') continue;
      if (e.vinculo_tipo === 'NENHUM') { corpo.material.color = new THREE.Color(e.id_elemento === 'EL01' ? '#a5c47f' : '#9aa3ad'); corpo.scale.y = H; corpo.position.y = H / 2; borda.scale.y = H; borda.position.y = H / 2; continue; }
      const av = e.avanco || 0; const h = Math.max(0.15, H * av);
      corpo.visible = av > 0.001; corpo.scale.y = h; corpo.position.y = h / 2;
      corpo.material.color = e.atrasoCritico ? new THREE.Color('#d32f2f') : new THREE.Color().setHSL(0.08 + 0.25 * av, 0.7, av >= 0.999 ? 0.42 : 0.5);
      borda.scale.y = H; borda.position.y = H / 2;
      g.children.filter((c) => c.userData.det).forEach((c) => (c.visible = av >= 0.999));
    }
  };
  const lbl = alvo.querySelector('#lblData'); const fase = alvo.querySelector('#lblFase'); const slider = alvo.querySelector('#slider');
  const mostrar = () => { const d = datas[+slider.value]; lbl.textContent = fmt.data(d); fase.textContent = d <= status ? 'real' : 'previsão'; aplicar(d); };
  slider.oninput = mostrar; mostrar();
  let anim = null; alvo.querySelector('#play').onclick = (ev) => {
    if (anim) { clearInterval(anim); anim = null; ev.target.textContent = '▶ Animar a obra'; return; }
    ev.target.textContent = '⏸ Parar'; slider.value = 0;
    anim = setInterval(() => { if (+slider.value >= datas.length - 1) { clearInterval(anim); anim = null; ev.target.textContent = '▶ Animar a obra'; return; } slider.value = +slider.value + 1; mostrar(); }, 350);
  };
  const ray = new THREE.Raycaster(); const mouse = new THREE.Vector2();
  renderer.domElement.addEventListener('click', (ev) => {
    const r = renderer.domElement.getBoundingClientRect();
    mouse.set(((ev.clientX - r.left) / r.width) * 2 - 1, -((ev.clientY - r.top) / r.height) * 2 + 1); ray.setFromCamera(mouse, cam);
    const alvos = Object.values(malhas).filter((g) => !['EL01', 'EL02'].includes(g.userData.e.id_elemento)).map((g) => g.userData.corpo);
    const hit = ray.intersectObjects(alvos, false)[0] || ray.intersectObjects(Object.values(malhas).map((g) => g.userData.corpo), false)[0];
    if (!hit) { painel.style.display = 'none'; return; }
    const e = Object.values(malhas).find((g) => g.userData.corpo === hit.object).userData.atual;
    painel.style.display = 'block';
    painel.innerHTML = `<b>${e.id_elemento} · ${e.nome_elemento}</b><br>Avanço: <b>${e.avanco == null ? 'existente' : fmt.pct(e.avanco, 0)}</b>${e.atrasoCritico ? '<br><span class="erro">Na cadeia do término e atrasado</span>' : ''}
      <table style="margin-top:6px"><tr><th class="t">Ligado a</th><th>Avanço</th></tr>${e.det.map((x) => `<tr><td class="t">${x.critica ? '🔴 ' : ''}${x.id} · ${x.nome || ''}</td><td>${fmt.pct(x.avanco, 0)}</td></tr>`).join('') || '<tr><td colspan=2>elemento existente</td></tr>'}</table>`;
  });
  const loop = () => { frame = requestAnimationFrame(loop); renderer.render(cena, cam); }; loop();
  window.addEventListener('resize', () => { if (!renderer) return; cam.aspect = box.clientWidth / box.clientHeight; cam.updateProjectionMatrix(); renderer.setSize(box.clientWidth, box.clientHeight); });
}
