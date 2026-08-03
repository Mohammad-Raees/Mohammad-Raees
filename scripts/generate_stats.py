#!/usr/bin/env python3
"""Generate static GitHub profile SVG cards (no external Vercel deps)."""

from __future__ import annotations

import json
import os
import urllib.request
from pathlib import Path

USERNAME = os.environ.get("GITHUB_USERNAME", "Mohammad-Raees")
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or ""
OUT = Path(__file__).resolve().parents[1] / "assets"


def gh(path: str):
    req = urllib.request.Request(
        f"https://api.github.com{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "profile-stats-generator",
            **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}),
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def esc(text: str) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def card(title: str, rows: list[tuple[str, str]], width=420, height=195) -> str:
    lines = []
    y = 58
    for label, value in rows:
        lines.append(
            f'<text x="28" y="{y}" fill="#9fefef" font-size="14" font-family="Segoe UI, Ubuntu, Sans-Serif">{esc(label)}</text>'
            f'<text x="{width - 28}" y="{y}" fill="#ffffff" font-size="14" font-weight="700" text-anchor="end" font-family="Segoe UI, Ubuntu, Sans-Serif">{esc(value)}</text>'
        )
        y += 26
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#1e1b4b"/>
    </linearGradient>
  </defs>
  <rect width="{width}" height="{height}" rx="12" fill="url(#bg)" stroke="#6366f1" stroke-width="1"/>
  <text x="28" y="32" fill="#a5b4fc" font-size="16" font-weight="700" font-family="Segoe UI, Ubuntu, Sans-Serif">{esc(title)}</text>
  <line x1="28" y1="42" x2="{width - 28}" y2="42" stroke="#334155" stroke-width="1"/>
  {''.join(lines)}
</svg>
'''


def langs_card(langs: list[tuple[str, float]], width=420, height=195) -> str:
    colors = ["#f1e05a", "#3178c6", "#3572A5", "#e34c26", "#563d7c", "#89e051", "#b07219", "#00ADD8"]
    total = sum(p for _, p in langs) or 1
    bar_x = 28
    bar_parts = []
    legend = []
    y = 70
    for i, (name, count) in enumerate(langs[:6]):
        pct = count / total
        w = max(2, int((width - 56) * pct))
        color = colors[i % len(colors)]
        bar_parts.append(f'<rect x="{bar_x}" y="50" width="{w}" height="12" fill="{color}"/>')
        bar_x += w
        legend.append(
            f'<circle cx="34" cy="{y}" r="5" fill="{color}"/>'
            f'<text x="46" y="{y + 4}" fill="#e2e8f0" font-size="13" font-family="Segoe UI, Ubuntu, Sans-Serif">{esc(name)} {pct*100:.1f}%</text>'
        )
        y += 20
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <defs>
    <linearGradient id="bg2" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#1e1b4b"/>
    </linearGradient>
  </defs>
  <rect width="{width}" height="{height}" rx="12" fill="url(#bg2)" stroke="#6366f1" stroke-width="1"/>
  <text x="28" y="32" fill="#a5b4fc" font-size="16" font-weight="700" font-family="Segoe UI, Ubuntu, Sans-Serif">Most Used Languages</text>
  <line x1="28" y1="42" x2="{width - 28}" y2="42" stroke="#334155" stroke-width="1"/>
  <rect x="28" y="50" width="{width - 56}" height="12" rx="6" fill="#1e293b"/>
  {''.join(bar_parts)}
  {''.join(legend)}
</svg>
'''


def quote_card() -> str:
    quote = "Ship fast. Learn faster. Build things that matter."
    author = "Mohammad Raees"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="680" height="90" viewBox="0 0 680 90">
  <rect width="680" height="90" rx="12" fill="#0f172a" stroke="#6366f1" stroke-width="1"/>
  <text x="340" y="40" fill="#e2e8f0" font-size="16" font-style="italic" text-anchor="middle" font-family="Georgia, serif">"{esc(quote)}"</text>
  <text x="340" y="66" fill="#a5b4fc" font-size="13" text-anchor="middle" font-family="Segoe UI, Ubuntu, Sans-Serif">— {esc(author)}</text>
</svg>
'''


def trophies_card(user: dict, langs_count: int) -> str:
    items = [
        ("Commits", "Active"),
        ("Repos", str(user.get("public_repos", 0))),
        ("Followers", str(user.get("followers", 0))),
        ("Langs", str(langs_count)),
        ("OSS", "Yes"),
        ("npm", "Live"),
    ]
    boxes = []
    x = 20
    for title, value in items:
        boxes.append(
            f'<rect x="{x}" y="45" width="100" height="70" rx="10" fill="#1e1b4b" stroke="#818cf8"/>'
            f'<text x="{x + 50}" y="75" fill="#c7d2fe" font-size="12" text-anchor="middle" font-family="Segoe UI, Ubuntu, Sans-Serif">{esc(title)}</text>'
            f'<text x="{x + 50}" y="98" fill="#ffffff" font-size="16" font-weight="700" text-anchor="middle" font-family="Segoe UI, Ubuntu, Sans-Serif">{esc(value)}</text>'
        )
        x += 110
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="680" height="140" viewBox="0 0 680 140">
  <rect width="680" height="140" rx="12" fill="#0f172a" stroke="#6366f1" stroke-width="1"/>
  <text x="20" y="30" fill="#a5b4fc" font-size="16" font-weight="700" font-family="Segoe UI, Ubuntu, Sans-Serif">Profile Highlights</text>
  {''.join(boxes)}
</svg>
'''


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    user = gh(f"/users/{USERNAME}")

    # Aggregate language bytes across repos
    repos = gh(f"/users/{USERNAME}/repos?per_page=100&type=owner&sort=updated")
    lang_bytes: dict[str, int] = {}
    commits_proxy = 0
    for repo in repos:
        if repo.get("fork"):
            continue
        commits_proxy += int(repo.get("size") or 0)
        name = repo["name"]
        try:
            langs = gh(f"/repos/{USERNAME}/{name}/languages")
        except Exception:
            continue
        for lang, count in langs.items():
            lang_bytes[lang] = lang_bytes.get(lang, 0) + int(count)

    sorted_langs = sorted(lang_bytes.items(), key=lambda x: x[1], reverse=True)

    stats = card(
        f"{USERNAME}'s GitHub Stats",
        [
            ("Public Repositories", str(user.get("public_repos", 0))),
            ("Followers", str(user.get("followers", 0))),
            ("Following", str(user.get("following", 0))),
            ("Public Gists", str(user.get("public_gists", 0))),
            ("Non-fork Projects", str(sum(1 for r in repos if not r.get("fork")))),
        ],
    )
    (OUT / "github-stats.svg").write_text(stats, encoding="utf-8")
    (OUT / "top-langs.svg").write_text(langs_card(sorted_langs or [("TypeScript", 1)]), encoding="utf-8")
    (OUT / "quote.svg").write_text(quote_card(), encoding="utf-8")
    (OUT / "trophies.svg").write_text(trophies_card(user, len(sorted_langs)), encoding="utf-8")
    print(f"Wrote SVGs to {OUT}")


if __name__ == "__main__":
    main()
