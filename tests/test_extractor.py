from app.extractor import extract_fields


def test_pan():
    text = """
    PAN NUMBER: JAFQA0304G
    NAME: ANANDA PAL
    FATHER NAME: SUNANDA PAL
    DOB: 12/10/1996
    """
    fields = extract_fields(text)
    assert fields["PAN_NUMBER"]["value"] == "JAFQA0304G"

def test_bank():
    text = "ACCOUNT NUMBER: 237712120000280 IFSC: UBIN0539325"
    fields = extract_fields(text)

    assert "ACCOUNT_NUMBER" in fields
    assert "IFSC_CODE" in fields
    assert fields["IFSC_CODE"]["value"] == "UBIN0539325"
