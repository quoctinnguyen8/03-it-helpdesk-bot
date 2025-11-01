"""JSON document loader implementation.

This module provides an implementation of the DocumentLoader interface
for reading JSON files using LangChain's JSONLoader.
"""

import json
from typing import List

from langchain_core.documents import Document

from knowledge_chat.domain.interfaces.document_loader import DocumentLoader


class JSONLoader(DocumentLoader):
    """Document loader for JSON files."""

    def load(self, file_path: str) -> List[Document]:
        """Load a JSON file and return its content as LangChain Documents.

        This loader converts JSON data into readable text format. It supports:
        - Objects: Converts key-value pairs into text
        - Arrays: Processes each item
        - Nested structures: Flattens into readable format

        Args:
            file_path (str): Path to the JSON file.

        Returns:
            List[Document]: A list containing LangChain Document objects
                with JSON content converted to text and metadata.
        """
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Convert JSON to readable text format
        text_content = self._json_to_text(data)

        # Create a single document with the JSON content
        document = Document(
            page_content=text_content,
            metadata={
                "source": file_path.split("\\")[-1].split("/")[-1],
                "file_type": "json",
            },
        )

        return [document]

    def _json_to_text(self, data, indent: int = 0) -> str:
        """Convert JSON data to readable text format.

        Args:
            data: JSON data (dict, list, or primitive type)
            indent: Current indentation level for nested structures

        Returns:
            str: Formatted text representation of the JSON data
        """
        lines = []
        prefix = "  " * indent

        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    lines.append(f"{prefix}{key}:")
                    lines.append(self._json_to_text(value, indent + 1))
                else:
                    lines.append(f"{prefix}{key}: {value}")

        elif isinstance(data, list):
            for i, item in enumerate(data):
                if isinstance(item, (dict, list)):
                    lines.append(f"{prefix}Item {i + 1}:")
                    lines.append(self._json_to_text(item, indent + 1))
                else:
                    lines.append(f"{prefix}- {item}")

        else:
            lines.append(f"{prefix}{data}")

        return "\n".join(lines)
