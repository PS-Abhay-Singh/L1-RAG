from typing import List

class ConversationMemory:
    def __init__(self):
        self.sessions: dict[str, List[dict]] = {}

    def add_message(self, session_id: str, speaker: str, text: str):
        session = self.sessions.setdefault(session_id, [])
        session.append({"speaker": speaker, "text": text})

    def get_history(self, session_id: str):
        return self.sessions.get(session_id, [])

    def clear(self, session_id: str):
        if session_id in self.sessions:
            del self.sessions[session_id]

conversation_memory = ConversationMemory()
