"""Hugging Face text-to-speech service using the Inference API."""

from huggingface_hub import InferenceClient

from knowledge_chat.config.settings import Settings
from knowledge_chat.domain.interfaces.tts_service import TTSService


class HuggingFaceTTSService(TTSService):
    """Text-to-speech using Hugging Face Inference API (cloud)."""

    def __init__(self, settings: Settings) -> None:
        """Initialize the Inference Client.

        Args:
            settings (Settings): Application settings
        """
        self.model_name = settings.hf_tts_model
        self.client = InferenceClient(model=self.model_name, token=settings.hf_token)

    def speak(self, text: str, output_path: str) -> str:
        """Convert text into speech and save as audio file.

        Args:
            text (str): The text to synthesize.
            output_path (str): File path to save output audio.

        Returns:
            str: The saved audio file path.
        """
        audio_bytes = self.client.text_to_speech(text)

        with open(output_path, "wb") as f:
            f.write(audio_bytes)

        return output_path
