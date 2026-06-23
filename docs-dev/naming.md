# Naming Convention — Folder & File Structure

This document specifies how sitemap URLs map to the file tree under
`skills/mql5/references/book/` and `skills/mql5/references/docs/`.

## Core Rules

1. **One subfolder level**: Under `book/` or `docs/`, at most one level of
   subfolder (the "chapter folder") is used. All pages within that chapter are
   `.md` files directly inside the chapter folder.

2. **`pics/` exception**: Each chapter folder may contain a `pics/` subfolder
   for images extracted from that chapter's pages.

3. **Sequential numbering**: Both chapter folders and files carry numeric
   prefixes that reflect their order in the source sitemap.

## Chapter Folders

A "chapter" corresponds to the **first URL path segment** after the sitemap root.

| Source URL pattern           | Chapter folder     |
|------------------------------|--------------------|
| `/en/book/intro` ...         | `00-intro/`        |
| `/en/book/basis` ...         | `01-basis/`        |
| `/en/docs/basis` ...         | `00-basis/`        |
| `/en/docs/standardlibrary` … | `34-standardlibrary/` |

- **Prefix**: 2-digit zero-padded number (00, 01, 02, …)
- **Suffix**: the URL path segment (e.g. `intro`, `basis`, `standardlibrary`)
- **Order**: by first occurrence in the sitemap

Chapters are numbered **globally** within each sitemap (book and docs are
independent numbering spaces).

## Files Within a Chapter

Each URL that belongs to a chapter becomes one `.md` file inside the chapter
folder. The filename encodes:

```
{4-digit global number}-{derived-name}.md
```

- **4-digit prefix**: sequential number matching the URL's position in the
  sitemap (0001, 0002, …). This is **global** across the entire sitemap, not
  reset per chapter.
- **Derived name**: the URL path **after** the depth-1 segment, with `/`
  replaced by `-`. If the URL **is** the depth-1 segment itself (the chapter
  index page), the name is the segment name.

### Derived-name rules

| URL path (after `/en/{book|docs}/`) | Chapter folder | File name           |
|-------------------------------------|----------------|---------------------|
| `intro`                             | `00-intro/`    | `0001-intro.md`     |
| `intro/edit_compile_run`            | `00-intro/`    | `0002-edit-compile-run.md` |
| `basis`                             | `01-basis/`    | `0015-basis.md`     |
| `basis/syntax`                      | `01-basis/`    | `0016-basis-syntax.md` |
| `basis/types/integer/integertypes`  | `01-basis/`    | `0019-basis-types-integer-integertypes.md` |
| `standardlibrary/mathematics/...`   | `34-standardlibrary/` | `1143-standardlibrary-mathematics-....md` |

### Root-level URLs

The very first URL in each sitemap (e.g. `https://www.mql5.com/en/book` or
`https://www.mql5.com/en/docs`) has no depth-1 segment. It is placed directly
under the references root as:

```
0000-book.md      (for book sitemap)
0000-docs.md      (for docs sitemap)
```

## Complete Example — Book (first 20)

```
skills/mql5/references/book/
├── 0000-book.md                              # /en/book
├── 00-intro/
│   ├── 0001-intro.md                         # /en/book/intro
│   ├── 0002-edit-compile-run.md              # /en/book/intro/edit_compile_run
│   ├── 0003-mql-wizard.md                    # /en/book/intro/mql_wizard
│   ├── ...
│   └── pics/
├── 01-basis/
│   ├── 0015-basis.md                         # /en/book/basis
│   ├── 0016-basis-identifiers.md             # /en/book/basis/identifiers
│   ├── 0017-basis-builtin-types.md           # /en/book/basis/builtin_types
│   ├── 0018-basis-builtin-types-integer-numbers.md
│   ├── ...
│   └── pics/
├── 02-oop/
│   ├── ...
│   └── pics/
...
```

## Complete Example — Docs (first 20)

```
skills/mql5/references/docs/
├── 0000-docs.md                              # /en/docs
├── 00-basis/
│   ├── 0001-basis.md                         # /en/docs/basis
│   ├── 0002-basis-syntax.md                  # /en/docs/basis/syntax
│   ├── 0003-basis-syntax-commentaries.md     # /en/docs/basis/syntax/commentaries
│   ├── 0004-basis-syntax-identifiers.md
│   ├── 0005-basis-syntax-reserved.md
│   ├── 0006-basis-types.md
│   ├── 0007-basis-types-integer.md
│   ├── 0008-basis-types-integer-integertypes.md
│   ├── ...
│   └── pics/
├── 01-constants/
│   ├── ...
│   └── pics/
...
```

## Image Handling

- Images are saved to `pics/` within the chapter folder where they appear.
- Filenames: `{original-filename}` or `{derived-name}.png` if no useful name.
- The Markdown reference uses a relative path: `![alt](pics/image.png)`.
- Per extraction spec: the `<img>` alt text is taken from the next sibling
  `<p>` element's innerHTML, not duplicated.

## Name Sanitization

When converting URL segments to file/folder names:

| Character | Replacement |
|-----------|-------------|
| `_`       | `-`         |
| `/`       | `-` (within filename) |
| Uppercase | lowercase   |
| Non-alphanumeric (except `-`) | removed |

Example: `builtin_types` → `builtin-types`, `MQL_Wizard` → `mql-wizard`.

## Validation

A post-extraction script should verify:
1. Every sitemap URL has exactly one output file.
2. File numbers are sequential with no gaps.
3. No file exceeds the 4-digit range (max 9999 URLs per sitemap).
4. Chapter folder names match the expected pattern: `{NN}-{segment}`.
