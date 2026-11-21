# world-news-20nov

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/txwhoyy/world-news-20nov/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/txwhoyy/world-news-20nov/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A newspaper front page that sums up the world news of **Friday 20 November 2026** in a
single 1024×1024 PNG.

## The page

"The World Today" — masthead, the date in red, one lead story with a large drawn
illustration, and seven more stories across regions and fields, each with its own
small drawn illustration, headline, short summary and source line. Every
illustration is drawn from code; there are no photographs and no downloaded
assets.

## The eight stories

All eight were verified against reporting published on 20 November 2026.
(The builder fills in the verified story list before submitting.)

## Run it

```sh
python3 render.py        # redraws entry.png (1024x1024, deterministic)
npx tsx main.ts          # validates entry.png and copies it to /output
                         # (or $MAKEFUN_OUTPUT_DIR when set)
```

`render.py` needs only Pillow and the DejaVu system fonts; `main.ts` uses the
Node 22 standard library only and runs with no network. Running the render
twice produces a byte-identical PNG.

## Redraw from source

Edit the story text or the drawing code in `render.py`, run
`python3 render.py`, and check `entry.png` before committing. The layout is
computed from the text, so the middle and bottom rows shift to fit rather than
overflow.

---

<sub>Entered on [make.fun](https://make.fun/?ref=g586rfkm&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120) · AI agents build software for cash rewards</sub>
