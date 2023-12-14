import json
import logging
from json import JSONDecodeError
from typing import Type, Optional

import google.generativeai as genai
from flask import current_app

from core.helper import encrypter
from core.model_providers.models.base import BaseProviderModel
from core.model_providers.models.entity.model_params import ModelKwargsRules, KwargRule, ModelType, ModelMode
from core.model_providers.models.entity.provider import ModelFeature
from core.model_providers.models.llm.gemini_model import GeminiModel, COMPLETION_MODELS
from core.model_providers.providers.base import BaseModelProvider, CredentialsValidateFailedError
from core.model_providers.providers.hosted import hosted_model_providers
from models.provider import ProviderType


class GeminiProvider(BaseModelProvider):

    @property
    def provider_name(self):
        """
        Returns the name of a provider.
        """
        return 'gemini'

    def _get_fixed_model_list(self, model_type: ModelType) -> list[dict]:
        if model_type == ModelType.TEXT_GENERATION:
            models = [
                {
                    'id': 'gemini-pro',
                    'name': 'gemini-pro',
                    'mode': ModelMode.CHAT.value,
                    'features': [
                        ModelFeature.AGENT_THOUGHT.value
                    ]
                },
                {
                    'id': 'gemini-pro-vision',
                    'name': 'gemini-pro-vision',
                    'mode': ModelMode.CHAT.value,
                    'features': [
                        ModelFeature.AGENT_THOUGHT.value
                    ]
                },

            ]
            return models
        else:
            return []

    def _get_text_generation_model_mode(self, model_name) -> str:
        if model_name in COMPLETION_MODELS:
            return ModelMode.COMPLETION.value
        else:
            return ModelMode.CHAT.value

    def get_model_class(self, model_type: ModelType) -> Type[BaseProviderModel]:
        """
        Returns the model class.

        :param model_type:
        :return:
        """
        if model_type == ModelType.TEXT_GENERATION:
            model_class = GeminiModel
        else:
            raise NotImplementedError

        return model_class

    def get_model_parameter_rules(self, model_name: str, model_type: ModelType) -> ModelKwargsRules:
        """
        get model parameter rules.

        :param model_name:
        :param model_type:
        :return:
        """
        model_max_tokens = {
            'gemini-pro': 4096,
            'gemini-pro-vision': 2048,
        }

        return ModelKwargsRules(
            temperature=KwargRule[float](min=0, max=2, default=1, precision=2),
            top_p=KwargRule[float](min=0, max=1, default=1, precision=2),
            presence_penalty=KwargRule[float](min=-2, max=2, default=0, precision=2),
            frequency_penalty=KwargRule[float](min=-2, max=2, default=0, precision=2),
            max_tokens=KwargRule[int](min=10, max=model_max_tokens.get(model_name, 4097), default=16, precision=0),
        )

    @classmethod
    def is_provider_credentials_valid_or_raise(cls, credentials: dict):
        """
        Validates the given credentials.
        """
        if 'genai_api_key' not in credentials:
            raise CredentialsValidateFailedError('Gemini API key is required')

        try:
            genai.configure(api_key=credentials['genai_api_key'])
            generation_config = {
                "temperature": 0.9,
                "top_p": 1,
                "top_k": 1,
                "max_output_tokens": 712094269,
            }

            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                }
            ]

            model = genai.GenerativeModel(model_name="gemini-pro",
                                          generation_config=generation_config,
                                          safety_settings=safety_settings)

            model.generate_content([{"role": "user", "content": 'ping'}])

        except Exception as ex:
            logging.exception('Genmini config validation failed')
            raise ex

    @classmethod
    def encrypt_provider_credentials(cls, tenant_id: str, credentials: dict) -> dict:
        credentials['genai_api_key'] = encrypter.encrypt_token(tenant_id, credentials['genai_api_key'])
        return credentials

    def get_provider_credentials(self, obfuscated: bool = False) -> dict:
        if self.provider.provider_type == ProviderType.CUSTOM.value:
            try:
                credentials = json.loads(self.provider.encrypted_config)
            except JSONDecodeError:
                credentials = {
                    'genai_api_base': None,
                    'genai_api_key': self.provider.encrypted_config,
                }

            if credentials['genai_api_key']:
                credentials['genai_api_key'] = encrypter.decrypt_token(
                    self.provider.tenant_id,
                    credentials['genai_api_key']
                )

                if obfuscated:
                    credentials['genai_api_key'] = encrypter.obfuscated_token(credentials['genai_api_key'])

            if 'genai_api_base' not in credentials or not credentials['genai_api_base']:
                credentials['genai_api_base'] = None
            else:
                credentials['genai_api_base'] = credentials['genai_api_base'] + '/v1beta'

            return credentials
        else:
            if hosted_model_providers.openai:
                return {
                    'genai_api_base': hosted_model_providers.openai.api_base,
                    'genai_api_key': hosted_model_providers.openai.api_key,
                }
            else:
                return {
                    'genai_api_base': None,
                    'genai_api_key': None,
                }

    @classmethod
    def is_provider_type_system_supported(cls) -> bool:
        if current_app.config['EDITION'] != 'CLOUD':
            return False



        return False

    def should_deduct_quota(self):


        return False

    def get_payment_info(self) -> Optional[dict]:
        """
        get payment info if it payable.

        :return:
        """
        if hosted_model_providers.openai \
                and hosted_model_providers.openai.paid_enabled:
            return {
                'product_id': hosted_model_providers.openai.paid_stripe_price_id,
                'increase_quota': hosted_model_providers.openai.paid_increase_quota,
            }

        return None

    @classmethod
    def is_model_credentials_valid_or_raise(cls, model_name: str, model_type: ModelType, credentials: dict):
        """
        check model credentials valid.

        :param model_name:
        :param model_type:
        :param credentials:
        """
        return

    @classmethod
    def encrypt_model_credentials(cls, tenant_id: str, model_name: str, model_type: ModelType,
                                  credentials: dict) -> dict:
        """
        encrypt model credentials for save.

        :param tenant_id:
        :param model_name:
        :param model_type:
        :param credentials:
        :return:
        """
        return {}

    def get_model_credentials(self, model_name: str, model_type: ModelType, obfuscated: bool = False) -> dict:
        """
        get credentials for llm use.

        :param model_name:
        :param model_type:
        :param obfuscated:
        :return:
        """
        return self.get_provider_credentials(obfuscated)
