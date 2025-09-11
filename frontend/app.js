const API_BASE = 'http://localhost:8000';

const form = document.getElementById('analyze-form');
const resultEl = document.getElementById('result');

function fmtList(arr) { return arr && arr.length ? arr.map(x => `- ${x}`).join('\n') : '-'; }

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const fileInput = document.getElementById('file');
  const query = document.getElementById('query').value;
  const username = document.getElementById('username').value || 'anonymous';
  if (!fileInput.files.length) { alert('Select a PDF'); return; }
  const fd = new FormData();
  fd.append('file', fileInput.files[0]);
  fd.append('query', query);
  fd.append('username', username);
  resultEl.textContent = 'Analyzing...';
  try {
    const resp = await fetch(`${API_BASE}/analyze`, { method: 'POST', body: fd });
    if (!resp.ok) { throw new Error(`${resp.status}`); }
    const data = await resp.json();
    const a = data.analysis || {};
    resultEl.innerHTML = `
      <div class="grid">
        <div class="card"><h3>Summary</h3><div>${a.summary || ''}</div></div>
        <div class="card"><h3>Insights</h3><pre>${fmtList(a.insights || [])}</pre></div>
        <div class="card"><h3>Recommendations</h3><pre>${fmtList(a.recommendations || [])}</pre></div>
        <div class="card"><h3>Risks</h3><pre>${fmtList(a.risks || [])}</pre></div>
        <div class="card"><h3>References</h3><pre>${fmtList(a.references || [])}</pre></div>
      </div>
      <div style="margin-top:12px;font-size:12px;color:#94a3b8;">Analysis ID: ${data.analysis_id}</div>
    `;
  } catch (err) {
    resultEl.textContent = `Error: ${err}`;
  }
});


