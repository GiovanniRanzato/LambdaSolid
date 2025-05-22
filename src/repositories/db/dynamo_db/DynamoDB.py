import boto3

from infrastructure.interfaces.ConfigI import ConfigI


class DynamoDB:
    def __init__(self, config: ConfigI):
        self.resource = boto3.resource(
            "dynamodb", region_name=config.get("DYNAMODB_REGION"), endpoint_url=config.get("LOCALSTACK_ENDPOINT_URL")
        )
