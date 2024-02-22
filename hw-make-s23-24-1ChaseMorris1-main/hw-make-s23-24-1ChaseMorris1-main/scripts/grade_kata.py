import logging
import tomllib
from logging.config import dictConfig
from pathlib import Path
from time import sleep

import requests

dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] [%(process)d] [%(levelname)s] in %(module)s: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S %z",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["console"]},
    }
)


class ApiError(Exception):
    pass


def user_complete_challenge(
    codewars_id: str, challenge_id: str, delay_between_request=0.8
) -> bool:
    """True if user compelete kata with a slug `challenge_slug`."""
    if len(codewars_id.strip()) == 0:
        # Empty string for a user id is automatically marked as false.
        return False

    current_page = 0
    while True:
        logging.debug("{}: searching on page {}".format(codewars_id, current_page + 1))
        payload = {"page": current_page}
        response_obj = requests.get(
            f"https://www.codewars.com/api/v1/users/{codewars_id}/code-challenges/completed",
            params=payload,
        )

        if response_obj.status_code == 200:
            response = response_obj.json()
            if "success" in response.keys() and not response["success"]:
                raise ApiError("api responds with '{}'".format(response["reason"]))
            if "data" not in response.keys():
                raise ApiError("api responds payload that does not contain 'data' key")

            logging.debug("full response:")
            logging.debug(response)

            for kata in response["data"]:
                if kata["id"] == challenge_id:
                    logging.info(
                        "user '{}' completed '{}' ({}) - found on page {}".format(
                            codewars_id, kata["name"], kata["id"], current_page + 1
                        )
                    )
                    return True

            # The target kata may not be on this page.
            if response["totalPages"] - (current_page + 1) <= 0:
                # Reached the end of the pages.
                return False
            current_page += 1

        elif response_obj.status_code == 404:
            raise ApiError("cannot find user or challenge")

        sleep(delay_between_request)


if __name__ == "__main__":
    config_path = Path(__file__).parent.parent / "kata.toml"

    if not config_path.exists():
        raise FileNotFoundError(f"cannot find {config_path}")

    with open(config_path, "rb") as in_f:
        config = tomllib.load(in_f)
        if len(config["kata"]["username"].strip()) == 0:
            raise ValueError("username is empty")

        if user_complete_challenge(config["kata"]["username"], config["kata"]["id"]):
            print("Checking kata ... pass")
        else:
            print("Checking kata ... fail")
