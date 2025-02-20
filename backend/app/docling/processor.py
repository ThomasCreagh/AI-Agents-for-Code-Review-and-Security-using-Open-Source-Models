from docling.document_converter import DocumentConverter
import os
import uuid

from app.ai.llm_rag_database.ai_init import db


def convert_bytes_to_docling(filename: str, data: bytes):
    temp_file_name = str(uuid.uuid4()) + "_" + filename
    temp_file_path = os.path.abspath(os.path.join(os.path.dirname(
        __file__), "temp", temp_file_name))
    print(temp_file_path)

    with open(temp_file_path, "wb") as byte_writer:
        byte_writer.write(data)

    docling_result = convert_filepath_to_docling(temp_file_path)
    os.remove(temp_file_path)
    return docling_result


def convert_filepath_to_docling(filepath):
    converter = DocumentConverter()
    return converter.convert(filepath)


def add_bytes_to_rag_db(filename: str, data: bytes):
    doc = convert_bytes_to_docling(filename, data)
    db.add_documents(doc)

# from enum import Enum
# class FileType(Enum):
#     pdf = ".pdf"
#     docx = ".docx"
#     xlsx = ".xlsx"
#     pptx = ".pptx"
#     markdown = ".md"
#     html = ".html"
#     xhtml = ".xhtml"
#     png = ".png"
#     jpeg = ".jpeg"
#     tiff = ".tiff"
#     bmp = ".bmp"
#     asciidoc = ".adoc"
