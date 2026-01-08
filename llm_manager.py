import os
from typing import Optional
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.models.bedrock import BedrockConverseModel
from action_models import AndroidAction

class LLMManager:
    """Manages LLM provider initialization and agent creation."""

    DEFAULT_MODELS = {
        "openai": "gpt-4o",
        "anthropic": "claude-sonnet-4",
        "gemini": "gemini-2.0-flash-exp",
        "bedrock": "anthropic.claude-sonnet-4-20250514-v1:0"
    }

    def __init__(self):
        self.provider = self._get_provider()
        self.model = self._get_model()
        self.agent = self._create_agent()

    def _get_provider(self) -> str:
        """Get provider from environment."""
        provider = os.environ.get("LLM_PROVIDER")
        if not provider:
            raise ValueError(
                "LLM_PROVIDER environment variable must be set. "
                "Valid values: openai, anthropic, gemini, bedrock"
            )
        if provider not in self.DEFAULT_MODELS:
            raise ValueError(
                f"Invalid LLM_PROVIDER '{provider}'. "
                f"Valid values: {', '.join(self.DEFAULT_MODELS.keys())}"
            )
        return provider

    def _get_model(self) -> str:
        """Get model name from environment or use default."""
        env_var = f"{self.provider.upper()}_MODEL"
        model = os.environ.get(env_var)
        if not model:
            model = self.DEFAULT_MODELS[self.provider]
        return model

    def _validate_credentials(self):
        """Validate that required credentials are present."""
        if self.provider == "openai":
            if not os.environ.get("OPENAI_API_KEY"):
                raise ValueError("OPENAI_API_KEY environment variable must be set")
        elif self.provider == "anthropic":
            if not os.environ.get("ANTHROPIC_API_KEY"):
                raise ValueError("ANTHROPIC_API_KEY environment variable must be set")
        elif self.provider == "gemini":
            if not os.environ.get("GOOGLE_API_KEY"):
                raise ValueError("GOOGLE_API_KEY environment variable must be set")
        elif self.provider == "bedrock":
            # Bedrock uses AWS credentials - boto3 will handle validation
            pass

    def _create_agent(self) -> Agent:
        """Create Pydantic AI agent with appropriate model."""
        self._validate_credentials()

        if self.provider == "openai":
            model = OpenAIChatModel(self.model)
        elif self.provider == "anthropic":
            model = AnthropicModel(self.model)
        elif self.provider == "gemini":
            model = GoogleModel(self.model)
        elif self.provider == "bedrock":
            model = BedrockConverseModel(self.model)

        # Create agent with structured output
        agent = Agent(
            model=model,
            output_type=AndroidAction,
            system_prompt=self._get_system_prompt()
        )

        return agent

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the Android agent."""
        return """You are an Android Driver Agent. Your job is to achieve the user's goal by navigating the UI.

You will receive:
1. The User's Goal.
2. A list of interactive UI elements (JSON) with their (x,y) center coordinates.

You must decide the next action to take.

Available Actions:
- tap: Tap at specific coordinates
- type: Type text into a field
- home: Go to home screen
- back: Go back to previous screen
- wait: Wait for loading or animation
- done: Task is complete

Always provide a clear reason for your action."""

    async def get_decision(self, goal: str, screen_context: str) -> AndroidAction:
        """Get LLM decision for next action."""
        prompt = f"""GOAL: {goal}

SCREEN_CONTEXT:
{screen_context}

What action should I take next?"""

        result = await self.agent.run(prompt)
        return result.data
