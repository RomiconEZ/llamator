#!/usr/bin/env python3
import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
from typing import List, Optional, Type

import colorama
from dotenv import load_dotenv

from .attack_provider.run_tests import setup_models_and_tests
from .attack_provider.test_base import TestBase
from .attacks.utils import create_attack_report_from_artifacts
from .client.chat_client import ClientBase
from .format_output.logo import print_logo
from .initial_validation import validate_artifacts_path, validate_custom_tests, validate_model, validate_tests
from .ps_logging import setup_logging

# At this stage, the api keys that the user sets are loaded
dotenv_path = os.path.join(os.getcwd(), ".env")
load_dotenv(dotenv_path)
colorama.init()

# Defining constants for text reset and brightness
RESET = colorama.Style.RESET_ALL
BRIGHT = colorama.Style.BRIGHT


def start_testing(
    attack_model: ClientBase,
    tested_model: ClientBase,
    config: dict,
    num_attempts: int = 1,
    num_threads: int = 1,
    tests: Optional[List[str]] = None,
    custom_tests: List[Type[TestBase]] = None,
):
    """
    Start testing.

    Parameters
    ----------
        attack_model : ClientBase
            The attacking model used to generate tests.
        tested_model : ClientBase
            The model being tested against the attacks.
        config : dict
            Configuration dictionary with the following keys:
            - 'enable_logging' : bool
                Whether to enable logging.
            - 'enable_reports' : bool
                Whether to generate xlsx reports.
            - 'artifacts_path' : Optional[str]
                Path to the folder for saving artifacts.
            - 'debug_level' : int
                Level of logging verbosity (default is 1).
                debug_level = 0 - WARNING.
                debug_level = 1 - INFO.
                debug_level = 2 - DEBUG.
        num_attempts : int, optional
            Number of attempts per test case (default is 1).
        num_threads : int, optional
            Number of threads for parallel test execution (default is 1).
        tests : Optional[List[str]], optional
            List of test names to execute (default is an empty list).
            Available tests: aim_jailbreak, base64_injection, complimentary_transition,
            do_anything_now_jailbreak, RU_do_anything_now_jailbreak, ethical_compliance,
            harmful_behavior, linguistic_evasion, self_refine, RU_self_refine,
            sycophancy_test, typoglycemia_attack, RU_typoglycemia_attack, ucar, RU_ucar.
        custom_tests : List[Type[TestBase]], optional
            List of custom test instances (default is an empty list).

    Returns
    -------
        None
    """

    # Extract values from the config dictionary
    enable_logging = config.get("enable_logging", True)
    enable_reports = config.get("enable_reports", False)
    artifacts_path = config.get("artifacts_path", None)
    debug_level = config.get("debug_level", 1)

    start_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    if artifacts_path is None:
        enable_logging = False
        enable_reports = False
        artifacts_run_path = None
        print("Logging and reports have been disabled.")
    else:
        # Validate the artifacts path
        if not validate_artifacts_path(artifacts_path):
            print("Invalid artifacts path.")
            return
        elif enable_reports is True or enable_logging is True:
            # Create a new folder named 'llamato_run_{start_timestamp}' inside artifacts_path
            run_folder_name = f"LLAMATOR_run_{start_timestamp}"
            run_folder_path = os.path.join(artifacts_path, run_folder_name)
            os.makedirs(run_folder_path, exist_ok=True)

            # Update artifacts_path to point to the new run folder
            artifacts_run_path = run_folder_path

    # Setup logging if enabled
    if enable_logging:
        setup_logging(debug_level, artifacts_run_path)

    # Program logo output
    print_logo()

    # Validate attack model
    if not validate_model(attack_model):
        logging.error("Attack model failed validation.")
        return

    # Validate tested model
    if not validate_model(tested_model):
        logging.error("Tested model failed validation.")
        return

    # Validate the test list
    if tests and not validate_tests(tests):
        logging.error("The test list contains invalid values.")
        return

    # Validate custom tests
    if custom_tests and not validate_custom_tests(custom_tests):
        logging.error("One or more custom tests failed validation.")
        return

    if enable_reports:
        # Running tests with the specified parameters
        setup_models_and_tests(
            attack_model,
            tested_model,
            num_attempts,
            num_threads,
            tests,
            custom_tests,
            artifacts_path=artifacts_run_path,
        )
    else:
        setup_models_and_tests(
            attack_model, tested_model, num_attempts, num_threads, tests, custom_tests, artifacts_path=None
        )

    # Thank you message at the end of the program
    logging.info(f"Completion of testing")

    # Явное закрытие файла лога в конце программы
    for handler in logging.getLogger().handlers:
        if isinstance(handler, RotatingFileHandler):
            handler.close()

    if enable_reports:
        create_attack_report_from_artifacts(
            artifacts_dir=artifacts_run_path, csv_folder_name="csv_report", report_file_name="attacks_report.xlsx"
        )
        pass

    print(f"{BRIGHT}{colorama.Fore.CYAN}Thank you for using LLAMATOR!{RESET}")
