import ollama

class LLM_DM:
    def __init__(self):
        self.model = 'GMDnD:latest' # Use the user's specified model

    def get_story_prompt(self, prompt):
        try:
            response = ollama.chat(model=self.model, messages=[{'role': 'user', 'content': prompt}])
            return response['message']['content']
        except Exception as e:
            return f"Error communicating with LLM: {e}"