"""Gom tin tuyển dụng mới qua Tavily Search API, ghi vào jobs.json.
Cần biến môi trường: TAVILY_API_KEY."""
import json, os, re, urllib.parse, urllib.request
from datetime import date, timedelta
from urllib.parse import urlparse

KEYWORDS = ["AI", "AIoT", "IoT", "Embedded", "Điện tử", "Firmware", "Edge AI", "Computer Vision"]
HCM = re.compile(r"hồ chí minh|ho chi minh|hcm|sài gòn|saigon|thủ đức", re.I)
FRESH = re.compile(r"fresher|intern|junior|thực tập|new grad", re.I)
KEEP_DAYS = 30
KEY = os.environ["TAVILY_API_KEY"]
DOMAINS = ["topcv.vn", "itviec.com", "topdev.vn", "vietnamworks.com", "joboko.com", "linkedin.com", "careerviet.vn", "123job.vn", "jobsgo.vn", "fptjobs.com", "vn.indeed.com", "jobsgo.vn"]
today = date.today()

def search(q):
    body = json.dumps({"query": q, "max_results": 10, "time_range": "week", "search_depth": "basic",
                       "include_domains": DOMAINS}).encode()
    req = urllib.request.Request("https://api.tavily.com/search", data=body,
        headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r).get("results", [])

data = json.load(open("jobs.json", encoding="utf-8"))
jobs = data["jobs"]
by_url = {j["u"]: j for j in jobs}

for kw in KEYWORDS:
    try:
        items = search(f"{kw} tuyển dụng Hồ Chí Minh")
    except Exception as e:
        print("Lỗi với", kw, e); continue
    for it in items:
        url, title, snip = it["url"], it.get("title", ""), it.get("content", "")
        text = f"{title} {snip}"
        if url in by_url or not HCM.search(text):
            continue
        tags = [k for k in KEYWORDS if k.lower() in text.lower()] or [kw]
        j = {"t": title[:120], "c": "", "loc": "Hồ Chí Minh", "lv": "fresher" if FRESH.search(text) else "mid",
             "tg": tags, "u": url, "src": urlparse(url).netloc.replace("www.", ""), "n": snip[:200],
             "first_seen": today.isoformat(), "isNew": True}
        jobs.append(j); by_url[url] = j

cut = (today - timedelta(days=KEEP_DAYS)).isoformat()
out = []
for j in jobs:
    if not j.get("manual"):
        if j.get("first_seen", "9999") < cut:
            continue
        j["isNew"] = j.get("first_seen") >= (today - timedelta(days=2)).isoformat()
    out.append(j)

data["jobs"], data["updated"] = out, today.isoformat()
json.dump(data, open("jobs.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("Tổng", len(out), "tin")
