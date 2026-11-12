---
name: gumroad-listing
description: Draft a Gumroad listing for a product dev finished, and once Justin approved the type, create it on his Gumroad through the signed-in browser. Load for PROMO-LISTINGS and PROMO-SALES, or when Justin says "list it" or asks how a product is selling.
---

# Gumroad listing

Justin's own Gumroad. Every listing is a draft until `send_guard.py gumroad-listing --routine PROMO-LISTINGS` says `auto`, and the first listing always waits for Justin's yes in chat.

## Draft (every time)

From `requests/promoter/<slug>.md` and the product's `marketing/listing.md`:

| Field | Rule |
|---|---|
| Title | What it does, in plain words, under 60 characters |
| Price | From SPEC.md; one-time; Tube Timer ($50) is the default anchor |
| Description | The problem the buyer feels, what it does, a 15-second demo GIF or screenshot, install, honest limits |
| Receipt note | How to install and where to get help |
| File | The release build; never source with keys |

Write it to `requests/justin/listing-<slug>.md` and the Notion queue. Stop.

## Publish (only when auto)

Signed-in browser, gumroad.com → New product. Fill exactly the approved draft. Save as **unpublished**, then publish only if the approval line says `publish`. Record the live URL in `daily/<date>/promoter.md`. Never change price, payout, tax or account settings.

## Sales (PROMO-SALES, read-only)

Read sales from Gumroad (dashboard in the browser, or the API with `GUMROAD_ACCESS_TOKEN` if Justin gave one: `GET https://api.gumroad.com/v2/sales`). Count a sale only with its Gumroad record. Never refund, never message buyers.
