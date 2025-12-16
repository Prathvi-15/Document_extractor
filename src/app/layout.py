def simple_layout(text):
    lines = text.split("\n")
    return [line.strip() for line in lines if line.strip()]
