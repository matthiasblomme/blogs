import subprocess, pathlib, time, re

DOCS_DIR    = pathlib.Path("docs")
POSTS_DIR   = DOCS_DIR / "posts"
OUTPUT      = POSTS_DIR / "index.md"
HOMEPAGE    = DOCS_DIR / "index.md"
BLOCK_START = "<!--LATEST_POST:START-->"
BLOCK_END   = "<!--LATEST_POST:END-->"


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


def first_h1(p: pathlib.Path) -> str:
    """Return first '# ' heading as title; fallback to filename."""
    title = p.stem.replace("-", " ")
    with p.open("r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if s.startswith("# "):
                title = s[2:].strip()
                break
    return title


def link_from_home(p: pathlib.Path) -> str:
    """Link path relative to docs/ (used on homepage)."""
    return p.as_posix().replace("docs/", "", 1)


def link_from_posts_index(p: pathlib.Path) -> str:
    """Link path relative to docs/posts (used on posts index)."""
    return p.relative_to(POSTS_DIR).as_posix()


# Collect all posts (support subfolders), ignore posts/index.md
posts = [p for p in POSTS_DIR.rglob("*.md") if p.name.lower() != "index.md"]

# Sort newest-first by last git commit
scored = sorted(((git_timestamp(p), p) for p in posts), key=lambda x: x[0], reverse=True)

# ---------- Generate posts landing page ----------
lines = ["# Posts", ""]
for ts, p in scored:
    date = time.strftime("%Y-%m-%d", time.localtime(ts))
    title = first_h1(p)
    lines.append(f"- **{date}** — [{title}]({link_from_posts_index(p)})")
lines.append("")  # trailing newline

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text("\n".join(lines), encoding="utf-8")

# ---------- Inject Latest Post block on homepage ----------
home = HOMEPAGE.read_text(encoding="utf-8")

if scored:
    _, latest_path = scored[0]
    latest_title = first_h1(latest_path)
    latest_link  = f"- [{latest_title}]({link_from_home(latest_path)})"
else:
    latest_link  = "_No posts yet._"

pattern = re.compile(
    re.escape(BLOCK_START) + r".*?" + re.escape(BLOCK_END),
    flags=re.DOTALL
)
replacement = f"{BLOCK_START}\n{latest_link}\n{BLOCK_END}"
if pattern.search(home):
    home = pattern.sub(replacement, home)
else:
    # fallback: append block if markers not found
    home = home.rstrip() + "\n\n" + replacement + "\n"

HOMEPAGE.write_text(home, encoding="utf-8")
