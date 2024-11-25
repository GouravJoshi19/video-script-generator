
# Video Script Generator

This project is a Video Script Generator that combines web scraping, natural language processing (NLP), and text-to-speech technologies to create personalized video scripts for Instagram posts. By integrating Amazon product insights and Instagram user data, it produces engaging and relevant scripts tailored to the user.

## Features

### 1. Amazon Product Review Generation
- **Accepts an Amazon product URL**.
- Scrapes product details such as:
  - Title
  - Price
  - Ratings and reviews
  - Description
- Uses **Cohere LLM API** to generate personalized product reviews based on the scraped information.

### 2. Instagram User Insights
- **Accepts an Instagram username**.
- Scrapes details including:
  - Username, Full Name, Biography
  - Followers and Following count
  - Total posts
- Fetches the **10 most recent posts** and determines the most famous post using engagement metrics:
  - Engagement Metric = Views / (Likes + Comments)

### 3. Audio and Text Extraction
- Downloads the most famous Instagram post (video or reel).
- Extracts **audio** from the post.
- Transcribes the audio into text using **OpenAI's Whisper model**.

### 4. Instagram Post Script Generation
- Combines:
  - Product reviews generated using Amazon data.
  - Transcribed text from the Instagram post.
- Uses **Cohere LLM API** to generate a cohesive and engaging Instagram post script.

### 5. Audio Generation
- Converts the generated script into **audio** using **gTTS (Google Text-to-Speech)**.
- Currently uses a default voice due to limitations in voice cloning technology.

## Future Improvements

- **Voice Cloning**: Integrate advanced voice cloning technologies to replicate the Instagram account’s voice. Explore models like **Wav2Lip** for realistic voice synthesis.
- **Reel Creation**: Develop functionality to generate Instagram reels by synchronizing the script audio with visuals from the Instagram post.

## Requirements

### Dependencies
- **Python 3.8+**
  
Libraries:
- `streamlit`
- `cohere`
- `instaloader`
- `moviepy`
- `whisper`
- `gtts`
- `beautifulsoup4`
- `requests`
- `pandas`
- `shutil`
- `os`

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/GouravJoshi19/video-script-generator.git
   cd video-script-generator
   ```

2. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Obtain API Keys**:
   - **Cohere API Key** for text generation.
   - **Instagram session ID** for authenticated scraping.
   - **Whisper model** for transcription (install via whisper).


## Usage

### Running the Streamlit App

1. **Start the app**:
   ```bash
   streamlit run app.py
   ```

2. **Navigate to the Amazon Product Review page**:
   - Enter the Amazon product URL to generate and view personalized product reviews.

3. **Navigate to the Instagram Insights page**:
   - Enter the Instagram username to fetch user details and download the most famous post.
   - Extract and transcribe audio from the post.

4. **View and download**:
   - Generated reviews and scripts.
   - Extracted audio and transcribed text.

5. **Sequence of Operations**:
   - Generate Reviews: Start by providing the Amazon product URL to generate product reviews.
   - Instagram User Insights: After reviews are generated, provide the Instagram username to fetch insights and transcribe the most famous post's audio.
   - Generate Script and Audio: Once the data is processed, generate the final script and audio for the Instagram post.

## Challenges

### 1. **Voice Cloning**
   - Currently using default voices provided by gTTS.
   - Matching the generated script’s voice to the Instagram account’s voice remains a work in progress.

### 2. **Reel Generation**
   - Generating a video reel with synchronized audio and visuals is computationally intensive.
   - **Wav2Lip** model could not run effectively on current hardware.

### 3. **Scraping Limitations**
   - Both Amazon and Instagram impose limitations on scraping activities after a certain number of requests per day. This can prevent        further scraping after exceeding the allowed requests, requiring either session resets or wait periods before scraping can continue. This challenge is a limitation when trying to fetch large amounts of data in a short time.
### 4. **Interface and Error Handling**
   - The user interface and error handling mechanisms are still a work in progress. Improvements are needed to make the app more     user-friendly and handle errors more gracefully during the execution of different tasks.

## Contribution

Contributions are welcome! Feel free to open issues or submit pull requests to enhance features or resolve limitations.
