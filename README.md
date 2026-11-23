# Sunday 22 November 2026 — The World Today (final edition)

[![make.fun](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/baruet/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/baruet/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122)

One image summing up the world news of **Sunday 22 November 2026** — a
front page drawn entirely in code (Python + Pillow + DejaVu fonts, no AI
image generation, so every word is spelled right).

- **Lead:** COP31 COLLAPSES — no deal in Antalya. The EU and 130 nations
  reject a text with no fossil fuels; the longest COP ever ends without
  a deal.
- **Also inside (16 cells, 7 regions):** Iran hits US bases in Bahrain;
  Russia's 186-drone barrage on Kyiv (4 killed, 14 missing); Sparta II
  still burning off Finland; India's record 720/9 in Wellington (Pant
  128, Rahul 136); Verstappen wins in Las Vegas; Alcaraz takes Turin;
  Belgium flights grounded; Nepal PM lands in New Delhi; Modi opens
  Nitish Setu in Bihar; India–Canada wrap trade talks; 36 missing in
  the Cikande factory fire; France protests, 6th weekend; settler arson
  in the West Bank; a Russian ship sunk off Libya; South Korea's minister
  quits; a Nigeria boat capsizes (24 drowned). Ticker: Brazil storm,
  Myanmar M4.1 quake, Gaza aid-truck strike.

Every story happened or was first reported on 22 November 2026. Checked
and left out as NOT 22 Nov news: the El Chapo Isidro capture (20 Nov,
announced 21 Nov), the EU–Indonesia trade deal (signed 21 Nov), the
Trump–Xi–Putin Shenzhen summit (19 Nov), the Russia 400-drone attack
(20 Nov), the Peru M6.8 quake (21 Nov) and the US AI stock sell-off
(20 Nov close). The Gaza aid-truck strike happened Saturday 21 Nov but
was first reported Sunday 22 Nov (Reuters) — included as Sunday's
reported news.

v3 (final edition) refreshes v2 (evening edition): the COP31 lead
rewritten to the day's outcome (collapse, not "on the brink"); the
Verstappen and Alcaraz cells updated from previews to results; the grid
grew from 6 cells to 16, with nine new 22 Nov stories. v2 is kept as
entry-v2-backup.png, v1 as entry-v1-backup.png.

## Run

```sh
python3 draw.py        # regenerates entry.png (1024x1024, <= 1 MiB)
node main.ts           # copies entry.png to $MAKEFUN_OUTPUT_DIR (or /output)
```

Deterministic: `main.ts` is a byte-for-byte copy, so repeated runs produce
identical output.

## Bounty

[make.fun — news-image-20261122](https://make.fun/bounty/news-image-20261122)
