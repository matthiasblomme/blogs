import subprocess, pathlib, time, re, calendar, math
from collections import defaultdict

DOCS_DIR      = pathlib.Path("docs")
POSTS_DIR     = DOCS_DIR / "posts"
INDEX_OUT     = POSTS_DIR / "index.md"
ARCHIVE_OUT   = POSTS_DIR / "archive.md"
HOMEPAGE      = DOCS_DIR / "index.md"

BLOCK_START   = "<!--LATEST_POST:START-->"
BLOCK_END     = "<!--LATEST_POST:END-->"
LATEST_COUNT  = 5

VALID_EXTS = {".md", ".markdown", ".mkd", ".mdown"}
WORDS_PER_MINUTE = 200


# ---------------- Git timestamp ----------------

def git_timestamp(p: pathlib.Path) -> int:
    try:
        ts = subprocess.check_output(
            ["git", "log", "-1", "--format=%ct", "--", str(p)],
            text=True
        ).strip()
        return int(ts) if ts else int(p.stat().st_mtime)
    except subprocess.CalledProcessError:
        return int(p.stat().st_mtime)


# ---------------- Text extraction helpers ----------------

def strip_front_matter(text: str) -> tuple[str, str | None]:
    """Return (body, front_matter_text or None)."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, flags=re.DOTALL)
    if m:
        return text[m.end():], m.group(1)
    return text, None


def extract_title(text: str, fallback: str) -> str:
    if text:
        fm_match = re.search(r"(?m)^title:\s*(.+?)\s*$", text)
        if fm_match:
            return fm_match.group(1).strip()

    for pat in [
        r"(?m)^\#\s+(.*\S)\s*$",
        r"(?m)^\#\#\s+(.*\S)\s*$",
        r"(?m)^\#{1,6}\s+(.*\S)\s*$"
    ]:
        m = re.search(pat, text)
        if m:
            return m.group(1).strip()

    return fallback


def extract_description(body: str) -> str:
    """
    First real paragraph:
    - skip headings
    - skip code blocks
    - skip lists
    """
    lines = body.splitlines()
    in_code = False
    para = []

    for line in lines:
        l = line.strip()

        if l.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if not l:
            if para:
                break
            continue
        if l.startswith(("#", "-", "*", ">")):
            continue

        para.append(l)

    desc = " ".join(para)
    desc = re.sub(r"\s+", " ", desc)
    return desc[:160].rstrip(". ") + "." if desc else ""


def calculate_reading_time(body: str) -> str:
    words = re.findall(r"\b\w+\b", body)
    minutes = max(1, math.ceil(len(words) / WORDS_PER_MINUTE))
    return f"{minutes} min"


# ---------------- Front-matter injection ----------------

def ensure_front_matter(p: pathlib.Path) -> tuple[str, str]:
    raw = p.read_text(encoding="utf-8-sig")
    body, fm = strip_front_matter(raw)

    title = extract_title(raw, p.stem.replace("-", " "))
    description = extract_description(body)
    reading_time = calculate_reading_time(body)

    cover = p.parent / "cover.png"
    image_line = "image: cover.png" if cover.exists() else None

    fm_lines = []
    if fm:
        fm_lines = [l for l in fm.splitlines() if l.strip()]
    else:
        fm_lines = []

    def has(key): return any(l.startswith(f"{key}:") for l in fm_lines)

    if not has("title"):
        fm_lines.insert(0, f"title: {title}")
    if image_line and not has("image"):
        fm_lines.append(image_line)
    if description and not has("description"):
        fm_lines.append(f"description: {description}")
    if not has("reading_time"):
        fm_lines.append(f"reading_time: {reading_time}")

    # Banner injection (idempotent)
    banner = ""
    banner_marker = "![cover](cover.png){ .md-banner }"

    if cover.exists():
        # Only inject banner if it's not already there
        if not body.lstrip().startswith(banner_marker):
            banner = banner_marker + "\n\n"

    new_text = (
            "---\n"
            + "\n".join(fm_lines)
            + "\n---\n\n"
            + banner
            + body.lstrip()
    )
    p.write_text(new_text, encoding="utf-8")

    return title, reading_time


# ---------------- Link helpers ----------------

def link_from_home(p: pathlib.Path) -> str:
    return p.as_posix().replace("docs/", "", 1)


def link_from_posts_index(p: pathlib.Path) -> str:
    return p.relative_to(POSTS_DIR).as_posix()


# ---------------- Collect posts ----------------

posts = [
    p for p in POSTS_DIR.rglob("*")
    if p.is_file()
       and p.suffix.lower() in VALID_EXTS
       and p.name.lower() not in ("index.md", "archive.md")
]

scored = []
for p in posts:
    title, reading_time = ensure_front_matter(p)
    scored.append((git_timestamp(p), p, title, reading_time))

scored.sort(key=lambda x: x[0], reverse=True)


# ---------------- Posts index ----------------

index_lines = ["# Posts", ""]
for ts, p, title, rt in scored:
    date = time.strftime("%Y-%m-%d", time.localtime(ts))
    index_lines.append(
        f"- **{date}** — [{title}]({link_from_posts_index(p)}) · _{rt}_"
    )
index_lines.append("")
INDEX_OUT.write_text("\n".join(index_lines), encoding="utf-8")


# ---------------- Archive ----------------

archive = defaultdict(lambda: defaultdict(list))
for ts, p, title, rt in scored:
    t = time.localtime(ts)
    archive[t.tm_year][t.tm_mon].append((ts, p, title, rt))

archive_lines = ["# Archive", ""]
for year in sorted(archive.keys(), reverse=True):
    archive_lines.append(f"## {year}")
    for mon in sorted(archive[year].keys(), reverse=True):
        archive_lines.append(f"### {calendar.month_name[mon]}")
        for ts, p, title, rt in archive[year][mon]:
            date = time.strftime("%Y-%m-%d", time.localtime(ts))
            archive_lines.append(
                f"- **{date}** — [{title}]({link_from_posts_index(p)}) · _{rt}_"
            )
        archive_lines.append("")
    archive_lines.append("")

ARCHIVE_OUT.write_text("\n".join(archive_lines).rstrip() + "\n", encoding="utf-8")


# ---------------- Homepage latest ----------------

home = HOMEPAGE.read_text(encoding="utf-8-sig")

latest = scored[:LATEST_COUNT]
if latest:
    block = "\n".join(
        f"- **{time.strftime('%Y-%m-%d', time.localtime(ts))}** — "
        f"[{title}]({link_from_home(p)}) · _{rt}_"
        for ts, p, title, rt in latest
    )
else:
    block = "_No posts yet._"

pattern = re.compile(re.escape(BLOCK_START) + r".*?" + re.escape(BLOCK_END), re.DOTALL)
replacement = f"{BLOCK_START}\n{block}\n{BLOCK_END}"
home = pattern.sub(replacement, home) if pattern.search(home) else home + "\n\n" + replacement

HOMEPAGE.write_text(home, encoding="utf-8")
