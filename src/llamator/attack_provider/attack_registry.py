import logging
import os
from typing import List, Optional, Tuple, Type

from ..attack_provider.test_base import TestBase
from ..client.attack_config import AttackConfig
from ..client.client_config import ClientConfig

logger = logging.getLogger(__name__)

# Registry of attack test classes
test_classes = []


# Decorator used to register attack test classes
def register_test(cls) -> None:
    """
    Decorator that registers test types.

    Parameters
    ----------
    cls : class
        The class of the test that needs to be registered.
    """
    global test_classes
    logger.debug(f"Registering attack test class: {cls.__name__}")
    test_classes.append(cls)
    return


def instantiate_tests(
    client_config: ClientConfig,
    attack_config: AttackConfig,
    basic_tests_with_attempts: Optional[List[Tuple[str, int]]] = None,
    custom_tests_with_attempts: Optional[List[Tuple[Type[TestBase], int]]] = None,
    artifacts_path: Optional[str] = None,
    multistage_depth: Optional[int] = 20,
) -> List[TestBase]:
    """
    Instantiate and return a list of test instances based on registered test classes
    and custom test classes.

    Parameters
    ----------
    client_config : ClientConfig
        Configuration object for the client.
    attack_config : AttackConfig
        Configuration object for the attack.
    basic_tests_with_attempts : List[Tuple[str, int]], optional
        List of basic test names and repeat counts (default is None).
    custom_tests_with_attempts : List[Tuple[Type[TestBase], int]], optional
        List of custom test classes and repeat counts (default is None).
    artifacts_path : str, optional
        The path to the folder where artifacts (logs, reports) will be saved (default is './artifacts').
    multistage_depth : int, optional
        The maximum allowed history length that can be passed to multi-stage interactions (default is 20).

    Returns
    -------
    List[TestBase]
        A list of instantiated test objects.
    """
    global test_classes

    csv_report_path = None

    if artifacts_path is not None:
        # Create 'csv_report' directory inside artifacts_path
        csv_report_path = os.path.join(artifacts_path, "csv_report")
        os.makedirs(csv_report_path, exist_ok=True)

    # List to store instantiated tests
    tests = []

    # Create instances of basic test classes
    if basic_tests_with_attempts is not None:
        basic_tests_dict = dict(basic_tests_with_attempts)
        for cls in test_classes:
            if cls.test_name in basic_tests_dict:
                num_attempts = basic_tests_dict[cls.test_name]

                test_instance = cls(
                    client_config,
                    attack_config,
                    artifacts_path=csv_report_path,
                    num_attempts=num_attempts,
                    multistage_depth=multistage_depth,
                )
                logger.debug(f"Instantiating attack test class: {cls.__name__} with {num_attempts} attempts")
                tests.append(test_instance)

    # Process custom tests with attempts
    if custom_tests_with_attempts is not None:
        for custom_test_cls, num_attempts in custom_tests_with_attempts:
            try:
                test_instance = custom_test_cls(
                    client_config,
                    attack_config,
                    artifacts_path=csv_report_path,
                    num_attempts=num_attempts,
                    multistage_depth=multistage_depth,
                )
                logger.debug(
                    f"Instantiating custom test class: {custom_test_cls.__name__} with {num_attempts} attempts"
                )
                tests.append(test_instance)
            except Exception as e:
                logger.error(f"Error instantiating custom test {custom_test_cls.__name__}: {e}")

    # Return the list of all instantiated tests
    return tests
