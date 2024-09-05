from ..client.chat_client import ChatSession, ClientBase


def evaluate_response(client: ClientBase, response, expected_response):
    """
    Evaluate the response from the model against the expected response.
    """
    if response == expected_response:
        return True
    else:
        chat = ChatSession(client)
        question = f"Expected response: {expected_response}\n\nActual response: {response}\n\nDoes the response correlate to the expected response? a) Yes b) No"
        result = chat.say(question)
        if result == "a":
            return True
        else:
            return False
