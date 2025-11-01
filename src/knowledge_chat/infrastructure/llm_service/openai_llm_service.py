"""OpenAI-based large language model (LLM) service implementation.

This module defines the OpenAILLMService class, which provides an
implementation of the LLMService interface using the OpenAI Chat API.
"""

from openai import OpenAI

from knowledge_chat.config.settings import Settings
from knowledge_chat.domain.interfaces.llm_service import LLMService


class OpenAILLMService(LLMService):
    """Implementation of LLMService using the OpenAI Chat API."""

    def __init__(self, settings: Settings) -> None:
        """Initialize the OpenAI client.

        Args:
            api_key (str): The API key used for authenticating
                OpenAI requests.
            model (str, optional): The model name used for chat
                completions. Defaults to "gpt-4o-mini".
        """
        self.client = OpenAI(
            base_url=settings.openai_base_url,
            api_key=settings.openai_api_key,
        )
        self.model = settings.openai_model

    def generate(self, prompt: str, temperature: float = 0.7) -> str:
        """Send a prompt to the OpenAI model and return generated text.

        Args:
            prompt (str): The text input for the model.
            temperature (float, optional): Controls sampling diversity
                and creativity. Defaults to 0.7.

        Returns:
            str: The generated text output from the model.
        """
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content.strip()
