from typing import List, Dict, Any
import json
import sys

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
            raise PermissionError("\033[91mYou Don't have Permission To Read"
                                  " Configuration file: \033[94m"
                                  f"{path}\033[0m")

        except FileNotFoundError:
            raise FileNotFoundError(
                f"\033[91mConfiguration file \033[94m'{path}'"
                "\033[91m Not Found\033[0m")

        except Exception as e:
             raise ValueError(f"\033[91m{e}"
                               "\nAn Error apears in configuration.json"
                               " File\033[0m")


class PacMan(ConfigurationFileTools):

    """   """

    def __init__(self):

        """   """

        self.config_path: str = self.get_config_path()
        self.game_config: Dict = self.get_game_config_dict()

    def get_config_path(self) -> str:

        """   """

        if  len(sys.argv) != 2 or not sys.argv[1] or not sys.argv[1].endswith(".json"):
             raise ValueError("\033[91mYou Must gave Correct two"
                              " argements:\n\n Input Example:\n\n\t"
                              "\033[92mpython3 \033[93mEntry_point.py"
                              " \033[94mconfigurationfile.json "
                              "(Must be json)\n\033[0m")
        else:
             return sys.argv[1]

    def get_game_config_dict(self) -> Dict:

        """   """

        s_config: str = self.separate_content_and_comments(self.config_path)["config"]

        config_d: Dict = json.loads(s_config)

        return config_d





    def get_valide_game_config(self) -> Dict[str, Dict]:


        """   """

        config = self.get_game_config_dict()

        # highscore file: "file name"
        # Level: data

        pass

def main():

    """   """

    try:
        config_d = PacMan().game_config
        print(config_d)

    except (PermissionError, FileNotFoundError, ValueError, json.JSONDecodeError) as e:
        print(e)

    except Exception as e:
        print(e)


main()

#  Now  Validate the Config File     !   !  !