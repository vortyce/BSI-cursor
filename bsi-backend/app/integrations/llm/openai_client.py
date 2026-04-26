import json
import time
from openai import OpenAI
from app.core.config import settings
from app.integrations.llm.base import BaseLLMClient
from app.core.logging_utils import get_logger

logger = get_logger("llm")

class OpenAIClient(BaseLLMClient):
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def get_interpretation(self, system_prompt: str, user_prompt: str):
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                logger.info("openai_call", f"Attempt {attempt + 1} to get interpretation")
                response = self.client.chat.completions.create(
                    model=settings.DEFAULT_LLM_MODEL,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    response_format={"type": "json_object"},
                    timeout=30
                )
                content = response.choices[0].message.content
                logger.info("openai_call", "Successfully received response from OpenAI")
                return json.loads(content), content
            except Exception as e:
                logger.error("openai_call", f"Error in attempt {attempt + 1}: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (attempt + 1))
                    continue
                raise Exception(f"OpenAI API Error after {max_retries} attempts: {str(e)}")
