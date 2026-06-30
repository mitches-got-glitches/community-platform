# A home of our own: moving the org off WhatsApp + Google

*A proposal for the committee and members — June 2026*

## The ask, in one paragraph
Right now our organisation lives on **WhatsApp** (chat) and **Google** (docs, files,
calendar, email). It works, but it's borrowed ground: our members' data sits on US
companies' servers, scattered across personal accounts, with no single home we control.
This proposes moving to **one self-hosted system we own** — for roughly the price of a
couple of streaming subscriptions a year — that does chat, files, a shared calendar, a
wiki, and task tracking in one place. Nothing we rely on today disappears overnight; we'd
move in stages, and you can keep WhatsApp for casual chat as long as you like.

---

## Why change at all?

Our current setup quietly costs us in ways that don't show up on a bill:

- **We don't own our own information.** Files live in people's personal Google Drives.
  Chat history lives in WhatsApp. When someone leaves — or just gets a new phone — pieces
  of the org's memory leave with them. There's no single place that *is* the organisation.
- **It's not really private or sovereign.** Our members' personal data sits with US
  platforms, subject to US law and used to build advertising profiles. For a community
  org that cares about its members, "we handed everyone's data to Google and Meta" is not
  a great answer — and under **UK GDPR we're responsible** for that data either way.
- **WhatsApp is chaos for actual organising.** No channels, no proper threads, no way to
  separate "committee business" from "social chat" from "this Saturday's event." Important
  decisions vanish up the scroll. Files shared in WhatsApp are effectively lost a week later.
- **It can't grow with us.** As we add members, "everyone in one WhatsApp group + a pile
  of Google Docs nobody can find" gets worse, not better.

We're not moving because the tools are *bad*. We're moving because the org deserves a
**home it actually owns.**

---

## What we'd get instead

One system — **Nextcloud** — that replaces the scattered Google bits, plus built-in chat
and calls to replace WhatsApp for org business:

| What we do today | Today's tool | In the new home |
|------------------|--------------|-----------------|
| Group chat & coordination | WhatsApp | **Channels** (per topic/event/committee), with replies & threads |
| Voice / video calls | WhatsApp / Meet | **Built-in calls** (no separate app or account) |
| Shared files | personal Google Drives | **One shared file store** the org owns, syncs to your devices |
| Documents & notes | Google Docs (scattered) | **A wiki / knowledge base** — findable, lasting |
| Who's doing what | WhatsApp messages | **A shared task board** |
| Events & rotas | Google Calendar | **A shared calendar** that syncs to your phone |

It's all **one login, one place**, and crucially — **it's ours.** It runs on a server we
rent in Europe, the data belongs to the organisation, and we can pick it up and move it
anywhere if we ever need to.

---

## What it costs

About **£160–180 a year, all-in** — server, backups, and our web address. That's it. No
per-member fees, no price hikes, no "upgrade for more storage" pop-ups. For an org our
size that's a few pounds per member per year, for something we fully control.

---

## Being honest: what changes, and what we give up

Trust matters more than hype, so here's the straight version.

**What changes for you, day to day:**
- You'll have **one account** for the org's system (separate from your personal Google).
- For org business, you'll open our chat instead of the WhatsApp group. It works on phone
  and computer, much like WhatsApp/Slack.
- **You don't have to abandon WhatsApp.** Keep it for casual/social chatter. We're moving
  the org's *work* into a proper home, not policing your group chats.

**What we give up (and why it's worth it):**
- **Convenience of "everyone's already on WhatsApp."** There's a small learning curve and
  a sign-in. In exchange we get channels, threads, lasting files, and ownership.
- **A big company keeping it running 24/7.** Our system is run by *us* — see the next
  section, because this is the one real risk and we're addressing it head-on.
- **A few niceties** (e.g. some slick Google integrations). We're choosing independence
  and privacy over polish. For our needs, the trade is worth it.

---

## "But who keeps it running?" — the honest risk, and the plan

This is the fair question, so here's the honest answer. Today it would be set up and
maintained by **one volunteer admin**. If that person stepped away with no plan, we'd be
stuck. We are **not** pretending that risk away — we're designing around it:

- **Everything is automated and written down**, so the whole system can be rebuilt from
  scratch with a single command if it's ever lost.
- **Backups run automatically every day** to a *separate* European provider, and we
  *test* that we can actually restore them — before we trust the system with real data.
- **The keys aren't in one person's head.** Critical passwords live in a shared, encrypted
  vault, so the org can recover even if the admin is unavailable.
- **We commit to training a second person within three months**, so it's never one
  person's secret knowledge. *(This is a firm commitment, not a vague hope — and if we
  can't find a second volunteer, we'll pay a specialist European service to keep it
  running rather than leave it fragile.)*

Compared to today — where the org's data is already scattered across personal accounts
with *no* backup and *no* recovery plan — this is a big step **up** in resilience, not down.

---

## How we'd move (no big-bang switch)

1. **Set it up quietly** and test it (including a full backup-and-restore) before anyone
   relies on it.
2. **Move the foundations first:** files, calendar, and the wiki — the things that benefit
   most from a real home.
3. **Invite members in**, with a short one-page guide and a hands-on session for anyone
   who wants it.
4. **Shift org chat over** channel by channel, keeping WhatsApp alive for casual use during
   the transition.
5. **Review after a month.** If something's not working (e.g. group video), we add or
   adjust. Nothing here is one-way.

If members are heavily tied to WhatsApp, there's even a future option to **bridge** WhatsApp
into our system so messages flow both ways — we've deliberately left that door open for
later rather than forcing a clean break now.

---

## What we're asking the committee to approve

1. A budget of **~£180/year** for the org's own collaboration system.
2. Going ahead with a **staged move** off Google/WhatsApp for *org business*, starting with
   files, calendar, and wiki.
3. **Naming a second volunteer** to be trained as co-admin within three months.

The result: a private, resilient, member-respecting home that the organisation **owns** —
for about the cost of a couple of streaming subscriptions a year.

---

*Want the technical detail behind these choices? See the architecture decision records in
`docs/architecture/` — every choice, every alternative, and why we picked what we did.*
