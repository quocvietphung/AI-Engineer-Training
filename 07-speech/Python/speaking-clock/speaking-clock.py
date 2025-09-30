from dotenv import load_dotenv
from datetime import datetime
import os
import azure.cognitiveservices.speech as speechsdk

# Hàm chính
def main():
    try:
        global speech_config

        # Load cấu hình từ .env
        load_dotenv()
        cog_key = os.getenv('COG_SERVICE_KEY')
        cog_region = os.getenv('COG_SERVICE_REGION')

        # Cấu hình dịch vụ Speech
        speech_config = speechsdk.SpeechConfig(subscription=cog_key, region=cog_region)

        # Nhận giọng nói
        command = TranscribeCommand()

        # Nếu người dùng nói đúng "What time is it?"
        if command.lower() == 'what time is it?':
            TellTime()

    except Exception as ex:
        print(ex)


# Hàm Speech-to-Text (nhận giọng nói)
def TranscribeCommand():
    command = ''

    # Dùng micro làm nguồn input
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config,
        audio_config=audio_config
    )

    print("Say something...")

    # Nhận một câu
    result = speech_recognizer.recognize_once()

    # Xử lý kết quả
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        command = result.text
        print("You said: {}".format(command))
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation.reason))

    return command


# Hàm Text-to-Speech (trả lời giờ hiện tại)
def TellTime():
    now = datetime.now()
    response_text = 'The time is {}:{:02d}'.format(now.hour, now.minute)

    # Dùng loa mặc định
    audio_config = speechsdk.audio.AudioConfig(use_default_speaker=True)
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=audio_config
    )

    # Nói câu trả lời
    speech_synthesizer.speak_text_async(response_text).get()

    # In ra console
    print(response_text)


if __name__ == "__main__":
    main()