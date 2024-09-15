import os
import json


def get_challenges():
    challenge_path = os.getcwd().replace('\\', '/') + f"/app/challenges"
    data = {}

    for language in [folder.name for folder in os.scandir(challenge_path) if folder.is_dir()]:
        data[language] = {}
        for challenge in [folder.name for folder in os.scandir(f"{challenge_path}/{language}") if folder.is_dir()]:
            config = open(f"{challenge_path}/{language}/{challenge}/config.json", 'r')
            json_config = json.load(config)
            data[language][challenge] = {
                "name": json_config["name"],
                "description": json_config["description"],
                "numberOfArgs": json_config["numberOfArgs"],
                "difficulty": json_config["difficulty"]
            }
            config.close()

    return data


def match_challenge(user_1: int, user_2: int):
    return 5;


challenge_data = get_challenges()