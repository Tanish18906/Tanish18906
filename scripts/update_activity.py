"""Refresh the cream/yellow contribution SVG using GitHub GraphQL.

Run in GitHub Actions with GITHUB_TOKEN. No third-party stats image service,
no additional dependencies, and no API secrets written to disk.
"""

import json
import os
from datetime import date
from pathlib import Path
from urllib.request import Request, urlopen
from xml.sax.saxutils import escape


LOGIN = os.environ.get("PROFILE_LOGIN", "Tanish18906")
TOKEN = os.environ.get("GITHUB_TOKEN")
OUTPUT = Path(__file__).resolve().parents[1] / "assets" / "activity.svg"
CREAM = "#F7F5EE"
INK = "#161616"
YELLOW = "#FACC00"
FONT = "Space Grotesk, Arial, DejaVu Sans, sans-serif"

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""


def fetch_calendar():
    if not TOKEN:
        raise SystemExit("GITHUB_TOKEN is required; keeping the existing SVG unchanged")
    request = Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "User-Agent": "tanish-profile-readme",
        },
        method="POST",
    )
    with urlopen(request, timeout=30) as response:
        result = json.load(response)
    if result.get("errors"):
        raise RuntimeError("GitHub GraphQL did not return contribution data")
    try:
        return result["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    except (KeyError, TypeError) as error:
        raise RuntimeError("GitHub did not return a contribution calendar") from error


def color(count):
    if count == 0:
        return "#E2DED2"
    if count <= 2:
        return "#F3E6A8"
    if count <= 5:
        return "#FADD60"
    if count <= 10:
        return YELLOW
    return INK


def render(calendar):
    weeks = calendar["weeks"][-53:]
    total = int(calendar["totalContributions"])
    rows = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1040 320" width="1040" height="320" role="img" aria-label="GitHub contribution calendar">',
        f'<title>{escape(LOGIN)} GitHub contribution activity</title>',
        f'<rect width="1040" height="320" fill="{CREAM}"/>',
        f'<rect x="2" y="2" width="1036" height="316" fill="none" stroke="{INK}" stroke-width="3"/>',
        f'<text x="34" y="48" font-family="{FONT}" font-size="29" font-weight="800" fill="{INK}">GITHUB ACTIVITY</text>',
        f'<text x="1007" y="46" text-anchor="end" font-family="{FONT}" font-size="21" font-weight="700" fill="{INK}">{total:,} CONTRIBUTIONS</text>',
        f'<path d="M34 68H1006" stroke="{INK}" stroke-width="2"/>',
    ]

    # Pre-collect month starts to prevent label overlap when week 0 has only a few days
    month_starts = []
    last_m = None
    for column, week in enumerate(weeks):
        if week["contributionDays"]:
            m = date.fromisoformat(week["contributionDays"][0]["date"]).strftime("%b")
            if m != last_m:
                month_starts.append((column, m))
                last_m = m

    valid_labels = {}
    for i, (col, m) in enumerate(month_starts):
        if i + 1 < len(month_starts):
            next_col = month_starts[i + 1][0]
            if next_col - col < 3:
                continue
        valid_labels[col] = m

    for column, week in enumerate(weeks):
        for day_idx, day in enumerate(week["contributionDays"]):
            count = int(day["contributionCount"])
            x = 40 + column * 18
            y = 123 + day_idx * 20
            rows.append(f'<rect x="{x}" y="{y}" width="13" height="13" rx="2" fill="{color(count)}"/>')
        if column in valid_labels:
            rows.append(f'<text x="{40+column*18}" y="104" font-family="{FONT}" font-size="18" font-weight="600" fill="{INK}">{valid_labels[column].upper()}</text>')
    rows.extend([
        f'<text x="37" y="300" font-family="{FONT}" font-size="15" font-weight="700" fill="{INK}" letter-spacing="1">VISIBLE GITHUB CONTRIBUTIONS · LAST 12 MONTHS</text>',
        f'<text x="801" y="300" font-family="{FONT}" font-size="15" font-weight="600" fill="{INK}">LESS</text>',
        '<rect x="860" y="286" width="15" height="15" rx="2" fill="#E2DED2"/>',
        '<rect x="881" y="286" width="15" height="15" rx="2" fill="#F3E6A8"/>',
        '<rect x="902" y="286" width="15" height="15" rx="2" fill="#FADD60"/>',
        f'<rect x="923" y="286" width="15" height="15" rx="2" fill="{YELLOW}"/>',
        f'<rect x="944" y="286" width="15" height="15" rx="2" fill="{INK}"/>',
        f'<text x="968" y="300" font-family="{FONT}" font-size="15" font-weight="600" fill="{INK}">MORE</text>',
        '</svg>',
    ])
    return "\n".join(rows)


def main():
    calendar = fetch_calendar()
    OUTPUT.write_text(render(calendar), encoding="utf-8")
    print(f"Updated {OUTPUT.name} from GitHub contribution data")


if __name__ == "__main__":
    main()
