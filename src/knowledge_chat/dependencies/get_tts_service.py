"""Dependency provider for the text-to-speech (TTS) service.

This module defines a factory function that initializes and returns
an instance of HuggingFaceTTSService using application settings.
"""

from knowledge_chat.config.settings import Settings
from knowledge_chat.domain.interfaces.tts_service import TTSService
from knowledge_chat.infrastructure.text_to_speech.huggingface_tts_service import \
    HuggingFaceTTSService


def get_tts_service() -> TTSService:
    """Create and return a configured TTS service instance.

    Loads the model configuration from environment variables using
    the Settings class.

    Returns:
        TTSService: An initialized text-to-speech service powered by
            a Hugging Face model.
    """
    settings = Settings()
    return HuggingFaceTTSService(settings=settings)
