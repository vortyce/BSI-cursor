from abc import ABC, abstractmethod

class BaseLLMClient(ABC):
    @abstractmethod
    def get_interpretation(self, system_prompt: str, user_prompt: str) -> tuple[dict, str]:
        """
        Retorna (dicionário da resposta, string bruta da resposta)
        """
        pass
