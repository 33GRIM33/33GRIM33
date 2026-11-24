"""Render 90 days from GitHub's public contribution calendar for the profile README."""

from datetime import date, timedelta
from html.parser import HTMLParser
from math import ceil
from pathlib import Path
import re
from urllib.request import Request, urlopen


class Calendar(HTMLParser):
    def __init__(self):
        super().__init__()
        self.dates = {}
        self.counts = {}
        self.tip = None
        self.text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "td" and "data-date" in attrs and "id" in attrs:
            self.dates[attrs["id"]] = date.fromisoformat(attrs["data-date"])
        elif tag == "tool-tip" and attrs.get("for") in self.dates:
            self.tip = self.dates[attrs["for"]]
            self.text = []

    def handle_data(self, data):
        if self.tip is not None:
            self.text.append(data)

    def handle_endtag(self, tag):
        if tag == "tool-tip" and self.tip is not None:
            count = re.match(r"(No|[0-9,]+) contributions?\b", "".join(self.text).strip())
            if count:
                number = count.group(1)
                self.counts[self.tip] = 0 if number == "No" else int(number.replace(",", ""))
            self.tip = None


def fetch_window():
    request = Request("https://github.com/users/33GRIM33/contributions", headers={
        "Accept-Language": "en-US",
        "User-Agent": "33GRIM33-profile-activity",
    })
    with urlopen(request, timeout=30) as response:
        html = response.read().decode("utf-8")
    calendar = Calendar()
    calendar.feed(html)
    end = max(calendar.counts)
    start = end - timedelta(days=89)
    days = [start + timedelta(days=i) for i in range(90)]
    if not all(day in calendar.counts for day in days):
        raise ValueError("GitHub returned an incomplete 90-day contribution window")
    return days, [calendar.counts[day] for day in days]


def render(days, values):
    left, right, top, bottom = 56, 854, 31, 170
    step = max(1, ceil(max(values) / 20)) * 5
    peak = max(step, ceil(max(values) / step) * step)

    def x(day):
        return left + (right - left) * day / 90

    def y(value):
        return bottom - (bottom - top) * value / peak

    horizontal = []
    y_labels = []
    for level in range(0, peak + 1, step):
        line_y = y(level)
        horizontal.append(f'M{left} {line_y:.2f}H{right}')
        y_labels.append(f'<text x="45" y="{line_y + 4:.2f}" text-anchor="end">{level}</text>')
    x_labels = [
        f'<text x="{x(day):.2f}" y="195" text-anchor="middle">{day}</text>'
        for day in range(0, 91, 10)
    ]
    points = " ".join(f"{x(i):.2f},{y(value):.2f}" for i, value in enumerate(values, 1))
    dates = f"{days[0]:%b} {days[0].day}, {days[0].year} to {days[-1]:%b} {days[-1].day}, {days[-1].year}"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 240">
  <title>{sum(values)} GitHub contributions from {dates}</title>
  <defs>
    <linearGradient id="area" x2="0" y2="1">
      <stop stop-color="#a6b4d8" stop-opacity=".44"/>
      <stop offset="1" stop-color="#a6b4d8" stop-opacity=".04"/>
    </linearGradient>
  </defs>
  <rect x="1" y="1" width="878" height="238" rx="13" fill="#131d2c" stroke="#4b6079"/>
  <path d="{' '.join(horizontal)}" stroke="#8b9cbb" opacity=".24" stroke-dasharray="3 5" fill="none"/>
  <polygon points="{x(1):.2f},{bottom} {points} {right},{bottom}" fill="url(#area)"/>
  <polyline points="{points}" fill="none" stroke="#c6d3ed" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
  <g fill="#c3cde2" font-family="Segoe UI, Arial, sans-serif" font-size="15">
    {' '.join(y_labels)}
    {' '.join(x_labels)}
    <text x="56" y="221" font-size="13">{dates}</text>
    <text x="854" y="221" text-anchor="end" font-size="13">Elapsed days</text>
  </g>
</svg>
'''


if __name__ == "__main__":
    output = Path(__file__).resolve().parents[1] / "assets" / "activity-90-days.svg"
    days, values = fetch_window()
    output.write_text(render(days, values), encoding="utf-8")
    print(f"Rendered {len(values)} days with {sum(values)} contributions")
