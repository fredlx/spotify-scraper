import os
import re
import csv
import json
from typing import List, Dict
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

def load_credentials():
    load_dotenv()
    return {
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "redirect_uri": os.getenv("REDIRECT_URI"),
    }

def get_spotify_session(use_oauth: bool, creds: Dict) -> spotipy.Spotify:
    if use_oauth:
        auth_manager = SpotifyOAuth(
            client_id=creds["client_id"],
            client_secret=creds["client_secret"],
            redirect_uri=creds["redirect_uri"],
            scope="playlist-read-private",
            open_browser=False
        )
    else:
        auth_manager = SpotifyClientCredentials(
            client_id=creds["client_id"],
            client_secret=creds["client_secret"]
        )
    return spotipy.Spotify(auth_manager=auth_manager)

def extract_playlist_id(url: str) -> str:
    return url.split("?")[0].split("/")[-1]

def safe_filename(name: str) -> str:
    return re.sub(r"[^\w\-_.]", "_", name.strip())

def get_all_tracks(session: spotipy.Spotify, playlist_id: str) -> List[Dict]:
    tracks, offset = [], 0
    while True:
        resp = session.playlist_tracks(playlist_id, offset=offset, limit=100)
        items = resp.get("items", [])
        if not items:
            break
        tracks.extend(items)
        offset += len(items)
    return tracks

def transform_tracks(tracks_raw: List[Dict]) -> List[Dict]:
    output = []
    for item in tracks_raw:
        t = item.get("track")
        if not t:
            continue
        output.append({
            "track": t["name"],
            "artist": ", ".join(a["name"] for a in t["artists"]),
            "album": t["album"]["name"],
            "release_date": t["album"]["release_date"],
            "added_at": item.get("added_at", "")[:10],
            "duration_ms": t["duration_ms"],
        })
    return output

def save_json(data: List[Dict], path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def save_csv(data: List[Dict], path: str):
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def run(playlist_url: str, use_oauth: bool = False):
    creds = load_credentials()
    session = get_spotify_session(use_oauth, creds)
    playlist_id = extract_playlist_id(playlist_url)
    playlist = session.playlist(playlist_id)
    playlist_name = safe_filename(playlist["name"])

    tracks_raw = get_all_tracks(session, playlist_id)
    data = transform_tracks(tracks_raw)

    os.makedirs("data", exist_ok=True)
    save_json(data, f"data/{playlist_name}.json")
    save_csv(data, f"data/{playlist_name}.csv")

    print(f"Exported to: data/{playlist_name}.csv / .json")
    
    
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Export Spotify playlist data.")
    parser.add_argument("playlist_link", help="Spotify playlist URL")
    parser.add_argument("--use-oauth", action="store_true", help="Use OAuth instead of Client Credentials")
    args = parser.parse_args()
    run(args.playlist_link, use_oauth=args.use_oauth)
    

if __name__ == "__main__":
    main()