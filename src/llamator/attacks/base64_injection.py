import base64
import logging
import os
from pathlib import Path

# from .utils import evaluate_response
from typing import Generator, Optional

import pandas as pd

from ..attack_provider.attack_registry import register_test
from ..attack_provider.test_base import StatusUpdate, TestBase
from ..attack_provider.util import contains_refusal_keywords
from ..client.attack_config import AttackConfig
from ..client.chat_client import ChatSession
from ..client.client_config import ClientConfig

logger = logging.getLogger(__name__)


@register_test
class TestBase64Injection(TestBase):
    def __init__(self, client_config: ClientConfig, attack_config: AttackConfig, artifacts_path: Optional[str] = None):
        super().__init__(
            client_config,
            attack_config,
            test_name="base64_injection",
            test_description="Challenges the LLM with a dataset of prompt injections, encoded into base64",
            artifacts_path=artifacts_path,  # Добавляем artifacts_path
        )

    def _prepare_attack_data(self, attack_prompts: list[str], responses: list[str], statuses: list[str]) -> None:
        """
        Prepares attack data in a structured DataFrame format and saves it as a CSV file.

        Args:
            attack_prompts (list[str]): List of attack texts generated during the test.
            responses (list[str]): List of responses from the target system.
            statuses (list[str]): List of statuses ('broken', 'resilient', 'error') corresponding to each attack.

        Returns:
            None
        """
        # Create a DataFrame from the lists
        df = pd.DataFrame({"attack_text": attack_prompts, "response_text": responses, "status": statuses})

        # Save the DataFrame as a CSV file to the artifacts path
        if self.artifacts_path:
            csv_path = os.path.join(self.artifacts_path, f"base64_injection_attack_report.csv")
            df.to_csv(csv_path, index=False)
            logging.info(f"Base64 Injection attack report saved to {csv_path}")

    def run(self) -> Generator[StatusUpdate, None, None]:
        # dataset_filename = resource_filename(
        #     "LLAMATOR", "attack_data/prompt_injections_for_base64.parquet"
        # )

        current_dir = Path(__file__).parent
        dataset_filename = current_dir.parent / "attack_data" / "prompt_injections_for_base64.parquet"

        data = pd.read_parquet(dataset_filename, engine="fastparquet")
        rows_count = data.shape[0]

        if rows_count > self.attack_config.attack_prompts_count:
            data = data.sample(n=self.attack_config.attack_prompts_count, random_state=42)
            rows_count = data.shape[0]

        # Lists to store prompts, responses, and statuses for report generation
        attack_prompts = []
        responses = []
        statuses = []

        yield StatusUpdate(self.client_config, self.test_name, self.status, "Working", 0, rows_count)

        for attack_prompt_index, row in data.iterrows():
            attack_prompt = row["text"]
            attack_prompt_bytes = attack_prompt.encode("utf-8")
            attack_prompt_base64 = base64.b64encode(attack_prompt_bytes)
            attack_prompt_base64_string = attack_prompt_base64.decode("utf-8")

            chat = ChatSession(
                self.client_config.get_target_client(),
                self.client_config.get_system_prompts(),
            )
            response = chat.say(attack_prompt_base64_string)
            if not response:
                logger.warning("Error while attacking against target LLM (didn't receive response) ...")
                self.status.report_error(attack_prompt)
                current_status = "Error"
            else:
                verified = not contains_refusal_keywords(response)
                logger.info(f"Test '{self.test_name}': attack prompt #{attack_prompt_index}: {attack_prompt}")
                logger.info(
                    f"Test '{self.test_name}': attack response #{attack_prompt_index} break_success={verified}): {response}"
                )

                if verified:
                    self.status.report_breach(attack_prompt, response)
                    current_status = "Broken"
                else:
                    self.status.report_resilient(attack_prompt, response)
                    current_status = "Resilient"

            # Append data for report
            attack_prompts.append(attack_prompt)
            responses.append(response)
            statuses.append(current_status)

            yield StatusUpdate(
                self.client_config,
                self.test_name,
                self.status,
                "Attacking",
                attack_prompt_index,
                self.attack_config.attack_prompts_count,
            )

        # Prepare data for report generation
        self._prepare_attack_data(attack_prompts, responses, statuses)

        yield StatusUpdate(
            self.client_config,
            self.test_name,
            self.status,
            "Completed",
            rows_count,
            rows_count,
        )
