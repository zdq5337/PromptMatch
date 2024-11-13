from typing import (
    Callable,
    Iterable,
    List,
)

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def recursive_character_text_splitter(
        documents: Iterable[Document],  # type: ignore
        chunk_size: int = 4000,
        chunk_overlap: int = 200,
        length_function: Callable[[str], int] = len,
        keep_separator: bool = False,
        add_start_index: bool = False,
        strip_whitespace: bool = True,

) -> List[Document]:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    splits = text_splitter.split_documents(documents=documents)
    return splits
