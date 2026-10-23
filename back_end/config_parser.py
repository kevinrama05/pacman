from typing import Union, TypedDict, cast
import json
import os


class ConfigDict(TypedDict):
    highscore_filename: str
    levels: int
    width: int
    height: int
    lives: int
    pacgum: int
    points_per_pacgum: int
    points_per_super_pacgum: int
    points_per_ghost: int
    seed: Union[int, float]
    level_max_timer: int


class ParseJSON:
    """
    This class is responsible for reading in the
    default_config.json file, validate the configurations
    and return the configurations in dictionary format.
    If they are missing required keys, or they have invalid
    values(e.g. negative numbers), it uses a default value.
    If there are unknown keys, they are ignored completely.

    Attributes:
        path (str): The path of the configuration file
    """
    def __init__(self, path: str) -> None:
        self.path = path

    def read_json(self) -> dict[str, Union[str, int, list[int]]]:
        """
        The read_json method reads from the default_configs.json file.
        It removes all the comments (lines starting with # or //) and
        empty lines.

        Args:
            None

        Returns:
            dict[str, Union[str, int]]: The .json file in dictionary format
        """
        with open(self.path, 'r') as file:
            str_file = ''
            for i in file.readlines():
                if i.strip() == '':
                    pass
                elif i.strip()[0] == '#':
                    pass
                elif i.strip()[0:2] == '//':
                    pass
                else:
                    str_file += i.strip()

        return cast(
            dict[str, Union[str, int, list[int]]], json.loads(str_file))

    def valid_highscore_filename(self, path: str) -> bool:
        """
        Checks if the filename for the highscore is vaild.
        If it is valid, returns True, else returns False.

        Args:
            path (str): The path wher the highscore is going to be saved

        Returns:
            bool: True if valid, else False
        """
        if not path or not path.endswith('.json'):
            return False
        if os.path.isdir(path):
            return False
        parent_dir = os.path.dirname(path)
        if parent_dir and not os.path.exists(parent_dir):
            return False
        try:
            with open(path, "a"):
                pass
        except PermissionError:
            return False
        except OSError:
            return False
        return True

    def validate_json(self) -> ConfigDict:
        """
        Checks and validates all the values in the dictionary. If the value is
        invalid, or a required key is missing completely, it uses a default
        value instead. For the unknown keys, they are skipped completely.

        Args:
            None

        Returns:
            ConfigDict: A dictionary of all the keys necessary for creating
                        the pacman game
        """
        json_dict = self.read_json()

        if 'highscore_filename' in json_dict:
            if isinstance(json_dict['highscore_filename'], str):
                if not self.valid_highscore_filename(
                        json_dict['highscore_filename']):
                    json_dict['highscore_filename'] = 'highscores.json'
            else:
                json_dict['highscore_filename'] = 'highscores.json'
        else:
            json_dict['highscore_filename'] = 'highscores.json'

        if 'levels' in json_dict:
            if isinstance(json_dict['levels'], int):
                if json_dict['levels'] > 20 or json_dict['levels'] < 1:
                    json_dict['levels'] = 10
            else:
                json_dict['levels'] = 10
        else:
            json_dict['levels'] = 10

        if 'height' in json_dict:
            if isinstance(json_dict['height'], int):
                if json_dict['height'] < 15 or json_dict['height'] > 35:
                    json_dict['height'] = 15
            else:
                json_dict['height'] = 15
        else:
            json_dict['height'] = 15

        if 'width' in json_dict:
            if isinstance(json_dict['width'], int):
                if json_dict['width'] < 15 or json_dict['width'] > 35:
                    json_dict['width'] = 15
            else:
                json_dict['width'] = 15
        else:
            json_dict['width'] = 15

        if 'pacgum' in json_dict:
            if isinstance(json_dict['pacgum'], int):
                max_pacgums = json_dict['height'] * json_dict['width'] - 26
                if (json_dict['pacgum'] < 42
                        or json_dict['pacgum'] > max_pacgums):
                    json_dict['pacgum'] = 42
            else:
                json_dict['pacgum'] = 42
        else:
            json_dict['pacgum'] = 42

        if 'lives' in json_dict:
            if isinstance(json_dict['lives'], int):
                if json_dict['lives'] > 8 or json_dict['lives'] < 1:
                    json_dict['lives'] = 3
            else:
                json_dict['lives'] = 3
        else:
            json_dict['lives'] = 3

        if 'points_per_pacgum' in json_dict:
            if isinstance(json_dict['points_per_pacgum'], int):
                if (json_dict['points_per_pacgum'] > 50
                        or json_dict['points_per_pacgum'] < 0):
                    json_dict['points_per_pacgum'] = 10
            else:
                json_dict['points_per_pacgum'] = 10
        else:
            json_dict['points_per_pacgum'] = 10

        if 'points_per_super_pacgum' in json_dict:
            if isinstance(json_dict['points_per_super_pacgum'], int):
                if (json_dict['points_per_super_pacgum'] > 100
                        or json_dict['points_per_super_pacgum'] < 0):
                    json_dict['points_per_super_pacgum'] = 50
            else:
                json_dict['points_per_super_pacgum'] = 50
        else:
            json_dict['points_per_super_pacgum'] = 50

        if 'points_per_ghost' in json_dict:
            if isinstance(json_dict['points_per_ghost'], int):
                if (json_dict['points_per_ghost'] > 1000
                        or json_dict['points_per_ghost'] < 0):
                    json_dict['points_per_ghost'] = 200
            else:
                json_dict['points_per_ghost'] = 200
        else:
            json_dict['points_per_ghost'] = 200

        if 'seed' in json_dict:
            if (isinstance(json_dict['seed'], int)
                    or isinstance(json_dict['seed'], float)):
                pass
            else:
                json_dict['seed'] = 42
        else:
            json_dict['seed'] = 42

        if 'level_max_timer' in json_dict:
            if isinstance(json_dict['level_max_timer'], int):
                if (json_dict['level_max_timer'] > 240
                        or json_dict['level_max_timer'] < 90):
                    json_dict['level_max_timer'] = 90
            else:
                json_dict['level_max_timer'] = 90
        else:
            json_dict['level_max_timer'] = 90

        return ConfigDict(
            highscore_filename=json_dict['highscore_filename'],
            levels=json_dict['levels'],
            width=json_dict['width'],
            height=json_dict['height'],
            lives=json_dict['lives'],
            pacgum=json_dict['pacgum'],
            points_per_pacgum=json_dict['points_per_pacgum'],
            points_per_super_pacgum=json_dict['points_per_super_pacgum'],
            points_per_ghost=json_dict['points_per_ghost'],
            seed=json_dict['seed'],
            level_max_timer=json_dict['level_max_timer']
        )
