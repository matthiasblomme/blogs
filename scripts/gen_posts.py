from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
import re
from urllib.parse import quote_plus
import yaml


# -----------------------------------------------------------------------------
# Paths / constants
# -----------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
POSTS_DIR = DOCS_DIR / "posts"
MKDOCS_YML = ROOT / "mkdocs.yml"

META_START = "<!--MD_POST_META:START-->"
META_END = "<!--MD_POST_META:END-->"

LATEST_START = "<!--MD_LATEST_POSTS:START-->"
LATEST_END = "<!--MD_LATEST_POSTS:END-->"

ALLPOSTS_START = "<!--MD_ALL_POSTS:START-->"
ALLPOSTS_END = "<!--MD_ALL_POSTS:END-->"

ARCHIVE_START = "<!--MD_ARCHIVE:START-->"
ARCHIVE_END   = "<!--MD_ARCHIVE:END-->"

WORDS_PER_MINUTE = 200
MIN_READING_MINUTES = 1

# Files in POSTS_DIR that are index/meta pages, not posts
_SKIP_NAMES = {"index.md", "archive.md"}


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def load_mkdocs_site_url() -> str:
    """
    Reads site_url from mkdocs.yml. Returns '' if not set.
    """
    if not MKDOCS_YML.exists():
        return ""
    data = yaml.safe_load(MKDOCS_YML.read_text(encoding="utf-8")) or {}
    return str(data.get("site_url", "")).rstrip("/")


