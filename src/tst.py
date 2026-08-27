from typing import List, Dict, Set, Tuple, Any
import json

class ConfigurationFileTools:

    """   """

    def is_comment(self, line: str) -> bool:

        """   """

        if line and line[0] == "#":
             return True
        elif line and len(line) >= 2 and line[:2] == "//":
             return True
        else:
             return False

    def separate_content_and_comments(self, path: str) -> Dict[str, str | List[str]]:

        """   """

        config: str = ""
        comments: List[str] = []
        try:
                with open(path, "r") as file:
                    lines = file.readlines()
                    for line in lines:
                        line = line.strip()
                        if self.is_comment(line):
                               comments.append(line)
                        else:
                             config += line + "\n"
                return {"config": config, "comments": comments}
                    
        except PermissionError:
            raise PermissionError("You Don't have Permission To Read"
                                  f" Configuration file: {path}")
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Configuration file not found: {path}")
        except Exception as e:
             raise ValueError(f"{e}"
                               "\nAn Error apears in configuration.json File")

class PacManTolls(ConfigurationFileTools):

    """   """

    def __init__(self, config_path: str = ):

        """   """

        self.config_path: str = config_path


    def get_configuration_dict(self) -> Dict:

        """   """

        s_config: str = self.separate_content_and_comments(self.config_path)["config"]

        d_config: Dict = json.loads(s_config)



