import streamlit as st
import requests
import logging

# Configure logging
logging.basicConfig(filename='scrapper.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Function to fetch images from Google using SerpAPI
def fetch_images(query, api_key):
    try:
        params = {
            "engine": "google",
            "q": query,
            "tbm": "isch",
            "api_key": api_key,
        }
        response = requests.get("https://serpapi.com/search", params=params)
        
        if response.status_code == 200:
            results = response.json()
            return [img['link'] for img in results.get('images_results', [])[:10]]
        else:
            logging.error(f"Error fetching images: {response.status_code} - {response.text}")
            st.error("Error fetching images. Please check your API key and try again.")
            return []
    except Exception as e:
        logging.exception("Exception occurred while fetching images")
        st.error("An unexpected error occurred. Please try again later.")
        return []

# Streamlit App
st.title("Image Scraper")

# User input for image search
query = st.text_input("What kind of images do you want to scrape?", "")

# Your SerpAPI Key (Make sure to keep this secure)
api_key = st.secrets['general']["serpapi_api_key"]  # Store your API key in Streamlit secrets

if st.button("Search"):
    if query:
        with st.spinner("Fetching images..."):
            images = fetch_images(query, api_key)
            if images:
                for index, img_url in enumerate(images):
                    st.image(img_url, use_column_width=True)
                    st.download_button(
                        "Download Image", 
                        img_url, 
                        "image.jpg", 
                        key=f"download_{index}"  # Unique key for each button
                    )
            else:
                st.error("No images found.")
    else:
        st.warning("Please enter a search term.")

# Log information when the app is run
logging.info("App has been run with query: %s", query)
