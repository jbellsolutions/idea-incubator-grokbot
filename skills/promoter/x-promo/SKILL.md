---
name: x-promo
description: Draft and, once approved, post product launches and how-tos on Justin's own X so the factory's products sell. Load for PROMO-POSTS or when Justin says "promote", "post about" or "launch" a product.
---

# X promotion for products

Justin's own X account, through the signed-in browser (the X API charges per post). The Revenue OS bot posts there too, so this bot posts **products only**.

## Rules

- Read Justin's last 20 posts before drafting. Never repeat a hook, a product or a format used in the last 7 days.
- At most 2 posts a day from this bot. No DMs, no replies to strangers, no follows, no likes in bulk.
- `send_guard.py x-product-post --routine PROMO-POSTS` before posting. Not auto → draft to `requests/justin/` and stop. The first post always waits for Justin.
- Honest copy: real screenshots, real limits, no invented numbers or fake urgency. Plain, warm, specific; lead with the problem.
- Every post carries the Gumroad link only after that listing is live.

## The launch sequence per product

| Post | What |
|---|---|
| 1 | The problem, the 15-second demo clip, the link |
| 2 | How it works (thread of 3–5) |
| 3 | A real use: one screenshot, one line |
| 4 | The free DIY version on GitHub, if there is one (only after Justin made that repo public) |

Draft them from `marketing/social.md`. Record each live post's URL in `daily/<date>/promoter.md`; a draft never counts.
