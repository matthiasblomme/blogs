---
date: 2026-03-17
title: 'How This Blog Works: MkDocs, Python, and GitHub Pages'
author: Matthias Blomme
description: A look behind the scenes at how this blog is built and deployed, using
  MkDocs Material, a custom Python script for metadata generation, and GitHub Actions
  for automated publishing.
tags:
- python
- mkdocs
- github-actions
- automation
- blogging
reading_time: 15 min
---

![cover](cover.png){ .md-banner }

<!--MD_POST_META:START-->
<div class="md-post-meta">
  <div class="md-post-meta-left">Matthias Blomme · 2026-03-17 · ⏱ 15 min</div>
  <div class="md-post-meta-right"><span class="post-share-label">Share:</span> <a class="post-share post-share-linkedin" href="https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fmatthiasblomme.github.io%2Fblogs%2Fposts%2Fblog-hosting%2Fblog-hosting%2F" target="_blank" rel="noopener" title="Share on LinkedIn">[<span class="in">in</span>]</a></div>
</div>
<hr class="md-post-divider"/>
<div class="md-post-tags"><span class="md-tag">python</span> <span class="md-tag">mkdocs</span> <span class="md-tag">github-actions</span> <span class="md-tag">automation</span> <span class="md-tag">blogging</span></div>
<!--MD_POST_META:END-->

# How this blog works: MkDocs, Python, and GitHub Pages

Ever wonder how this blog works without dragging in WordPress and all the other nonsense people keep calling "simple"? It’s markdown, MkDocs, a Python script, and GitHub Pages.

That’s it.

I wanted a blog setup that does the job, doesn’t get in the way, and doesn’t turn publishing a post into some stupid ritual. I want to write content in Markdown (because no annoying layout issues) and just be done with it. So this is what I built.
At the core, it’s just Markdown files in a git repo. Which makes sense, because that’s what blog posts are in the first place. Content. They don’t need a bloated system wrapped around them.
Everything around that is there to make life easier: generate the repetitive bits, publish cleanly, and keep the whole thing low-maintenance.

## The stack

The setup is deliberately simple (a often misused word, I'll try to respect it's meaning):

- MkDocs with the Material theme
- A custom Python script called `gen_posts.py`
- GitHub Actions for build and deployment
- GitHub Pages for hosting

MkDocs turns it into a site, the Python script cleans up the repetitive work, and GitHub takes care of the rest.

Simple setup, works well.

To be clear, I do not care if the Python script is the most complex piece in this whole setup. That is not what makes the setup complex. If it works, and if it is a write-once-and-forget kind of script, I still consider the end result simple.

The focus here is writing content. If the setup lets me do that without getting in the way, then it is simple. That is the definition that matters here.

## MkDocs is the foundation

MkDocs takes the Markdown files and turns them into an actual website. The Material theme makes it look decent without needing to spend time fighting layout and styling.

Most of the setup sits in `mkdocs.yml`:

```yaml
site_name: eMBee Integration Blogs
site_url: https://matthiasblomme.github.io/blogs/

theme:
  name: material
  features:
    - content.code.copy
    - navigation.sections
    - navigation.tabs
    - navigation.instant
    - content.tags
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      toggle:
        icon: material/weather-night
        name: Switch to dark mode
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      toggle:
        icon: material/weather-sunny
        name: Switch to light mode

nav:
  - Home: index.md
  - Posts:
      - All posts: posts/index.md
      - Archive: posts/archive.md
  - About: about.md
```

That gives me dark mode, some decent navigation, code copy buttons, tags, and a few other useful bits out of the box.

I also use:

```yaml
use_directory_urls: true
```

That keeps the URLs clean. So instead of this:

```text
/posts/my-post/my-post.md
```

you get this:

```text
/posts/my-post/my-post/
```

Looks better, cleaner URL, less junk, easier to include for cross-references. MkDocs does most of the work here, which is exactly what I want from it.

## The Python script does the annoying work

This is where the automation comes in.

The script handles the repetitive bits I don’t want to touch every time I publish a post. Things like reading time, metadata injection, and generating the post overview pages.

### Reading time

You see a lot of blogs out there boasting about reading time. Partly to lure you in, partly to show off how much they wrote. Obviously I wanted that too, but not badly enough to maintain it manually.

This is the relevant part:

```python
WORDS_PER_MINUTE = 130
CODE_WORDS_PER_MINUTE = 75

def estimate_reading_time_minutes(md_body: str) -> int:
    # Extract code blocks (read slower)
    code_blocks = re.findall(r"```.*?```", md_body, flags=re.DOTALL)
    code_words = re.findall(r"\b\w+\b", " ".join(code_blocks))

    # Strip markdown for prose word count
    cleaned = strip_markdown(md_body)
    prose_words = re.findall(r"\b\w+\b", cleaned)

    prose_minutes = len(prose_words) / WORDS_PER_MINUTE
    code_minutes = len(code_words) / CODE_WORDS_PER_MINUTE

    return max(1, int(round(prose_minutes + code_minutes)))
```

Code blocks are counted at a slower reading pace: 75 WPM instead of 130 for normal prose. Which makes sense, because nobody reads code the same way they read a paragraph. Half the time you read it twice just to check whether it actually does what you think it does. I did not pull those numbers out of nowhere either, they are based on reading speed estimates I found online.

### Metadata and post listings

The script fills in the repetitive bits inside each post and also updates the overview pages. Not empty filler, but useful bits I want to keep consistent without having to create or update them manually every time.

For the metadata block inside a post, I use these markers:

```html
<!--MD_POST_META:START-->

<!--MD_POST_META:END-->
```

That section gets replaced automatically based on the front matter and the site config. So things like the publishing date, reading time, tags, and share link are generated for me instead of being maintained by hand.

