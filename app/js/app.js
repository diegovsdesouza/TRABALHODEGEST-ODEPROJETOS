// Roteador e login.
import { sb } from './db.js';
import { paginaDashboard, paginaPrazo, paginaCusto, paginaAgil, paginaConferencia } from './paginas.js';
import { paginaLancamentos } from './telas.js';
import { paginaCenarios } from './cenarios.js';
import { paginaRiscos, paginaContratos, paginaPessoas } from './paginas2.js';
import { paginaModelo3D } from './modelo3d.js';

const el = document.getElementById('conteudo');
let usuario = null;
const rotas = {
  '#/dashboard': paginaDashboard, '#/lancamentos': paginaLancamentos, '#/prazo': paginaPrazo,
  '#/custo': paginaCusto, '#/agil': paginaAgil, '#/riscos': paginaRiscos, '#/contratos': paginaContratos, '#/pessoas': paginaPessoas, '#/cenarios': paginaCenarios, '#/3d': paginaModelo3D, '#/conferencia': paginaConferencia,
};

async function navegar() {
  const h = rotas[location.hash] ? location.hash : '#/dashboard';
  document.querySelectorAll('nav a').forEach((a) => a.classList.toggle('ativo', a.getAttribute('href') === h));
  el.innerHTML = '<p class="carregando">Carregando…</p>';
  try { await rotas[h](el, { usuario }); }
  catch (e) { console.error(e); el.innerHTML = `<div class="alerta">Erro: ${e.message}</div>`; }
}

const dlg = document.getElementById('dlgLogin'); const btn = document.getElementById('btnLogin');
function mostrarUsuario() {
  document.getElementById('quem').textContent = usuario ? usuario.email : 'visitante (só leitura)';
  btn.textContent = usuario ? 'Sair' : 'Entrar';
}
btn.onclick = async () => { if (usuario) { await sb.auth.signOut(); return; } document.getElementById('msgLogin').textContent = ''; dlg.showModal(); };
document.getElementById('formLogin').addEventListener('submit', async (ev) => {
  const acao = ev.submitter?.value; if (acao === 'cancelar') return;
  ev.preventDefault();
  const f = new FormData(ev.target); const msg = document.getElementById('msgLogin');
  const cred = { email: f.get('email'), password: f.get('senha') };
  const { error } = acao === 'criar' ? await sb.auth.signUp(cred) : await sb.auth.signInWithPassword(cred);
  if (error) { msg.textContent = error.message; return; }
  if (acao === 'criar') { msg.textContent = 'Conta criada. Se o Supabase pedir confirmação, confirme pelo e-mail e depois clique em Entrar.'; }
  dlg.close();
});
sb.auth.onAuthStateChange((_e, sess) => { const antes = usuario?.id; usuario = sess?.user ?? null; mostrarUsuario(); if (antes !== usuario?.id && location.hash === '#/lancamentos') navegar(); });
document.getElementById('dataCorte').addEventListener('change', navegar);
window.addEventListener('hashchange', navegar);
const { data } = await sb.auth.getSession(); usuario = data.session?.user ?? null; mostrarUsuario();
navegar();
