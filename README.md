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

1. **Russia hits Kyiv's bridges in overnight barrage** — Russian missiles
   struck three of Kyiv's road bridges overnight, killing eight people and
   injuring 28 across nine regions. Source: Reuters.
2. **Russian missile crashes in Poland** — Poland said two Russian missiles
   and a drone violated its airspace overnight; Warsaw condemned the
   incursion as intentional. Source: BBC.
3. **UK and EU agree new deal at summit** — Britain and the EU agreed a deal
   on food exports, emissions trading and a youth mobility scheme at their
   Brussels summit. Source: BBC.
4. **Trump threatens ban on overseas AI data centres** — President Trump
   threatened to ban US firms from building AI data centres abroad,
   escalating his technology crackdown. Source: BBC.
5. **Houthi missile hits Riyadh tower** — A Houthi missile damaged the
   sovereign wealth fund tower in Riyadh, and Saudi defences intercepted
   more missiles on Friday. Source: AP / Sky News.
6. **Tech sell-off deepens after Anthropic debut** — Anthropic shares fell a
   day after their blockbuster Nasdaq debut, and Asian markets slid —
   Japan's Nikkei down 4.8%. Source: BBC / CNBC.
7. **Cost-of-living protests sweep Europe** — Thousands marched across
   Europe on Friday against the cost of living, in coordinated protests
   over prices and household bills. Source: BBC.
8. **BepiColombo reaches Mercury after eight years** — The BepiColombo probe
   reached Mercury after an eight-year, six-billion-mile voyage; it enters
   orbit on Saturday. Source: BBC / NPR.

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
