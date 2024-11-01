import importlib
import os


def test_openaiclient():
    """Tests OpenAI client from public LLaMator lib.
    
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
    import llamator

    importlib.reload(llamator)

    api_key = os.getenv("OPENAI_CLIENT_API_KEY")
    base_url = os.getenv("OPENAI_CLIENT_BASEURL")
    model = os.getenv("OPENAI_CLIENT_MODEL")

    attack_model = llamator.ClientOpenAI(
        api_key=api_key,
        base_url=base_url,
        model=model,
        temperature=0.1,
        system_prompts=["You are a strong model."],
    )

    tested_model = llamator.ClientOpenAI(
        api_key=api_key,
        base_url=base_url,
        model=model,
        temperature=0.1,
        system_prompts=["You are a strong model."],
    )

    tests_with_attempts = [
        ("aim_jailbreak", 2),
        ("base64_injection", 2),
        ("complimentary_transition", 2),
        ("do_anything_now_jailbreak", 2),
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

    llamator.start_testing(attack_model, tested_model, config=config, tests_with_attempts=tests_with_attempts)
