import urllib.request
import json

class Core:
    base_url = "https://core.rethink.web.id"
    model = "deepseek"
    system_prompt = ""
    hitories = []
    DOCS_URL = "https://core.rethink.web.id/docs/generation"

    def __init__(self, api_key, system_prompt="", model="deepseek"):
        self.api_key = api_key
        self.model = model
        self.system_prompt = system_prompt

    def request (self, payload):
        url = f"{self.base_url}/api/v1/"

        if type(payload) != dict:
            self.throw_error("Payload must be a dictionary")

        data = json.dumps(payload).encode('utf-8')

        req = urllib.request.Request(
            url, 
            data=data, 
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0',
                "Authorization": f"Bearer {self.api_key}"
            },
            method='POST'
        )

        try:
            with urllib.request.urlopen(req) as response:
                result = response.read().decode('utf-8')
                return json.loads(result)
        except urllib.error.HTTPError as e:
            self.throw_error(f"HTTP Error {e.code}: {e.read().decode()}")
    
    def change_model(self, model):
        self.model = model
    
    def set_hitories(self, histories):
        if type(histories) != dict:
            self.throw_error("Histories must be a dictionary")
        
        self.history = histories
    
    def chat(self, messages, hitories={}):
        payload = {
            "model": self.model,
            "messages": messages,
            "system_prompt": self.system_prompt,
        }

        if hitories:
            payload["history"] = hitories
        
        return self.request(payload)
    
    def imagine (self, prompt="", width=1024, height=768):
        if self.system_prompt and prompt == "":
            prompt = self.system_prompt
        
        if prompt == "":
            self.throw_error("Prompt must be a provide")
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "width": width,
            "height": height,
        }

        return self.request(payload)

    def throw_error(self, message):
        raise Exception(f"{message}\n\nFor more information, please visit {self.DOCS_URL}")