"""Gọi LLM qua REST (không cần cài SDK). Hỗ trợ Gemini và OpenAI — chọn theo provider."""
import json
import urllib.error
import urllib.request

ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
OPENAI_ENDPOINT = "https://api.openai.com/v1/chat/completions"


class LLMError(Exception):
    pass


def generate_json(api_key, model, system, user, schema, temperature=0.2, timeout=60, provider="gemini"):
    if provider == "openai":
        return _openai_json(api_key, model, system, user, schema, temperature, timeout)
    return _gemini_json(api_key, model, system, user, schema, temperature, timeout)


def _to_openai_schema(node):
    """Schema kiểu Gemini (type viết hoa) -> JSON Schema strict cho OpenAI."""
    t = node.get("type", "").lower()
    out = {"type": t}
    if "enum" in node:
        out["enum"] = node["enum"]
    if t == "object":
        out["properties"] = {k: _to_openai_schema(v) for k, v in node.get("properties", {}).items()}
        out["required"] = list(node.get("properties", {}).keys())  # strict mode: mọi field đều required
        out["additionalProperties"] = False
    elif t == "array":
        out["items"] = _to_openai_schema(node["items"])
    return out


def _openai_json(api_key, model, system, user, schema, temperature, timeout):
    body = {
        "model": model,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "response_format": {"type": "json_schema",
                            "json_schema": {"name": "tutor_reply", "strict": True, "schema": _to_openai_schema(schema)}},
    }
    if not model.startswith(("gpt-5", "o")):  # các model reasoning không nhận temperature
        body["temperature"] = temperature
    req = urllib.request.Request(OPENAI_ENDPOINT, data=json.dumps(body).encode("utf-8"),
                                 headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
                                 method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")
        try:
            detail = json.loads(detail)["error"]["message"]
        except (ValueError, KeyError, TypeError):
            pass
        hint = {404: " — kiểm tra OPENAI_MODEL.", 401: " — kiểm tra OPENAI_API_KEY.", 429: " — hết quota hoặc gọi quá nhanh."}.get(e.code, "")
        raise LLMError(f"OpenAI trả lỗi {e.code}: {detail}{hint}") from e
    except urllib.error.URLError as e:
        raise LLMError(f"Không kết nối được OpenAI: {e.reason}") from e
    try:
        text = data["choices"][0]["message"]["content"]
        u = data.get("usage", {})
        usage = {"promptTokenCount": u.get("prompt_tokens"), "candidatesTokenCount": u.get("completion_tokens")}
        return json.loads(text), usage
    except (KeyError, IndexError, ValueError, TypeError) as e:
        raise LLMError(f"OpenAI không trả JSON hợp lệ (finish_reason: {data.get('choices', [{}])[0].get('finish_reason')})") from e


def _gemini_json(api_key, model, system, user, schema, temperature, timeout):
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
