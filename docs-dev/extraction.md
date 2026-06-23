# Extraction Workflow — Web Content to Markdown

Two-phase pipeline: download HTML (lossless) → convert to Markdown (offline).

```
Phase 1: sitemap XML → URL list → fetch HTML → save to html_cache/
Phase 2: html_cache/ HTML → parse → download images → write Markdown
```

- **Input**: `sitemaps/sitemap_book_en.xml`, `sitemaps/sitemap_docs_en.xml`
- **HTML cache**: `html_cache/book/`, `html_cache/docs/`
- **Output**: `skills/mql5/references/book/`, `skills/mql5/references/docs/`
- **Tool**: Python script using `requests` + `beautifulsoup4`

## Script — `scripts/extract.py`

### CLI

```bash
# Phase 1: download HTML
python scripts/extract.py download --sitemap sitemaps/sitemap_book_en.xml
python scripts/extract.py download --all

# Phase 2: convert to Markdown
python scripts/extract.py convert --sitemap sitemaps/sitemap_book_en.xml
python scripts/extract.py convert --all

# Debug single page (fetches + analyzes)
python scripts/extract.py debug URL
```

Options (download/convert):
- `--sitemap PATH` — single sitemap
- `--all` — all known sitemaps
- `--force` — re-process everything (ignore progress log)
- `--dry-run` — show plan without processing

### Phase 1 — Download

1. Parse sitemap XML → URL list
2. Build file map (naming convention, see `naming.md`)
3. For each URL:
   - Skip if already cached (idempotent)
   - Fetch HTML with retry + rate limiting (0.5s delay)
   - Save raw HTML to `html_cache/{label}/{NN-chapter}/{NNNN-name}.html`
4. Progress: `html_cache/{label}/.download.log`

HTML files are saved as-is — no parsing, no transformation.

### Phase 2 — Convert

1. Parse sitemap XML → URL list (same mapping)
2. For each URL:
   - Skip if already converted (idempotent)
   - Read local HTML from `html_cache/`
   - Parse `#help` content → elements
   - Convert elements to Markdown
   - Download images to `pics/` subfolder
   - Write `.md` file
3. Progress: `{output_dir}/.convert.log`

### HTML Cache Structure

```
html_cache/
├── book/
│   ├── 0000-book.html
│   ├── .download.log
│   ├── 00-intro/
│   │   ├── 0001-intro.html
│   │   ├── 0002-intro-edit-compile-run.html
│   │   └── ...
│   └── ...
└── docs/
    ├── 0000-docs.html
    ├── .download.log
    ├── 00-basis/
    │   ├── 0001-basis.html
    │   └── ...
    └── ...
```

Filenames mirror the markdown output (same 4-digit prefix, same derived name).

## Content Extraction Rules

### Main Content Selector

```css
#help > h1:nth-child(1)
```

Extract from this `<h1>` through to the last content element.

**Fallback**: If no `h1` exists (e.g. root pages like `/en/book`), use the
first `<Tag>` child of `#help` as the start element.

### Table Handling

| Has `<thead>` | Meaning | Render as |
|---------------|---------|-----------|
| Yes           | Data table with headers | Markdown table with `|---|` separator |
| No            | Code block or console output | Fenced code block (` ``` `) |

Tables without `<thead>` on mql5.com typically contain:
- MQL5 code (with `<span>` color classes for syntax highlighting)
- MetaTrader 5 Strategy Tester console output

### Image Handling

The `<img>` is often nested inside `<p class="p_ImageCaption">`.

**Alt text extraction**:
1. Try `img.find_next_sibling("p")`
2. If not found, try `img.parent.find_next_sibling("p")`
3. Fall back to `img.get("alt", "")`

**`<p>` containing `<img>`**: The `<p>` is treated as an image block —
the `<img>` is routed through the image download path.

### Code Blocks

- `<pre><code>` → fenced code block with language detection
- Language detected from CSS classes (`mql`, `cpp`, `sql`, etc.)
- Text whitespace preserved (no space-joining)

## Debug Target — TesterStatistics

URL: `https://www.mql5.com/en/book/automation/tester/tester_testerstatistics`

Content boundaries:
- Start: `#help > h1:nth-child(1)` → "Getting testing financial statistics: TesterStatistics"
- End: `p.p_Text:nth-child(45)`

Exercises: data tables (thead), code blocks (no thead), images, console output.

## Error Handling

| Error | Phase 1 | Phase 2 |
|-------|---------|---------|
| HTTP 404 | Skip, log, continue | N/A (offline) |
| HTTP 429/5xx | Retry with backoff | N/A |
| Missing HTML | N/A | Log warning, skip |
| Parse error | N/A | Log error, skip |
| Image download fail | N/A | Log warning, use original URL |

## Resumability

Each phase has its own progress log. Re-running skips completed items.
Use `--force` to re-process everything.
