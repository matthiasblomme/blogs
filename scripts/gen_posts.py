from pathlib import Path
import re
import yaml
from datetime import datetime, date
from urllib.parse import quote_plus

ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
POSTS_DIR = DOCS_DIR / "posts"
MKDOCS_YML = ROOT / "mkdocs.yml"

META_START = "<!--MD_POST_META:START-->"
META_END = "<!--MD_POST_META:END-->"


def load_site_url() -> str:
    if not MKDOCS_YML.exists():
        return ""
    data = yaml.safe_load(MKDOCS_YML.read_text(encoding="utf-8")) or {}
    return str(data.get("site_url", "")).rstrip("/")


SITE_URL = load_site_url()


def sanitize_front_matter_text(fm_text: str) -> str:
    """
    Auto-quote title/description when they contain ':' and are unquoted.
    Keeps your existing markdown valid without manual edits.
    """
    fixed_lines = []
    for line in fm_text.splitlines():
        stripped = line.strip()
        for key in ("title", "description"):
            prefix = f"{key}:"
            if stripped.startswith(prefix):
                value = line.split(":", 1)[1].strip()
                if ":" in value and not (value.startswith('"') or value.startswith("'")):
                    line = f'{key}: "{value}"'
                break
        fixed_lines.append(line)
    return "\n".join(fixed_lines)


def parse_front_matter(text: str):
    if not text.startswith("---"):
        return {}, text

    _, fm_text, body = text.split("---", 2)
    fm_text = sanitize_front_matter_text(fm_text)
    data = yaml.safe_load(fm_text) or {}
    return data, body.lstrip()


def normalize_date(value) -> str:
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if value is None:
        return ""
    return str(value)


def build_meta_block(fm: dict, page_url: str) -> str:
    author = fm.get("author")
    date_value = normalize_date(fm.get("date"))
    reading_time = fm.get("reading_time")
    tags = fm.get("tags") or []

    left_parts = []
    if author:
        left_parts.append(str(author))
    if date_value:
        left_parts.append(date_value)
    if reading_time:
        left_parts.append(f"⏱ {reading_time}")

    left_text = " · ".join(left_parts)

    right_html = ""
    if page_url:
        share_url = "https://www.linkedin.com/sharing/share-offsite/?url=" + quote_plus(page_url)
        right_html = (
            '<span class="post-share-label">Share:</span>'
            f'<a class="post-share post-share-linkedin" '
            f'href="{share_url}" target="_blank" rel="noopener" '
            f'title="Share on LinkedIn">'
            f'in'
            f'</a>'
        )



    tags_html = ""
    if isinstance(tags, (list, tuple)) and tags:
        # show in the same order as in front-matter
        tag_items = " ".join(f'<span class="md-tag">{str(t)}</span>' for t in tags)
        tags_html = f'<div class="md-tags">{tag_items}</div>'

    return (
        f"{META_START}\n"
        f'<div class="md-post-meta">\n'
        f'  <div class="md-post-meta-left">{left_text}</div>\n'
        f'  <div class="md-post-meta-right">{right_html}</div>\n'
        f"</div>\n"
        f'<hr class="md-post-divider"/>\n'
        f"{tags_html}\n"
        f"{META_END}"
    )


def remove_existing_meta_block(body: str) -> str:
    # Remove any previous injected block between markers (single or multiple occurrences).
    pattern = re.compile(rf"{re.escape(META_START)}.*?{re.escape(META_END)}\s*", re.DOTALL)
    return re.sub(pattern, "", body).lstrip()


def compute_page_url(md_path: Path) -> str:
    if not SITE_URL:
        return ""
    rel_path = md_path.resolve().relative_to(DOCS_DIR.resolve())
    page_path = rel_path.with_suffix("").as_posix()
    # use_directory_urls: true → trailing slash
    return f"{SITE_URL}/{page_path}/"


def inject_after_banner(body: str, meta_block: str) -> str:
    lines = body.splitlines()
    out = []
    inserted = False

    for line in lines:
        out.append(line)
        # banner line looks like: ![cover](cover.png){ .md-banner }
        if (not inserted) and line.strip().startswith("![cover]") and ".md-banner" in line:
            out.append("")
            out.append(meta_block)
            out.append("")
            inserted = True

    if not inserted:
        # No banner found: put meta at top
        out.insert(0, meta_block)
        out.insert(1, "")

    return "\n".join(out).strip() + "\n"


def process_post(md_path: Path):
    raw = md_path.read_text(encoding="utf-8")
    fm, body = parse_front_matter(raw)
    if not fm:
        return

    body = remove_existing_meta_block(body)

    page_url = compute_page_url(md_path)
    meta_block = build_meta_block(fm, page_url)

    new_body = inject_after_banner(body, meta_block)

    # Preserve your YAML front-matter (but dump safely)
    new_text = (
            "---\n"
            + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True).strip()
            + "\n---\n\n"
            + new_body
    )

    md_path.write_text(new_text, encoding="utf-8")


def main():
    for md in POSTS_DIR.rglob("*.md"):
        if md.name.lower() == "index.md":
            continue
        process_post(md)

    print("Post meta generation complete.")


if __name__ == "__main__":
    main()
