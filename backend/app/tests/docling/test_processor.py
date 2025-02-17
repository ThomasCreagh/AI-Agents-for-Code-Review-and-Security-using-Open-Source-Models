from app.docling.processor import convert_filepath_to_docling


def test_convert_filepath_to_docling():
    filepath = "app/tests/docling/test_files/Laidlaw_Programme_2025_Scholars_(Proposal_Template).docx"
    result = convert_filepath_to_docling(filepath)

    assert result is not None
    assert len(result.model_dump()) > 0
