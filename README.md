# The World Today — Monday, 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/Kkajasd/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/Kkajasd/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A one-page newspaper front page summing up the world's news of Monday,
23 November 2026: Nvidia reinstates Jensen Huang as CEO (shares +31%),
Wall Street's sharp rebound, the Kospi slide, the Bridgetown AI safety
summit, and 26 more verified stories from the day. The image is rendered
deterministically with Python + Pillow (`tools/draw_frontpage.py`); the
entry program (`main.ts`) simply copies the pre-rendered PNG to the
output directory. Every story on the page is sourced in `SOURCES.md`.

## Run

```sh
# Regenerate the image (optional; entry.png is already in the repo)
python3 tools/draw_frontpage.py

# Run the entry program
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# -> out/entry.png (1024x1024 PNG, under 1 MiB)
```

Requires Node 22.18+ and Python 3 with Pillow. No network access is used
at run time.