Here is what the generated block looks like:

```html
<div class="md-post-meta">
  <div class="md-post-meta-left">Matthias Blomme · 2026-03-17 · ⏱ 15 min</div>
  <div class="md-post-meta-right"><span class="post-share-label">Share:</span> <a class="post-share post-share-linkedin" href="https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fmatthiasblomme.github.io%2Fblogs%2Fposts%2Fblog-hosting%2Fblog-hosting%2F" target="_blank" rel="noopener" title="Share on LinkedIn">[<span class="in">in</span>]</a></div>
</div>
<hr class="md-post-divider"/>
<div class="md-post-tags"><span class="md-tag">python</span> <span class="md-tag">mkdocs</span> <span class="md-tag">github-actions</span> <span class="md-tag">automation</span> <span class="md-tag">blogging</span></div>
```

It does the same for the post listings across the site:

```html
<!--MD_LATEST_POSTS:START-->
<!--MD_LATEST_POSTS:END-->

<!--MD_ALL_POSTS:START-->
<!--MD_ALL_POSTS:END-->

<!--MD_ARCHIVE:START-->
<!--MD_ARCHIVE:END-->
```

Those markers are used in:

- `docs/index.md`
- `docs/posts/index.md`
- `docs/posts/archive.md`

Posts are collected, sorted by date, and rendered into markdown resulting in entries like this:

```markdown
- **2026-03-17** - [Post Title](path/to/post.md) · *5 min*
```

So instead of updating post metadata, the homepage, the posts page, and the archive separately, I just write the post, insert some markers, and let the script deal with the rest.

## The front matter is the only thing I really maintain

Every post starts with a bit of front matter at the top. That is basically the only structured input I still fill in myself.

```yaml
---
date: 2026-03-17
title: "My Post Title"
author: Matthias Blomme
description: A brief description for SEO and previews
tags:
  - python
  - automation
---
```

That block tells the rest of the setup what it needs to know. The date is used for sorting, the title and description are used in generated pages and previews, and the tags become part of the metadata.

So while most of the workflow is automated, this is still the one bit I fill in myself. Which is fair enough, because this is the bit that defines the post.

`reading_time` is optional. If I leave it out, and I do, the script calculates it and injects it automatically. Exactly how it should be.

So in practice, I write the post, fill in the front matter, and let the rest of the setup take care of everything around it.

## GitHub Actions handles deployment

Once the post is written and pushed, I want the rest to happen automatically. I do not want publishing to depend on me remembering a bunch of extra steps.

That hands-off workflow lives in `.github/workflows/mkdocs-pages.yml`:

```yaml
name: Build & Deploy MkDocs to GitHub Pages

on:
  push:
    branches: [ "main", "master" ]
  pull_request:
    branches: [ "main", "master" ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: actions/setup-python@v5
        with:
          python-version: "3.x"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Generate Posts index + Latest Post
        run: python scripts/gen_posts.py

      - name: Build site
        run: mkdocs build --strict

      - name: Upload Pages artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./site

  deploy:
    if: github.event_name == 'push'
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/deploy-pages@v4
```

So the flow is pretty straightforward. On every pull request, the site gets built to make sure nothing is broken. On every push to `main`, that same process runs again and the result gets deployed to GitHub Pages.

`gen_posts.py` runs before MkDocs builds the site, so all generated metadata and post listings are already in place by then.

Which means my part stays simple: write the post, commit it, push it, done.

## The writing workflow is stupidly simple

Here’s that word again, simple. But I think I can live up to it.

Once the setup is in place, the workflow itself is pretty minimal. Which is the whole point.

1. Create a new folder under `docs/posts/`
2. Write the markdown file with front matter
3. Add images to that same folder
4. Commit and push, or open a PR
5. Let GitHub Actions handle the rest

That is the whole process.

I write the post, add the metadata, throw in any images it needs, and push it. The script updates the generated bits, MkDocs builds the site, and GitHub Actions deploys it.

Which means I get to focus on writing instead of babysitting the publishing process.

## File structure

The repo itself is not doing anything weird either. It is just organized in a way that makes sense for this setup.

```text
blogs/
├── docs/
│   ├── index.md
│   ├── about.md
│   ├── assets/
│   │   ├── extra.css
│   │   └── logo.jpg
│   └── posts/
│       ├── index.md
│       ├── archive.md
│       └── my-post/
│           ├── my-post.md
│           └── cover.png
├── scripts/
│   └── gen_posts.py
├── mkdocs.yml
├── requirements.txt
└── .github/
    └── workflows/
        └── mkdocs-pages.yml
```

The `docs` folder holds the actual site content. Posts live under `docs/posts/`, each in their own folder, together with the images that belong to them. Which makes life easier, because I do not need to go hunting through some shared assets folder every time I want to update a post.

The script lives in `scripts/`, the MkDocs config sits at the root, and the GitHub Actions workflow is under `.github/workflows/`.

So the structure stays easy to follow: content where it belongs, automation off to the side, config where you would expect it.

## Closing

So that’s the setup.

Markdown for the writing, MkDocs for the site, Python for the repetitive bits, and GitHub Actions to push it live. It does what I need, stays out of the way, and does not turn publishing a blog post into a separate project.

That matters more than people like to admit. Because the moment your blog setup needs troubleshooting before you can publish something, the setup itself is becoming the problem.

This one is simpler (last one, I promise) than that. Which is exactly why it works.

## Resources

- [MkDocs](https://www.mkdocs.org/)
- [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)
- [GitHub Pages](https://pages.github.com/)
- [This blog's source code](https://github.com/matthiasblomme/blogs)

---

Written by [Matthias Blomme](https://www.linkedin.com/in/matthiasblomme/)
