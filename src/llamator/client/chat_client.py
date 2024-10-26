import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from .langchain_integration import get_langchain_chat_models_info

logger = logging.getLogger(__name__)

# Introspect langchain for supported models
chat_models_info = get_langchain_chat_models_info()


class ClientBase(ABC):
    """
    Base class for interacting with chat models.
    The history and new messages are passed as a list of dictionaries.

    Attributes
    ----------
    system_prompts : Optional[List[str]]
        Optional system prompts to guide the conversation.
    model_description : Optional[str]
        Optional model description to guide the conversation.

    Methods
    -------
    interact(history: List[Dict[str, str]], messages: List[Dict[str, str]]) -> Dict[str, str]
        Takes the conversation history and new messages, sends them to the LLM, and returns a new response.
    """

    # Attributes that can be None by default
    system_prompts: Optional[List[str]] = None
    model_description: Optional[str] = None

    @abstractmethod
    def interact(self, history: List[Dict[str, str]], messages: List[Dict[str, str]]) -> Dict[str, str]:
        """
        Takes the conversation history and new messages, sends them to the LLM, and returns a new response.

        Parameters
        ----------
        history : List[Dict[str, str]]
            A list of past messages representing the conversation history.

        messages : List[Dict[str, str]]
            A list of new messages to be sent to the LLM.

        Returns
        -------
        Dict[str, str]
            The response from the LLM in dictionary format, with "role" and "content" fields.
        """
        pass


class ChatSession:
    """
    Maintains a single conversation session, including the history, and supports optional system prompts.

    Attributes
    ----------
    client : ClientBase
        The client responsible for interacting with the LLM.

    system_prompts : Optional[List[str]]
        A list of system prompts used to initialize the conversation (if any).

    history : List[Dict[str, str]]
        The conversation history, containing both user and assistant messages.

    Methods
    -------
    say(user_prompt: str) -> str
        Sends a user message to the LLM, updates the conversation history, and returns the assistant's response.
    """

    def __init__(self, client: ClientBase, system_prompts: Optional[List[str]] = None):
        """
        Initializes the ChatSession with a client and optional system prompts.

        Parameters
        ----------
        client : ClientBase
            The client that handles interaction with the LLM.

        system_prompts : Optional[List[str]]
            A list of system prompts to guide the conversation from the start.
        """
        self.client = client
        self.system_prompts = None
        if system_prompts:
            self.system_prompts = [
                {"role": "system", "content": system_prompt_text} for system_prompt_text in system_prompts
            ]
        self.history = []

    def say(self, user_prompt: str) -> str:
        """
        Sends a user message to the LLM, updates the conversation history, and returns the assistant's response.

        Parameters
        ----------
        user_prompt : str
            The user's message to be sent to the LLM.

        Returns
        -------
        str
            The response from the assistant (LLM) as a string.
        """
        logger.debug(f"say: system_prompt={self.system_prompts}")
        logger.debug(f"say: prompt={user_prompt}")
        input_messages = []
        if len(self.history) == 0 and self.system_prompts:
            input_messages.extend(self.system_prompts)
        input_messages.append({"role": "user", "content": user_prompt})

        result = self.client.interact(self.history, input_messages)
        logger.debug(f"say: result={result}")

        self.history.extend(input_messages)  # Update the conversation history
        self.history.append(result)  # Add the response to the history

        return result["content"]
