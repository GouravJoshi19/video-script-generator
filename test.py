import instaloader
from moviepy.editor import VideoFileClip
import os
import logging
import shutil
import re

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
                self.loader.download_post(post, target="downloads")  # Save to 'downloads' folder
                print(f"Post downloaded successfully: {shortcode}")

            except Exception as e:
                print(f"Error downloading the post: {e}")

    @staticmethod
    def extract_shortcode(url):
        # Regex to extract shortcode from the URL
        match = re.search(r"instagram\.com/p/([A-Za-z0-9_-]+)/?", url)
        return match.group(1) if match else None



    def _process_video(self, post):
        """Process the video by downloading and extracting audio."""
        try:
            video_path = f"{self.temp_dir}/{post.shortcode}.mp4"
            self.loader.download_post(post, target=self.temp_dir)

            with VideoFileClip(video_path) as video:
                audio_path = self._extract_audio(video, post.shortcode)
                return {
                    'duration': video.duration,
                  
                    'audio_path': audio_path
                }
        except Exception as e:
            logging.error(f"Video processing failed for {post.shortcode}: {e}")
            return None

ig=InstagramScraper()
ig.authenticate("johncena2350","new password johncena2350")
profile_info,post_info=ig.fetch_creator_content("sid.content")
print(profile_info)
print(post_info)
ig.download_post(post_info['Post URL'])