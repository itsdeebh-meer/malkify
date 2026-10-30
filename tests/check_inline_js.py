from html.parser import HTMLParser
from pathlib import Path
import subprocess
import tempfile

class InlineScripts(HTMLParser):
    def __init__(self):
        super().__init__()
        self.current = None
        self.scripts = []
    def handle_starttag(self, tag, attrs):
        if tag == "script":
            attrs = dict(attrs)
            if "src" not in attrs:
                self.current = (attrs.get("type", ""), [])
    def handle_data(self, data):
        if self.current is not None:
            self.current[1].append(data)
    def handle_endtag(self, tag):
        if tag == "script" and self.current is not None:
            self.scripts.append(self.current)
            self.current = None

files = list(Path(".").glob("**/*.html"))
assert files, "No HTML files found"
checked = 0
with tempfile.TemporaryDirectory() as tmp:
    for html in files:
        parser = InlineScripts()
        parser.feed(html.read_text(encoding="utf-8"))
        for index, (kind, chunks) in enumerate(parser.scripts):
            source = "".join(chunks).strip()
            if not source:
                continue
            suffix = ".mjs" if kind == "module" else ".js"
            target = Path(tmp) / f"inline-{checked}{suffix}"
            target.write_text(source, encoding="utf-8")
            subprocess.run(["node", "--check", str(target)], check=True)
            checked += 1
print(f"Validated {len(files)} HTML documents and {checked} inline JavaScript blocks.")
