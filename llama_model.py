from flask import Flask, request, jsonify
from llama_cpp import Llama

app = Flask(__name__)

llm = Llama(
    model_path="models/llama-3/Meta-Llama-3-8B-Instruct-Q4_K_M.gguf",
    n_ctx=2048,
    n_threads=8
)
def generate_response(prompt, max_tokens=128):
    try:
        assert isinstance(prompt, str), "Prompt bir string olmalı!"
        print("Prompt gönderiliyor:\n", prompt)
        result = llm.create_completion(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=0.7,
            top_p=0.95,
            stop=["\n"]
            

        )
        print("LLM yanıtı:", result)
        return result["choices"][0]["text"].strip()
    except Exception as e:
        print("LLM hata verdi:", e)
        return "Yanıt üretilemedi."



@app.route("/v1/completions", methods=["POST"])
def completions():
    data = request.get_json()
    prompt = data.get("prompt", "")
    max_tokens = data.get("max_tokens", 128)
    output = llm(prompt, max_tokens=max_tokens)
    return jsonify(output)
print("Model başarıyla yüklendi:", llm.model_path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)