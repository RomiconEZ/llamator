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

    tests = [
        "aim_jailbreak",
        "base64_injection",
        # "complimentary_transition",
        # "do_anything_now_jailbreak",
        # "RU_do_anything_now_jailbreak",
        # "ethical_compliance",
        # "harmful_behavior",
        # "linguistic_evasion",
        # "self_refine",
        # "RU_self_refine",
        # "sycophancy_test",
        # "typoglycemia_attack",
        # "RU_typoglycemia_attack",
        # "ucar",
        # "RU_ucar",
        # "amnesia",
        # "authoritative_role_impersonation",
        # "contextual_redirection",
        # "affirmative_suffix",
        # "system_prompt_stealer",
    ]

    config = {
        "enable_logging": True,  # Включить логирование
        "enable_reports": True,  # Включить генерацию отчетов
        "artifacts_path": "./artifacts",  # Путь к директории для сохранения артефактов
        "debug_level": 1,  # Уровень логирования: 0 - WARNING, 1 - INFO, 2 - DEBUG
    }

    llamator.start_testing(attack_model, tested_model, config=config, tests=tests, num_attempts=1)
