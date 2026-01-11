import os
import google.generativeai as genai
from typing import List, Dict
from app.models.assistant import AssistantMessage

# genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

class AssistantService:
    def __init__(self, api_key: str = None):
        if api_key:
            genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def get_response(self, mode: str, user_level: str, history: List[AssistantMessage], query: str, context: str = ""):
        system_prompt = f"""
        You are Lumina, an AI English tutor. 
        User Level: {user_level}
        Current Mode: {mode}
        
        Instructions:
        - Use simple, clear explanations appropriate for {user_level} level.
        - Encourage the user but stay professional.
        - If the mode is 'Explain', focus on grammar and vocabulary rules with examples.
        - If the mode is 'Practice', provide exercises and give feedback on user answers.
        - If the mode is 'Translate', provide bilingual examples.
        - If the mode is 'Quiz me', ask a short question and wait for the answer.
        
        Lesson Context: {context}
        """
        
        chat = self.model.start_chat(history=[
            {"role": m.role, "parts": [m.content]} for m in history
        ])
        
        # In a real app, we'd add the system prompt as the first message or use a system_instruction constructor
        # For simplicity with this SDK version:
        full_query = f"{system_prompt}\n\nUser Question: {query}"
        response = chat.send_message(full_query)
        
        return response.text
