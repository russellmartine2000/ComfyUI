# AI API Node for ComfyUI

A custom ComfyUI node that enables integration with multiple AI API providers including OpenAI, Claude (Anthropic), Google Gemini, and other OpenAI-compatible APIs.

## Features

- **Multi-Provider Support**: Works with OpenAI, Claude, Gemini, and generic OpenAI-compatible APIs
- **Flexible Configuration**: Customizable API base URL and authentication
- **Complete Control**: Adjust temperature, max tokens, and other parameters
- **System Prompts**: Optional system prompt support for better control
- **Error Handling**: Comprehensive error handling with detailed error messages
- **Output Formats**: Returns both extracted text and full JSON response

## Supported Providers

### 1. OpenAI
- Models: GPT-4, GPT-3.5-turbo, etc.
- API Base: `https://api.openai.com/v1`
- Provider: `openai`

### 2. Claude (Anthropic)
- Models: claude-3-opus-20240229, claude-3-sonnet-20240229, etc.
- API Base: `https://api.anthropic.com`
- Provider: `claude`

### 3. Google Gemini
- Models: gemini-pro, gemini-pro-vision, etc.
- API Base: `https://generativelanguage.googleapis.com`
- Provider: `gemini`

### 4. Generic (OpenAI-Compatible)
Use this for any service that provides an OpenAI-compatible API:
- OpenRouter (`https://openrouter.ai/api/v1`)
- Local LLMs (LM Studio, Ollama with OpenAI compatibility, etc.)
- Azure OpenAI
- Any other OpenAI-compatible endpoint
- Provider: `generic`

### 5. Custom (OpenAI-Compatible with Custom Base URL)
Use this for custom API endpoints that follow the OpenAI API format:
- Custom API deployments
- Self-hosted LLMs with OpenAI-compatible interfaces
- Development/testing endpoints
- Specify your own API base URL
- Provider: `custom`

## Installation

1. Copy `nodes_ai_api.py` to your ComfyUI `custom_nodes` directory
2. Ensure `aiohttp` is installed (it should already be in ComfyUI's requirements)
3. Restart ComfyUI

## Usage

### Node Inputs

**Required:**
- `prompt` (STRING): The text prompt to send to the AI
- `api_base` (STRING): Base URL for the API endpoint
- `api_key` (STRING): Your API authentication key
- `provider` (DROPDOWN): Select from: openai, claude, gemini, generic, custom
- `model` (STRING): The model name/identifier
- `max_tokens` (INT): Maximum tokens to generate (1-32768)
- `temperature` (FLOAT): Response randomness (0.0-2.0)

**Optional:**
- `system_prompt` (STRING): System-level instructions for the AI

### Node Outputs

1. `response_text` (STRING): The extracted text response from the AI
2. `full_response_json` (STRING): Complete JSON response for debugging

## Examples

### Example 1: OpenAI GPT-4
```
prompt: "Explain quantum computing in simple terms"
api_base: "https://api.openai.com/v1"
api_key: "sk-..."
provider: "openai"
model: "gpt-4"
max_tokens: 500
temperature: 0.7
```

### Example 2: Claude
```
prompt: "Write a short poem about AI"
api_base: "https://api.anthropic.com"
api_key: "sk-ant-..."
provider: "claude"
model: "claude-3-opus-20240229"
max_tokens: 300
temperature: 1.0
system_prompt: "You are a creative poet"
```

### Example 3: Google Gemini
```
prompt: "What is the capital of France?"
api_base: "https://generativelanguage.googleapis.com"
api_key: "AIza..."
provider: "gemini"
model: "gemini-pro"
max_tokens: 100
temperature: 0.5
```

### Example 4: Local LLM (LM Studio)
```
prompt: "Hello, how are you?"
api_base: "http://localhost:1234/v1"
api_key: "not-needed"
provider: "generic"
model: "local-model"
max_tokens: 200
temperature: 0.8
```

### Example 5: OpenRouter
```
prompt: "Explain machine learning"
api_base: "https://openrouter.ai/api/v1"
api_key: "sk-or-..."
provider: "generic"
model: "anthropic/claude-3-opus"
max_tokens: 1000
temperature: 0.7
```

### Example 6: Custom API Endpoint
```
prompt: "Generate a summary"
api_base: "https://my-custom-api.example.com/v1"
api_key: "custom-key-123"
provider: "custom"
model: "my-custom-model"
max_tokens: 500
temperature: 0.8
```

## Workflow Integration

This node can be integrated into ComfyUI workflows to:
1. Generate image descriptions or captions
2. Create dynamic prompts based on AI responses
3. Analyze or describe generated images
4. Build conversational AI pipelines
5. Generate metadata or tags for images

## Error Handling

The node includes comprehensive error handling:
- Validates API key presence
- Checks for empty prompts
- Validates provider selection
- Handles API request failures
- Returns error messages in both outputs

## Security Notes

- API keys are handled securely within the node
- Never commit workflows containing API keys to version control
- Consider using environment variables for API keys in production

## Troubleshooting

**Import Error:**
- Ensure `aiohttp` is installed: `pip install aiohttp`

**API Request Fails:**
- Verify your API key is correct and active
- Check the API base URL format
- Ensure you have sufficient API credits/quota
- Check your internet connection

**Empty Response:**
- Try increasing `max_tokens`
- Adjust the `temperature` parameter
- Verify the model name is correct

## Development

### Running Tests
```bash
cd /path/to/ComfyUI
python -m pytest tests-unit/custom_nodes_test/test_ai_api_node.py -v
```

### Demo Script
```bash
python demo_ai_api_node.py
```

## License

This node follows the same license as ComfyUI.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Changelog

### Version 1.0.0
- Initial release
- Support for OpenAI, Claude, Gemini, and generic providers
- Comprehensive error handling
- Full test coverage
