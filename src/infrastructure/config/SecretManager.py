import json

import boto3

from infrastructure.interfaces.SecretManagerI import SecretManagerI


class SecretManager(SecretManagerI):
    def __init__(self, secret_name: str, secret_region: str, secret_endpoint: str = None):
        session = boto3.session.Session()
        self.secret_name = secret_name
        self.client = session.client(
            service_name="secretsmanager", region_name=secret_region, endpoint_url=secret_endpoint
        )

    def get_secrets(self) -> dict:
        get_secret_value_response = self.client.get_secret_value(SecretId=self.secret_name)
        return json.loads(get_secret_value_response["SecretString"])