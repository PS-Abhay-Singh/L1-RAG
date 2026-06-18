from langchain_ollama import ChatOllama

_clients: dict[str, ChatOllama] = {}

def get_llm(model: str = "qwen2.5:3b", temperature: float = 0) -> ChatOllama:
    key = f"{model}:{temperature}"
    if key not in _clients:
        _clients[key] = ChatOllama(model=model, temperature=temperature)
    return _clients[key]
