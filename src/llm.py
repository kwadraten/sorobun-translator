from openai import OpenAI
from openai import OpenAIError, APIConnectionError
from pathlib import Path
import os
import logging
import json

class Model:

    def __init__(self, config_path: Path | None = None) -> None:
        self.config_path = Path(os.path.abspath(".")) / Path("config.json")
        if config_path:
            self.config_path = config_path
        with open(self.config_path, "rt", encoding="utf-8") as config_file:
            config = json.load(config_file)

        self.base_client = OpenAI(api_key=config["base_key"], base_url=config["base_api"])
        
        if config.get("reasoning_api") and config.get("reasoning_key"):
            self.reasoning_client = OpenAI(api_key=config["reasoning_key"], base_url=config["reasoning_key"])
        else:
            self.reasoning_client = self.base_client
        
        self.base_model = config["base_model"]
        if config.get("reasoning_model"):
            self.reasoning_model = config["reasoning_model"]

        self.check_availability()

    def check_availability(self) -> None:
        try:
            self.base_client.models.list()
            self.reasoning_client.models.list()
        except APIConnectionError as e:
            logging.error(f"Availability Check Failed. Please check your api url and secret key: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")

    def predict(self, prompt: str, is_reasoning: bool) -> str:
        messages = [  
            {"role": "user", "content": prompt}
        ]  

        client = self.base_client
        model = self.base_model
        if is_reasoning:
            client = self.reasoning_client
            model = self.reasoning_model

        try:  
            response = client.chat.completions.create(  
                model= model,
                messages=messages,
                max_tokens=5000,  
                temperature=0.7,
                top_p=1.0,
                frequency_penalty=0.0, 
                presence_penalty=0.0,
            )

            return response.choices[0].message.content

        except OpenAIError as e:
            logging.error(f"OpenAI API Error: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")