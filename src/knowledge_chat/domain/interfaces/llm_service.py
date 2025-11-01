"""Large language model (LLM) service interface module.

This module defines the abstract LLMService interface, which specifies
the required method for text generation using a large language model.
"""

from abc import ABC, abstractmethod


class LLMService(ABC):
    """Abstract interface for large language model text generation."""

    @abstractmethod
    def generate(self, prompt: str, temperature: float = 0.7) -> str:
        """Generate text using a large language model.

        Args:
            prompt (str): The input text prompt to send to the model.
            temperature (float, optional): Sampling temperature that
                controls randomness and creativity of the output.
                Defaults to 0.7.

        Returns:
            str: The generated text response from the model.
        """
