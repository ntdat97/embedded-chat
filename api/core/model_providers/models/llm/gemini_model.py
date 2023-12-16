import logging
from typing import List, Optional, Any

import openai
from langchain.callbacks.manager import Callbacks
from langchain.schema import LLMResult

from core.model_providers.error import LLMBadRequestError, LLMAPIConnectionError, LLMAPIUnavailableError, \
    LLMRateLimitError, LLMAuthorizationError
from core.model_providers.models.entity.message import PromptMessage
from core.model_providers.models.entity.model_params import ModelMode, ModelKwargs
from core.model_providers.models.llm.base import BaseLLM
from core.model_providers.providers.base import BaseModelProvider
from core.third_party.langchain.llms.gemini_llm import EnhanceGemini

COMPLETION_MODELS = [

]

CHAT_MODELS = [
    'gemini-pro',  # 2048 tokens
    'gemini-pro-vision',  # 2048 tokenss
]

MODEL_MAX_TOKENS = {
    'gemini-pro': 4096,
    'gemini-pro-vision': 2048,
}


class GeminiModel(BaseLLM):
    def __init__(self, model_provider: BaseModelProvider,
                 name: str,
                 model_kwargs: ModelKwargs,
                 streaming: bool = False,
                 callbacks: Callbacks = None):
        if name in COMPLETION_MODELS:
            self.model_mode = ModelMode.COMPLETION
        else:
            self.model_mode = ModelMode.CHAT

        super().__init__(model_provider, name, model_kwargs, streaming, callbacks)

    def _init_client(self) -> Any:
        provider_model_kwargs = self._to_model_kwargs_input(self.model_rules, self.model_kwargs)
        return EnhanceGemini(
            model=self.name,
            google_api_key=self.credentials.get('google_api_key'),
            **provider_model_kwargs
        )

    def _run(self, messages: List[PromptMessage],
             stop: Optional[List[str]] = None,
             callbacks: Callbacks = None,
             **kwargs) -> LLMResult:
        """
        run predict by prompt messages and stop words.

        :param messages:
        :param stop:
        :param callbacks:
        :return:
        """

        prompts = self._get_prompt_from_messages(messages)

        extra_kwargs = {}

        generate_kwargs = {
            'stop': stop,
            "callbacks": callbacks,
        }
        if isinstance(prompts, str):
            generate_kwargs['prompts'] = [prompts]
        else:
            generate_kwargs['messages'] = [prompts]
        return self._client.generate([prompts], stop, callbacks, **extra_kwargs)

    def get_num_tokens(self, messages: List[PromptMessage]) -> int:
        """
        get num tokens of prompt messages.

        :param messages:
        :return:
        """
        contents = [message.content for message in messages]
        return max(self._client.get_num_tokens("".join(contents)), 0)

    def _set_model_kwargs(self, model_kwargs: ModelKwargs):
        provider_model_kwargs = self._to_model_kwargs_input(self.model_rules, model_kwargs)
        if self.name in COMPLETION_MODELS:
            for k, v in provider_model_kwargs.items():
                if hasattr(self.client, k):
                    setattr(self.client, k, v)
        else:
            extra_model_kwargs = {
                'top_p': provider_model_kwargs.get('top_p'),
                'frequency_penalty': provider_model_kwargs.get('frequency_penalty'),
                'presence_penalty': provider_model_kwargs.get('presence_penalty'),
            }

            self.client.temperature = provider_model_kwargs.get('temperature')
            self.client.max_tokens = provider_model_kwargs.get('max_tokens')
            self.client.model_kwargs = extra_model_kwargs

    def handle_exceptions(self, ex: Exception) -> Exception:
        if isinstance(ex, openai.error.InvalidRequestError):
            logging.warning("Invalid request to OpenAI API.")
            return LLMBadRequestError(str(ex))
        elif isinstance(ex, openai.error.APIConnectionError):
            logging.warning("Failed to connect to OpenAI API.")
            return LLMAPIConnectionError(ex.__class__.__name__ + ":" + str(ex))
        elif isinstance(ex, (openai.error.APIError, openai.error.ServiceUnavailableError, openai.error.Timeout)):
            logging.warning("OpenAI service unavailable.")
            return LLMAPIUnavailableError(ex.__class__.__name__ + ":" + str(ex))
        elif isinstance(ex, openai.error.RateLimitError):
            return LLMRateLimitError(str(ex))
        elif isinstance(ex, openai.error.AuthenticationError):
            return LLMAuthorizationError(str(ex))
        elif isinstance(ex, openai.error.OpenAIError):
            return LLMBadRequestError(ex.__class__.__name__ + ":" + str(ex))
        else:
            return ex

    @property
    def support_streaming(self):
        return False
