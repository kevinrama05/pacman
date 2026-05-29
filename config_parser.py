import json


class ConfigParser:
    REQUIRED = {
            "highscore_filename": list,
            "level": list,
            "width": int,
            "height": int,
            "lives": int,
            "pacgum": int,
            "points_per_pacgum": int,
            "points_per_super_pacgum": int,
            "points_per_ghost": int,
            "seed": int,
            "level_max_time": int
        }

    def load_file(self, filename):
        with open(filename, "r") as f:
            lines = f.readlines()

        cleaned_lines = [
            line for line in lines
            if not line.strip().startswith("#")
        ]

        cleaned_json = "".join(cleaned_lines)

        return json.loads(cleaned_json)

    def check_keys(self, config: dict) -> dict:

        missing = self.REQUIRED.keys() - config.keys()

        if missing:
            raise ValueError(f"Missing keys: {missing}")

        invalid = config.keys() - self.REQUIRED.keys()

        if invalid:
            raise ValueError(f"Invalid keys: {invalid}")

        validated = {}

        for key, expected_type in self.REQUIRED.items():
            value = config[key]

            try:
                validated[key] = expected_type(value)
            except (ValueError, TypeError):
                raise ValueError(
                    f"Invalid type for '{key}': "
                    f"expected {expected_type.__name__}"
                )

        return validated

    def parse(self, arg: str) -> dict:
        data = self.load_file(arg)

        cleaned_data = self.check_keys(data)

        return cleaned_data
