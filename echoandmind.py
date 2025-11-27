import streamlit as st
import requests
from datetime import datetime, timedelta

API_KEY = "AIzaSyDPYinjx7l7brS5GGkQBEbFgNIHqz-gRps"
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

st.title("YouTube API Debug Test")

test_keyword = st.text_input("Test keyword", "motivation")
days = st.number_input("Days back", min_value=1, max_value=30, value=5)

if st.button("Test YouTube search"):
    published_after = (datetime.utcnow() - timedelta(days=int(days))).isoformat("T") + "Z"

    params = {
        "part": "snippet",
        "q": test_keyword,
        "type": "video",
        "order": "viewCount",
        "maxResults": 5,
        "publishedAfter": published_after,
        "key": API_KEY
    }

    resp = requests.get(YOUTUBE_SEARCH_URL, params=params)
    st.write("Status code:", resp.status_code)

    data = resp.json()
    st.subheader("Raw API response:")
    st.json(data)

    if "error" in data:
        st.error("YouTube API error:")
        st.json(data["error"])
    else:
        items = data.get("items", [])
        st.write("Items length:", len(items))
