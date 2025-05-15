# main.py

from audioSample import record_audio
from voiceRecognition import recognize_speech, is_matching_speaker, get_reference_embedding
from threatDetection import is_threat
from audioAlert import play_audio
from sendMessage import notify_user

import os

def main():
    # 1. Record audio sample
    audio_file = record_audio(duration=5, sample_rate=44100, folder='audio_samples')

    # 2. Speech recognition
    recognized_text = recognize_speech(audio_file)
    print(f"Recognized Text: {recognized_text}")

    # 3. Speaker verification
    reference_audio = "reference_person.wav"  # Ensure this exists
    if not os.path.exists(reference_audio):
        print("Reference audio file for speaker verification not found.")
        return
    ref_embedding = get_reference_embedding(reference_audio)
    is_speaker = is_matching_speaker(audio_file, ref_embedding)
    print(f"Speaker match: {'Yes' if is_speaker else 'No'}")

    # 4. Threat detection
    threat_detected = is_threat(recognized_text)
    print(f"Threat detected: {'Yes' if threat_detected else 'No'}")

    # 5. If threat detected and speaker matches, trigger alert and notification
    if threat_detected and is_speaker:
        # Play audio alert
        alert_folder = "AlertMessage"
        alert_file = next((f for f in os.listdir(alert_folder) if f.endswith(".mp3")), None)
        if alert_file:
            play_audio(os.path.join(alert_folder, alert_file))
        else:
            print("No alert audio file found.")

        # Send notifications
        notify_user('sms', '+33638925598', 'ALERT: John Doe is in Danger!')
        notify_user('email', 'recipient@example.com', 'Threat Detected', f"Threat detected in audio: {recognized_text}")

if __name__ == "__main__":
    main()
