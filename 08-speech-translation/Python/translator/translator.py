from dotenv import load_dotenv
import os
import azure.cognitiveservices.speech as speechsdk

def main():
    try:
        global translation_config

        # Load config
        load_dotenv()
        cog_key = os.getenv('COG_SERVICE_KEY')
        cog_region = os.getenv('COG_SERVICE_REGION')

        # Configure translation
        translation_config = speechsdk.translation.SpeechTranslationConfig(
            subscription=cog_key,
            region=cog_region
        )

        # Default input language (speech you talk into the mic)
        translation_config.speech_recognition_language = "en-US"

        # Supported target languages
        translation_config.add_target_language("fr")
        translation_config.add_target_language("es")
        translation_config.add_target_language("hi")

        # Loop for user
        targetLanguage = ''
        while targetLanguage != 'quit':
            targetLanguage = input(
                "\nEnter a target language\n fr = French\n es = Spanish\n hi = Hindi\n Enter anything else to stop\n"
            ).lower()

            if targetLanguage in translation_config.target_languages:
                Translate(targetLanguage)
            else:
                targetLanguage = 'quit'

    except Exception as ex:
        print("Error:", ex)


def Translate(targetLanguage):
    # Audio config: microphone
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

    # Create recognizer with translation
    recognizer = speechsdk.translation.TranslationRecognizer(
        translation_config=translation_config,
        audio_config=audio_config
    )

    print(f"\nSpeak now (will translate to {targetLanguage})...")

    # Recognize one utterance
    result = recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.TranslatedSpeech:
        print("\nRecognized (en-US):", result.text)
        print(f"Translated ({targetLanguage}):", result.translations[targetLanguage])

        # Synthesize translation (text -> speech)
        speech_config = speechsdk.SpeechConfig(
            subscription=os.getenv('COG_SERVICE_KEY'),
            region=os.getenv('COG_SERVICE_REGION')
        )
        speech_config.speech_synthesis_language = targetLanguage
        speech_synth = speechsdk.SpeechSynthesizer(speech_config=speech_config)
        speech_synth.speak_text_async(result.translations[targetLanguage]).get()

    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized")
    else:
        print("Error:", result.reason)


if __name__ == "__main__":
    main()