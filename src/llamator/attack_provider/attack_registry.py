import logging
from typing import List, Type

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
    basic_tests: List[str] = None,
    custom_tests: List[Type[TestBase]] = None,
) -> List[Type[TestBase]]:
    """
    Instantiate and return a list of test instances based on registered test classes
    and custom test classes.

    Parameters
    ----------
    client_config : ClientConfig
        Configuration object for the client.
    attack_config : AttackConfig
        Configuration object for the attack.
    basic_tests : List[str], optional
        List of basic test names that need to be instantiated (default is None).
    custom_tests : List[Type[TestBase]], optional
        List of custom test classes that need to be instantiated (default is None).

    Returns
    -------
    List[Type[TestBase]]
        A list of instantiated test objects.
    """

    # List to store instantiated tests
    tests = []

    # Create instances of basic test classes
    if basic_tests is not None:
        for cls in test_classes:
            test_instance = cls(client_config, attack_config)
            if test_instance.test_name in basic_tests:
                logger.debug(f"Instantiating attack test class: {cls.__name__}")
                tests.append(test_instance)

    # Create instances of custom test classes
    if custom_tests is not None:
        for custom_test in custom_tests:
            test_instance = custom_test(client_config, attack_config)
            logger.debug(f"Instantiating attack test class: {cls.__name__}")
            tests.append(test_instance)

    # Return the list of all instantiated tests
    return tests
