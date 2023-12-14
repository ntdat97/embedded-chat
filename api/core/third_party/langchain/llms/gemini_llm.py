from typing import (
    Dict,
)

import google.generativeai as genai  # type: ignore[import]
from langchain.utils import get_from_dict_or_env
from langchain_google_genai import ChatGoogleGenerativeAI


class EnhanceGemini(ChatGoogleGenerativeAI):

    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key and python package exists in environment."""
        google_api_key = get_from_dict_or_env(
            values, "google_api_key", "GOOGLE_API_KEY"
        )
        values["google_api_key"] = google_api_key
        return values

∏
