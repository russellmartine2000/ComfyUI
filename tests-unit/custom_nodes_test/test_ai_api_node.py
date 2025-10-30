"""
Unit tests for AI API Node
"""

import pytest
import json
import sys
import os

# Add custom_nodes to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'custom_nodes'))

from nodes_ai_api import AIAPINode


class TestAIAPINode:
    """Test cases for AIAPINode"""
    
    def test_node_initialization(self):
        """Test that node can be initialized"""
        node = AIAPINode()
        assert node is not None
    
    def test_input_types(self):
        """Test that INPUT_TYPES returns correct structure"""
        input_types = AIAPINode.INPUT_TYPES()
        
        # Check required fields exist
        assert "required" in input_types
        assert "prompt" in input_types["required"]
        assert "api_base" in input_types["required"]
        assert "api_key" in input_types["required"]
        assert "provider" in input_types["required"]
        assert "model" in input_types["required"]
        assert "max_tokens" in input_types["required"]
        assert "temperature" in input_types["required"]
        
        # Check optional fields
        assert "optional" in input_types
        assert "system_prompt" in input_types["optional"]
    
    def test_return_types(self):
        """Test that node has correct return types"""
        assert AIAPINode.RETURN_TYPES == ("STRING", "STRING")
        assert AIAPINode.RETURN_NAMES == ("response_text", "full_response_json")
    
    def test_node_attributes(self):
        """Test node class attributes"""
        assert AIAPINode.FUNCTION == "request_ai"
        assert AIAPINode.CATEGORY == "ai_api"
        assert AIAPINode.OUTPUT_NODE == True
    
    def test_empty_api_key(self):
        """Test that empty API key returns error"""
        node = AIAPINode()
        response_text, response_json = node.request_ai(
            prompt="Test prompt",
            api_base="https://api.openai.com/v1",
            api_key="",
            provider="openai",
            model="gpt-3.5-turbo",
            max_tokens=100,
            temperature=0.7
        )
        
        assert "API key is required" in response_text
        response_dict = json.loads(response_json)
        assert "error" in response_dict
    
    def test_empty_prompt(self):
        """Test that empty prompt returns error"""
        node = AIAPINode()
        response_text, response_json = node.request_ai(
            prompt="",
            api_base="https://api.openai.com/v1",
            api_key="test-key",
            provider="openai",
            model="gpt-3.5-turbo",
            max_tokens=100,
            temperature=0.7
        )
        
        assert "Prompt cannot be empty" in response_text
        response_dict = json.loads(response_json)
        assert "error" in response_dict
    
    def test_unsupported_provider(self):
        """Test that unsupported provider returns error"""
        node = AIAPINode()
        response_text, response_json = node.request_ai(
            prompt="Test prompt",
            api_base="https://api.example.com",
            api_key="test-key",
            provider="unsupported_provider",
            model="test-model",
            max_tokens=100,
            temperature=0.7
        )
        
        assert "Unsupported provider" in response_text
        response_dict = json.loads(response_json)
        assert "error" in response_dict
    
    def test_extract_openai_response(self):
        """Test extracting response from OpenAI format"""
        node = AIAPINode()
        mock_response = {
            "choices": [{
                "message": {
                    "content": "Test response"
                }
            }]
        }
        
        result = node._extract_response_text(mock_response, "openai")
        assert result == "Test response"
    
    def test_extract_claude_response(self):
        """Test extracting response from Claude format"""
        node = AIAPINode()
        mock_response = {
            "content": [{
                "text": "Test claude response"
            }]
        }
        
        result = node._extract_response_text(mock_response, "claude")
        assert result == "Test claude response"
    
    def test_extract_gemini_response(self):
        """Test extracting response from Gemini format"""
        node = AIAPINode()
        mock_response = {
            "candidates": [{
                "content": {
                    "parts": [{
                        "text": "Test gemini response"
                    }]
                }
            }]
        }
        
        result = node._extract_response_text(mock_response, "gemini")
        assert result == "Test gemini response"
    
    def test_extract_invalid_response(self):
        """Test extracting response from invalid format"""
        node = AIAPINode()
        mock_response = {
            "invalid": "data"
        }
        
        # Should return JSON string when extraction fails
        result = node._extract_response_text(mock_response, "openai")
        assert "invalid" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
