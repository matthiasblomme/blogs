# eMBee Integration Blogs

Welcome to my personal blog --- built with
[MkDocs](https://www.mkdocs.org/) and [Material for
MkDocs](https://squidfunk.github.io/mkdocs-material/).\
This repo contains the source of the site, written entirely in Markdown
and auto-deployed to **GitHub Pages**.

------------------------------------------------------------------------

## ✨ Features

-   **Markdown-based blogging** --- write posts in plain `.md` files
    under `docs/posts/`
-   **MkDocs Material theme** --- clean, responsive, and customizable
-   **Dynamic navigation**:
    -   🆕 *Latest posts* section on the homepage (auto-updated, showing
        the newest 5 posts)
    -   📜 Flat [Posts index](docs/posts/index.md) (all posts, newest
        first)
    -   🗂️ [Archive view](docs/posts/archive.md) (grouped by year &
        month)
-   **Automatic deployment** to GitHub Pages on every push to `main`
    (via GitHub Actions)
-   **Local preview** with hot-reload while writing

------------------------------------------------------------------------

## 🗂 Repo Structure

    .
    ├── docs/                # All content lives here
    │   ├── index.md          # Homepage
    │   ├── about.md          # About page
    │   └── posts/            # Blog posts
    │       ├── index.md      # Auto-generated: flat list of all posts
    │       ├── archive.md    # Auto-generated: grouped archive
    │       └── <post folders>
    │           └── my_post.md
    ├── scripts/
    │   └── gen_posts.py      # Script that builds posts index, archive & latest section
    ├── mkdocs.yml            # MkDocs configuration
    ├── requirements.txt      # Python dependencies
    └── .github/
        └── workflows/
            └── mkdocs-pages.yml  # GitHub Actions build + deploy workflow

------------------------------------------------------------------------

## 🚀 Local Development

Clone the repo and install requirements:

``` powershell
# Create virtual environment (optional but recommended)
py -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install MkDocs + theme
pip install -r requirements.txt
```

Generate the latest posts section & archive, then start the local dev
server:

``` powershell
python .\scripts\gen_posts.py
mkdocs serve
```

Your site will be available at: <http://127.0.0.1:8000/>

------------------------------------------------------------------------

## 📦 Deployment

This repo is wired with a GitHub Actions workflow
(`.github/workflows/mkdocs-pages.yml`):

-   On every push to `main` (or `master`), the workflow:
    1.  Checks out the repo
    2.  Installs dependencies
    3.  Runs `scripts/gen_posts.py` to refresh posts index & archive
    4.  Builds the site with `mkdocs build`
    5.  Publishes the static site to **GitHub Pages**

Published site URL:

    https://<your-username>.github.io/<your-repo>/

------------------------------------------------------------------------

## 📝 Writing a New Post

1.  Create a new folder inside `docs/posts/` (optional but helps keep
    images organized).
2.  Add a new Markdown file, e.g.:

``` markdown
# My New Blog Post Title

Intro text…

## Section 1
Details…

## Section 2
More details…
```

3.  (Optional) Add YAML front-matter at the top for a custom title:

``` markdown
---
title: Custom Display Title
---

# My New Blog Post Title
```

4.  Commit and push.\
    The CI pipeline will update the homepage **Latest Posts**, the
    **Posts index**, and the **Archive** automatically.

------------------------------------------------------------------------

## ⚡ Tips

-   **Images**: put them alongside your post in a subfolder
    (`docs/posts/my-post/img.png`) and reference with relative paths:\
    `![alt](img.png)`

-   **Local strict build**:

    ``` powershell
    mkdocs build --strict
    ```

    (fails on broken links --- useful for catching issues early)

-   **Hide the "Edit on GitHub" button**: in `mkdocs.yml`, add:

    ``` yaml
    theme:
      name: material
      hide:
        - edit
    ```

------------------------------------------------------------------------

## 💡 Credits

-   Built with [MkDocs](https://www.mkdocs.org/)
-   Theme: [Material for
    MkDocs](https://squidfunk.github.io/mkdocs-material/)
-   Blog engine customizations: dynamic index/archive generator in
    `scripts/gen_posts.py`

------------------------------------------------------------------------

☕🐔💻 Happy blogging!
