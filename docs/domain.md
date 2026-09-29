# Domain

**Decision (29 September 2026): use `buildingbeautifully.org`, and backorder
`buildingbeautifully.com` as a hedge.**

`.org` is not a consolation prize here. For a policy and advocacy project run
out of a think tank it is the more natural signal, and it is what most of the
comparable projects use.

## Status

| Domain | State |
| --- | --- |
| `buildingbeautifully.org` | available, unregistered, no DNS records |
| `buildingbeautifully.com` | registered 2015-12-29 via Bluehost, expires **2026-12-29**, serves a parking page, status `clientTransferProhibited` (an ordinary registrar lock) |

## Turning the .org on

Steps 1 and 2 need a card and the registrar's control panel, so they are
yours. Step 3 onwards is one config change and one command — see the Custom
domain section of the README for the records and the exact syntax.

1. Register `buildingbeautifully.org`. Cloudflare Registrar sells at cost with
   no markup on renewal and includes WHOIS privacy; Porkbun and Namecheap are
   also fine. Avoid the registrar upsells — hosting, email, SSL, site builder.
   None of it is needed; GitHub Pages serves the site and issues the
   certificate.
2. Add the A, AAAA and `www` CNAME records from the README.
3. Wait for `nslookup buildingbeautifully.org` to return the four A records.
4. Set `custom_domain` in `config.json`, push, set the domain on the Pages API,
   then enable Enforce HTTPS once the certificate is issued.

Do not do step 4 before step 3 resolves. Setting a custom domain that DNS does
not yet point at takes the live site down until it propagates.

## Backordering the .com

Worth doing, but go in with realistic expectations: the holder has renewed for
eleven consecutive years, and a parking page is often a deliberately held
asset rather than a forgotten one. The likeliest outcome is that it renews.

**It will not drop on the expiry date.** The sequence after 2026-12-29 is:

| Stage | Length | Who can recover it |
| --- | --- | --- |
| Auto-renew grace | up to ~45 days, registrar's choice | the current holder, at normal price |
| Redemption grace | 30 days, ICANN-mandated | the current holder, at a penalty fee |
| Pending delete | 5 days | nobody |
| Drops | — | first catcher wins |

So the earliest it could actually become available is roughly **February to
March 2027**. Place the backorder well before then — DropCatch, SnapNames and
NameJet are the established catchers, typically $60–80 and only charged if
they catch it. If more than one person has backordered, it goes to a private
auction between them and the price is open-ended.

Set a calendar reminder for **mid-December 2026** to place the backorder, and
another for **March 2027** to check the outcome.

The alternative is a broker approach to the current holder now (GoDaddy Domain
Broker, Sedo). That costs a non-refundable fee regardless of outcome and
signals that an institution wants the name, which rarely lowers the asking
price.

## If MI wants to own this

The repository is on a personal GitHub account and the domain would be
registered in a personal name. If **Building Beautifully** is to read as an
institutional project — and it will, once the URL appears in a City Journal
piece or a briefing — it is worth asking MI comms and IT now whether they want
the registration held institutionally, or the site on a `manhattan.institute`
subdomain instead. Cheap to settle now, awkward to unwind later. The workshop
handout notes the Institute reimburses the domain either way.
