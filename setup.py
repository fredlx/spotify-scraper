from setuptools import setup

setup(
    name="spotify_playlist_scraper",
    version="0.1",
    py_modules=["spotify_scraper"],
    install_requires=["spotipy", "python-dotenv"],
    entry_points={
        "console_scripts": [
            "spotify-scraper=spotify_scraper:main"
        ],
    },
)