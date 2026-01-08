import os
import requests
import json

class PerplexityClient:
    def __init__(self, api_key=None, base_url="https://api.perplexity.ai"):
        self.api_key = api_key or os.getenv("PERPLEXITY_API_KEY")
        if not self.api_key:
            raise ValueError("Perplexity API key is required. Set PERPLEXITY_API_KEY env var or pass it to the constructor.")
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def chat_completion(self, messages, model="sonar", temperature=0.2):
        """
        Send a chat completion request to the Perplexity API.
        """
        url = f"{self.base_url}/chat/completions"
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error calling Perplexity API: {e}")
            raise

    def generate_roadmap(self, topic, difficulty="Intermediate"):
        """
        Helper method specifically to generate a roadmap for a topic.
        Results are returned as text.
        """
        system_prompt = (
            "You are an expert curriculum designer. "
            f"Create a structured learning roadmap for the given topic at an {difficulty} level. "
            "Return the response as a clear, numbered list of main topics, "
            "with sub-points for each. Do not include conversational filler."
        )
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Create a learning roadmap for: {topic}"}
        ]
        
        result = self.chat_completion(messages)
        return result['choices'][0]['message']['content']
