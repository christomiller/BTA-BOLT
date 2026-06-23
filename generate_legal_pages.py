import json, os, html, re

BASE = os.path.dirname(os.path.abspath(__file__))


def summary_to_bullets(summary):
    # split into sentences on ". " followed by a capital letter, to avoid
    # breaking on abbreviations like "Inc." or "St."
    sentences = re.split(r"(?<=[.])\s+(?=[A-Z])", summary.strip())
    items = "".join(f"<li>{html.escape(s.strip())}</li>" for s in sentences if s.strip())
    return f'<ul class="summary-list">{items}</ul>'
props = json.load(open(os.path.join(BASE, "properties/bta_properties.json")))
legal_data = json.load(open(os.path.join(BASE, "properties/legal_docs_data.json")))

with open(os.path.join(BASE, "LegalDocsTemplate.html")) as f:
    template = f.read()

out_dir = os.path.join(BASE, "properties/legal")
os.makedirs(out_dir, exist_ok=True)

for p in props:
    key = p["key"]
    name = p["Property"]
    entry = legal_data.get(key)

    note_block = ""
    if entry and entry.get("note"):
        note_block = f'<div class="legal-note"><strong>Note:</strong> {html.escape(entry["note"])}</div>'

    if not entry:
        note_block = (
            '<div class="legal-note"><strong>Note:</strong> '
            'No legal documents have been scanned/identified for this property yet.</div>'
        )
        rows = '<tr><td colspan="3"><em>No documents available.</em></td></tr>'
    else:
        row_html = []
        for doc in entry["documents"]:
            link = f'../legal_docs/{key}/{doc["file"]}'
            row_html.append(
                f'<tr><td>{html.escape(doc["type"])}</td>'
                f'<td><a href="{link}">{html.escape(doc["title"])}</a></td>'
                f'<td>{summary_to_bullets(doc["summary"])}</td></tr>'
            )
        rows = "\n".join(row_html)

    page = template.replace("__PROPERTY_NAME__", html.escape(name)).replace(
        "__NOTE_BLOCK__", note_block
    ).replace("__DOC_ROWS__", rows)

    # the back-link and title use __PROPERTY_NAME__ as both display text and filename;
    # property page filenames use the raw (unescaped) name
    page = page.replace(
        f'../pages/{html.escape(name)}.html', f'../pages/{name}.html'
    )

    out_path = os.path.join(out_dir, f"{key}.html")
    with open(out_path, "w") as f:
        f.write(page)
    print("wrote", out_path)

print("done,", len(props), "property pages generated")
