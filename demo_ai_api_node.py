#!/usr/bin/env python3
"""
Demo script showing how to use the AI API Node
This demonstrates the node's capabilities without making actual API calls
"""

import sys
import os

# Add custom_nodes to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'custom_nodes'))

from nodes_ai_api import AIAPINode


def demo_node_structure():
    """Demonstrate the node's structure and configuration"""
    print("=" * 70)
    print("AI API Node - Structure Demo")
    print("=" * 70)
    
    # Show input types
    input_types = AIAPINode.INPUT_TYPES()
    print("\n📝 Required Inputs:")
    for key in input_types["required"]:
        print(f"  - {key}")
    
    print("\n📝 Optional Inputs:")
    for key in input_types.get("optional", {}):
        print(f"  - {key}")
    
    print(f"\n📤 Return Types: {AIAPINode.RETURN_TYPES}")
    print(f"📤 Return Names: {AIAPINode.RETURN_NAMES}")
    print(f"📁 Category: {AIAPINode.CATEGORY}")
    print(f"🔧 Function: {AIAPINode.FUNCTION}")


def demo_validation():
    """Demonstrate input validation"""
    print("\n" + "=" * 70)
    print("Input Validation Demo")
    print("=" * 70)
    
    node = AIAPINode()
    
    # Test 1: Empty API key
    print("\n🔍 Test 1: Empty API Key")
    response_text, _ = node.request_ai(
        prompt="Hello",
        api_base="https://api.openai.com/v1",
        api_key="",
        provider="openai",
        model="gpt-3.5-turbo",
        max_tokens=100,
        temperature=0.7
    )
    print(f"   Result: {response_text}")
    
    # Test 2: Empty prompt
    print("\n🔍 Test 2: Empty Prompt")
    response_text, _ = node.request_ai(
        prompt="",
        api_base="https://api.openai.com/v1",
        api_key="test-key",
        provider="openai",
        model="gpt-3.5-turbo",
        max_tokens=100,
        temperature=0.7
    )
    print(f"   Result: {response_text}")
    
    # Test 3: Unsupported provider
    print("\n🔍 Test 3: Unsupported Provider")
    response_text, _ = node.request_ai(
        prompt="Hello",
        api_base="https://api.example.com",
        api_key="test-key",
        provider="invalid_provider",
        model="test-model",
        max_tokens=100,
        temperature=0.7
    )
    print(f"   Result: {response_text}")


def demo_response_extraction():
    """Demonstrate response extraction for different providers"""
    print("\n" + "=" * 70)
    print("Response Extraction Demo")
    print("=" * 70)
    
    node = AIAPINode()
    
    # OpenAI format
    print("\n🤖 OpenAI Response Format:")
    openai_response = {
        "choices": [{
            "message": {"content": "This is an OpenAI response"}
        }]
    }
    text = node._extract_response_text(openai_response, "openai")
    print(f"   Extracted: {text}")
    
    # Claude format
    print("\n🤖 Claude Response Format:")
    claude_response = {
        "content": [{
            "text": "This is a Claude response"
        }]
    }
    text = node._extract_response_text(claude_response, "claude")
    print(f"   Extracted: {text}")
    
    # Gemini format
    print("\n🤖 Gemini Response Format:")
    gemini_response = {
        "candidates": [{
            "content": {
                "parts": [{"text": "This is a Gemini response"}]
            }
        }]
    }
    text = node._extract_response_text(gemini_response, "gemini")
    print(f"   Extracted: {text}")


def demo_usage_examples():
    """Show example usage for different providers"""
    print("\n" + "=" * 70)
    print("Usage Examples")
    print("=" * 70)
    
    examples = [
        {
            "name": "OpenAI API",
            "api_base": "https://api.openai.com/v1",
            "provider": "openai",
            "model": "gpt-4",
            "description": "Standard OpenAI API"
        },
        {
            "name": "Claude API",
            "api_base": "https://api.anthropic.com",
            "provider": "claude",
            "model": "claude-3-opus-20240229",
            "description": "Anthropic Claude API"
        },
        {
            "name": "Gemini API",
            "api_base": "https://generativelanguage.googleapis.com",
            "provider": "gemini",
            "model": "gemini-pro",
            "description": "Google Gemini API"
        },
        {
            "name": "OpenRouter",
            "api_base": "https://openrouter.ai/api/v1",
            "provider": "generic",
            "model": "anthropic/claude-3-opus",
            "description": "OpenRouter with OpenAI-compatible API"
        },
        {
            "name": "Local LLM",
            "api_base": "http://localhost:1234/v1",
            "provider": "generic",
            "model": "local-model",
            "description": "Local LLM with OpenAI-compatible API (e.g., LM Studio)"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n📌 Example {i}: {example['name']}")
        print(f"   Description: {example['description']}")
        print(f"   API Base: {example['api_base']}")
        print(f"   Provider: {example['provider']}")
        print(f"   Model: {example['model']}")


if __name__ == "__main__":
    demo_node_structure()
    demo_validation()
    demo_response_extraction()
    demo_usage_examples()
    
    print("\n" + "=" * 70)
    print("✅ Demo completed successfully!")
    print("=" * 70)
    print("\n💡 To use this node in ComfyUI:")
    print("   1. Place nodes_ai_api.py in the custom_nodes directory")
    print("   2. Restart ComfyUI")
    print("   3. Find 'AI API Request' node in the 'ai_api' category")
    print("   4. Configure with your API credentials")
    print("   5. Connect to other nodes in your workflow")
    print()
