# SNaP — project page

Static project page for **SNaP: One-Step Posterior Sampling for Noisy Inverse Problems**
(Shoushtari*, Chandler*, Shi, Kamilov; *equal contribution).

## Publish on GitHub Pages

```bash
git init
git add .
git commit -m "SNaP project page"
git branch -M main
git remote add origin git@github.com:<user-or-org>/<repo>.git
git push -u origin main
```

Then in the repository: **Settings → Pages → Build and deployment → Source: Deploy from a
branch → Branch: `main` / `(root)`**.

For a URL of the form `https://<name>.github.io/`, name the repository `<name>.github.io`.
Otherwise the page lands at `https://<user>.github.io/<repo>/`.

## Before you publish — things to fill in

All of these are marked with HTML comments in `index.html`:

| What | Where |
|---|---|
| arXiv link | the `arXiv (soon)` button — replace `href="#"` and drop `class="... disabled"` and the `onclick` |
| Code link | the `Code (soon)` button — same treatment |
| Author homepages | the `publication-authors` block — wrap each name in an `<a href="...">` |
| Venue badge | `<span class="badge">Preprint</span>` → e.g. the venue name |
| BibTeX | the `#BibTeX` section — add the arXiv id / venue |
| `og:image` URL | the Open Graph meta tag, once the page has a live address |

## Layout

```
index.html                 the page (generated — see below)
template.html              source template with <!--TABLE_*--> placeholders
build_page.py              fills the placeholders with the results tables
static/css/index.css       all styling (no framework dependency)
static/js/index.js         tabs, lightbox, BibTeX copy, scroll reveal
static/images/             figures extracted from the paper
static/pdfs/snap_paper.pdf the paper
.nojekyll                  serve files starting with _ and skip Jekyll
```

### Editing

Prose, figures and section structure: edit `template.html`, then run

```bash
python3 build_page.py
```

which regenerates `index.html`. The results tables are built from the numbers in
`build_page.py` — best and second-best cells are ranked automatically, so changing a value
there keeps the highlighting consistent.

If you would rather not keep the build step, edit `index.html` directly and delete
`template.html` and `build_page.py`.

### Local preview

```bash
python3 -m http.server 8000
```

and open <http://localhost:8000>.

## Figure provenance

All figures are the embedded raster images from the paper PDF (Figures 1–16), downsampled to at most
2000 px wide. Replace any of them with the original vector or high-resolution source if you have it — same
filenames, and nothing else needs to change.

## Credits

Page layout adapted from the [Nerfies](https://github.com/nerfies/nerfies.github.io)
project-page template. Licensed under
[CC BY-SA 4.0](http://creativecommons.org/licenses/by-sa/4.0/).
