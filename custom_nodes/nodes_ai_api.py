"""
ComfyUI Node for AI API Integration
Supports multiple AI providers: OpenAI, Claude (Anthropic), Google Gemini, and others
"""

import json
import aiohttp
import asyncio
import logging
from typing import Dict, Any, Tuple


class AIAPINode:
    """
    A ComfyUI node that integrates with various AI API providers.
    Supports OpenAI, Claude, Gemini, and other compatible APIs.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": "Hello, how are you?",
                    "tooltip": "The prompt to send to the AI"
                }),
                "api_base": ("STRING", {
                    "default": "https://api.openai.com/v1",
                    "tooltip": "Base URL for the API (e.g., https://api.openai.com/v1, https://api.anthropic.com, https://generativelanguage.googleapis.com)"
                }),
                "api_key": ("STRING", {
                    "default": "",
                    "tooltip": "Your API key for authentication"
                }),
                "provider": (["openai", "claude", "gemini", "generic", "custom"], {
                    "default": "openai",
                    "tooltip": "AI provider type"
                }),
                "model": ("STRING", {
                    "default": "gpt-3.5-turbo",
                    "tooltip": "Model name (e.g., gpt-4, claude-3-opus-20240229, gemini-pro)"
                }),
                "max_tokens": ("INT", {
                    "default": 1024,
                    "min": 1,
                    "max": 32768,
                    "step": 1,
                    "tooltip": "Maximum number of tokens to generate"
                }),
                "temperature": ("FLOAT", {
                    "default": 0.7,
                    "min": 0.0,
                    "max": 2.0,
                    "step": 0.1,
                    "tooltip": "Temperature for response randomness"
                }),
            },
            "optional": {
                "system_prompt": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "tooltip": "System prompt (optional)"
                }),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("response_text", "full_response_json")
    FUNCTION = "request_ai"
    CATEGORY = "ai_api"
    OUTPUT_NODE = True
    
    DESCRIPTION = "Makes requests to various AI API providers (OpenAI, Claude, Gemini, and others). Supports custom API bases and keys."

    async def _make_openai_request(self, api_base: str, api_key: str, model: str, 
                                   prompt: str, system_prompt: str, max_tokens: int, 
                                   temperature: float) -> Dict[str, Any]:
        """Make request to OpenAI-compatible API"""
        url = f"{api_base.rstrip('/')}/chat/completions"
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"API request failed with status {response.status}: {error_text}")
                return await response.json()

    async def _make_claude_request(self, api_base: str, api_key: str, model: str,
                                   prompt: str, system_prompt: str, max_tokens: int,
                                   temperature: float) -> Dict[str, Any]:
        """Make request to Claude (Anthropic) API"""
        url = f"{api_base.rstrip('/')}/v1/messages"
        
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        if system_prompt:
            payload["system"] = system_prompt
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"API request failed with status {response.status}: {error_text}")
                return await response.json()

    async def _make_gemini_request(self, api_base: str, api_key: str, model: str,
                                   prompt: str, system_prompt: str, max_tokens: int,
                                   temperature: float) -> Dict[str, Any]:
        """Make request to Google Gemini API"""
        url = f"{api_base.rstrip('/')}/v1/models/{model}:generateContent?key={api_key}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        # Combine system prompt with user prompt for Gemini
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        payload = {
            "contents": [{
                "parts": [{"text": full_prompt}]
            }],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens
            }
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"API request failed with status {response.status}: {error_text}")
                return await response.json()

    async def _make_generic_request(self, api_base: str, api_key: str, model: str,
                                    prompt: str, system_prompt: str, max_tokens: int,
                                    temperature: float) -> Dict[str, Any]:
        """Make request to generic OpenAI-compatible API"""
        # Generic provider defaults to OpenAI format
        return await self._make_openai_request(api_base, api_key, model, prompt, 
                                               system_prompt, max_tokens, temperature)

    def _extract_response_text(self, response_data: Dict[str, Any], provider: str) -> str:
        """Extract text from API response based on provider"""
        try:
            if provider == "openai" or provider == "generic" or provider == "custom":
                return response_data["choices"][0]["message"]["content"]
            elif provider == "claude":
                return response_data["content"][0]["text"]
            elif provider == "gemini":
                return response_data["candidates"][0]["content"]["parts"][0]["text"]
            else:
                return str(response_data)
        except (KeyError, IndexError) as e:
            logging.error(f"Error extracting response text: {e}")
            return json.dumps(response_data, indent=2)

    def _run_async_request(self, loop, provider: str, api_base: str, api_key: str,
                          model: str, prompt: str, system_prompt: str, 
                          max_tokens: int, temperature: float) -> Dict[str, Any]:
        """Helper to run async request in a loop"""
        if provider == "openai":
            return loop.run_until_complete(
                self._make_openai_request(api_base, api_key, model, prompt, 
                                         system_prompt, max_tokens, temperature)
            )
        elif provider == "claude":
            return loop.run_until_complete(
                self._make_claude_request(api_base, api_key, model, prompt,
                                         system_prompt, max_tokens, temperature)
            )
        elif provider == "gemini":
            return loop.run_until_complete(
                self._make_gemini_request(api_base, api_key, model, prompt,
                                         system_prompt, max_tokens, temperature)
            )
        elif provider == "generic" or provider == "custom":
            return loop.run_until_complete(
                self._make_generic_request(api_base, api_key, model, prompt,
                                           system_prompt, max_tokens, temperature)
            )
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def _sync_request(self, provider: str, api_base: str, api_key: str,
                     model: str, prompt: str, system_prompt: str,
                     max_tokens: int, temperature: float) -> Dict[str, Any]:
        """Helper to run request in a new event loop (for threaded execution)"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return self._run_async_request(loop, provider, api_base, api_key,
                                          model, prompt, system_prompt, max_tokens, temperature)
        finally:
            loop.close()

    def request_ai(self, prompt: str, api_base: str, api_key: str, provider: str,
                   model: str, max_tokens: int, temperature: float, 
                   system_prompt: str = "") -> Tuple[str, str]:
        """
        Main function to make AI API requests
        
        Args:
            prompt: The user prompt
            api_base: Base URL for the API
            api_key: API authentication key
            provider: AI provider type
            model: Model name
            max_tokens: Maximum tokens to generate
            temperature: Response randomness
            system_prompt: Optional system prompt
            
        Returns:
            Tuple of (response_text, full_response_json)
        """
        if not api_key:
            error_msg = "API key is required"
            logging.error(error_msg)
            return (error_msg, json.dumps({"error": error_msg}))
        
        if not prompt:
            error_msg = "Prompt cannot be empty"
            logging.error(error_msg)
            return (error_msg, json.dumps({"error": error_msg}))
        
        try:
            # Create event loop if needed
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # Event loop is already running, we need to use a thread
                    import concurrent.futures
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(self._sync_request, provider, api_base, api_key, 
                                                model, prompt, system_prompt, max_tokens, temperature)
                        response_data = future.result()
                else:
                    # Event loop exists but not running
                    response_data = self._run_async_request(loop, provider, api_base, api_key,
                                                           model, prompt, system_prompt, max_tokens, temperature)
            except RuntimeError:
                # No event loop exists
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                response_data = self._run_async_request(loop, provider, api_base, api_key,
                                                       model, prompt, system_prompt, max_tokens, temperature)
            
            # Extract response text
            response_text = self._extract_response_text(response_data, provider)
            full_response_json = json.dumps(response_data, indent=2)
            
            logging.info(f"AI API request successful. Provider: {provider}, Model: {model}")
            return (response_text, full_response_json)
            
        except Exception as e:
            error_msg = f"Error making AI API request: {str(e)}"
            logging.error(error_msg)
            return (error_msg, json.dumps({"error": error_msg}))


# Node registration
NODE_CLASS_MAPPINGS = {
    "AIAPINode": AIAPINode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AIAPINode": "AI API Request"
}
