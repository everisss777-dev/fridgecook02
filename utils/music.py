
from urllib.parse import quote

def fixed_playlist_collection():
    # fixed example collections
    return {
        "korean": {
            "relaxed": {
                "spotify": "https://open.spotify.com/playlist/37i9dQZF1DXaVK0rV7b7vT",
                "youtube": "https://www.youtube.com/watch?v=8W27WwJw85o&list=PLk-k4YJd8lZ"
            },
            "party": {
                "spotify": "https://open.spotify.com/playlist/37i9dQZF1DX9tPFwDMOaN1",
                "youtube": "https://www.youtube.com/watch?v=7o2G6qH1w8A&list=PLpartyKR"
            }
        },
        "japanese": {
            "relaxed": {
                "spotify": "https://open.spotify.com/playlist/37i9dQZF1DX4zXL7jYu8DC",
                "youtube": "https://www.youtube.com/watch?v=JChillJP&list=PLjpop"
            }
        },
        "global": {
            "comfort": {
                "spotify": "https://open.spotify.com/playlist/37i9dQZF1DX3PFzdbtx1Us",
                "youtube": "https://www.youtube.com/watch?v=comfortmix&list=PLcomfort"
            },
            "focus": {
                "spotify": "https://open.spotify.com/playlist/37i9dQZF1DX4sWSpwq3LiO",
                "youtube": "https://www.youtube.com/watch?v=focusmix&list=PLfocus"
            },
            "energizing": {
                "spotify": "https://open.spotify.com/playlist/37i9dQZF1DX76Wlfdnj7AP",
                "youtube": "https://www.youtube.com/watch?v=energymix&list=PLenergy"
            }
        }
    }

def recommend_playlists(cuisines, mood, fixed):
    # return fixed first if available; also include generic search links
    results = []
    for c in cuisines:
        key = c.lower()
        if key in fixed and mood in fixed[key]:
            sel = fixed[key][mood]
            results.append({"title": f"{c.title()} • {mood}", "spotify": sel["spotify"], "youtube": sel["youtube"]})
    # add searches
    query = quote(f"{' '.join(cuisines)} {mood} cooking playlist")
    results.append({"title": "Search • Spotify", "spotify": f"https://open.spotify.com/search/{query}", "youtube": f"https://www.youtube.com/results?search_query={query}"})
    return results
