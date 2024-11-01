import importlib
import os

from dotenv import load_dotenv


def test_openaiclient():
    """Tests OpenAI client from local LLaMator lib.
    
    Environment variables
    ----------
    OPENAI_CLIENT_API_KEY : str
        API key for OpenAI compatible API
    OPENAI_CLIENT_BASEURL : str
        URL of OpenAI compatible API
    OPENAI_CLIENT_MODEL : str
        Type of model
    """
    # Перезагрузка необходимых модулей
    import llamator.client.specific_chat_clients
    import llamator.main

    importlib.reload(llamator.client.specific_chat_clients)
    importlib.reload(llamator.main)

    from llamator.client.specific_chat_clients import ClientOpenAI

    api_key = os.getenv("OPENAI_CLIENT_API_KEY")
    base_url = os.getenv("OPENAI_CLIENT_BASEURL")
    model = os.getenv("OPENAI_CLIENT_MODEL")

    attack_model = ClientOpenAI(
        api_key=api_key,
        base_url=base_url,
        model=model,
        temperature=0.1,
        system_prompts=["You are a strong model."],
    )

    tested_model = ClientOpenAI(
        api_key=api_key,
        base_url=base_url,
        model=model,
        temperature=0.1,
        system_prompts=["You are a strong model."],
    )

    tests_with_attempts = [
        ("aim_jailbreak", 2),
        # ("base64_injection", 2),
        # ("complimentary_transition", 2),
        # ("do_anything_now_jailbreak", 2),
        # ("RU_do_anything_now_jailbreak", 2),
        # ("ethical_compliance", 2),
        # ("harmful_behavior", 2),
        # ("linguistic_evasion", 2),
        # ("past_tense", 2),
        # ("sycophancy_test", 2),
        # ("typoglycemia_attack", 2),
        # ("RU_typoglycemia_attack", 2),
        # ("ucar", 2),
        # ("RU_ucar", 2),
    ]

    config = {
        "enable_logging": True,  # Включить логирование
        "enable_reports": True,  # Включить генерацию отчетов
        "artifacts_path": "./artifacts",  # Путь к директории для сохранения артефактов
        "debug_level": 1,  # Уровень логирования: 0 - WARNING, 1 - INFO, 2 - DEBUG
        "report_language": "ru",  # Язык отчета: 'en', 'ru'
    }

    from llamator.main import start_testing

    start_testing(attack_model, tested_model, config=config, tests_with_attempts=tests_with_attempts)


def test_langchainclient_yandexgpt():
    """Tests LangChain client from local LLaMator lib using Yandex GPT backend.
    
    Environment variables
    ----------
    YC_API_KEY : str
        Yandex Cloud API key
    FOLDER_ID : str
        Yandex Cloud folder ID
    """
    # Загружаем переменные окружения из .env файла
    load_dotenv()

    # Перезагрузка необходимых модулей
    import llamator.client.specific_chat_clients
    import llamator.main

    importlib.reload(llamator.client.specific_chat_clients)
    importlib.reload(llamator.main)

    # Получаем переменные из окружения
    folder_ID = os.getenv("FOLDER_ID")

    from llamator.client.specific_chat_clients import ClientLangChain

    attack_model = ClientLangChain(
        backend="yandex_gpt",
        system_prompts=["You are a model for generating attacks on other models"],
        model_uri=f"gpt://{folder_ID}/yandexgpt-lite/latest",
    )

    tested_model = ClientLangChain(
        backend="yandex_gpt",
        model_description="You are a support bot",
        model_uri=f"gpt://{folder_ID}/yandexgpt-lite/latest",
    )

    tests_with_attempts = [
        ("aim_jailbreak", 2),
        # ("base64_injection", 2),
        # ("complimentary_transition", 2),
        # ("do_anything_now_jailbreak", 2),
        # ("RU_do_anything_now_jailbreak", 2),
        # ("ethical_compliance", 2),
        # ("harmful_behavior", 2),
        # ("linguistic_evasion", 2),
        # ("past_tense", 2),
        # ("sycophancy_test", 2),
        # ("typoglycemia_attack", 2),
        # ("RU_typoglycemia_attack", 2),
        # ("ucar", 2),
        # ("RU_ucar", 2),
    ]
    
    config = {
        "enable_logging": True,  # Включить логирование
        "enable_reports": True,  # Включить генерацию отчетов
        "artifacts_path": "./artifacts",  # Путь к директории для сохранения артефактов
        "debug_level": 1,  # Уровень логирования: 0 - WARNING, 1 - INFO, 2 - DEBUG
        "report_language": "ru",  # Язык отчета: 'en', 'ru'
    }

    from llamator.main import start_testing

    start_testing(attack_model, tested_model, config=config, tests_with_attempts=tests_with_attempts)
