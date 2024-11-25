import moviepy.editor as mp
import whisper
import os

WORK_DIR = "data"

class process_audio:
    def extract_audio(self, path):
        # Ensure the 'extracted_audio' directory exists within WORK_DIR
        extracted_audio_dir = os.path.join(WORK_DIR,"extracted_audio")
        os.makedirs(extracted_audio_dir, exist_ok=True)

        # Generate audio file path in the 'extracted_audio' directory
        base_name = os.path.splitext(os.path.basename(path))[0]
        audio_file = os.path.join(extracted_audio_dir, f"{base_name}.mp3")

        # Extract audio and save it to the target directory
        clip = mp.VideoFileClip(path)
        clip.audio.write_audiofile(audio_file)

        return f"{base_name}.mp3"
    
    def transcribe_with_whisper(self, audio_file):
        # Directories
        extracted_audio_dir = os.path.join(WORK_DIR, "extracted_audio")
        transcribed_text_dir = os.path.join(WORK_DIR, "transcribed_text")
        os.makedirs(transcribed_text_dir, exist_ok=True)

        # Check if the audio file is in the 'extracted_audio' directory
        audio_file_path = os.path.join(extracted_audio_dir, audio_file)
        if not os.path.exists(audio_file_path):
            raise FileNotFoundError(f"Audio file '{audio_file}' not found in {extracted_audio_dir}.")

        # Load Whisper model and transcribe
        model = whisper.load_model("base")
        result = model.transcribe(audio_file_path)

        # Save transcription to 'transcribed_text' directory
        base_name = os.path.splitext(os.path.basename(audio_file))[0]
        output_file_path = os.path.join(transcribed_text_dir, f"{base_name}.txt")
        with open(output_file_path, "w", encoding="utf-8") as f:
            f.write(result['text'])

        return output_file_path  

def main():
    audio=process_audio()
    audio.extract_audio('./data/Video-7.mp4')
    audio.transcribe_with_whisper('./Video-7.mp3')
if __name__=="__main__":
    main()