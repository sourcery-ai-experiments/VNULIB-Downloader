"""Create PDF for books."""

from __future__ import annotations

import os
from concurrent.futures import ProcessPoolExecutor
import img2pdf
from .link_parse import Link
from ..utils import logger


class CreatePDF:
    """Create PDF for books.

    Args:
        - links (list[Link]): The list of links object.
    """

    def __init__(self, links: list[Link], download_directory: str) -> None:
        self.links: list[Link] = links
        self.download_directory: str = download_directory
        self.executor = ProcessPoolExecutor()

    @staticmethod
    def process(directory: str, name: str) -> None:
        """Merge all images in a directory into a single PDF.

        Args:
            directory (str): The directory containing the images.
            name (str): Name of pdf file.
        """
        pdf_file_name: str = os.path.join(directory, f"{name}.pdf")
        logger.info(msg=f'Creating PDF: "{pdf_file_name}"')
        list_files: list[str] = [os.path.join(directory, item) for item in os.listdir(directory)]
        if any(map(lambda file: file.endswith(".pdf"), list_files)):
            return
        pdf_file: bytes | None = img2pdf.convert(list_files)
        if pdf_file is not None:
            with open(pdf_file_name, "wb") as f:
                f.write(pdf_file)
            logger.info(msg=f'Created PDF: "{pdf_file_name}"')

    def book_handler(self, book_directory: str, link: Link) -> None:
        """Book handler, create PDF for Book's files.

        Args:
            directory (str): The directory containing the subdirectories.
            link (Link): The book's Link.
        """
        for file in link.files:
            self.executor.submit(
                CreatePDF.process,
                os.path.join(book_directory, file.name),
                file.name,
            )

    def create_pdf(self) -> None:
        """Create PDF."""
        for link in self.links:
            match link.original_type:
                case "book":
                    self.book_handler(os.path.join(self.download_directory, link.name), link)
                case "preview" | "page":
                    self.executor.submit(
                        self.process,
                        os.path.join(self.download_directory, link.files[0].name),
                        link.files[0].name,
                    )
                case _:
                    pass
        self.executor.shutdown()
