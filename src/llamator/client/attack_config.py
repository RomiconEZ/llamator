from ..client.client_config import ClientConfig


class AttackConfig:
    def __init__(self, attack_client: ClientConfig):
        self.attack_client = attack_client
