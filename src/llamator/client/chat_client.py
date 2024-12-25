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
    Manages a multi-stage interaction between attacking and defending chat models.

    Attributes
    ----------
    attacker_session : ChatSession
        The session for the attacking model.
    defender_session : ChatSession
        The session for the defending model.
    stop_criterion : Optional[Callable[[List[Dict[str, str]]], bool]], optional
        A function that determines whether to stop the conversation based on the defender's responses.
    history_limit : int
        The maximum allowed history length for the attacking model.
    current_step : int
        The current step of the attacking model.

    Methods
    -------
    start_conversation(start_prompt: str) -> bool
        Starts the conversation using the attacking model and alternates between attacker and defender until a stopping condition is met.
    get_attacker_responses() -> List[Dict[str, str]]
        Returns the responses of the attacking model.
    get_defender_responses() -> List[Dict[str, str]]
        Returns the responses of the defending model.
    get_current_step() -> int
        Returns the current step of the attacking model.
    """

    def __init__(
        self,
        attacker_session: ChatSession,
        defender_session: ChatSession,
        stop_criterion: Optional[Callable[[List[Dict[str, str]]], bool]] = None,
        history_limit: int = 20,
    ):
        """
        Initializes the MultiStageInteractionSession with attacker and defender sessions, a stopping criterion, and a history limit.

        Parameters
        ----------
        attacker_session : ChatSession
            The session for the attacking model.
        defender_session : ChatSession
            The session for the defending model.
        stop_criterion : Optional[Callable[[List[Dict[str, str]]], bool]], optional
            A function that takes the defender's history and returns True if the conversation should stop.
            If None, a default criterion that always returns False is used. (default is None)
        history_limit : int, optional
            The maximum number of messages allowed in the attacking model's history. (default is 20)
        """
        self.attacker_session = attacker_session
        self.defender_session = defender_session
        self.stop_criterion = stop_criterion if stop_criterion is not None else self.default_stop_criterion
        self.history_limit = history_limit
        self.current_step = 1

    @staticmethod
    def default_stop_criterion(defender_history: List[Dict[str, str]]) -> bool:
        """
        Default stopping criterion that never stops the conversation.

        Parameters
        ----------
        defender_history : List[Dict[str, str]]
            The history of the defender model.

        Returns
        -------
        bool
            Always returns False.
        """
        return False

    def start_conversation(self, start_prompt: str) -> bool:
        """
        Starts the conversation with the attacking model and alternates between attacker and defender.

        Parameters
        ----------
        start_prompt : str
            The initial prompt sent by the attacking model to start the conversation.

        Returns
        -------
        bool
            Returns True if the stopping criterion was met, otherwise False.
        """
        logger.debug("Starting multi-stage conversation.")

        # Атакующая модель начинает разговор
        attacker_response = self.attacker_session.say(start_prompt)
        logger.debug(f"Current step: {self.current_step}")
        logger.debug(f"Attacker response: {attacker_response}")

        while True:
            # Передаём ответ атакующей модели защищающей модели
            defender_response = self.defender_session.say(attacker_response)
            logger.debug(f"Defender response: {defender_response}")

            # Проверяем критерий остановки
            if self.stop_criterion(defender_history=self.defender_session.history):
                logger.debug("Stopping criterion met.")
                return True

            # Проверяем ограничение на длину истории атакующей модели
            if self.current_step == self.history_limit:
                logger.debug("History limit exceeded.")
                return False

            # Передаём ответ защищающей модели атакующей модели
            self.current_step += 1
            logger.debug(f"Current step: {self.current_step}")
            attacker_response = self.attacker_session.say(defender_response)
            logger.debug(f"Attacker response: {attacker_response}")

    def get_attacker_responses(self) -> List[Dict[str, str]]:
        """
        Retrieves the responses of the attacking model.

        Returns
        -------
        List[Dict[str, str]]
            The responses of the attacking model's session.
        """
        return [message for message in self.attacker_session.history if message["role"] == "assistant"]

    def get_defender_responses(self) -> List[Dict[str, str]]:
        """
        Retrieves the responses of the defending model.

        Returns
        -------
        List[Dict[str, str]]
            The responses of the defending model's session.
        """
        return [message for message in self.defender_session.history if message["role"] == "assistant"]

    def get_current_step(self) -> int:
        """
        Returns the current step of the attacking model.

        Returns
        -------
        int
            The current step of the attacking model.
        """
        return self.current_step
