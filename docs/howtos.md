# How To Use

## Notebooks Examples
* RAG Chatbot testing via API (RU) - [GitHub](https://github.com/RomiconEZ/llamator/blob/main/examples/llamator-api.ipynb)
* Testing the Gandalf webbot - [GitHub](https://github.com/RomiconEZ/llamator/blob/main/examples/llamator-selenium.ipynb)
* Telegram bot testing via Telethon (RU) - [GitHub](https://github.com/RomiconEZ/llamator/blob/main/examples/llamator-telegram.ipynb)
* LangChain client testing with custom attack (RU)](https://github.com/RomiconEZ/llamator/blob/main/examples/llamator-langchain-custom-attack.ipynb)

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

# List of tests
tests = [
    "aim_jailbreak",
    "base64_injection",
    "complimentary_transition",
    "do_anything_now_jailbreak",
    "RU_do_anything_now_jailbreak",
    "ethical_compliance",
    "harmful_behavior",
    "linguistic_evasion",
    "sycophancy_test",
    "typoglycemia_attack",
    "past_tense",
    "RU_typoglycemia_attack",
    "ucar",
    "RU_ucar",
]

# Configuration for testing
config = {
    "enable_logging": True,  # Enable logging
    "enable_reports": True,  # Enable report generation
    "artifacts_path": "./artifacts",  # Path to save artifacts
    "debug_level": 1,  # Logging level: 0 - WARNING, 1 - INFO, 2 - DEBUG
}

# Start testing
llamator.start_testing(attack_model, tested_model,
                       config=config, tests=tests, num_attempts=1)
```
