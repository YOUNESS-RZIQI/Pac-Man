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
        self.config: Dict = self.get_config_dict()
        self.highscore_filename: str = self.extract_highscore_filename()
        self.levels_configs: Dict = self.get_valide_game_config()

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

    def get_config_dict(self) -> Dict[str, Dict]:

        """   """

        s_config: str = self.separate_content_and_comments(self.config_path)["config"]

        config_d: Dict = json.loads(s_config)
        return config_d

    def extract_highscore_filename(self) -> str:

        """   """

        self.fix_highscore_file()
        name: str = self.config["highscore_filename"]
        del self.config["highscore_filename"]

        return name

    def fix_highscore_file(self) -> None:

        """   """

        if "highscore_filename" not in self.config.keys():
             self.config["highscore_filename"] = "highscores.json"

        if not isinstance(self.config["highscore_filename"], str):
             self.config["highscore_filename"] = "highscores.json"

        if isinstance(self.config["highscore_filename"], str) and not self.config["highscore_filename"].endswith(".json"):
             self.config["highscore_filename"] = "highscores.json"


# need to check if there is any thign wrong 



    def data_default_asingment(slef, data_type: str) -> int:

        """   """

        if data_type == "width":
             return 15
        elif data_type == "height":
             return 15
        elif data_type == "lives":
             return 3
        elif data_type == "pacgum":
             return 42
        elif data_type == "points_per_pacgum":
            return 10
        elif data_type == "points_per_super_pacgum":
             return 50
        elif data_type == "points_per_ghost":
             return 200
        elif data_type == "seed":
             return 0
        elif data_type == "level_max_time":
             return 90
        else:
             return 0

    def is_data_val_respeketed(self, data_type: str, val: Any) -> bool:

        """   """

        if data_type == "width":
            if not isinstance(val, int) or 100 < val or val < 15:
                return  False

        elif data_type == "height":
            if not isinstance(val, int) or 100 < val or val < 15:
                return  False

        elif data_type == "lives":
            if not isinstance(val, int) or 20 < val or val <= 0:
                return  False

        elif data_type == "pacgum":
            if not isinstance(val, int) or 300 < val or val <= 0:
                return  False

        elif data_type == "points_per_pacgum":
            if not isinstance(val, int) or 100 < val or val <= 0:
                return  False

        elif data_type == "points_per_super_pacgum":
            if not isinstance(val, int) or 100 < val or val <= 0:
                return  False

        elif data_type == "points_per_ghost":
            if not isinstance(val, int) or 10000 < val or val <= 200:
                return  False

        elif data_type == "seed":
            if not isinstance(val, int):
                return  False

        elif data_type == "level_max_time":
            if not isinstance(val, int) or 10000 < val or val <= 5:
                return  False

        return True

    def get_valide_game_config(self) -> Dict[str, Dict]:


        """   """

        d_dflt_data: Dict = {
                    "width": 28,
                    "height": 31,
                    "lives": 3,
                    "pacgum": 42,
                    "points_per_pacgum": 10,
                    "points_per_super_pacgum": 50,
                    "points_per_ghost": 200,
                    "seed": 0,
                    "level_max_time": 80
                    }

        new_config: Dict[str, Dict] = {}

        i_level_num: int = 1

        for s_level, d_data in self.config.items():

            if not isinstance(s_level, str):
                s_level = f"levle {i_level_num}"
                print(f"\033[93mWarning: Ivalide Levle Name. Default Used \033[0m")

            if not isinstance(d_data, dict):
                new_config[s_level] = d_dflt_data
                i_level_num += 1
                print(f"\033[93mWarning: Invalide Game Data. Default Used \033[0m")
                continue

            # fix existing keys
            for data_name, data_val in d_data.items():

                 if data_name in d_dflt_data:
                        if data_name == "width":
                            respect: bool = self.is_data_val_respeketed("width", data_val)
                            if not respect:
                                d_data[data_name] = self.data_default_asingment("width")

                        elif data_name == "height":
                            respect: bool = self.is_data_val_respeketed("height", data_val)
                            if not respect:
                                d_data[data_name] = self.data_default_asingment("height")

                        elif data_name == "lives":
                            respect: bool = self.is_data_val_respeketed("lives", data_val)
                            if not respect:
                                d_data[data_name] = self.data_default_asingment("lives")

                        elif data_name == "pacgum":
                            respect: bool = self.is_data_val_respeketed("pacgum", data_val)
                            if not respect:
                                d_data[data_name] = self.data_default_asingment("pacgum")

                        elif data_name == "points_per_pacgum":
                            respect: bool = self.is_data_val_respeketed("points_per_pacgum", data_val)
                            if not respect:
                                d_data[data_name] = self.data_default_asingment("points_per_pacgum")

                        elif data_name == "points_per_super_pacgum":
                            respect: bool = self.is_data_val_respeketed("points_per_super_pacgum", data_val)
                            if not respect:
                                d_data[data_name] = self.data_default_asingment("points_per_super_pacgum")

                        elif data_name == "points_per_ghost":
                            respect: bool = self.is_data_val_respeketed("points_per_ghost", data_val)
                            if not respect:
                                d_data[data_name] = self.data_default_asingment("points_per_ghost")

                        elif data_name == "seed":
                            respect: bool = self.is_data_val_respeketed("seed", data_val)
                            if not respect:
                                d_data[data_name] = self.data_default_asingment("seed")

                        elif data_name == "level_max_time":
                            respect: bool = self.is_data_val_respeketed("level_max_time", data_val)
                            if not respect:
                                d_data[data_name] = self.data_default_asingment("level_max_time")


                        
            

            #check if missing main key

            i_level_num += 1
            new_config[s_level] = d_data

        return new_config

def main():

    """   """

    # try:
    pac_obj = PacMan()
    print(pac_obj.levels_configs)
    
    # except (PermissionError, FileNotFoundError, ValueError, json.JSONDecodeError) as e:
    #     print(e)

    # except Exception as e:
    #     print(e)


main()
