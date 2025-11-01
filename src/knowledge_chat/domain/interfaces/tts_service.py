"""Text-to-speech service interface module.

This module defines the abstract TTSService interface, which specifies
the required methods for text-to-speech synthesis implementations.
"""

from abc import ABC, abstractmethod


class TTSService(ABC):
    """Abstract interface for text-to-speech (TTS) services."""

    @abstractmethod
    def speak(self, text: str, output_path: str) -> str:
        """Convert text into speech and save it as an audio file.

        Args:
            text (str): The input text to synthesize into speech.
            output_path (str): Path where the generated audio file
                should be saved.

        Returns:
            str: The path to the saved audio file.
        """
