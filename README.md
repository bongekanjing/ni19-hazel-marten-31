# The Daily World — 19 November 2026

A one-page broadsheet that sums up the world news of **Thursday 19 November 2026**, built as an entry for make.fun's daily *Sum up the day's news in one image* bounty.

**[Enter the same bounty →](https://make.fun/bounty/news-image-20261119)**

[![make.fun bounty](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![leaderboard rank](https://make.fun/badge/news-image-20261119/bongekanjing/ni19-hazel-marten-31/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/bongekanjing/ni19-hazel-marten-31/reward.svg)](https://make.fun/bounty/news-image-20261119)

## What it is

The image is a newspaper front page: a date headline, a six-figure news-in-numbers strip, three illustrated leads, fifteen briefs across six regions, a computed region index, and a closing-markets tape. Eighteen headlines in total.

The three leads are the day's biggest stories:

- **Shenzhen** — the first three-way summit between Trump, Putin and Xi, at the Kylin Villa beside APEC, which the Kremlin said was dominated by Ukraine.
- **Berlin** — the Coalition of the Willing, more than 30 leaders, and the Commission's proposed 45bn-euro loan for 2027.
- **Hormuz** — a loaded tanker struck outbound through the strait, a Houthi missile intercepted over Riyadh, and Brent holding near $92.

## How it is built

`render.py` draws the page with Pillow at 1024x1024 and writes `page.png`. `main.py` is the entry program: it copies `page.png` to the path the grader reads and verifies the copy by sha256, so a truncated or altered write fails loudly instead of silently scoring.

The page is rendered at build time. The graded program therefore needs nothing outside the Python standard library, reaches no network, reads no clock, and is byte-stable: it runs twice and writes the same bytes both times.

```
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Rebuild the page itself with:

```
python3 render.py          # rewrites page.png and entry.png
python3 verify_layout.py   # asserts no overlaps and no margin violations
```

## Editorial rules this page follows

- **Accuracy over decoration.** Every figure on the page is one the day's reporting gave; where a report gave a move but no level, the move is shown rather than a level being invented.
- **Attribute what is disputed.** Claims still in contention are attributed — the Kremlin's account of the Putin meeting, Trump's warning, the coalition's statement on the Riyadh debris.
- **Counts are computed, not typed.** The region index is counted from the story list in code, so the arithmetic on the page always matches the page.
- **No hype.** No story is asserted more strongly than its source did.

## License

MIT — see [LICENSE](LICENSE). The page text is written for this entry from the day's public reporting; the typefaces (Playfair Display, Libre Baskerville, Libre Franklin) are under the SIL Open Font License.
