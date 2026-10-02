#!/usr/bin/env python3
"""Audit a materialized site offline. No crawler, browser automation or network IO."""
import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

FRAMER_RUNTIME = re.compile(
    r"(?:framerusercontent\.com/(?:sites|modules)/|events\.framer\.com|"
    r"framer\.com/m/|https?://[^\s\"']*/(?:framer|framer-motion)(?:@|/))", re.I
)
ASSET_HOSTS = {"framerusercontent.com", "fonts.framer.com"}


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids, self.links, self.assets = set(), [], []
        self.inline_code, self.code_tag = [], None
        self.base = None
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in {"script", "style"}:
            self.code_tag = tag
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("name"):
            self.ids.add(attrs["name"])
        if tag == "base" and attrs.get("href"):
            self.base = attrs["href"]
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
        if tag in {"img", "script", "iframe", "audio", "video", "source"} and attrs.get("src"):
            self.assets.append(attrs["src"])
        if tag == "video" and attrs.get("poster"):
            self.assets.append(attrs["poster"])
        if tag == "link" and attrs.get("href") and set(attrs.get("rel", "").split()) & {"stylesheet", "icon", "preload", "modulepreload"}:
            self.assets.append(attrs["href"])

    def handle_endtag(self, tag):
        if tag == self.code_tag:
            self.code_tag = None

    def handle_data(self, data):
        if self.code_tag:
            self.inline_code.append(data)


def route_for(path, root):
    relative = path.relative_to(root).as_posix()
    if relative == "index.html":
        return "/"
    if relative.endswith("/index.html"):
        return "/" + relative[:-10]
    return "/" + relative


def audit(root, origin=None, routes=None):
    root = Path(root).resolve()
    if not root.is_dir():
        raise ValueError("Site directory does not exist")
    synthetic_origin = "https://local.invalid"
    local_hosts = {"local.invalid"}
    if origin:
        parsed = urlsplit(origin)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("--origin must be an HTTP(S) origin")
        local_hosts.add(parsed.netloc)
    pages = {}
    issues, warnings = [], []
    for file in sorted(root.rglob("*.html")):
        if file.is_symlink() or not file.resolve().is_relative_to(root):
            continue
        text = file.read_text(encoding="utf-8")
        page = pages[file] = Page(text)
        if any(FRAMER_RUNTIME.search(value) for value in page.assets):
            issues.append({"file": str(file.relative_to(root)), "kind": "framer-runtime"})
        if any(FRAMER_RUNTIME.search(value) for value in page.inline_code):
            warnings.append({"file": str(file.relative_to(root)), "kind": "review-inline-framer-reference"})
    if not pages:
        issues.append({"kind": "no-html-pages"})
    for file in sorted(root.rglob("*")):
        if file.is_symlink() or file.suffix not in {".js", ".mjs", ".css"} or not file.is_file():
            continue
        if FRAMER_RUNTIME.search(file.read_text(encoding="utf-8", errors="replace")):
            warnings.append({"file": str(file.relative_to(root)), "kind": "review-code-framer-reference"})

    def resolve(raw, page_route):
        base_uri = page_route if urlsplit(page_route).scheme else synthetic_origin + page_route
        url = urlsplit(urljoin(base_uri, raw))
        if url.scheme not in {"http", "https"} or url.netloc not in local_hosts:
            return None, url
        relative = unquote(url.path).lstrip("/")
        candidate = (root / relative).resolve()
        if not candidate.is_relative_to(root):
            return False, url
        options = [candidate, candidate / "index.html"]
        if not candidate.suffix:
            options.append(candidate.with_suffix(".html"))
        return next((item for item in options if item.is_file() and not item.is_symlink()), False), url

    for file, page in pages.items():
        source = file.relative_to(root).as_posix()
        base = route_for(file, root)
        if page.base:
            base = urljoin(base, page.base)
        for kind, values in (("link", page.links), ("asset", page.assets)):
            for raw in values:
                target, url = resolve(raw, base)
                if target is False:
                    issues.append({"file": source, "kind": "missing-" + kind, "url": raw})
                elif target in pages and url.fragment and not url.fragment.startswith(":~:text="):
                    if unquote(url.fragment) not in pages[target].ids:
                        issues.append({"file": source, "kind": "missing-anchor", "url": raw})
                elif target is None and kind == "asset" and url.hostname in ASSET_HOSTS:
                    issues.append({"file": source, "kind": "remote-framer-asset", "url": raw})
                if url.netloc in local_hosts - {"local.invalid"}:
                    issues.append({"file": source, "kind": "link-to-source-domain", "url": raw})
        if page.base:
            warnings.append({"file": source, "kind": "base-element", "url": page.base})
    for route in routes or []:
        path = route.get("localPath") if isinstance(route, dict) else route
        if not isinstance(path, str):
            raise ValueError("Each expected route needs a localPath string")
        target, _ = resolve(path, "/")
        if target not in pages:
            issues.append({"kind": "missing-page", "url": path})
    return {"htmlPages": len(pages), "issues": issues, "warnings": warnings,
            "limits": "Static HTML links/assets/anchors and known Framer references only; no visual, CSS url(), srcset, JS-import, form or browser validation."}


