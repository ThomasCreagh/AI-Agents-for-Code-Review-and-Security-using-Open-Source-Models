import os
from enum import Enum
from docling.document_converter import DocumentConverter
# import PyPDF2


class FileType(Enum):
    pdf = ".pdf"
    docx = ".docx"
    xlsx = ".xlsx"
    pptx = ".pptx"
    markdown = ".md"
    html = ".html"
    xhtml = ".xhtml"
    png = ".png"
    jpeg = ".jpeg"
    tiff = ".tiff"
    bmp = ".bmp"
    asciidoc = ".adoc"


class DoclingDocumentConversion:
    def __init__(self, filepath):
        self.filepath: str = filepath
        self.docling_document = self.get_docling_document()
        print(self.docling_document.json())
        # self.filename, self.fileextention = os.path.splitext(self.filepath)
        #
        # if not self.fileextention:
        #     ValueError("no fileextention given")
        #
        # self.filetype: FileType = self.map_extention_to_filetype(
        #     self.fileextention)
        # self.metadata: dict = self.get_metadata()

    # def map_extention_to_filetype(self, extention: str) -> FileType:
    #     normalized_extention = extention.lower()
    #     for file_type in FileType:
    #         if normalized_extention == file_type.value:
    #             return file_type

    def get_docling_document(self):
        converter = DocumentConverter()
        return converter.convert(self.filepath)


test_doc = DoclingDocumentConversion(
    "./processor.py")
# "./Laidlaw_Programme_2025_Scholars_(Proposal_Template).docx")

# def get_metadata(self) -> str:
#     with open(self.filepath, 'rb') as file_reader:
#         match self.filetype:
#             case pdf:
#                 pdf_reader = PyPDF2.PdfReader(file)
#                 return pdf_reader.metadata
#             case docx:
#
#             case xlsx:
#             case pptx:
#             case markdown:
#             case html:
#             case xhtml:
#             case png:
#             case jpeg:
#             case tiff:
#             case bmp:
#             case markdown:
#             case asciidoc:
