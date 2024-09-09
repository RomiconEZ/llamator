#!/usr/bin/env python3
import logging

import os

from dotenv import load_dotenv
# At this stage, the api keys that the user sets are loaded
dotenv_path = os.path.join(os.getcwd(), ".env")
load_dotenv(dotenv_path)
from typing import List, Type, Optional

# Initializing colorama for color output in the console
import colorama

from .attack_provider.run_tests import setup_models_and_tests
from .attack_provider.test_base import TestBase
from .client.chat_client import ClientBase
from .format_output.logo import print_logo
from .initial_validation import validate_custom_tests, validate_model, validate_tests
from .ps_logging import setup_logging

colorama.init()

# Defining constants for text reset and brightness
RESET = colorama.Style.RESET_ALL
BRIGHT = colorama.Style.BRIGHT


def start_testing(
    attack_model: ClientBase,
    tested_model: ClientBase,
    num_attempts: int = 1,
    num_threads: int = 1,
    tests: Optional[List[str]] = None,
    custom_tests: List[Type[TestBase]] = None,
    debug_level: int = 1,
):
    """
    Start testing.

    Parameters
    ----------
        attack_model : ClientBase
            The attacking model used to generate tests.
        tested_model : ClientBase
            The model being tested against the attacks.
        num_attempts : int, optional
            Number of attempts per test case (default is 1).
        num_threads : int, optional
            Number of threads for parallel test execution (default is 1).
        tests : Optional[List[str]], optional
            List of test names to execute (default is an empty list).
            Available tests: aim_jailbreak, base64_injection, complimentary_transition,
            do_anything_now_jailbreak, ethical_compliance, harmful_behavior, linguistic_evasion,
            self_refine, sycophancy_test, typoglycemia_attack, ucar.
        custom_tests : List[Type[TestBase]], optional
            List of custom test instances (default is an empty list).
        debug_level : int, optional
            Level of logging verbosity (default is 1).
            debug_level = 0 - WARNING.
            debug_level = 1 - INFO.
            debug_level = 2 - DEBUG.

    Returns
    -------
        None
    """

    # Setting the logging level (default is 1)
    setup_logging(debug_level)

    # Program logo output
    print_logo()

    # Checking the operation of the attacking model
    if not validate_model(attack_model):
        logging.error("Attack model failed validation.")
        return

    # Checking the operation of the tested model
    if not validate_model(tested_model):
        logging.error("Tested model failed validation.")
        return

    # Check the submitted list of tests
    if tests and not validate_tests(tests):
        logging.error("The test list contains invalid values.")
        return

    # Check the submitted list of custom tests
    if custom_tests and not validate_custom_tests(custom_tests):
        logging.error("One or more custom tests failed validation.")
        return

    # Running tests with the specified parameters
    setup_models_and_tests(
        attack_model, tested_model, num_attempts, num_threads, tests, custom_tests
    )

    # Thank you message at the end of the program
    logging.info(
        f"Completion of testing"
    )
    print(
        f"{BRIGHT}{colorama.Fore.CYAN}Thank you for using LLAMATOR!{RESET}"
    )
