import streamlit as st
import requests
from datetime import datetime, timedelta

# =========================
# CONFIG
# =========================
API_KEY = "AIzaSyDPYinjx7l7brS5GGkQBEbFgNIHqz-gRps"

YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"

# =========================
# STREAMLIT UI
# =========================
st.title("YouTube Viral Topics Tool")

days = st.number_input("Enter Days to Search (1-30):", min_value=1, max_value=30, value=5)

# Your broader keywords
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
    "matthew mcconaughey wisdom"
]

max_results_per_keyword = st.slider("Max results per keyword", 1, 10, 5)

if st.button("Search"):
    # Calculate publishedAfter based on days
    published_after = (datetime.utcnow() - timedelta(days=int(days))).isoformat("T") + "Z"
    st.write(f"Searching videos published after: `{published_after}`")

    for keyword in keywords:
        st.subheader(f"Keyword: {keyword}")
        params = {
            "part": "snippet",
            "q": keyword,
            "type": "video",
            "order": "viewCount",
            "publishedAfter": published_after,
            "maxResults": max_results_per_keyword,
            "key": API_KEY,
            "relevanceLanguage": "en"
        }

        try:
            response = requests.get(YOUTUBE_SEARCH_URL, params=params)
            data = response.json()

            items = data.get("items", [])
            if not items:
                st.write(f"❌ No videos found for keyword: **{keyword}**")
                continue

            # Optional: get extra stats (views/likes) using videos endpoint
            video_ids = ",".join(item["id"]["videoId"] for item in items)
            vid_params = {
                "part": "snippet,statistics",
                "id": video_ids,
                "key": API_KEY
            }
            vid_resp = requests.get(YOUTUBE_VIDEO_URL, params=vid_params).json()
            vid_items = {v["id"]: v for v in vid_resp.get("items", [])}

            for item in items:
                vid_id = item["id"]["videoId"]
                video = vid_items.get(vid_id, {})
                snippet = video.get("snippet", item["snippet"])
                stats = video.get("statistics", {})

                title = snippet.get("title", "No title")
                channel = snippet.get("channelTitle", "Unknown channel")
                url = f"https://www.youtube.com/watch?v={vid_id}"
                views = stats.get("viewCount", "N/A")

                st.markdown(f"**[{title}]({url})**")
                st.write(f"Channel: {channel}")
                st.write(f"Views: {views}")
                st.write("---")

        except Exception as e:
            st.error(f"Error for keyword '{keyword}': {e}")
