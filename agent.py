import os
from groq import Groq
from spam_tool import unified_spam_detector

# ---------------------------------------
# 🔐 Initialize Groq Client
# ---------------------------------------
groq_key = os.getenv("GROQ_API_KEY")

if not groq_key:
    raise ValueError("GROQ_API_KEY not found in environment variables.")

client = Groq(api_key=groq_key)


# ---------------------------------------
# 🛡 Hybrid ML + LLM Agent
# ---------------------------------------
def llama_agent(user_input: str = None, image_path: str = None):

    # Validate input
    if not user_input and not image_path:
        return {"detail": "Provide either text or an image file."}

    # ---------------------------------------
    # Step 1: Run ML Detection Tool
    # ---------------------------------------
    result = unified_spam_detector.invoke({
        "message_text": user_input,
        "image_path": image_path
    })

    if result.get("status") == "error":
        return {"error": result.get("message", "Spam detection failed.")}

    message_source = result.get("source", "text")
    prediction = result.get("prediction", "Unknown")
    spam_prob = float(result.get("spam_probability", 0.0))

    verdict = prediction.upper()

    # ---------------------------------------
    # ✅ Correct Confidence Calculation
    # ---------------------------------------
    if verdict == "SPAM":
        confidence_score = spam_prob
    else:
        confidence_score = 1 - spam_prob

    confidence = round(confidence_score * 100, 2)

    # ---------------------------------------
    # Extract Text Preview
    # ---------------------------------------
    text_preview = (
        result.get("text_preview")
        or result.get("extracted_text")
        or user_input
        or "N/A"
    )

    # ---------------------------------------
    # Step 2: LLM Reasoning Prompt
    # ---------------------------------------
    reasoning_prompt = f"""
You are an AI cybersecurity and fraud-awareness assistant.

The user has shared a {message_source} message.

Message content:
{text_preview[:600]}

Model classification result: {verdict}
Model confidence score: {confidence}%

IMPORTANT INSTRUCTIONS:

If the message is classified as SPAM:

Respond in this exact structured format:

1) Why is this likely a scam or spam?
   - Clearly explain the red flags.
   - Mention the possible scam type (phishing, investment scam, lottery scam, etc.).

2) What should you do?
   - Provide 3–4 clear safety steps.
   - Keep instructions practical and easy to follow.

3) How to report cybercrime in India:
   - Tell the user to report at the official Cyber Crime Portal:
     https://cybercrime.gov.in
   - Mention the cybercrime helpline number: 1930

If the message is classified as HAM:

- Reassure the user politely.
- Mention that no major scam indicators were detected.
- Give 1–2 light online safety reminders.

Tone:
Friendly, protective, clear, concise.

Do NOT mention model confidence unless it is below 60%.
If confidence is below 60%, add a short note that the message is borderline and should be manually verified.
"""

    # ---------------------------------------
    # Step 3: Call Groq LLM
    # ---------------------------------------
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": reasoning_prompt}],
        )

        explanation = completion.choices[0].message.content.strip()

    except Exception:
        explanation = "⚠️ Unable to generate safety explanation at the moment."

    # ---------------------------------------
    # Step 4: Return Clean API Response
    # ---------------------------------------
    return {
        "source": message_source,
        "verdict": verdict,
        "confidence": confidence,
        "safety_analysis": explanation,
    }