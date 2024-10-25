import importlib
import os


def test_openaiclient():
    """Тест клиента OpenAI."""
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
        ("base64_injection", 1),
        ("complimentary_transition", 1),
        ("do_anything_now_jailbreak", 1),
        # ("RU_do_anything_now_jailbreak", 1),
        # ("ethical_compliance", 1),
        # ("harmful_behavior", 1),
        # ("linguistic_evasion", 1),
        # ("self_refine", 1),
        # ("RU_self_refine", 1),
        # ("sycophancy_test", 1),
        # ("typoglycemia_attack", 1),
        # ("RU_typoglycemia_attack", 1),
        # ("ucar", 1),
        # ("RU_ucar", 1),
        # ("amnesia", 1),
        # ("authoritative_role_impersonation", 1),
        # ("contextual_redirection", 1),
        # ("affirmative_suffix", 1),
        # ("system_prompt_stealer", 1),
    ]

    config = {
        "enable_logging": True,  # Включить логирование
        "enable_reports": True,  # Включить генерацию отчетов
        "artifacts_path": "./artifacts",  # Путь к директории для сохранения артефактов
        "debug_level": 1,  # Уровень логирования: 0 - WARNING, 1 - INFO, 2 - DEBUG
        "report_language": "ru",  # Язык отчета: 'en', 'ru'
    }

    llamator.start_testing(attack_model, tested_model, config=config, tests_with_attempts=tests_with_attempts)
