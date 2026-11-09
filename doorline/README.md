# Doorline: Management & Maintenance

Apartment management and maintenance software for small and mid-size properties. There is a **Manager** side (rent ledger, late fees, notices, renewals, work orders, vendors, make-ready board, reports) and a **Maintenance** side (tech phone app, clock-in, punch lists with photos, plus pool, pest and Freon logs).

Brought over from the earlier Claude project. The live working copy is at https://claude.ai/artifact/5WumbKfA11msUYuaeEE8Hr.

## What's here

| Path | What it is |
| --- | --- |
| `index.html` | The whole app in one file. Open it in a browser. It runs on built-in sample data (fake residents, `555` phone numbers) and saves on the device. |
| `docs/competition.md` | Doorline vs. Yardi, RealPage, Entrata, AppFolio, Buildium, Rent Manager and Property Meld: features, prices and the 10-task race. |
| `docs/maintenance-software-comparison.md` | How each competitor handles maintenance, and how Doorline does it differently. |
| `docs/launch-checklist.md` | The steps from forming the LLC to the first paying property. |
| `docs/attorney-outline.md` | What the trial agreement, subscription agreement and data terms need to cover. |

## Status

- Working: work orders, the tech app, the make-ready board, inspection logs, the rent ledger, notices and training.
- Demo only: online rent payments, tenant screening and listings, until Stripe and a screening partner are connected.
- Not yet connected: a real database (Supabase) and sign-in. See section 3 of the launch checklist.

## Run it

Open `doorline/index.html` in any browser, or serve the repo with `python3 -m http.server` and go to `/doorline/`.
