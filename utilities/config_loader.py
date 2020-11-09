import yaml
from yaml import Loader, YAMLError

LOG_LEVELS = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]
FILE_TYPES = ["CSV", "JSON"]
DEFAULT_HEADERS = [
    "title",
    "company",
    "city",
    "state",
    "country",
    "zip_code",
    "min_pay",
    "max_pay",
    "pay_type",
    "match",
    "keywords",
    "url",
]
DEFAULT_COMPACT_HEADERS = [
    "title",
    "company",
    "location",
    "salary",
    "url",
]


class Config:
    def __init__(self, config_path="config.yaml"):

        config = self.__load_config(config_path)
        search_params = config["search_params"]
        file_config = config["file_config"]

        # Validate Log Level
        self.LOG_LEVEL = config["log_level"]
        if self.LOG_LEVEL is not None:
            self.LOG_LEVEL = self.LOG_LEVEL.upper()
        if self.LOG_LEVEL not in LOG_LEVELS:
            raise ValueError("Invalid Log Level")

        # Validate Search Params
        self.SEARCH_KEYWORDS = search_params["search_keywords"]
        if self.SEARCH_KEYWORDS is None:
            self.SEARCH_KEYWORDS = []
        if not isinstance(self.SEARCH_KEYWORDS, list):
            raise TypeError("Expected Type list")

        self.LOCATIONS = search_params["locations"]
        if not isinstance(self.LOCATIONS, list):
            raise TypeError("Expected Type list")
        if not self.LOCATIONS:
            raise ValueError("Locations cannot be Empty")

        self.SUB_KEYWORDS = search_params["sub_keywords"]
        if self.SUB_KEYWORDS is None:
            self.SUB_KEYWORDS = []
        if not isinstance(self.SUB_KEYWORDS, list):
            raise TypeError("Expected Type list")
        self.SUB_KEYWORDS = list(map(lambda i: i.lower(), self.SUB_KEYWORDS))

        self.RADIUS = search_params["radius"]
        if not isinstance(self.RADIUS, int):
            raise TypeError("Expected Type int")
        if self.RADIUS < 0:
            raise ValueError("Expected Positive Integer")

        # Validate File Configs
        self.FILE_NAME = file_config["file_name"]
        if "." in self.FILE_NAME:
            raise ValueError("Invalid Character for File Name")

        self.FILE_TYPE = file_config["file_type"].lower()
        if self.FILE_TYPE.upper() not in FILE_TYPES:
            raise NotImplementedError(f"'{self.FILE_TYPE}' is not Implemented yet")

        self.COMPACT = file_config["compact"]
        if self.COMPACT:
            self.HEADERS = DEFAULT_COMPACT_HEADERS
        else:
            self.HEADERS = DEFAULT_HEADERS

        self.ITEM_LIMIT = file_config["item_limit"]
        if self.ITEM_LIMIT is None:
            self.ITEM_LIMIT = 0
        if not isinstance(self.ITEM_LIMIT, int):
            raise TypeError("Expected Type int")
        if self.ITEM_LIMIT < 0:
            raise ValueError("Expected Positive Integer")

    @staticmethod
    def __load_config(config_path: str):
        """Loads config_path with pyyaml
        Args:
            config_path: Path to config file
        """
        try:
            with open(config_path, "r") as config_file:
                return yaml.load(stream=config_file, Loader=Loader)
        except FileNotFoundError:
            raise FileNotFoundError(f"No such File: '{config_path}'")
        except YAMLError:
            raise YAMLError("Error Parsing Config File")
