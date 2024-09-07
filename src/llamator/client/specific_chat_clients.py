import logging
from typing import Dict, List, Optional

from langchain.schema import AIMessage, BaseMessage, HumanMessage
from langchain_core.outputs.llm_result import LLMResult

from .chat_client import ClientBase
from .langchain_integration import get_langchain_chat_models_info
from openai import OpenAI

logger = logging.getLogger(__name__)

# Type representing list of messages (history)
MessageList = List[BaseMessage]

# Introspect langchain for supported models
chat_models_info = get_langchain_chat_models_info()


class FakeChatClient(ClientBase):
    def interact(self, history: List[Dict[str, str]], messages: List[Dict[str, str]]) -> Dict[str, str]:
        return {"role": "assistant", "content": "FakeChat response"}


class ClientLangChain(ClientBase):
    """
    Wrapper for interacting with models through LangChain.

    Parameters
    ----------
    backend : str
        The backend name to use for model initialization.
    system_prompts : Optional[List[str]]
        List of system prompts for initializing the conversation context (optional).
    **kwargs
        Additional arguments passed to the model's constructor.

    Methods
    -------
    _convert_to_langchain_format(messages: List[Dict[str, str]]) -> List[BaseMessage]
        Converts messages in the format List[Dict[str, str]] to the format used by LangChain (HumanMessage, AIMessage).

    _convert_from_langchain_format(message: BaseMessage) -> Dict[str, str]
        Converts a LangChain message (HumanMessage, AIMessage) back to a dictionary format.

    interact(history: List[Dict[str, str]], messages: List[Dict[str, str]]) -> Dict[str, str]
        Takes conversation history and new messages, sends a request to the model, and returns the response as a dictionary.
    """

    def __init__(self, backend: str, system_prompts: Optional[List[str]] = None, **kwargs):

        if backend in chat_models_info:
            self.client = chat_models_info[backend].model_cls(**kwargs)
        else:
            raise ValueError(
                f"Invalid backend name: {backend}. Supported backends: {', '.join(chat_models_info.keys())}"
            )
        self.system_prompts = system_prompts

    @staticmethod
    def _convert_to_langchain_format(messages: List[Dict[str, str]]) -> List[BaseMessage]:
        """
        Converts messages in the format List[Dict[str, str]] to the format used by LangChain (HumanMessage, AIMessage).

        Parameters
        ----------
        messages : List[Dict[str, str]]
            List of messages to convert.

        Returns
        -------
        List[BaseMessage]
            Messages in LangChain format.
        """
        langchain_messages = []
        for msg in messages:
            if msg["role"] == "user":
                langchain_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                langchain_messages.append(AIMessage(content=msg["content"]))
            elif msg["role"] == "system":
                langchain_messages.append(
                    AIMessage(content=msg["content"])
                )  # In LangChain, there is no "system" role, using AIMessage
        return langchain_messages

    @staticmethod
    def _convert_from_langchain_format(message: BaseMessage) -> Dict[str, str]:
        """
        Converts a LangChain message (HumanMessage, AIMessage) back to a dictionary format.

        Parameters
        ----------
        message : BaseMessage
            A message in LangChain format to convert.

        Returns
        -------
        Dict[str, str]
            The message in dictionary format with keys 'role' and 'content'.
        """
        role = "user" if isinstance(message, HumanMessage) else "assistant"
        return {"role": role, "content": message.content}

    def interact(self, history: List[Dict[str, str]], messages: List[Dict[str, str]]) -> Dict[str, str]:
        """
        Takes conversation history and new messages, sends a request to the model, and returns the response.

        Parameters
        ----------
        history : List[Dict[str, str]]
            The conversation history.

        messages : List[Dict[str, str]]
            New messages to be processed.

        Returns
        -------
        Dict[str, str]
            The response from the model in dictionary format.
        """
        # Convert history and new messages to LangChain format
        langchain_history = ClientLangChain._convert_to_langchain_format(history)
        langchain_messages = ClientLangChain._convert_to_langchain_format(messages)

        # Update history and send request to LLM
        langchain_history += langchain_messages
        try:
            llm_result: LLMResult = self.client.generate(messages=[langchain_history])
            response_message: BaseMessage = AIMessage(content=llm_result.generations[0][0].text)
        except Exception as e:
            logger.warning(f"Chat inference failed with error: {e}")
            raise

        # Convert response back to dictionary format
        return ClientLangChain._convert_from_langchain_format(response_message)


class ClientOpenAI(ClientBase):
    """
    Wrapper for interacting with OpenAI-compatible API.
    This client can be used to interact with any language model that supports the OpenAI API, including but not limited to OpenAI models.

    Parameters
    ----------
    api_key : str
        The API key for authentication.
    base_url : str
        The base URL of the OpenAI-compatible API.
    model : str
        The model identifier to use for generating responses.
    temperature : float
        The temperature setting for controlling randomness in the model's responses.
    system_prompts : Optional[List[str]]
        List of system prompts for initializing the conversation context (optional).
    model_description : str
        Description of the model, including domain and other features (optional).

    Methods
    -------
    interact(history: List[Dict[str, str]], messages: List[Dict[str, str]]) -> Dict[str, str]
        Takes conversation history and new messages, sends a request to the OpenAI-compatible API, and returns the response.
    """

    def __init__(
        self,
        api_key: str,
        base_url: str,
        model: str,
        temperature: float = 0.1,
        system_prompts: Optional[List[str]] = None,
        model_description: Optional[str] = None,
    ):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.temperature = temperature
        self.system_prompts = system_prompts
        self.model_description = model_description


    # TODO: вернуть конвертер


    def interact(self, history: List[Dict[str, str]], messages: List[Dict[str, str]]) -> Dict[str, str]:
        """
        Takes conversation history and new messages, sends a request to the OpenAI-compatible API, and returns the response.

        Parameters
        ----------
        history : List[Dict[str, str]]
            The conversation history.

        messages : List[Dict[str, str]]
            New messages to be processed.

        Returns
        -------
        Dict[str, str]
            The response from the model in dictionary format.
        """
        # Add new messages to the history
        history += messages

        try:
            # Send the history to the model and get the result
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=history,
                temperature=self.temperature,  # Send messages to the API
            )
            # Extract the response text from the API
            response_content = completion.choices[0].message.content
            response_message = {"role": "assistant", "content": response_content}
        except Exception as e:
            logger.warning(f"Chat inference failed with error: {e}")
            raise

        # Add the response to the history and return the result
        history.append(response_message)
        return response_message
