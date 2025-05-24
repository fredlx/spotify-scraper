# Project Scope
Spotify Scraper that extracts list of tracks from public spotify lists and saves the results into a csv/json file.

Data extracted:
- song names, 
- artists, 
- albuns,
- duration,
- date released, 
- date added 

# Considerations:
- Uses Spotify API (needs signin for credentials)
- Stores credentials in .env
- Fetch 100 tracks at a time (which is the max per request)
- Saves to data/ folder and names the files with playlist name
- Authentication methods: Client and OAuth
- Audio features are not implemented yet

# Usage:
'''bash
spotify-scraper "\<\list_url\>\" 

spotify-scraper "\<\list_url\>\" --use-oauth
''''

It is a work in progress.