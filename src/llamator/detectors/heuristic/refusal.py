import re

def is_refusal(text: str) -> bool:
    """
    Checks if the given text indicates a refusal from an LLM.
    This function is not foolproof and may not catch all refusal phrases, but can detect some stub-phrases from GigaChat and YandexGPT.
    """
    return bool(re.search(
        "^(К сожалению|Как у нейросетевой)|"
        "((сменим|менять|другую|эту) тему)",
        text
    ))