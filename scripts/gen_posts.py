import subprocess, pathlib, time, re, calendar
from collections import defaultdict

DOCS_DIR      = pathlib.Path("docs")
POSTS_DIR     = DOCS_DIR / "posts"
INDEX_OUT     = POSTS_DIR / "index.md"
ARCHIVE_OUT   = POSTS_DIR / "archive.md"
HOMEPAGE      = DOCS_DIR / "index.md"
BLOCK_START   = "<!--LATEST_POST:START-->"
BLOCK_END     = "<!--LATEST_POST:END-->"
LATEST_COUNT  = 5   # number of posts to show on homepage


def git_timestamp(p: pathlib.Path) -> int:
    """Last commit time for file (fallback to mtime)."""
    try:
        ts = subprocess.check_output(
            ["git", "log", "-1", "--format=%ct", "--", str(p)],
            text=True
        ).strip()
        return int(ts) if ts else int(p.stat().st_mtime)
    except subprocess.CalledProcessError:
        return int(p.stat().st_mtime)


def extract_title(p: pathlib.Path) -> str:
    """
    Title resolution order:
      1) YAML front-matter 'title:'
      2) first H1 (# )
      3) first H2 (## )
      4) first heading any level
      5) filename fallback
    Handles UTF-8 BOM via 'utf-8-sig'.
    """
    text = p.read_text(encoding="utf-8-sig")

    # 1) front-matter
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, flags=re.DOTALL)
    if m:
        fm = m.group(1)
        mt = re.search(r"(?m)^title:\s*(.+?)\s*$", fm)
        if mt:
            return mt.group(1).strip()

    # 2) first H1
    mh1 = re.search(r"(?m)^\#\s+(.*\S)\s*$", text)
    if mh1:
        return mh1.group(1).strip()

    # 3) first H2
    mh2 = re.search(r"(?m)^\#\#\s+(.*\S)\s*$", text)
    if mh2:
        return mh2.group(1).strip()

    # 4) any heading
    many = re.search(r"(?m)^\#{1,6}\s+(.*\S)\s*$", text)
    if many:
        return many.group(1).strip()

    # 5) fallback
    return p.stem.replace("-", " ")


def link_from_home(p: pathlib.Path) -> str:
    """Link path relative to docs/ (used on homepage)."""
    return p.as_posix().replace("docs/", "", 1)


def link_from_posts_index(p: pathlib.Path) -> str:
    """Link path relative to docs/posts (used on posts index + archive)."""
    return p.relative_to(POSTS_DIR).as_posix()


# Collect all posts (support subfolders), ignore posts/index.md & posts/archive.md
posts = [
    p for p in POSTS_DIR.rglob("*.md")
    if p.name.lower() not in ("index.md", "archive.md")
]

# Sort newest-first by last git commit
scored = sorted(((git_timestamp(p), p) for p in posts), key=lambda x: x[0], reverse=True)

# ---------- Generate posts landing page (flat list) ----------
index_lines = ["# Posts", ""]
for ts, p in scored:
    date = time.strftime("%Y-%m-%d", time.localtime(ts))
    title = extract_title(p)
    index_lines.append(f"- **{date}** — [{title}]({link_from_posts_index(p)})")
index_lines.append("")  # trailing newline

INDEX_OUT.parent.mkdir(parents=True, exist_ok=True)
INDEX_OUT.write_text("\n".join(index_lines), encoding="utf-8")

# ---------- Generate archive (Year -> Month) ----------
archive_map: dict[int, dict[int, list[tuple]]] = defaultdict(lambda: defaultdict(list))
for ts, p in scored:
    t = time.localtime(ts)
    archive_map[t.tm_year][t.tm_mon].append((ts, p, extract_title(p)))

archive_lines = ["# Archive", ""]
for year in sorted(archive_map.keys(), reverse=True):
    archive_lines.append(f"## {year}")
    archive_lines.append("")
    for mon in sorted(archive_map[year].keys(), reverse=True):
        month_name = calendar.month_name[mon]
        archive_lines.append(f"### {month_name}")
        for ts, p, title in archive_map[year][mon]:
            date = time.strftime("%Y-%m-%d", time.localtime(ts))
            archive_lines.append(f"- **{date}** — [{title}]({link_from_posts_index(p)})")
        archive_lines.append("")
    archive_lines.append("")

ARCHIVE_OUT.write_text("\n".join(archive_lines).rstrip() + "\n", encoding="utf-8")

# ---------- Inject Latest Posts block on homepage ----------
home = HOMEPAGE.read_text(encoding="utf-8-sig")

if scored:
    latest_posts = scored[:LATEST_COUNT]
    latest_links = []
    for ts, p in latest_posts:
        title = extract_title(p)
        date = time.strftime("%Y-%m-%d", time.localtime(ts))
        latest_links.append(f"- **{date}** — [{title}]({link_from_home(p)})")
    latest_block = "\n".join(latest_links)
else:
    latest_block = "_No posts yet._"

pattern = re.compile(re.escape(BLOCK_START) + r".*?" + re.escape(BLOCK_END), flags=re.DOTALL)
replacement = f"{BLOCK_START}\n{latest_block}\n{BLOCK_END}"
if pattern.search(home):
    home = pattern.sub(replacement, home)
else:
    home = home.rstrip() + "\n\n" + replacement + "\n"

HOMEPAGE.write_text(home, encoding="utf-8")
