# main.py
import logging

from app.App import App
from containers import Container


def lambda_handler(
    event: dict,
    context: dict | None = None,
):
    try:
        logging.info("lambda_handler called")

        container = Container()
        container.wire(modules=["src.main"])

        app = App()
        app.run(event, context)

    except Exception as e:
        logging.error("Error in lambda_handler: %s", str(e))
