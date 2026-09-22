# Runbook: getting Nextcloud Talk push notifications working

**Goal:** diagnose and fix "I'm not getting Talk notifications" on a member's phone, in the order that finds the cause fastest. Covers **Android and iOS**.

**Who this is for:** the admin. The member-facing summary lives in [What to tell members](#what-to-tell-members) and should be folded into the onboarding guide (DOC-5, issue #39) rather than sent as-is.

**How push works here (the one-paragraph version):** Talk does not talk to Google or Apple directly. The server sends the notification to **Nextcloud's push proxy** (`push-notifications.nextcloud.com:443`), which forwards it via **FCM** (Android) or **APNs** (iOS) to the device. Two consequences drive everything below: the app **must** come from the official store, and a **working test push does not mean notifications will arrive** — the server still decides, per message, whether to generate one at all.

**Most of this ladder is server-side and platform-neutral.** Steps 3–5 behave identically on both platforms; only steps 1, 2 and 6 differ. Resist the urge to treat an iPhone report as a separate problem until you have ruled those three out.

## Triage ladder

Work top to bottom. Each step either ends the investigation or rules out a layer.

### 1. Check where the app was installed from
| Platform | No push if… |
|---|---|
| Android | installed from **F-Droid** (ships without Google Play Services) or self-built |
| iOS | **self-compiled via Xcode** |

This is by design, not a fault. A de-Googled Android device cannot receive push at all — see [Known constraints](#known-constraints).
- ❌ Any of the above → **this is the cause.** Reinstall from Play Store / App Store, or accept that the device cannot receive push.
- ✅ Official store build → continue.

### 2. Run the in-app push test — **Android only**
> Avatar (top right of the conversation list) → **Settings** → **Advanced** → **Diagnosis** → **Test push notifications**

The button only appears when Play Services are present, so its absence is itself the answer to step 1.
- ✅ **Test notification arrives** → transport, registration, proxy and FCM all work. The fault is in *generation* or *display* — go to step 3.
- ❌ **Test fails or errors** → the fault is server-side or in registration — skip to step 7.

**iOS has no in-app equivalent.** The server-side `notification:test-push` command is the only direct test, and we have no `occ` on managed hosting — so on iPhone this step is unavailable and you must diagnose by elimination through steps 3–6. **If a member has both an Android and an iOS device, test on the Android one first** — it is the only way to get a clean transport verdict without provider support.

### 3. Close every active Talk session (the most likely cause — both platforms)
Talk **does not generate a notification for a conversation you already have an active session in** — and per the [upstream docs](https://github.com/nextcloud/talk-android/blob/master/docs/notifications.md), *"this also applies for tabs that are open in the background."*
- Close **all** browser tabs showing Nextcloud/Talk — including on other machines.
- Quit the **Talk desktop client** if installed; it suppresses push to mobile the same way ([talk-desktop#403](https://github.com/nextcloud/talk-desktop/issues/403)).
- Re-test using the [clean test procedure](#clean-test-procedure) below.

This was the cause in our own 2026-09 pilot: test pushes worked perfectly while a forgotten background tab silently suppressed every real notification.

### 4. Check the per-conversation notification level (both platforms)
**Group conversations default to notifying only on `@`-mention**, not on every message. This is the most common "notifications are broken" report that is not a fault.
- Open the conversation → its settings → set to **Always notify** (vs *Notify when mentioned* / *Never*).
- **Chat and call notifications are configured independently per conversation** (Talk 13+) — someone getting calls but no messages, or the reverse, is looking at this setting, not a platform bug.
- One-to-one conversations notify on every message by default, so **test with a 1:1 first** to isolate this.

### 5. Check the Nextcloud-side user status and notification settings (both platforms)
- **User status set to "Do not disturb"** — set from the avatar menu in the web UI, and the calendar integration can set it **automatically during meetings**. This is separate from the phone's own DND.
- **Personal settings → Notifications** — a per-activity-type grid; the Talk rows can be off independently of everything else.
- **Settings → Security → Devices & sessions** — delete **stale duplicate device entries**. Old registrations from reinstalls or replaced handsets can interfere with delivery.

### 6. Check the device side

**Android:**
- **Notification permission granted** — Android 13+ prompts once, and the prompt is easy to dismiss.
- **Battery set to "Unrestricted"** for Talk — adaptive battery otherwise kills the background connection.
- **Notification channels** — Talk registers several (messages, calls, ongoing); one being off while others work looks exactly like a partial failure.
- **Do Not Disturb** on the device.

**iOS:**
- **Settings → Nextcloud Talk → Notifications → Allow Notifications** must be on.
- **Focus modes** (iOS 15+) as well as Do Not Disturb — a Focus with Talk not on the allow-list silences it without any visible sign.
- **Background App Refresh** enabled for Talk.
- **Transient Apple-side failures:** Apple occasionally stops delivering (call) notifications to a device for no reachable reason. These **normally clear within 24 hours** — if everything else checks out, wait a day before escalating.

Note that **reinstalling the app resets these on both platforms**, so re-check after any reinstall.

### 7. Server side (test push failed)
Check in the admin UI:
- **Notifications app enabled** — push silently does nothing without it.
- **Background jobs set to Cron**, with a recent last-run, on the admin overview page.

**On managed hosting this is where we run out of road.** We have no `occ`, so the usual `notification:test-push` command and the server log are both unavailable — see [ADR-0012](../architecture/0012-diy-vs-managed-nextcloud.md). Outbound reachability to the push proxy cannot be verified from our side either. If the test push fails and the two checks above look correct, **raise a provider support ticket**; there is no self-service fix.

## Clean test procedure

Getting a *trustworthy* result matters more than getting a fast one — most false results come from testing wrong.

1. Use a **second account** (a dedicated test user is worth keeping for exactly this). You are **never** notified about your own messages.
2. Sign that account in from a **private/incognito window**, so it cannot disturb the main session. Suppression applies to the **recipient's** sessions, not the sender's.
3. **Close every Nextcloud/Talk tab** in the recipient's normal browser, on every machine.
4. **Lock the phone** — backgrounding the app is not the same test.
5. Send a message in a **one-to-one** conversation.

## What to tell members

Two things account for nearly every report, on both platforms, and both are counter-intuitive enough that members will otherwise conclude Talk is broken:

- **"If you keep Talk open in a browser tab, your phone will stay silent."** The server thinks you are already reading. Close the tab when you want phone notifications.
- **"In group channels you are only notified when someone `@`-mentions you"** unless you change that channel to *Always notify*.

Plus the standard setup steps: install from the **Play Store / App Store**, allow notifications when prompted, and then —
- **Android:** set the app's battery usage to **Unrestricted**.
- **iPhone:** check Talk is allowed through any **Focus** mode you use, and leave **Background App Refresh** on.

→ **DOC-5 input:** fold the above into the member onboarding guide, alongside the [Collabora tracking-protection note](managed-nextcloud-pilot.md#pilot-findings-2026-08--running-log).

## Known constraints

- **De-Googled and F-Droid Android users cannot receive push**, full stop. Relevant given the privacy leanings in our membership — those members need to open the app to check for messages, and should be told so during onboarding rather than discovering it.
- **iOS cannot be self-tested.** No in-app diagnosis, and `notification:test-push` needs `occ` we do not have — so an iPhone-only report can be narrowed but never definitively confirmed without provider support.
- **No `occ` on managed hosting** caps server-side diagnosis at step 7 for every platform.
