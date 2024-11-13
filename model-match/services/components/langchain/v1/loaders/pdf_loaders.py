from typing import List

from langchain_community.document_loaders.pdf import PyPDFium2Loader
from langchain_core.documents import Document


def py_pdf_ium2_loader(file_path: str) -> List[Document]:
    loader = PyPDFium2Loader(file_path=file_path)
    doc = loader.load()
    return doc
