import io
import os
import re
import json
from typing import List, Dict, Any

from reportlab.pdfgen import canvas
from PIL import Image

try:
    import fitz
except Exception:
    fitz = None

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

def extract_text_from_pdf(pdf_path: str) -> str:
    if fitz is None:
        return ""
    doc = fitz.open(pdf_path)
    parts: List[str] = []
    for page in doc:
        parts.append(page.get_text("text"))
    doc.close()
    text = "\n".join(parts)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def chunk_text(text: str, max_chars: int = 2000) -> List[str]:
    chunks: List[str] = []
    current: List[str] = []
    current_len = 0
    for paragraph in text.split("\n\n"):
        if current_len + len(paragraph) + 2 > max_chars:
            if current:
                chunks.append("\n\n".join(current))
            current = [paragraph]
            current_len = len(paragraph)
        else:
            current.append(paragraph)
            current_len += len(paragraph) + 2
    if current:
        chunks.append("\n\n".join(current))
    return chunks

def summarize_text_naive(text: str, max_sentences: int = 5) -> str:
    sentences = re.split(r"(?<=[.!?])\s+", text)
    top = [s for s in sentences if len(s.strip()) > 0][:max_sentences]
    return " ".join(top).strip()

def extract_simple_insights(text: str, top_k: int = 5) -> List[str]:
    findings: List[str] = []
    patterns = [r"revenue[^\n\.]*", r"profit[^\n\.]*", r"margin[^\n\.]*", r"guidance[^\n\.]*", r"risk[^\n\.]*"]
    for p in patterns:
        m = re.search(p, text, flags=re.IGNORECASE)
        if m:
            findings.append(m.group(0).strip())
    if not findings and text:
        findings = [s.strip() for s in re.split(r"\n+", text) if len(s.strip()) > 0][:top_k]
    return findings[:top_k]

def extract_simple_risks(text: str, top_k: int = 5) -> List[str]:
    risks: List[str] = []
    for line in text.splitlines():
        if re.search(r"risk|uncertain|challenge|headwind|pressure", line, flags=re.IGNORECASE):
            risks.append(line.strip())
    if not risks and text:
        risks = extract_simple_insights(text, top_k)
    return risks[:top_k]

def naive_recommendations(text: str, top_k: int = 3) -> List[str]:
    recs: List[str] = []
    if re.search(r"strong\s+growth|beat|raised\s+guidance|record", text, re.IGNORECASE):
        recs.append("Consider Buy based on reported strength and guidance")
    if re.search(r"flat|mixed|inline", text, re.IGNORECASE):
        recs.append("Consider Hold pending further catalysts")
    if re.search(r"miss|decline|lowered\s+guidance|weak", text, re.IGNORECASE):
        recs.append("Consider Sell due to weakness and risks")
    if not recs:
        recs.append("Further analysis required; consider Neutral/Hold")
    return recs[:top_k]

def render_reference_pdf(snippets: List[str]) -> bytes:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)
    y = 800
    for s in snippets:
        for line in re.findall(r".{1,90}", s):
            c.drawString(40, y, line)
            y -= 14
            if y < 60:
                c.showPage()
                y = 800
        y -= 10
    c.save()
    data = buffer.getvalue()
    buffer.close()
    return data

def analyze_document(pdf_path: str, query: str) -> Dict[str, Any]:
    text = extract_text_from_pdf(pdf_path)
    if not text:
        text = ""
    use_openai = bool(os.getenv("OPENAI_API_KEY")) and OpenAI is not None
    if use_openai:
        try:
            client = OpenAI()
            model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            system = (
                "You analyze financial PDFs and answer user questions. "
                "Return STRICT JSON with keys: summary(string), insights(array of strings), "
                "recommendations(array of strings), risks(array of strings), references(array of strings)."
            )
            prompt = (
                "User query:\n" + query.strip() + "\n\n" +
                "PDF content (may be truncated):\n" + text[:120000]
            )
            resp = client.chat.completions.create(
                model=model,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
            )
            content = resp.choices[0].message.content if resp.choices else "{}"
            data = json.loads(content or "{}")
            return {
                "summary": data.get("summary", ""),
                "insights": data.get("insights", []),
                "recommendations": data.get("recommendations", []),
                "risks": data.get("risks", []),
                "references": data.get("references", []),
                "query": query,
                "provider": "openai",
                "model": model,
            }
        except Exception:
            pass
    summary = summarize_text_naive(text)
    insights = extract_simple_insights(text)
    risks = extract_simple_risks(text)
    recommendations = naive_recommendations(text)
    references = [f"snippet:{i+1}" for i in range(min(5, len(insights)))]
    return {
        "summary": summary,
        "insights": insights,
        "recommendations": recommendations,
        "risks": risks,
        "references": references,
        "query": query,
        "provider": "heuristic",
    }