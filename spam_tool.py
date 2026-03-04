from langchain.tools import tool
from typing import Optional
from runtime.text_runtime import detect_spam_from_text
from runtime.image_runtime import detect_spam_from_image

@tool("unified_spam_detector", return_direct=True)
def unified_spam_detector(
    message_text: Optional[str] = None,
    image_path: Optional[str] = None
):
    """
    Unified Spam Detection Tool
    """

    if image_path:
        result = detect_spam_from_image(image_path)
        result["source"] = "image"
        return result

    elif message_text:
        result = detect_spam_from_text(message_text)
        result["source"] = "text"
        return result

    else:
        return {
            "status": "error",
            "message": "Provide either message_text or image_path."
        }