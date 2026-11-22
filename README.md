# Sunday 22 November 2026 — The World Today (evening edition)

[![make.fun](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/baruet/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/baruet/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122)

One image summing up the world news of **Sunday 22 November 2026** — a
front page drawn entirely in code (Python + Pillow + DejaVu fonts, no AI
image generation, so every word is spelled right).

- **Lead:** COP31 on the brink in Antalya — final 10-page text put to
  vote with no fossil fuels named; first COP to admit 1.5°C will be
  breached; deal far from certain.
- **Also inside:** Iran hits US bases in Bahrain; India's record 720/9
  in Wellington (Pant 128, Rahul 136); Nepal PM lands in New Delhi;
  Verstappen on pole in Las Vegas; Modi opens Nitish Setu in Bihar;
  India–Canada wrap trade talks; plus a ticker with the Turin final,
  the Cikande search and the Myanmar quake.

Every story was verified as 22 November 2026 news (first reported that
day, or happening that day). Checked and left out as NOT 22 Nov news:
the El Chapo Isidro capture (announced 21 Nov), the Trump–Xi–Putin
Shenzhen summit (19 Nov), the EU–Indonesia trade deal (signed 21 Nov)
and the US AI stock sell-off (20 Nov close).

v2 (evening edition) refreshes v1 (morning edition): the COP31 lead
rewritten to the day's outcome, the cricket cell updated to the
completed day four, and the ticker refreshed. v1 is kept as
entry-v1-backup.png.

## Run

```sh
python3 draw.py        # regenerates entry.png (1024x1024, <= 1 MiB)
node main.ts           # copies entry.png to $MAKEFUN_OUTPUT_DIR (or ./out)
```

Deterministic: `main.ts` is a byte-for-byte copy, so repeated runs produce
identical output.

## Bounty

[make.fun — news-image-20261122](https://make.fun/bounty/news-image-20261122)
