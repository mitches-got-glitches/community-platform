# Record of Processing Activities (RoPA) + DPA register

UK GDPR **Art 30** record of how the org processes personal data, plus the **Art 28** register of Data Processing Agreements with each processor. The org is the **data controller**; each SaaS vendor that touches member data must be a **processor bound by a DPA**. This is **required before real member data lands** (R-15, R-26) — the IONOS pilot uses real data, so the Nextcloud-provider DPA is a hard gate.

## Processing activities (Art 30)
| Activity | Personal data | Data subjects | Purpose | Lawful basis | Retention | Location / processor |
|---|---|---|---|---|---|---|
| Collaboration | names, files, messages, calendars | members/volunteers | run the org | legitimate interest / consent — **TODO confirm** | TODO | Nextcloud provider (IONOS pilot → prod TBD) |
| Human email | correspondence + attachments | members + contacts | day-to-day mail | legitimate interest — TODO | TODO | Migadu (planned) / Proton (current) |
| Outreach CRM | contacts, donors, supporters, engagement | members/supporters/donors | mobilisation, comms, fundraising | consent / legitimate interest — TODO | TODO | Qomon |
| Secrets vault | mostly org credentials (minimal PII) | admins | operate the stack | legitimate interest | while in use | Proton Pass |

## DPA register (Art 28)
| Processor | Processes | DPA obtained? | No-marketing / EU-storage confirmed? | Notes |
|---|---|---|---|---|
| Nextcloud provider (IONOS pilot) | member collaboration data | **TODO — before real data** | **TODO** (IONOS marketing-consent flag — R-26) | gate for the real-data pilot |
| The Good Cloud (prod candidate) | member collaboration data | TODO | likely yes (no-ads ethos) | in pre-sales questions |
| Migadu | member correspondence | TODO | TODO | ([ADR-0011](../architecture/0011-custom-domain-email-via-migadu.md)) |
| Qomon | member/supporter CRM | **TODO** | TODO | already in use (R-28) |
| Netcup / BorgBase | infra (DIY path) | TODO | TODO | only if we self-host |

## Also to hold (governance)
Privacy notice to members, lawful-basis note, breach-response procedure (Art 33 log), and a data-subject-request (access/deletion) process. **TODO** — link once written (GOV-3).
