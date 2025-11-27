import streamlit as st
import requests

# =========================
# CONFIG
# =========================
API_KEY = "AIzaSyDPYinjx7l7brS5GGkQBEbFgNIHqz-gRps"
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

# =========================
# LOW-QUOTA SEARCH FUNCTION
# =========================
def search_youtube_low_quota(keyword: str, max_results: int = 3):
    """
    One cheap search call per keyword.
    No stats, no publishedAfter filter.
    """
    params = {
        "part": "snippet",
        "q": keyword,
        "type": "video",
        "order": "relevance",   # cheaper + good enough
        "maxResults": max_results,
        "key": API_KEY
    }

    resp = requests.get(YOUTUBE_SEARCH_URL, params=params)
    data = resp.json()

    # Explicitly handle API errors (quotaExceeded, etc.)
    if "error" in data:
        msg = data["error"].get("message", "Unknown API error")
        raise RuntimeError(msg)

    return data.get("items", [])


# =========================
# STREAMLIT UI
# =========================
st.title("YouTube Viral Topics Tool (Low-Quota Mode)")

st.write(
    "This version is optimized to use **very little YouTube quota**.\n"
    "Tip: keep keywords per run small (3–8)."
)

# Put your own broader keywords here
keywords = [
    "motivational podcast clip",
    "deep conversation moments",
    "introspective podcast highlights",
    "emotional podcast short",
    "philosophical podcast clip",
    "life advice podcast moment",
    "rare podcast wisdom",
    "underrated inspirational podcast",
    "powerful interview moment",
    "joe rogan life advice",
    "theo von emotional story",
    "matthew mcconaughey wisdom",
]

max_results = st.slider("Max results per keyword", 1, 10, 3)

# Let user choose how many keywords to run this session
num_keywords = st.slider(
    "How many keywords to search this run?",
    min_value=1,
    max_value=min(len(keywords), 10),  # hard cap for safety
    value=5,
)

st.write(
    f"Selected first **{num_keywords}** keywords from your list for this run "
    "(to protect your daily quota)."
)

if st.button("Run search"):
    for kw in keywords[:num_keywords]:
        st.subheader(f"Keyword: {kw}")
        try:
            items = search_youtube_low_quota(kw, max_results=max_results)
        except RuntimeError as e:
            st.error(f"API error for '{kw}': {e}")
            break  # stop further calls if quotaExceeded or other error
        except Exception as e:
            st.error(f"Unexpected error for '{kw}': {e}")
            continue

        if not items:
            st.write(f"❌ No videos found for keyword: **{kw}**")
            continue

        for item in items:
            vid_id = item["id"]["videoId"]
            snippet = item["snippet"]
            title = snippet.get("title", "No title")
            channel = snippet.get("channelTitle", "Unknown channel")
            url = f"https://www.youtube.com/watch?v={vid_id}"

            st.markdown(f"**[{title}]({url})**")
            st.write(f"Channel: {channel}")
            st.write("---")
