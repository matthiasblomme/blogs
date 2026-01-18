import pathlib
import re
import time
import math
import calendar
from collections import defaultdict
from datetime import date as sysdate

# ---------------- Configuration ----------------

DOCS_DIR     = pathlib.Path("docs")
POSTS_DIR    = DOCS_DIR / "posts"
INDEX_OUT    = POSTS_DIR / "index.md"
ARCHIVE_OUT  = POSTS_DIR / "archive.md"
HOMEPAGE     = DOCS_DIR / "index.md"

BLOCK_START  = "<!--LATEST_POST:START-->"
BLOCK_END    = "<!--LATEST_POST:END-->"
LATEST_COUNT = 5

VALID_EXTS = {".md", ".markdown", ".mkd", ".mdown"}
WORDS_PER_MINUTE = 200
BANNER_MARKER = "![cover](cover.png){ .md-banner }"


# ---------------- Helpers ----------------

def strip_front_matter(text: str):
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, flags=re.DOTALL)
    if m:
        return text[m.end():], m.group(1).splitlines()
    return text, []


def extract_title(text: str, fallback: str) -> str:
    for pat in [
        r"(?m)^title:\s*(.+)$",
        r"(?m)^\#\s+(.*)$",
        r"(?m)^\#\#\s+(.*)$",
        r"(?m)^\#{1,6}\s+(.*)$"
    ]:
        m = re.search(pat, text)
        if m:
            return m.group(1).strip()
    return fallback


def extract_date(fm_lines):
    for line in fm_lines:
        if line.startswith("date:"):
            return line.split(":", 1)[1].strip()
    return None


def extract_description(body: str) -> str:
    lines = body.splitlines()
    in_code = False
    para = []

    for line in lines:
        l = line.strip()

        if l.startswith("```"):
            in_code = not in_code
            continue
        if in_code or not l:
            if para:
                break
            continue
        if l.startswith(("#", "-", "*", ">")):
            continue

        para.append(l)

    desc = " ".join(para)
    desc = re.sub(r"\s+", " ", desc)
    return (desc[:160].rstrip(". ") + ".") if desc else ""


def calculate_reading_time(body: str) -> str:
    words = re.findall(r"\b\w+\b", body)
    minutes = max(1, math.ceil(len(words) / WORDS_PER_MINUTE))
    return f"{minutes} min"


def link_from_home(p: pathlib.Path) -> str:
    return p.as_posix().replace("docs/", "", 1)


def link_from_posts_index(p: pathlib.Path) -> str:
    return p.relative_to(POSTS_DIR).as_posix()


# ---------------- Front-matter + Banner ----------------

def ensure_front_matter(p: pathlib.Path):
    raw = p.read_text(encoding="utf-8-sig")
    body, fm_lines = strip_front_matter(raw)

    title = extract_title(raw, p.stem.replace("-", " "))
    description = extract_description(body)
    reading_time = calculate_reading_time(body)

    existing_date = extract_date(fm_lines)
    post_date = existing_date or sysdate.today().isoformat()

    def has(key):
        return any(l.startswith(f"{key}:") for l in fm_lines)

    new_fm = []

    if not has("title"):
        new_fm.append(f"title: {title}")
    new_fm.append(f"date: {post_date}")

    cover = p.parent / "cover.png"
    if cover.exists() and not has("image"):
        new_fm.append("image: cover.png")

    if description and not has("description"):
        new_fm.append(f"description: {description}")

    if not has("reading_time"):
        new_fm.append(f"reading_time: {reading_time}")

    # merge with existing (preserve manual fields)
    merged = new_fm + [l for l in fm_lines if not any(l.startswith(k.split(":")[0] + ":") for k in new_fm)]

    banner = ""
    if cover.exists() and not body.lstrip().startswith(BANNER_MARKER):
        banner = BANNER_MARKER + "\n\n"

    new_text = (
            "---\n"
            + "\n".join(merged)
            + "\n---\n\n"
            + banner
            + body.lstrip()
    )

    p.write_text(new_text, encoding="utf-8")

    return post_date, title, reading_time


# ---------------- Collect Posts ----------------

posts = [
    p for p in POSTS_DIR.rglob("*")
    if p.is_file()
       and p.suffix.lower() in VALID_EXTS
       and p.name.lower() not in ("index.md", "archive.md")
]

entries = []
for p in posts:
    post_date, title, rt = ensure_front_matter(p)
    entries.append((post_date, p, title, rt))

entries.sort(key=lambda x: x[0], reverse=True)


# ---------------- Posts Index ----------------

index_lines = ["# Posts", ""]
for d, p, title, rt in entries:
    index_lines.append(f"- **{d}** — [{title}]({link_from_posts_index(p)}) · _{rt}_")
index_lines.append("")

INDEX_OUT.write_text("\n".join(index_lines), encoding="utf-8")


# ---------------- Archive ----------------

archive = defaultdict(lambda: defaultdict(list))
for d, p, title, rt in entries:
    y, m, _ = d.split("-")
    archive[int(y)][int(m)].append((d, p, title, rt))

archive_lines = ["# Archive", ""]
for year in sorted(archive.keys(), reverse=True):
    archive_lines.append(f"## {year}")
    for month in sorted(archive[year].keys(), reverse=True):
        archive_lines.append(f"### {calendar.month_name[month]}")
        for d, p, title, rt in archive[year][month]:
            archive_lines.append(f"- **{d}** — [{title}]({link_from_posts_index(p)}) · _{rt}_")
        archive_lines.append("")
    archive_lines.append("")

ARCHIVE_OUT.write_text("\n".join(archive_lines).rstrip() + "\n", encoding="utf-8")


# ---------------- Homepage Latest ----------------

home = HOMEPAGE.read_text(encoding="utf-8-sig")

latest = entries[:LATEST_COUNT]
if latest:
    block = "\n".join(
        f"- **{d}** — [{title}]({link_from_home(p)}) · _{rt}_"
        for d, p, title, rt in latest
    )
else:
    block = "_No posts yet._"

pattern = re.compile(re.escape(BLOCK_START) + r".*?" + re.escape(BLOCK_END), re.DOTALL)
replacement = f"{BLOCK_START}\n{block}\n{BLOCK_END}"

home = pattern.sub(replacement, home) if pattern.search(home) else home + "\n\n" + replacement
HOMEPAGE.write_text(home, encoding="utf-8")
