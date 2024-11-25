import streamlit as st
import pyttsx3
import os

# Set up the paths for directories
WORK_DIR = "data"
SCRIPTS_DIR = os.path.join(WORK_DIR, "Scripts")
AUDIO_DIR = os.path.join(WORK_DIR, "generated_audio")

# Ensure the generated audio directory exists
os.makedirs(AUDIO_DIR, exist_ok=True)

# Initialize the TTS engine
engine = pyttsx3.init()

def setup_voice():
    """Set the voice to male if available, else use default voice."""
    voices = engine.getProperty("voices")
    for voice in voices:
        if "male" in voice.name.lower():  # Check for a male voice
            engine.setProperty("voice", voice.id)
            break
    else:
        st.warning("No male voice found. Using default voice.")

def generate_audio_from_script(script_file):
    """Generate audio file from the script text."""
    script_path = os.path.join(SCRIPTS_DIR, script_file)

    # Read the script content
    with open(script_path, "r", encoding="utf-8") as file:
        text = file.read()

    # Generate the output audio filename
    base_name = os.path.splitext(script_file)[0]
    audio_file_path = os.path.join(AUDIO_DIR, f"{base_name}.mp3")

    # Save the audio file
    engine.save_to_file(text, audio_file_path)
    engine.runAndWait()

    return audio_file_path


def process_scripts():
    """Process each script file in the Scripts directory and generate audio."""
    if not os.path.exists(SCRIPTS_DIR):
        st.error(f"Scripts directory not found: {SCRIPTS_DIR}")
        return

    script_files = [f for f in os.listdir(SCRIPTS_DIR) if f.endswith(".txt")]

    if not script_files:
        st.warning("No script files found in the Scripts directory.")
        return

    st.subheader("Processing Scripts to Audio")

    for script_file in script_files:
        with st.spinner(f"Generating audio for {script_file}..."):
            audio_file_path = generate_audio_from_script(script_file)
            st.success(f"Audio generated: {audio_file_path}")
            st.audio(audio_file_path, format="audio/mp3")
            st.markdown(f"**Audio File**: {audio_file_path}")

def main():
    st.title("Script to Audio Generator")

    # Setup voice
    setup_voice()

    # Process scripts
    if st.button("Generate Audio from Scripts"):
        process_scripts()

    # Show generated audio files
  

if __name__ == "__main__":
    main()
