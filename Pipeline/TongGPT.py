import os
from openai import AzureOpenAI, OpenAI

# from utils import local_image_to_data_url, resize, extract_json


def get_api_key(key_path="key.txt"):
    """Read API key from file."""
    # Try to find key.txt in different locations
    possible_paths = [
        key_path,
        os.path.join(os.path.dirname(__file__), key_path),
        os.path.join(os.path.dirname(__file__), "..", key_path),
        os.path.join(os.path.dirname(__file__), "..", "..", key_path),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            with open(path, "r") as f:
                return f.readline().strip()
    
    # Fall back to environment variable
    api_key = os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if api_key:
        return api_key
    
    raise FileNotFoundError(f"API key file not found. Please create key.txt or set OPENROUTER_API_KEY environment variable.")


class LLMClient:
    """
    Unified LLM client supporting multiple backends: OpenRouter, OpenAI, and Azure OpenAI.
    """
    
    def __init__(self, model="openai/gpt-4o", api_type="openrouter", base_url=None, api_key=None, api_version=None):
        """
        Initialize the LLM client.
        
        Args:
            model: Model name/identifier
            api_type: One of "openrouter", "openai", or "azure"
            base_url: Custom API base URL (optional)
            api_key: API key (if not provided, reads from key.txt or environment)
            api_version: API version (required for Azure)
        """
        self.MODEL = model
        self.api_type = api_type.lower()
        self.api_key = api_key or get_api_key()
        
        if self.api_type == "openrouter":
            self.base_url = base_url or "https://openrouter.ai/api/v1"
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url,
            )
        elif self.api_type == "openai":
            self.client = OpenAI(
                api_key=self.api_key,
                base_url=base_url if base_url else None,
            )
        elif self.api_type == "azure":
            if not api_version:
                api_version = "2024-02-01"
            self.client = AzureOpenAI(
                api_key=self.api_key,
                api_version=api_version,
                azure_endpoint=base_url or "https://api.tonggpt.mybigai.ac.cn/proxy/eastus2",
            )
        else:
            raise ValueError(f"Unsupported api_type: {api_type}. Supported: openrouter, openai, azure")
    
    def send_request(self, payload):
        """Send a chat completion request."""
        response = self.client.chat.completions.create(
            model=payload.get("model", self.MODEL),
            messages=payload["messages"],
            temperature=payload.get("temperature", 0),
            max_tokens=payload.get("max_tokens", 4096),
        )
        return response


# Legacy class for backward compatibility
class TongGPT(LLMClient):
    """Legacy class for backward compatibility with existing code."""
    
    def __init__(self, MODEL="gpt-35-turbo-0125", REGION="westus"):
        # Check for environment variable to determine API type
        api_type = os.environ.get("LLM_API_TYPE", "openrouter")
        base_url = os.environ.get("LLM_BASE_URL")
        
        super().__init__(
            model=MODEL,
            api_type=api_type,
            base_url=base_url,
        )

    def send_request(self, kw):
        if isinstance(kw, str):
            # Simple text request
            response = self.client.chat.completions.create(
                model=self.MODEL,
                messages=[{"role": "user", "content": kw}],
            )
            print(response.model_dump_json(indent=2))
            print(".....")
            print(response.choices[0].message.content)
            return response
        else:
            # Payload request
            return super().send_request(kw)


class GPT4o(LLMClient):
    """GPT-4o compatible client."""
    
    def __init__(self, MODEL="gpt-4-turbo-2024-04-09", REGION="westus"):
        api_type = os.environ.get("LLM_API_TYPE", "openrouter")
        base_url = os.environ.get("LLM_BASE_URL")
        
        # Map model names to OpenRouter equivalents if using OpenRouter
        if api_type == "openrouter" and not MODEL.startswith("openai/"):
            MODEL = f"openai/{MODEL}"
        
        super().__init__(
            model=MODEL,
            api_type=api_type,
            base_url=base_url,
        )

    def send_request(self, payload):
        response = self.client.chat.completions.create(
            model=payload.get("model", self.MODEL),
            messages=payload["messages"],
            temperature=payload.get("temperature", 0),
            max_tokens=payload.get("max_tokens", 4096),
        )
        return response


class GPT4V(GPT4o):
    """GPT-4 Vision compatible client."""
    
    def __init__(self, MODEL="gpt-4-vision-preview", REGION="australiaeast"):
        super().__init__(MODEL, REGION)


# if __name__ == "__main__":
#     # Example usage with OpenRouter
#     client = LLMClient(model="openai/gpt-4o", api_type="openrouter")
#     response = client.send_request({
#         "messages": [{"role": "user", "content": "Say Hello!"}],
#         "temperature": 0,
#         "max_tokens": 100,
#     })
#     print(response.choices[0].message.content)