def sanitize_front_matter_text(fm_text: str) -> str:
    """
    Auto-quote title/description when they contain ':' and are unquoted.
    Prevents YAML ScannerError like: "mapping values are not allowed here".
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


def parse_front_matter(text: str) -> tuple[dict, str]:
    """
    Returns (front_matter_dict, body_without_front_matter).
    If no front matter present, returns ({}, original_text).
    """
    if not text.startswith("---"):
        return {}, text

    # Split into: --- fm --- body
    try:
        _, fm_text, body = text.split("---", 2)
    except ValueError:
        # malformed front matter
        return {}, text

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


def parse_date_for_sort(value) -> datetime:
    """
    Parses date from front-matter for sorting.
    Accepts datetime/date/string. Unknown formats -> very old date.
    """
    if isinstance(value, datetime):
        return value
    if isinstance(value, date):
        return datetime(value.year, value.month, value.day)
    if isinstance(value, str):
        # try YYYY-MM-DD first
        try:
            return datetime.strptime(value.strip().strip("'").strip('"'), "%Y-%m-%d")
        except ValueError:
            pass
        # try ISO-ish
        try:
            return datetime.fromisoformat(value.strip().strip("'").strip('"'))
        except ValueError:
            pass
    return datetime(1970, 1, 1)


def strip_markdown(text: str) -> str:
    """
    Very rough markdown stripping for word count:
    - remove code blocks
    - remove inline code
    - remove images/links markup
    """
    # remove fenced code blocks
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    # remove inline code
    text = re.sub(r"`[^`]*`", " ", text)
    # remove images ![alt](url)
    text = re.sub(r"!\[[^\]]*\]\([^\)]*\)", " ", text)
    # remove links [text](url) -> keep text
    text = re.sub(r"\[([^\]]+)\]\([^\)]*\)", r"\1", text)
    # remove HTML tags (your meta blocks etc.)
    text = re.sub(r"<[^>]+>", " ", text)
    return text


def estimate_reading_time_minutes(md_body: str) -> int:
    cleaned = strip_markdown(md_body)
    words = re.findall(r"\b\w+\b", cleaned)
    minutes = max(MIN_READING_MINUTES, int(round(len(words) / WORDS_PER_MINUTE)))
    return minutes


def format_reading_time(minutes: int) -> str:
    return f"{minutes} min"


def compute_page_url(site_url: str, md_path: Path) -> str:
    """
    Produces a URL that matches use_directory_urls: true behavior:
    /relative/path/to/page/
    """
    if not site_url:
        return ""
    rel = md_path.resolve().relative_to(DOCS_DIR.resolve())
    page_path = rel.with_suffix("").as_posix()
    return f"{site_url}/{page_path}/"


# -----------------------------------------------------------------------------
# Meta block injection
# -----------------------------------------------------------------------------
def build_meta_block(fm: dict, page_url: str) -> str:
    author = fm.get("author")
    date_value = normalize_date(fm.get("date"))
    reading_time = fm.get("reading_time")
    tags = fm.get("tags") or []

    left_parts: list[str] = []
    if author:
        left_parts.append(str(author))
    if date_value:
        left_parts.append(str(date_value))
    if reading_time:
        left_parts.append(f"⏱ {reading_time}")

    left_text = " · ".join(left_parts)

    right_html = ""
    if page_url:
        share_url = "https://www.linkedin.com/sharing/share-offsite/?url=" + quote_plus(page_url)
        right_html = (
            '<span class="post-share-label">Share:</span> '
            f'<a class="post-share post-share-linkedin" '
            f'href="{share_url}" target="_blank" rel="noopener" '
            f'title="Share on LinkedIn">[<span class="in">in</span>]</a>'
        )

    tags_html = ""
    if isinstance(tags, (list, tuple)) and tags:
        tag_items = " ".join(f'<span class="md-tag">{str(t)}</span>' for t in tags)
        tags_html = f'<div class="md-post-tags">{tag_items}</div>'

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
    pattern = re.compile(rf"{re.escape(META_START)}.*?{re.escape(META_END)}\s*", re.DOTALL)
    return re.sub(pattern, "", body).lstrip()


def inject_after_banner(body: str, meta_block: str) -> str:
    """
    Inserts meta block after banner line `![cover](...){ .md-banner }` if present,
    else inserts at top of body.
    """
    lines = body.splitlines()
    out: list[str] = []
    inserted = False

    for line in lines:
        out.append(line)
        if (not inserted) and line.strip().startswith("![cover]") and ".md-banner" in line:
            out.append("")
            out.append(meta_block)
            out.append("")
            inserted = True

    if not inserted:
        out.insert(0, meta_block)
        out.insert(1, "")

    return "\n".join(out).strip() + "\n"


# -----------------------------------------------------------------------------
# Index generation
# -----------------------------------------------------------------------------
@dataclass
class Post:
    md_path: Path
    title: str
    date_sort: datetime
    date_display: str
    reading_time: str
    rel_url: str


def collect_posts(site_url: str) -> list[Post]:
    posts: list[Post] = []

    for md in POSTS_DIR.rglob("*.md"):
        if md.name.lower() in _SKIP_NAMES:
            continue

        raw = md.read_text(encoding="utf-8")
        fm, body = parse_front_matter(raw)
        if not fm:
            continue

        title = str(fm.get("title", md.stem))
        dt_sort = parse_date_for_sort(fm.get("date"))
        dt_disp = normalize_date(fm.get("date"))

        # ensure reading_time exists
        rt = fm.get("reading_time")
        if not rt:
            mins = estimate_reading_time_minutes(body)
            rt = format_reading_time(mins)

        # rel_url for mkdocs internal links (use directory urls)
        rel = md.resolve().relative_to(DOCS_DIR.resolve())
        rel_url = rel.with_suffix("").as_posix() + "/"

        posts.append(
            Post(
                md_path=md,
                title=title,
                date_sort=dt_sort,
                date_display=dt_disp,
                reading_time=str(rt),
                rel_url=rel_url,
            )
        )

    # newest first
    posts.sort(key=lambda p: p.date_sort, reverse=True)
    return posts


def replace_between_markers(text: str, start: str, end: str, replacement: str) -> str:
    """
    Replaces the content between markers (inclusive markers stay).
    If markers missing, appends them + replacement at the end.
    """
    pattern = re.compile(rf"{re.escape(start)}.*?{re.escape(end)}", re.DOTALL)
    block = f"{start}\n{replacement}\n{end}"
    if pattern.search(text):
        return pattern.sub(block, text)
    return text.rstrip() + "\n\n" + block + "\n"


def render_latest_posts(posts: list[Post], limit: int = 5) -> str:
    lines = []
    for p in posts[:limit]:
        lines.append(f"- **{p.date_display}** — [{p.title}]({p.rel_url}) · *{p.reading_time}*")
    return "\n".join(lines) if lines else "_No posts yet._"


def render_all_posts(posts: list[Post]) -> str:
    lines = []
    for p in posts:
        lines.append(f"- **{p.date_display}** — [{p.title}]({p.rel_url}) · *{p.reading_time}*")
    return "\n".join(lines) if lines else "_No posts yet._"


def render_archive(posts: list[Post]) -> str:
    """
    Renders posts grouped by year then month, newest first.
    Uses directory URL format consistent with other index pages.
    """
    from collections import defaultdict
    import calendar

    groups: dict[int, dict[int, list[Post]]] = defaultdict(lambda: defaultdict(list))
    for p in posts:
        groups[p.date_sort.year][p.date_sort.month].append(p)

    lines: list[str] = []
    for year in sorted(groups.keys(), reverse=True):
        lines.append(f"## {year}")
        for month in sorted(groups[year].keys(), reverse=True):
            lines.append(f"### {calendar.month_name[month]}")
            for p in groups[year][month]:
                lines.append(
                    f"- **{p.date_display}** — [{p.title}]({p.rel_url}) · *{p.reading_time}*"
                )
            lines.append("")
    return "\n".join(lines).rstrip()


def update_index_pages(posts: list[Post]):
    # Home index
    home_index = DOCS_DIR / "index.md"
    if home_index.exists():
        txt = home_index.read_text(encoding="utf-8")
        txt = replace_between_markers(txt, LATEST_START, LATEST_END, render_latest_posts(posts, limit=5))
        home_index.write_text(txt, encoding="utf-8")

    # Posts overview: prefer docs/posts.md if it exists, else docs/posts/index.md
    posts_overview = DOCS_DIR / "posts.md"
    if not posts_overview.exists():
        posts_overview = POSTS_DIR / "index.md"

    if posts_overview.exists():
        txt = posts_overview.read_text(encoding="utf-8")
        txt = replace_between_markers(txt, ALLPOSTS_START, ALLPOSTS_END, render_all_posts(posts))
        posts_overview.write_text(txt, encoding="utf-8")


def update_archive_page(posts: list[Post], verbose: bool = False):
    archive_path = POSTS_DIR / "archive.md"
    if not archive_path.exists():
        return

    txt = archive_path.read_text(encoding="utf-8")
    new_txt = replace_between_markers(txt, ARCHIVE_START, ARCHIVE_END, render_archive(posts))

    if new_txt == txt:
        if verbose:
            print("  [skip] archive.md (unchanged)")
        return

    archive_path.write_text(new_txt, encoding="utf-8")
    if verbose:
        print("  [write] archive.md")


# -----------------------------------------------------------------------------
# Per-post processing
# -----------------------------------------------------------------------------
def process_post(site_url: str, md_path: Path, verbose: bool = False) -> bool:
    """
    Processes a single post: ensures reading_time, injects meta block.
    Returns True if the file was written, False if unchanged (skipped).
    """
    raw = md_path.read_text(encoding="utf-8")
    fm, body = parse_front_matter(raw)
    if not fm:
        return False

    # Ensure reading_time exists (compute if missing; preserve if already set)
    if not fm.get("reading_time"):
        mins = estimate_reading_time_minutes(body)
        fm["reading_time"] = format_reading_time(mins)

    # Remove previously injected meta block and re-inject (idempotent)
    body = remove_existing_meta_block(body)

    page_url = compute_page_url(site_url, md_path)
    meta_block = build_meta_block(fm, page_url)
    new_body = inject_after_banner(body, meta_block)

    new_text = (
        "---\n"
        + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True).strip()
        + "\n---\n\n"
        + new_body
    )

    if new_text == raw:
        if verbose:
            print(f"  [skip] {md_path.name}")
        return False

    md_path.write_text(new_text, encoding="utf-8")
    if verbose:
        print(f"  [write] {md_path.name}")
    return True


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generate post meta and index pages.")
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Print per-file status (skipped vs written).",
    )
    args = parser.parse_args()
    verbose = args.verbose

    site_url = load_mkdocs_site_url()

    # 1) Update each post (reading_time + meta block injection)
    written = skipped = 0
    for md in POSTS_DIR.rglob("*.md"):
        if md.name.lower() in _SKIP_NAMES:
            continue
        if process_post(site_url, md, verbose=verbose):
            written += 1
        else:
            skipped += 1

    # 2) Rebuild homepage + posts overview lists
    posts = collect_posts(site_url)
    update_index_pages(posts)

    # 3) Rebuild archive page
    update_archive_page(posts, verbose=verbose)

    print(f"Done. Posts: {written} written, {skipped} skipped.")


if __name__ == "__main__":
    main()
