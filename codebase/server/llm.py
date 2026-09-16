"""Gọi Gemini qua REST (không cần cài SDK)."""
import json
import urllib.error
import urllib.request

ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


class LLMError(Exception):
    pass


def generate_json(api_key, model, system, user, schema, temperature=0.2, timeout=60):
    body = {
        "system_instruction": {"parts": [{"text": system}]},
        "contents": [{"role": "user", "parts": [{"text": user}]}],
        "generationConfig": {
            "temperature": temperature,
            "responseMimeType": "application/json",
            "responseSchema": schema,
        },
    }
    req = urllib.request.Request(
        ENDPOINT.format(model=model),
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "x-goog-api-key": api_key},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")
        try:
            detail = json.loads(detail)["error"]["message"]
        except (ValueError, KeyError, TypeError):
            pass
        hint = ""
        if e.code == 404:
            hint = " — kiểm tra GEMINI_MODEL trong codebase/.env có đúng tên model không."
        elif e.code in (400, 401, 403):
            hint = " — kiểm tra GEMINI_API_KEY trong codebase/.env."
        elif e.code == 429:
            hint = " — hết quota hoặc gọi quá nhanh, đợi một chút rồi thử lại."
        raise LLMError(f"Gemini trả lỗi {e.code}: {detail}{hint}") from e
    except urllib.error.URLError as e:
        raise LLMError(f"Không kết nối được Gemini: {e.reason}") from e

    try:
        cand = data["candidates"][0]
        text = "".join(p.get("text", "") for p in cand["content"]["parts"])
        usage = data.get("usageMetadata", {})
        return json.loads(text), usage
    except (KeyError, IndexError, ValueError) as e:
        reason = data.get("candidates", [{}])[0].get("finishReason") or data.get("promptFeedback")
        raise LLMError(f"Gemini không trả JSON hợp lệ (finishReason/feedback: {reason})") from e
