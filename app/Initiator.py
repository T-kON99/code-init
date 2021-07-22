import requests
from bs4 import BeautifulSoup
import time
import os
from typing import Union
import app.read as read
import config.config as config
from app.Platform import Uhunt, ProjectEuler, Platform
import app.utils as utils


class Initiator(object):
    def __init__(self, platform: str):
        self.__platform_handler = {
            "projecteuler": ProjectEuler,
            "uhunt": Uhunt,
        }
        assert (
            platform in self.__platform_handler
        ), f"Unsupported platform given {platform}"
        self.__platform = platform

    def generate_code(self, problem_no: int, src_lang: str, overwrite: bool = False):
        SRC_FILE_PATH = f"{config.ROOT}/{problem_no}.{src_lang}"
        handler: Platform
        handler = self.__platform_handler[self.__platform]()
        problem_details = handler.get_problem_no(problem_no, overwrite=overwrite)
        problem_text = problem_details["title"] + "\n\n" + problem_details["content"]
        if overwrite or not os.path.isfile(SRC_FILE_PATH):
            print(f"[INFO]: Creating file {SRC_FILE_PATH}")
            with open(SRC_FILE_PATH, mode="w", encoding="utf8") as src_file:
                src_file.write(utils.insert_src(src_lang, problem_text))
        else:
            print(
                f"[INFO]: Skipping creation of file {SRC_FILE_PATH} as it already exists"
            )
        return SRC_FILE_PATH


if __name__ == "__main__":
    print("Running from submodule")
    a = Initiator("projecteuler").generate_code(1, "cpp")
    print(a)
