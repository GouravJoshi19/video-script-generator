import streamlit as st
import instaloader
import logging
import datetime as dt
import pandas as pd
import re
import os

WORK_DIR='data'
# Logger setup
logging.basicConfig(level=logging.INFO)

# Time delay settings
TIME_DELAY = 60  # in seconds
if "last_scrape_time" not in st.session_state:
    st.session_state.last_scrape_time = None

# Instagram Scraper Class
class InstagramScraper:
    def __init__(self):
        self.loader = instaloader.Instaloader(download_videos=True)
        self.temp_dir = "temp_downloads"
        os.makedirs(self.temp_dir, exist_ok=True) 

    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate the user using provided Instagram credentials."""
        try:
            self.loader.login(username, password)
            return True
        except Exception as e:
            logging.error(f"Authentication failed: {e}")
            return False

    def fetch_creator_content(self, username: str, max_posts: int = 10):
        """Fetch content from a given Instagram creator's profile."""
        try:
            profile = instaloader.Profile.from_username(self.loader.context, username)
            profile_info = {
                "Username": profile.username,
                "Full Name": profile.full_name,
                "Biography": profile.biography,
                "Followers": profile.followers,
                "Following": profile.followees,
                "Posts Count": profile.mediacount,
            }

            # Gather recent post information
            posts_info = []
            for post in profile.get_posts():
                posts_info.append({
                    "Caption": post.caption or "No caption",
                    "Likes": post.likes,
                    "Comments": post.comments,
                    "Is Video": post.is_video,
                    "Views (if reel)": post.video_view_count if post.is_video else "N/A",
                    "Post URL": f"https://www.instagram.com/p/{post.shortcode}/",  # Construct URL
                })
                if len(posts_info) >= 10:  # Limit to 10 posts
                    break

                return profile_info, posts_info
        except Exception as e:
            logging.error(f"Content fetching failed: {e}")
            return None

    def download_post(self, url):
            try:
                # Extract the shortcode from the Instagram URL
                shortcode = self.extract_shortcode(url)
                if not shortcode:
                    raise ValueError("Invalid Instagram URL. Could not extract shortcode.")

                # Load the post using the shortcode
                post = instaloader.Post.from_shortcode(self.loader.context, shortcode)

                # Download the post
                self.loader.download_post(post, target=WORK_DIR)  # Save to 'downloads' folder
                print(f"Post downloaded successfully: {shortcode}")

            except Exception as e:
                print(f"Error downloading the post: {e}")

    @staticmethod
    def extract_shortcode(url):
        # Regex to extract shortcode from the URL
        match = re.search(r"instagram\.com/p/([A-Za-z0-9_-]+)/?", url)
        return match.group(1) if match else None

def main():
    scraper = InstagramScraper()

    # Input fields for Instagram login credentials
    instagram_username = str(st.text_input("Enter your Instagram username", type="default"))
    instagram_password = str(st.text_input("Enter your Instagram password", type="password"))

    if st.button("Authenticate"):
        with st.spinner("Authentication"):
            scraper.authenticate(instagram_username,instagram_password)
            st.success("Authentication Successful")

    # Input field for Instagram profile username
    target_username = str(st.text_input("Enter the Instagram profile username to scrape"))


    # Check if enough time has passed since the last scrape
    now = dt.datetime.now()
    if st.session_state.last_scrape_time:
        time_since_last_scrape = (now - st.session_state.last_scrape_time).total_seconds()
        if time_since_last_scrape < TIME_DELAY:
            remaining_time = TIME_DELAY - time_since_last_scrape
            st.warning(f"Please wait {int(remaining_time)} seconds before scraping again.")
            return

    # Define weights for engagement factors
    WEIGHTS = {"likes": 0.4, "comments": 0.4, "views": 0.2, "recency": 0.1}

    if st.button("Fetch Profile Details"):
        with st.spinner("Fetching profile details..."):
            # Update scrape timestamp
            st.session_state.last_scrape_time = dt.datetime.now()

            # Fetch profile details
            profile_info, posts_info = scraper.fetch_creator_content(target_username)

            if profile_info:
                st.success("Profile details fetched successfully!")
                st.subheader("Profile Information")
                for key, value in profile_info.items():
                    st.markdown(f"**{key}**: {value}")

                st.subheader("Recent Posts Information")
                if posts_info:
                    # Prepare a list for tabular data
                    post_data = []

                    # Add engagement and recency factors
                    for post in posts_info:
                        likes = post.get("Likes", 0)
                        comments = post.get("Comments", 0)
                        views = post.get("Views (if reel)", 0)
                        
                        # Calculate engagement score
                        engagement_score = (
                            views * WEIGHTS["views"]/
                            (likes * WEIGHTS["likes"]
                            + comments * WEIGHTS["comments"])
                        )

                       
                    
                        # Add data to the list
                        post_data.append({
                            "Caption": post.get("Caption", "No Caption"),
                            "Likes": likes,
                            "Comments": comments,
                            "Views (if reel)": views,
                            "Engagement Score": round(engagement_score, 2)
                        })

                    # Convert to a DataFrame for tabular display
                    posts_df = pd.DataFrame(post_data)

                    # Display the DataFrame in Streamlit
                    st.subheader("Tabular View of Posts")
                    st.dataframe(posts_df)

                    # Highlight the most successful post
                    best_post = posts_df.loc[posts_df["Engagement Score"].idxmax()]
                    scraper.download_post(best_post['Post URL'])
                    st.subheader("Most Successful Post")
                    st.write(f"**Caption**: {best_post['Caption']}")
                    st.write(f"**Overall Score**: {best_post['Engagement Score']:.2f}")
                    
                else:
                    st.info("No recent posts found for this profile.")
            else:
                st.error("Failed to fetch profile details. Please check the username.")

if __name__ == "__main__":
    main()
