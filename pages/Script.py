import streamlit as st
import instaloader
import time
import logging
from datetime import datetime, timedelta
import os

# Logger setup
logging.basicConfig(level=logging.INFO)

# Time delay settings
TIME_DELAY = 60  # in seconds
if "last_scrape_time" not in st.session_state:
    st.session_state.last_scrape_time = None

# Instagram Scraper Class
class InstagramScraper:
    def __init__(self):
        self.loader = instaloader.Instaloader()

    def authenticate(self, username: str, password: str):
        """Authenticate the user using provided Instagram credentials."""
        try:
            self.loader.login(username, password)
            logging.info("Authentication successful!")
            st.success("Authentication successful!")
        except Exception as e:
            logging.error(f"Authentication failed: {e}")
            st.error("Failed to authenticate. Please check your credentials.")

    def fetch_profile_info(self, username: str):
        """Fetch details of the Instagram profile."""
        print("started")
        try:
            profile = instaloader.Profile.from_username(self.loader.context, username)
            print(profile)
            # Gather basic profile information
            profile_info = {
                "Username": profile.username,
                "Full Name": profile.full_name,
                "Biography": profile.biography,
                "Followers": profile.followers,
                "Following": profile.followees,
                "Posts Count": profile.mediacount,
            }
            st.write(profile_info)
            # Gather recent post information
            posts_info = []
            for post in profile.get_posts():
                posts_info.append({
                    "Caption": post.caption or "No caption",
                    "Likes": post.likes,
                    "Comments": post.comments,
                    "Is Video": post.is_video,
                    "Views (if reel)": post.video_view_count if post.is_video else "N/A",
                })
                if len(posts_info) >= 10:  # Limit to 10 posts
                    break

            return profile_info, posts_info

        except Exception as e:
            logging.error(f"Failed to fetch profile details for {username}: {e}")
            st.error("Failed to fetch profile details. Please check the username.")
            return None, None


def main():
    scraper = InstagramScraper()

    # Input fields for Instagram login credentials
    instagram_username = st.text_input("Enter your Instagram username", type="default")
    instagram_password = st.text_input("Enter your Instagram password", type="password")

    if st.button("Login"):
        with st.spinner("Authenticating..."):
            scraper.authenticate(instagram_username, instagram_password)

    # Input field for Instagram profile username
    target_username = st.text_input("Enter the Instagram profile username to scrape")

    # Check if enough time has passed since the last scrape
    now = datetime.now()
    if st.session_state.last_scrape_time:
        time_since_last_scrape = (now - st.session_state.last_scrape_time).total_seconds()
        if time_since_last_scrape < TIME_DELAY:
            remaining_time = TIME_DELAY - time_since_last_scrape
            st.warning(f"Please wait {int(remaining_time)} seconds before scraping again.")
            return

    if st.button("Fetch Profile Details"):
        with st.spinner("Fetching profile details..."):
            # Update scrape timestamp
            st.session_state.last_scrape_time = datetime.now()

            # Fetch profile details
            profile_info, posts_info = scraper.fetch_profile_info(target_username)

            if profile_info:
                st.success("Profile details fetched successfully!")
                st.subheader("Profile Information")
                for key, value in profile_info.items():
                    st.markdown(f"**{key}**: {value}")

                st.subheader("Recent Posts Information")
                if posts_info:
                    for idx, post in enumerate(posts_info, start=1):
                        st.markdown(f"**Post {idx}:**")
                        st.markdown(f"- **Caption**: {post['Caption']}")
                        st.markdown(f"- **Likes**: {post['Likes']}")
                        st.markdown(f"- **Comments**: {post['Comments']}")
                        st.markdown(f"- **Is Video**: {'Yes' if post['Is Video'] else 'No'}")
                        st.markdown(f"- **Views**: {post['Views (if reel)']}")
                        st.markdown("---")
                else:
                    st.info("No recent posts found for this profile.")

            else:
                st.error("Failed to fetch profile details. Please check the username.")