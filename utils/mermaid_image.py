import base64
import zlib

def encode_mermaid(diagram_text: str) -> str:
    compressed = zlib.compress(diagram_text.encode("utf-8"))
    return base64.urlsafe_b64encode(compressed).decode("utf-8")

def render_mermaid_as_image(mermaid_code: str):
    encoded = encode_mermaid(mermaid_code)
    url = f"https://kroki.io/mermaid/png/{encoded}"
    return url