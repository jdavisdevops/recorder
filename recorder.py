import pyaudio
import wave
import whisper
import pyperclip
import threading


# Function to record audio
def record_audio(filename, rate=16000, channels=1):
    p = pyaudio.PyAudio()

    stream = p.open(
        format=pyaudio.paInt16,
        channels=channels,
        rate=rate,
        input=True,
        frames_per_buffer=1024,
    )

    frames = []

    def record():
        print("Recording... Press Enter to stop.")
        while not stop_recording.is_set():
            data = stream.read(1024)
            frames.append(data)

        print("Finished recording.")
        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(filename, "wb")
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(rate)
        wf.writeframes(b"".join(frames))
        wf.close()

    stop_recording = threading.Event()
    thread = threading.Thread(target=record)
    thread.start()

    input()  # Wait for the user to press Enter
    stop_recording.set()
    thread.join()


# Function to transcribe audio using Whisper
def transcribe_audio(filename):
    model = whisper.load_model("base")
    result = model.transcribe(filename)
    return result["text"]


# Function to save transcript to a text file
def save_transcript_to_file(transcript, filename):
    with open(filename, "w") as file:
        file.write(transcript)


# Record audio
audio_filename = "audio.wav"
record_audio(audio_filename)

# Transcribe audio
transcript = transcribe_audio(audio_filename)
print("Transcript:", transcript)

# Copy transcript to clipboard
pyperclip.copy(transcript)
print("Transcript copied to clipboard.")

# Save transcript to a text file
transcript_filename = "transcript.txt"
save_transcript_to_file(transcript, transcript_filename)
print(f"Transcript saved to {transcript_filename}.")

import os

os.remove(audio_filename)
print(f"Deleted the audio file: {audio_filename}")
