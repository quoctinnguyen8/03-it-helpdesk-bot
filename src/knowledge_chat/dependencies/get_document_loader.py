"""Dependency provider for the document loader.

This module defines a factory function that initializes and returns
a DocumentLoader implementation using application settings.

Returns a MultiFormatLoader that supports multiple file types:
- Plain text (.txt)
- PDF documents (.pdf)
- Markdown files (.md, .markdown)
- JSON files (.json)
"""

from knowledge_chat.domain.interfaces.document_loader import DocumentLoader
from knowledge_chat.infrastructure.document_loader.multi_format_loader import \
    MultiFormatLoader


def get_document_loader() -> DocumentLoader:
    """Create and return a configured DocumentLoader instance.

    Returns a MultiFormatLoader that automatically detects file types
    and uses the appropriate loader for each format.

    Returns:
        DocumentLoader: An initialized multi-format loader for reading documents.
    """

    return MultiFormatLoader()
