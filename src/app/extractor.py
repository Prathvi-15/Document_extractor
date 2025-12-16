import re

# ===================== REGEX ===================== #
PAN_REGEX = r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"
GST_REGEX = r"\b[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]\b"
AADHAAR_REGEX = r"\b\d{4}\s\d{4}\s\d{4}\b"
IFSC_REGEX = r"\b[A-Z]{4}0[A-Z0-9]{6}\b"
DOB_REGEX = r"\b\d{2}[/-]\d{2}[/-]\d{4}\b"

BANK_NAMES = [
    "STATE BANK OF INDIA", "SBI", "HDFC BANK",
    "ICICI BANK", "AXIS BANK", "CANARA BANK",
    "PUNJAB NATIONAL BANK", "BANK OF BARODA",
    "UNION BANK", "IDBI BANK", "YES BANK"
]

AADHAAR_IGNORE = [
    "GOVERNMENT", "INDIA", "AADHAAR",
    "UNIQUE", "IDENTIFICATION", "AUTHORITY",
    "MALE", "FEMALE", "DOB"
]

# ===================== HELPERS ===================== #
def clean_lines(text):
    return [l.strip() for l in text.split("\n") if l.strip()]

def detect_document_type(text):
    if re.search(GST_REGEX, text):
        return "GST"
    if re.search(PAN_REGEX, text):
        return "PAN"
    if re.search(AADHAAR_REGEX, text):
        return "AADHAAR"
    if re.search(IFSC_REGEX, text) or "BANK" in text:
        return "BANK"
    return "UNKNOWN"

# ===================== PAN ===================== #
def extract_pan(text):
    fields = {}
    lines = clean_lines(text)

    pan = re.search(PAN_REGEX, text)
    if pan:
        fields["PAN_NUMBER"] = {"value": pan.group(), "confidence": 0.98}

    for i, line in enumerate(lines):
        if "NAME" in line and "FATHER" not in line:
            if i + 1 < len(lines):
                fields["NAME"] = {"value": lines[i + 1], "confidence": 0.90}
            break

    for i, line in enumerate(lines):
        if "FATHER" in line:
            if i + 1 < len(lines):
                fields["FATHER_NAME"] = {"value": lines[i + 1], "confidence": 0.90}
            break

    dob = re.search(DOB_REGEX, text)
    if dob:
        fields["DOB"] = {"value": dob.group(), "confidence": 0.90}

    return fields

# ===================== AADHAAR ===================== #
def extract_aadhaar(text):
    fields = {}
    lines = clean_lines(text)

    aadhaar_match = re.search(AADHAAR_REGEX, text)
    aadhaar_index = -1

    if aadhaar_match:
        fields["AADHAAR_NUMBER"] = {
            "value": aadhaar_match.group(),
            "confidence": 0.95
        }
        for i, line in enumerate(lines):
            if aadhaar_match.group() in line:
                aadhaar_index = i
                break

    # -------- NAME --------
    name_candidates = []

    for i, line in enumerate(lines):
        if aadhaar_index != -1 and i >= aadhaar_index:
            break

        if not line.isupper():
            continue

        if any(sym in line for sym in ["+", "-", ")", "(", "/", "_"]):
            continue

        words = line.split()
        if not (2 <= len(words) <= 3):
            continue

        if any(bad in line for bad in AADHAAR_IGNORE):
            continue

        if sum(1 for w in words if len(w) <= 2) >= 2:
            continue

        name_candidates.append((i, line))

    if name_candidates:
        name_candidates.sort(key=lambda x: abs(x[0] - aadhaar_index))
        fields["NAME"] = {
            "value": name_candidates[0][1],
            "confidence": 0.92
        }

    # -------- ADDRESS --------
    address_lines = []
    if "NAME" in fields:
        name_idx = lines.index(fields["NAME"]["value"])
        for line in lines[name_idx + 1 : aadhaar_index]:
            if any(skip in line for skip in ["DOB", "MALE", "FEMALE"]):
                continue
            address_lines.append(line)

    if address_lines:
        fields["ADDRESS"] = {
            "value": ", ".join(address_lines),
            "confidence": 0.80
        }

    return fields

# ===================== BANK ===================== #
def extract_bank(text):
    fields = {}
    lines = clean_lines(text)

    # Bank name
    for bank in BANK_NAMES:
        if bank in text:
            fields["BANK_NAME"] = {"value": bank, "confidence": 0.90}
            break

    # IFSC
    ifsc_match = re.search(IFSC_REGEX, text)
    if ifsc_match:
        fields["IFSC_CODE"] = {"value": ifsc_match.group(), "confidence": 0.98}

    # Account number
    for line in lines:
        if "ACCOUNT" in line:
            acc = re.search(r"\b\d{10,18}\b", line)
            if acc:
                fields["ACCOUNT_NUMBER"] = {
                    "value": acc.group(),
                    "confidence": 0.95
                }
                break

    # Account holder name
    first_name = ""
    last_name = ""

    for line in lines:
        if "FIRST NAME" in line:
            first_name = line.split(":")[-1].strip()
        if "LAST NAME" in line:
            last_name = line.split(":")[-1].strip()

    if first_name or last_name:
        fields["ACCOUNT_HOLDER_NAME"] = {
            "value": f"{first_name} {last_name}".strip(),
            "confidence": 0.90
        }

    return fields

# ===================== GST ===================== #
def extract_gst(text):
    fields = {}
    lines = clean_lines(text)

    gst = re.search(GST_REGEX, text)
    if gst:
        fields["GSTIN"] = {"value": gst.group(), "confidence": 0.98}

    for line in lines:
        if "LEGAL NAME" in line or "TRADE NAME" in line:
            fields["BUSINESS_NAME"] = {
                "value": line.split(":")[-1].strip(),
                "confidence": 0.85
            }
            break

    return fields

# ===================== MAIN ===================== #
def extract_fields(text):
    doc_type = detect_document_type(text)

    if doc_type == "PAN":
        return extract_pan(text)
    if doc_type == "AADHAAR":
        return extract_aadhaar(text)
    if doc_type == "BANK":
        return extract_bank(text)
    if doc_type == "GST":
        return extract_gst(text)

    return {}
