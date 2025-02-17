from docling.document_converter import DocumentConverter


def convert_filepath_to_docling(filepath):
    converter = DocumentConverter()
    return converter.convert(filepath)


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
