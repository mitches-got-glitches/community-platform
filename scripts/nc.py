#!/usr/bin/env python3
"""Small Nextcloud API helper for this repo's just recipes.

Credentials come from the environment (NC_URL, NC_USER, NC_PASS), resolved from
the BAFZ Vault by `pass-cli run` — see the justfile. They are read in-process and
used to build an Authorization header, so the secret never appears in a command
line, where /proc/<pid>/cmdline would expose it to any user on the machine.
"""
import base64
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

DAV_NS = "{DAV:}"


def env(name):
    v = os.environ.get(name)
    if not v:
        sys.exit(f"{name} is not set — run this through `just`, not directly.")
    return v.rstrip("/") if name == "NC_URL" else v


class NC:
    def __init__(self):
        self.url = env("NC_URL")
        auth = f"{env('NC_USER')}:{env('NC_PASS')}".encode()
        self.hdr = {"Authorization": "Basic " + base64.b64encode(auth).decode()}

    def _open(self, path, method="GET", body=None, extra=None):
        req = urllib.request.Request(self.url + path, data=body, method=method)
        for k, v in {**self.hdr, **(extra or {})}.items():
            req.add_header(k, v)
        return urllib.request.urlopen(req)

    def ocs(self, path, method="GET", payload=None):
        body = json.dumps(payload).encode() if payload is not None else None
        extra = {"OCS-APIRequest": "true", "Accept": "application/json",
                 "Content-Type": "application/json"}
        with self._open(path, method, body, extra) as r:
            raw = r.read()
        return json.loads(raw) if raw else None

    def deck(self, path):
        extra = {"OCS-APIRequest": "true", "Accept": "application/json"}
        with self._open("/index.php/apps/deck/api/v1.0" + path, extra=extra) as r:
            return json.load(r)

    def dav_list(self, path):
        """Immediate children of a WebDAV collection: (href, is_dir)."""
        body = ('<?xml version="1.0"?><d:propfind xmlns:d="DAV:"><d:prop>'
                '<d:resourcetype/></d:prop></d:propfind>').encode()
        with self._open("/remote.php/dav/files/" + urllib.parse.quote(env("NC_USER")) + path,
                        "PROPFIND", body, {"Depth": "1", "Content-Type": "application/xml"}) as r:
            tree = ET.fromstring(r.read())
        out = []
        for resp in tree.findall(DAV_NS + "response")[1:]:  # [0] is the collection itself
            href = urllib.parse.unquote(resp.find(DAV_NS + "href").text)
            out.append((href, resp.find(f".//{DAV_NS}collection") is not None))
        return out

    def dav_get(self, path):
        with self._open("/remote.php/dav/files/" + urllib.parse.quote(env("NC_USER")) + path) as r:
            return r.read().decode()


def walk_wiki(nc):
    """Yield (collective, relative path, markdown) for every wiki page."""
    root = "/.Collectives"
    prefix = f"/remote.php/dav/files/{env('NC_USER')}/.Collectives/"
    stack = [urllib.parse.quote(root)]
    while stack:
        for href, is_dir in nc.dav_list(stack.pop()):
            rel = href[len(prefix):].rstrip("/")
            if not rel:
                continue
            if is_dir:
                stack.append(urllib.parse.quote("/.Collectives/" + rel))
            elif rel.endswith(".md"):
                collective, _, page = rel.partition("/")
                yield collective, page or rel, nc.dav_get("/.Collectives/" + urllib.parse.quote(rel))


def cmd_check(nc, _):
    d = nc.ocs("/ocs/v2.php/cloud/capabilities")["ocs"]["data"]
    v = d["version"]
    caps = d["capabilities"]
    print(f"✅ authenticated as {env('NC_USER')}")
    print(f"   Nextcloud {v['string']}  (Talk {caps.get('spreed', {}).get('version', '—')})")
    sub = caps.get("support", {})
    if sub.get("hasValidSubscription"):
        print(f"   subscription: {sub.get('desktopEnterpriseChannel', 'yes')}")
    return 0


def cmd_users(nc, _):
    ids = nc.ocs("/ocs/v1.php/cloud/users")["ocs"]["data"]["users"]
    print(f"{len(ids)} account(s)")
    for uid in ids:
        u = nc.ocs(f"/ocs/v1.php/cloud/users/{urllib.parse.quote(uid)}")["ocs"]["data"]
        groups = ",".join(u.get("groups") or []) or "—"
        print(f"  {uid:20} {u.get('displayname','') :25} {u.get('email') or '—':30} [{groups}]")
    return 0


def cmd_user_add(nc, args):
    if len(args) < 2:
        sys.exit("usage: user-add <login> <email>")
    login, email = args[0], args[1]
    r = nc.ocs("/ocs/v1.php/cloud/users", "POST", {"userid": login, "email": email})
    meta = r["ocs"]["meta"]
    if meta["statuscode"] != 100:
        sys.exit(f"failed: {meta['message']}")
    print(f"✅ created {login} — activation email sent to {email}")
    print("   Next: add to Teams, add to Talk channels, record in the access register.")
    return 0


def cmd_wiki_export(nc, args):
    out = Path(args[0] if args else "wiki-export")
    n = 0
    for collective, page, text in walk_wiki(nc):
        dest = out / collective / page
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text)
        n += 1
    print(f"✅ exported {n} page(s) to {out}/")
    print("   Contains member content — keep it out of this public repo.")
    return 0


def cmd_wiki_todo(nc, _):
    found = 0
    for collective, page, text in walk_wiki(nc):
        if "🎬" in text:
            count = text.count("🎬")
            print(f"  {count}x  {collective}/{page}")
            found += count
    print(f"{found} screen recording placeholder(s) outstanding" if found
          else "✅ no outstanding screen-recording placeholders")
    return 0


def cmd_deck_card(nc, args):
    if len(args) < 2:
        sys.exit("usage: deck-card <board> <card>")
    board, card = int(args[0]), int(args[1])
    for stack in nc.deck(f"/boards/{board}/stacks"):
        for c in stack.get("cards") or []:
            if c["id"] != card:
                continue
            desc = c.get("description") or ""
            done = desc.count("- [x]") + desc.count("- [X]")
            total = done + desc.count("- [ ]")
            print(f"{c['title']}  [{stack['title']}]")
            if c.get("duedate"):
                print(f"   due: {c['duedate'][:10]}")
            labels = ", ".join(l["title"] for l in c.get("labels") or [])
            people = ", ".join(a["participant"]["displayname"] for a in c.get("assignedUsers") or [])
            if labels:
                print(f"   labels: {labels}")
            if people:
                print(f"   assigned: {people}")
            if total:
                print(f"   checklist: {done}/{total} done")
            print("\n" + desc)
            return 0
    sys.exit(f"card {card} not found on board {board} (archived cards aren't listed)")


COMMANDS = {"check": cmd_check, "users": cmd_users, "user-add": cmd_user_add,
            "wiki-export": cmd_wiki_export, "wiki-todo": cmd_wiki_todo,
            "deck-card": cmd_deck_card}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        sys.exit("usage: nc.py {" + "|".join(COMMANDS) + "} [args]")
    try:
        sys.exit(COMMANDS[sys.argv[1]](NC(), sys.argv[2:]))
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code} {e.reason} — {e.url}")
