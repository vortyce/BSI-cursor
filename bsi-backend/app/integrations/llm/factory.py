from app.core.config import settings
from app.integrations.llm.openai_client import OpenAIClient

class LLMClientFactory:
    @staticmethod
    def get_client():
        """
        Factory simples para obter o cliente de LLM baseado na configuração.
        """
        if settings.DEFAULT_LLM_PROVIDER == "openai":
            return OpenAIClient()
        
        raise ValueError(f"Provedor de LLM '{settings.DEFAULT_LLM_PROVIDER}' não é suportado.")
