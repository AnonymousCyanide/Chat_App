from collections import defaultdict
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json

class UserManager:
    def __init__(self):
        self.active_users: dict[str, WebSocket] = {}

    def add_user(self, user_id: str, websocket: WebSocket):
        self.active_users[user_id] = websocket

    def remove_user(self, user_id: str):
        if user_id in self.active_users:
            del self.active_users[user_id]

    def get_user_socket(self, user_id: str) -> WebSocket | None:
        return self.active_users.get(user_id)

    def list_users(self):
        return list(self.active_users.keys())

class ChatManager:
    def __init__(self):
        self.user_chats = defaultdict(set)  # user_id -> set of chat_ids
        self.chat_members = defaultdict(set)  # chat_id -> set of user_ids
        self.chat_history = defaultdict(list)  # chat_id -> list of messages

    def add_user_to_chat(self, user_id: str, chat_id: str):
        self.user_chats[user_id].add(chat_id)
        self.chat_members[chat_id].add(user_id)

    def send_message(self, chat_id: str, sender_id: str, content: str):
        msg = {"from": sender_id, "text": content}
        self.chat_history[chat_id].append(msg)
        return msg

    def get_chat_users(self, chat_id: str):
        return self.chat_members[chat_id]

    def get_history(self, chat_id: str):
        return self.chat_history[chat_id]
