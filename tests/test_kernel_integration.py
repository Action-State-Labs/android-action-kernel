import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from kernel import get_llm_decision
from action_models import TapAction

@pytest.mark.asyncio
async def test_get_llm_decision_returns_action():
    with patch.dict('os.environ', {
        "LLM_PROVIDER": "openai",
        "OPENAI_API_KEY": "test-key"
    }):
        with patch('kernel.LLMManager') as mock_manager_class:
            mock_manager = MagicMock()
            mock_manager.get_decision = AsyncMock(
                return_value=TapAction(coordinates=[100, 200], reason="test")
            )
            mock_manager_class.return_value = mock_manager

            action = await get_llm_decision("test goal", "test context")

            assert isinstance(action, TapAction)
            assert action.coordinates == [100, 200]
