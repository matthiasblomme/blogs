import subprocess, pathlib, time

POSTS_DIR = pathlib.Path("docs/posts")
OUTPUT = POSTS_DIR / "index.md"
HOMEPAGE = pathlib.Path("docs/index.md")
PLACEHOLDER = "<!--LATEST_POST-->"

def git_timestamp(p: pathlib.Path) -> int:
    # returns last commit unix timestamp for this file
    ts = subprocess.check_output(
        ["git", "log", "-1", "--format=%ct", "--", str(p)],
        text=True
    ).strip()
    return int(ts) if ts else int(p.stat().st_mtime)

def rel_link(p: pathlib.Path) -> str:
    # mkdocs links are relative to docs/
    return str(p).replace("\\", "/").replace("docs/", "")

# collect posts (exclude index.md)
posts = [p for p in POSTS_DIR.glob("*.md") if p.name.lower() != "index.md"]
posts += [p for p in POSTS_DIR.glob("*/*.md") if p.name.lower() != "index.md"]  # allow subfolders

scored = sorted(
    [(git_timestamp(p), p) for p in posts],
    key=lambda x: x[0],
    reverse=True
)

# generate posts index
lines = [
    "# Posts",
    "",
    "_Newest first. This page is generated during the build._",
    ""
]
for ts, p in scored:
    t = time.strftime("%Y-%m-%d", time.localtime(ts))
    # read title from first markdown heading or fallback to filename
    title = p.stem.replace("-", " ")
    with p.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("# "):
                title = line.strip()[2:].strip()
                break
    lines.append(f"- **{t}** — [{title}]({rel_link(p)})")

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")

# update homepage latest post placeholder
home = HOMEPAGE.read_text(encoding="utf-8")
if scored:
    latest_link = f"- [{title}]({rel_link(scored[0][1])})"
else:
    latest_link = "_No posts yet._"
home = home.replace(PLACEHOLDER, latest_link)
HOMEPAGE.write_text(home, encoding="utf-8")
