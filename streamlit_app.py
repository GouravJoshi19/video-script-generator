import streamlit as st
from src.scraper import get_product_details
from src.llm import LLM
from bs4 import BeautifulSoup
import requests
import os
from datetime import datetime
import shutil

# Set up the title for the app
st.set_page_config(page_title="Video Script Generator", layout="wide")
st.title("Video Script Generator")

# Create the working directory for storing files
WORK_DIR = "data"
if not os.path.exists(WORK_DIR):
    os.mkdir(WORK_DIR)

# Function to fetch product details from Amazon
def get_product_info(url, headers):
    try:
        webpage = requests.get(url, headers=headers)
        webpage.raise_for_status()  # Raise an error for invalid responses
        soup = BeautifulSoup(webpage.text, "html.parser")
        details = get_product_details()

        # Extract product details
        title = details.get_title(soup)
        price = details.get_price(soup)
        ratings = details.get_rating(soup)
        rating_count = details.get_rating_count(soup)
        info = details.get_description(soup)

        return {"title": title, "price": price, "ratings": ratings, "rating_count": rating_count, "info": info}
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching product details: {e}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None

def generate_review(details):
    llm=LLM()
    review=llm.generate_review(details)
    return review

def clear_work_dir():
    """Remove all files from the WORK_DIR directory."""
    for filename in os.listdir(WORK_DIR):
        file_path = os.path.join(WORK_DIR, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            st.error(f"Failed to delete {file_path}: {e}")

def save_review_to_file(review_text, product_title):
    """Saves the review text to a file in the WORK_DIR directory."""
    clear_work_dir()
    try:
        # Generate a filename based on the product title or timestamp
        sanitized_title = "".join(c for c in product_title if c.isalnum() or c in (" ", "-")).rstrip()
        filename = f"{sanitized_title.replace(' ', '_')}_review_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
        filepath = os.path.join(WORK_DIR, filename)

        # Save the review text to the file
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(review_text)

        # Notify the user of the saved file
        st.success(f"Review saved successfully to {filepath}")
    except Exception as e:
        st.error(f"Failed to save the review: {e}")

def main():

    if "details" not in st.session_state:
        st.session_state.details =[]

    url = st.text_input("Enter the product URL from Amazon")
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    if st.button("Submit"):
        with st.spinner("Fetching details from the site..."):
            st.session_state.details = get_product_info(url, HEADERS)
    
            if st.session_state.details:
                 # Save the details to session state
                st.success("Details have been fetched successfully")
                st.markdown(f"**Title**: {st.session_state.details['title']}")
                st.markdown(f"**Price**: {st.session_state.details['price']}")
                st.markdown(f"**Ratings**: {st.session_state.details['ratings']} ({st.session_state.details['rating_count']} reviews)")
                st.markdown(f"**Description**: {st.session_state.details['info']}")

    if st.button("Generate Review"):
            review=generate_review(st.session_state.details)
            save_review_to_file(review,product_title=st.session_state.details['title'])
            with st.spinner("Generating review"):
                st.subheader("Generated Review")
                st.write(review)

            # Add an option to download the review as a text file
            text_data = f"Generated Review:\n\n{review}"
            st.download_button(
                label="Download Review as Text",
                data=text_data,
                file_name="review.txt",
                mime="text/plain"
            )
if __name__=="__main__":
    main()