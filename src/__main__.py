from typing import List, Dict, Any
import json
import sys

class ConfigFileTools:

    """   """

    def __is_comment(self, line: str) -> bool:

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
                        if self.__is_comment(line):
                               comments.append(line)
                        else:
                             config += line + "\n"
                return {"config": config, "comments": comments}
                    
        except PermissionError:
            raise PermissionError("\033[91mError:\n\tYou Don't have Permission "
                                  "To Read Configuration file: \033[94m"
                                  f"{path}\033[0m")

        except FileNotFoundError:
            raise FileNotFoundError(
                f"\033[91mConfiguration file \033[94m'{path}'"
                "\033[91m Not Found\033[0m")

        except Exception as e:
             raise ValueError(f"\033[91m{e}"
                               "\nAn Error apears in configuration.json"
                               " File\033[0m")

    def get_config_path(self, min_args_num: int, pos: int) -> str:

        """   """

        if  len(sys.argv) != min_args_num or not sys.argv[pos] or not sys.argv[pos].endswith(".json"):
             raise ValueError("\033[91mYou Must gave Correct two"
                              " argements:\n\n Input Example:\n\n\t"
                              "\033[92mpython3 \033[93mEntry_point.py"
                              " \033[94mconfigurationfile.json "
                              "(Must be json)\n\033[0m")
        else:
             return sys.argv[1]

    def get_json_config_dict(self) -> Dict[str, Dict]:

        """   """

        s_config: str = self.separate_content_and_comments(self.config_path)["config"]
        try:
            config_d: Dict = json.loads(s_config)
        except Exception as e:
            print(f"\033[91mJSON Error in {self.config_path}:\n\t\033[93m{e}\033[0m\n")
            sys.exit(1)


        return config_d


class PacMan(ConfigFileTools):

    """   """

    def __init__(self):

        """   """

        self.config_path: str = self.get_config_path(2, 1)
        self.config: Dict = self.get_json_config_dict()
        self.highscores_filename: str = "highscores.json"
        self.levels_configs: Dict = self.get_valide_game_config()

# need to check if there is any thign wrong 


    def __data_default_asingment(self, data_type: str) -> int:

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

    def __is_data_val_respeketed(self, data_type: str, val: Any) -> bool:

        """   """

        if data_type == "width":
            if not isinstance(val, int) or 100 < val or val < 15:
                print(f"\033[93mWarning: Ivalide 'width'. Default Used \033[0m")
                return  False

        elif data_type == "height":
            if not isinstance(val, int) or 100 < val or val < 15:
                print(f"\033[93mWarning: Ivalide 'height'. Default Used \033[0m")
                return  False

        elif data_type == "lives":
            if not isinstance(val, int) or 20 < val or val <= 0:
                print(f"\033[93mWarning: Ivalide 'lives'. Default Used \033[0m")
                return  False

        elif data_type == "pacgum":
            if not isinstance(val, int) or 300 < val or val <= 0:
                print(f"\033[93mWarning: Ivalide 'pacgum'. Default Used \033[0m")
                return  False

        elif data_type == "points_per_pacgum":
            if not isinstance(val, int) or 100 < val or val <= 0:
                print(f"\033[93mWarning: Ivalide 'points_per_pacgum'. Default Used \033[0m")
                return  False

        elif data_type == "points_per_super_pacgum":
            if not isinstance(val, int) or 100 < val or val <= 0:
                print(f"\033[93mWarning: Ivalide 'points_per_super_pacgum'. Default Used \033[0m")
                return  False

        elif data_type == "points_per_ghost":
            if not isinstance(val, int) or 10000 < val or val < 200:
                print(f"\033[93mWarning: Ivalide 'points_per_ghost'. Default Used \033[0m")
                return  False

        elif data_type == "seed":
            if not isinstance(val, int):
                print(f"\033[93mWarning: Ivalide 'seed'. Default Used \033[0m")
                return  False

        elif data_type == "level_max_time":
            if not isinstance(val, int) or 10000 < val or val <= 5:
                print(f"\033[93mWarning: Ivalide 'level_max_time'. Default Used \033[0m")
                return  False

        return True

    def __add_messing_data_and_remove_extra(self, keys_visited: Dict, d_data: Dict) -> None:

        """   """

        for key, viseted in keys_visited.items():
            if not viseted:
                d_data[key] = self.__data_default_asingment(key)
                print(f"\033[93mWarning: '{key}' Was not Found. Default Used \033[0m")

        expected_keys: List = ["width","height","lives","pacgum","points_per_pacgum",
                               "points_per_super_pacgum","points_per_ghost","seed",
                               "level_max_time"]
        new_data: Dict = {}

        for key, val in d_data.items():
            if key in expected_keys:
                new_data[key] = val

        d_data = new_data

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

        for s_level, d_data in self.config.items():

            if not isinstance(d_data, dict):
                new_config[s_level] = d_dflt_data
                print(f"\033[93mWarning: Invalide Game Data. Default Used \033[0m")
                continue

            keys_visited: Dict = {"width": 0, "height": 0, "lives": 0, "pacgum": 0,
                    "points_per_pacgum": 0, "points_per_super_pacgum": 0,
                    "points_per_ghost": 0, "seed": 0, "level_max_time": 0,}

            for data_name, data_val in list(d_data.items()):
                if data_name in d_dflt_data:
                    respected: bool = self.__is_data_val_respeketed(data_name, data_val)
                    if not respected:
                        d_data[data_name] = self.__data_default_asingment(data_name)
                    keys_visited[data_name] = 1

            self.__add_messing_data_and_remove_extra(keys_visited, d_data)
            new_config[s_level] = d_data



        return new_config





def main():

    """   """

    try:
        pac_obj = PacMan()

        for level, data in pac_obj.levels_configs.items():
            print(level, "\n\t", data)
    
    except Exception as e:

        _, _, tb = sys.exc_info()
        while tb.tb_next:
            tb = tb.tb_next

        print(f"Line: {tb.tb_lineno}")
        print(f"Error: {e}")


main()
