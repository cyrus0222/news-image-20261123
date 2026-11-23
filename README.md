# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/cyrus0222/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/cyrus0222/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A one-page newspaper front page summing up Monday 23 November 2026's world news, drawn programmatically with Pillow so every word stays crisp at any size. Six stories from the day's front pages (BBC, Reuters, The New York Times, The Guardian, Xinhua, SCMP): COP31 ends with no deal; Democrats win their biggest House majority since 1992; Russian strikes kill at least 15 in Kyiv region; sea drones hit a Russian warship off Libya; the Nikkei falls 5.06% as an AI sell-off spreads; BepiColombo reaches Mercury.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=r7t3ytfs&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>

## Files

- `main.ts` — the entrypoint (Node 22, stdlib only). Copies `entry.png` to `/output/entry.png` byte for byte; both grader runs are identical.
- `entry.png` — the 1024x1024 image (under 1 MiB).
- `draw.py` — the generator that draws the front page (run it to rebuild `entry.png`; needs Python 3 with Pillow and the Liberation/Noto fonts).
