// R13 · Assistente de IA (função do Netlify). A chave da IA NÃO fica no repositório:
// ela é configurada no painel do Netlify como variável de ambiente GEMINI_API_KEY (Google AI Studio, gratuita).
// Sem chave, a função responde 501 e o site usa o assistente local (respostas calculadas pelo próprio sistema).
export default async (req) => {
  const chave = process.env.GEMINI_API_KEY;
  if (!chave) return new Response(JSON.stringify({ erro: 'sem_chave' }), { status: 501, headers: { 'content-type': 'application/json' } });
  const { pergunta = '', contexto = '' } = await req.json().catch(() => ({}));
  if (!pergunta.trim()) return new Response(JSON.stringify({ erro: 'pergunta vazia' }), { status: 400 });
  const modelo = process.env.GEMINI_MODEL || 'gemini-2.5-flash';
  const instrucao = 'Você é o assistente do escritório de projetos do G7 (Plásticos Abrantes, linha de injeção e pintura de para-choques). '
    + 'Responda em português do Brasil, de forma direta e curta (até 8 linhas). Use SOMENTE os números do contexto abaixo, que foram calculados '
    + 'pelo sistema com as convenções oficiais da disciplina; cite a fonte (tabela ou convenção) e a unidade de cada número. '
    + 'Se a resposta não estiver no contexto, diga que o sistema não tem esse dado. Não invente números.\n\nCONTEXTO:\n' + String(contexto).slice(0, 30000);
  const r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${modelo}:generateContent?key=${chave}`, {
    method: 'POST', headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ systemInstruction: { parts: [{ text: instrucao }] }, contents: [{ role: 'user', parts: [{ text: String(pergunta).slice(0, 2000) }] }],
      generationConfig: { temperature: 0.2, maxOutputTokens: 800 } }) });
  const j = await r.json().catch(() => ({}));
  const texto = j?.candidates?.[0]?.content?.parts?.map((p) => p.text).join('') || null;
  if (!r.ok || !texto) return new Response(JSON.stringify({ erro: j?.error?.message || 'falha na IA' }), { status: 502, headers: { 'content-type': 'application/json' } });
  return new Response(JSON.stringify({ resposta: texto, modelo }), { headers: { 'content-type': 'application/json' } });
};
