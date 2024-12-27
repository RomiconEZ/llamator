import logging
from abc import ABC, abstractmethod
from typing import Callable, Dict, List, Optional

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

    system_prompts : List[Dict[str, str]]
        A list of system prompts used to initialize the conversation (if any).

    history : List[Dict[str, str]]
        The conversation history, containing both user and assistant messages.

    use_history : Optional[bool]
        Determines whether to use the existing conversation history.
        If False, only the system prompts and the current user prompt are used.
        Defaults to True.

    Methods
    -------
    say(user_prompt: str, use_history: bool = True) -> str
        Sends a user message to the LLM, updates the conversation history, and returns the assistant's response.

    clear_history() -> None
        Clears the conversation history and re-initializes it with system prompts.
    """

    def __init__(
        self, client: ClientBase, system_prompts: Optional[List[str]] = None, use_history: Optional[bool] = True
    ):
        """
        Initializes the ChatSession with a client and optional system prompts.

        Parameters
        ----------
        client : ClientBase
            The client that handles interaction with the LLM.

        system_prompts : Optional[List[str]]
            A list of system prompts to guide the conversation from the start.

        use_history : Optional[bool]
            Determines whether to use the existing conversation history.
            If False, only the system prompts and the current user prompt are used.
            Defaults to True.
        """
        self.client = client
        self.use_history = use_history
        if system_prompts:
            self.system_prompts = [
                {"role": "system", "content": system_prompt_text} for system_prompt_text in system_prompts
            ]
        else:
            self.system_prompts = []
        # Initialize history with system prompts
        self.history = list(self.system_prompts)

    def say(self, user_prompt: str) -> str:
        """
        Sends a user message to the LLM, updates the conversation history based on the use_history flag,
        and returns the assistant's response.

        Parameters
        ----------
        user_prompt : str
            The user's message to be sent to the LLM.

        Returns
        -------
        str
            The response from the assistant (LLM) as a string.
        """
        logger.debug(f"say: system_prompts={self.system_prompts}")
        logger.debug(f"say: prompt={user_prompt}")

        # Interact with the LLM
        result = self.client.interact(
            history=self.history if self.use_history else list(self.system_prompts),
            messages=[{"role": "user", "content": user_prompt}],
        )
        logger.debug(f"say: result={result}")

        self.history.append({"role": "user", "content": user_prompt})
        self.history.append(result)

        return result["content"]

    def clear_history(self) -> None:
        """
        Clears the conversation history and re-initializes it with system prompts.
        """
        self.history = list(self.system_prompts)


class MultiStageInteractionSession:
    """
    Manages a multi-stage interaction between attacker and tested chat clients.

    Attributes
    ----------
    attacker_session : ChatSession
        The session for the attacker.
    tested_client_session : ChatSession
        The session for the tested client.
    stop_criterion : Optional[Callable[[List[Dict[str, str]]], bool]], optional
        A function that determines whether to stop the conversation based on the tested client's responses.
    refine_tested_client_prompt : Optional[Callable[..., str]], optional
        A function that refines the tested client's response before passing it to the attacker.
    refine_attacker_prompt : Optional[Callable[..., str]], optional
        A function that refines the attacker's response before passing it to the tested client.
    history_limit : int
        The maximum allowed history length for the attacker.
    current_step : int
        The current step of the attacker.
    refine_args : tuple
        Additional positional arguments for both refine_tested_client_prompt and refine_attacker_prompt.
    refine_kwargs : dict
        Additional keyword arguments for both refine_tested_client_prompt and refine_attacker_prompt.

    Methods
    -------
    start_conversation(start_prompt: str) -> bool
        Starts the conversation using the attacker and alternates between attacker and tested client until a stopping condition is met.
    get_attacker_responses() -> List[Dict[str, str]]
        Returns the responses of the attacker.
    get_tested_client_responses() -> List[Dict[str, str]]
        Returns the responses of the tested client.
    get_current_step() -> int
        Returns the current step of the attacker.
    """

    def __init__(
        self,
        attacker_session: ChatSession,
        tested_client_session: ChatSession,
        stop_criterion: Optional[Callable[[List[Dict[str, str]]], bool]] = None,
        refine_tested_client_prompt: Optional[Callable[..., str]] = None,
        refine_attacker_prompt: Optional[Callable[..., str]] = None,
        history_limit: int = 20,
        refine_args: Optional[tuple] = None,
        refine_kwargs: Optional[dict] = None,
    ):
        """
        Initializes the MultiStageInteractionSession.

        Parameters
        ----------
        attacker_session : ChatSession
            The session for the attacker.
        tested_client_session : ChatSession
            The session for the tested client.
        stop_criterion : Optional[Callable[[List[Dict[str, str]]], bool]], optional
            A function that takes the tested client's history and returns True if the conversation should stop.
            If None, a default criterion that always returns False is used. (default is None)
        refine_tested_client_prompt : Optional[Callable[..., str]], optional
            A function that refines the tested client's response before passing it to the attacker.
            If None, a default function that returns the response unchanged is used. (default is None)
        refine_attacker_prompt : Optional[Callable[..., str]], optional
            A function that refines the attacker's response before passing it to the tested client.
            If None, a default function that returns the response unchanged is used. (default is None)
        history_limit : int, optional
            The maximum number of messages allowed in the attacker's history. (default is 20)
        refine_args : Optional[tuple], optional
            Additional positional arguments for both refine_tested_client_prompt and refine_attacker_prompt. (default is None)
        refine_kwargs : Optional[dict], optional
            Additional keyword arguments for both refine_tested_client_prompt and refine_attacker_prompt. (default is None)
        """
        self.attacker_session = attacker_session
        self.tested_client_session = tested_client_session
        self.stop_criterion = stop_criterion if stop_criterion is not None else self.default_stop_criterion
        self.refine_tested_client_prompt = (
            refine_tested_client_prompt if refine_tested_client_prompt is not None else self.default_refine_tested_client_prompt
        )
        self.refine_attacker_prompt = (
            refine_attacker_prompt if refine_attacker_prompt is not None else self.default_refine_attacker_prompt
        )
        self.history_limit = history_limit
        self.current_step = 1
        self.refine_args = refine_args if refine_args is not None else ()
        self.refine_kwargs = refine_kwargs if refine_kwargs is not None else {}

    @staticmethod
    def default_stop_criterion(tested_client_history: List[Dict[str, str]]) -> bool:
        """
        Default stopping criterion that never stops the conversation.

        Parameters
        ----------
        tested_client_history : List[Dict[str, str]]
            The history of the tested client.

        Returns
        -------
        bool
            Always returns False.
        """
        return False

    @staticmethod
    def default_refine_tested_client_prompt(tested_client_response: str, *args, **kwargs) -> str:
        """
        Default refine_tested_client_prompt function that returns the response unchanged.

        Parameters
        ----------
        tested_client_response : str
            The response from the tested client.
        *args : tuple
            Additional positional arguments (not used).
        **kwargs : dict
            Additional keyword arguments (not used).

        Returns
        -------
        str
            The original tested client's response.

        # Usage Example:
        # If you have additional variables, they can be accessed via args or kwargs.
        # For example, to append a suffix from kwargs:
        # suffix = kwargs.get('suffix', '')
        # return tested_client_response + suffix
        """
        return tested_client_response

    @staticmethod
    def default_refine_attacker_prompt(attacker_response: str, *args, **kwargs) -> str:
        """
        Default refine_attacker_prompt function that returns the response unchanged.

        Parameters
        ----------
        attacker_response : str
            The response from the attacker.
        *args : tuple
            Additional positional arguments (not used).
        **kwargs : dict
            Additional keyword arguments (not used).

        Returns
        -------
        str
            The original attacker's response.

        # Usage Example:
        # If you have additional variables, they can be accessed via args or kwargs.
        # For example, to prepend a prefix from kwargs:
        # prefix = kwargs.get('prefix', '')
        # return prefix + attacker_response
        """
        return attacker_response

    def start_conversation(self, start_prompt: str) -> bool:
        """
        Starts the conversation with the attacker and alternates between attacker and tested client.

        Parameters
        ----------
        start_prompt : str
            The initial prompt sent by the attacker to start the conversation.

        Returns
        -------
        bool
            Returns True if the stopping criterion was met, otherwise False.
        """
        logger.debug("Starting multi-stage conversation.")

        # Attacker initiates the conversation
        attacker_response = self.attacker_session.say(start_prompt)
        logger.debug(f"Step {self.current_step}: Attacker response: {attacker_response}")

        while True:
            # Send attacker's response to the tested client
            tested_client_response = self.tested_client_session.say(attacker_response)
            logger.debug(f"Step {self.current_step}: Tested client response: {tested_client_response}")

            # Check stopping criterion
            if self.stop_criterion(tested_client_history=self.tested_client_session.history):
                logger.debug("Stopping criterion met.")
                return True

            # Check history limit
            if self.current_step >= self.history_limit:
                logger.debug("History limit exceeded.")
                return False

            # Refine the tested client's response before sending to attacker
            refined_tested_client_response = self.refine_tested_client_prompt(
                tested_client_response, *self.refine_args, **self.refine_kwargs
            )
            logger.debug(f"Step {self.current_step}: Refined tested client response: {refined_tested_client_response}")

            # Send the refined response to the attacker
            attacker_response = self.attacker_session.say(refined_tested_client_response)
            logger.debug(f"Step {self.current_step}: Attacker response: {attacker_response}")

            # Increment step
            self.current_step += 1
            logger.debug(f"Current step incremented to: {self.current_step}")

            # Refine the attacker's response before the next loop iteration
            refined_attacker_response = self.refine_attacker_prompt(
                attacker_response, *self.refine_args, **self.refine_kwargs
            )
            logger.debug(f"Step {self.current_step}: Refined attacker response: {refined_attacker_response}")

            # Update attacker_response for the next iteration
            attacker_response = refined_attacker_response

    def get_attacker_responses(self) -> List[Dict[str, str]]:
        """
        Retrieves the responses of the attacker.

        Returns
        -------
        List[Dict[str, str]]
            The responses of the attacker's session.
        """
        return [message for message in self.attacker_session.history if message["role"] == "assistant"]

    def get_tested_client_responses(self) -> List[Dict[str, str]]:
        """
        Retrieves the responses of the tested client.

        Returns
        -------
        List[Dict[str, str]]
            The responses of the tested client's session.
        """
        return [message for message in self.tested_client_session.history if message["role"] == "assistant"]

    def get_current_step(self) -> int:
        """
        Returns the current step of the attacker.

        Returns
        -------
        int
            The current step of the attacker.
        """
        return self.current_step
