from llama_cpp.server.app import app

if __name__ == "__main__":
    app.model_path = "models/llama-3/Meta-Llama-3-8B-Instruct-Q4_K_M.gguf"
    app.n_ctx = 2048
    app.n_threads = 8
    app.run(host="0.0.0.0", port=8000)