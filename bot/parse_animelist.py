import requests
from pocketbase import PocketBase

HEADERS = {
    "User-Agent": "AniParseBot/1.0"
}

# --- PocketBase config ---
pb = PocketBase("http://127.0.0.1:8090")  # your PocketBase URL
pb.admins.auth_with_password("mihail.gm.kms@gmail.com", "NqJVRqc5n*?q)Xb")  # admin login

page = 50
# --- AniLiberty API endpoint ---
url = f"https://anilibria.top/api/v1/anime/releases/latest?limit={page}"  # check doc for exact endpoint
base_url = "https://anilibria.top"

resp = requests.get(url)
resp.raise_for_status()
data = resp.json()

for a in data:
    if not a.get("is_ongoing"):
        continue

    # Fetch rating from Shikimori
    try:
        search_url = f"https://shikimori.one/api/animes?search={a["name"].get("english", "")}&status=ongoing"
        resp = requests.get(search_url, headers=HEADERS)
        resp.raise_for_status()
        shikimori_data = resp.json()
        score = shikimori_data[0].get('score')
    except Exception:
        ...
    print(score)

    rec = {
        "title": a["name"]["main"],
        "titleEn": a["name"].get("english") or "",
        "altName": a["name"].get("alternative") or "",
        "alias": a.get("alias", ""),
        "description": a.get("description", ""),
        "type": a.get("type", {}).get("value", ""),
        "episodeTotal": a.get("episodes_total", 0),
        "episodeCaptured": a.get("episodes_total", 0),  # или количество вышедших
        "isOngoing": a.get("is_ongoing", False),
        "year": a.get("year", 0),
        "season": a.get("season", {}).get("description", ""),
        "avDuration": str(a.get("average_duration_of_episode", "")),
        "linkToView": f'https://anilibria.top/anime/releases/release/{a.get("alias","")}/episodes',
        "ageRating": a.get("age_rating", {}).get("label", ""),
        "posterScr": base_url + a.get("poster", {}).get("src", ""),
        "posterOptScr": base_url + a.get("poster", {}).get("optimized", {}).get("src", ""),
        "generes": [g["name"] for g in a.get("genres", [])],
        "favCount": a.get("added_in_users_favorites", 0),
        "publishDay": a.get("publish_day", {}).get("value", None),
        "pubDayDesc": a.get("publish_day", {}).get("description", ""),
        "score": score,  # Add score from Shikimori
    }

    try:
        existing = None
        if rec["alias"]:
            try:
                existing = pb.collection("titles").get_first_list_item(f'alias="{rec["alias"]}"')
            except Exception as e:
                if hasattr(e, 'status') and "404" in str(e):
                    existing = None
                else:
                    raise

        if existing:
            pb.collection("titles").update(existing.id, rec)
            print("Updated:", rec["title"])
        else:
            pb.collection("titles").create(rec)
            print("Added:", rec["title"])

    except Exception as e:
        print("Error adding/updating", rec["title"], e)
