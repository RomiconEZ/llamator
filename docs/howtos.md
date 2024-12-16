# How To Use

## Notebooks Examples

- **RAG Chatbot testing via API (RU)** - [GitHub](https://github.com/RomiconEZ/llamator/blob/release/examples/llamator-api.ipynb)
- **Testing the Gandalf webbot** - [GitHub](https://github.com/RomiconEZ/llamator/blob/release/examples/llamator-selenium.ipynb)
- **Telegram bot testing via Telethon (RU)** - [GitHub](https://github.com/RomiconEZ/llamator/blob/release/examples/llamator-telegram.ipynb)
- **LangChain client testing with custom attack (RU)** - [GitHub](https://github.com/RomiconEZ/llamator/blob/release/examples/llamator-langchain-custom-attack.ipynb)
- **WhatsApp client testing via Selenium (ENG)** - [GitHub](https://github.com/RomiconEZ/llamator/blob/release/examples/llamator-whatsapp.ipynb)


## Installation Guide

```bash
pip install llamator
```

## Usage Guide (using LM Studio)

```python
import llamator

# Initialize the attack model
attack_model = llamator.ClientOpenAI(
    api_key="lm-studio",
    base_url="http://localhost:1234/v1",
    model="model-identifier",
    temperature=0.1,
    system_prompts=["You are an attacking model."],
)

# Initialize the tested model
tested_model = llamator.ClientOpenAI(
    api_key="lm-studio",
    base_url="http://localhost:1234/v1",
    model="model-identifier",
    temperature=0.1,
    system_prompts=["You are a defensive model."],
)

# List of tests with the number of attempts
tests_with_attempts = [
    ("aim_jailbreak", 2),
    ("base64_injection", 2),
    ("complimentary_transition", 2),
    ("do_anything_now_jailbreak", 2),
    # Uncomment the following lines to include additional tests
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

# Configuration for testing
config = {
    "enable_logging": True,  # Enable logging
    "enable_reports": True,  # Enable report generation
    "artifacts_path": "./artifacts",  # Path to save artifacts
    "debug_level": 1,  # Logging level: 0 - WARNING, 1 - INFO, 2 - DEBUG
    "report_language": "en",  # Report language: 'en', 'ru'
}

# Start testing
llamator.start_testing(
    attack_model,
    tested_model,
    config=config,
    tests_with_attempts=tests_with_attempts
)
```