def self_test():
    from tempfile import TemporaryDirectory
    with TemporaryDirectory() as temp:
        root = Path(temp)
        assert audit(root)["issues"] == [{"kind": "no-html-pages"}]
        (root / "notas").mkdir()
        (root / "notas" / "estreia").mkdir()
        (root / "assets").mkdir()
        (root / "assets" / "capa.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
        (root / "index.html").write_text('<a href="/notas/estreia/?x=1#se%C3%A7%C3%A3o">Ler</a><img src="assets/capa.svg"><a href="https://external.example/">Externo</a><a href="https://framer.com/m/Component-test.js">Fonte pública</a>', encoding="utf-8")
        detail = root / "notas" / "estreia" / "index.html"
        detail.write_text('<h1 id="seção">Título</h1><a href="../../">Home</a>', encoding="utf-8")
        result = audit(root, "https://source.framer.app", ["/", "/notas/estreia"])
        assert result["htmlPages"] == 2 and not result["issues"], result
        detail.write_text('<a href="/perdida">404</a><a href="/#ausente">Âncora</a><script src="https://framerusercontent.com/sites/x.js"></script><a href="https://source.framer.app/">Sai para origem</a>', encoding="utf-8")
        kinds = {issue["kind"] for issue in audit(root, "https://source.framer.app", ["/faltou"])["issues"]}
        assert {"missing-link", "missing-anchor", "framer-runtime", "link-to-source-domain", "missing-page"} <= kinds, kinds
        detail.write_text('<base href="https://external.example/"><a href="/external">Externo</a><script>const reference = "https://framer.com/m/test.js";</script>', encoding="utf-8")
        result = audit(root)
        assert not any(issue["kind"] == "framer-runtime" for issue in result["issues"]), result
        assert any(warning["kind"] == "review-inline-framer-reference" for warning in result["warnings"]), result
    print("Self-test passed: connected routes, nested paths, UTF-8 anchors, source escapes, missing pages and Framer runtime.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site", nargs="?")
    parser.add_argument("--origin")
    parser.add_argument("--routes", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return 0
    if not args.site:
        parser.error("site is required unless --self-test is used")
    expected = None
    if args.routes:
        expected = json.loads(args.routes.read_text(encoding="utf-8"))
        if isinstance(expected, dict):
            expected = expected["routes"]
        if not isinstance(expected, list):
            parser.error("routes must be an array or an object with a routes array")
    try:
        report = audit(args.site, args.origin, expected)
    except (ValueError, OSError) as error:
        parser.error(str(error))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report["issues"] else 0


if __name__ == "__main__":
    sys.exit(main())
