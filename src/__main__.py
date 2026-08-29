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
        self.level_up_def: int = 0
        self.level: int = 1
        self.default_data: Dict = {"lives": 3, "pacgum": 42,
                            "points_per_pacgum": 10,
                            "points_per_super_pacgum": 50,
                            "points_per_ghost": 200,
                            "seed": 42,
                            "level_max_time": 80}


    def __is_respeceted_data(self, data_name: str, val: Any) -> bool:

        """   """

        if data_name == "lives":
            if isinstance(val, bool) or  not isinstance(val, int) or 3 < val or val <= 0:
                print(f"\033[93mWarning: Ivalide 'lives'. Default Used \033[0m")
                return  False

        elif data_name == "pacgum":
            if isinstance(val, bool) or  not isinstance(val, int) or 300 < val or val <= 0:
                print(f"\033[93mWarning: Ivalide 'pacgum'. Default Used \033[0m")
                return  False

        elif data_name == "points_per_pacgum":
            if isinstance(val, bool) or  not isinstance(val, int) or 100 < val or val <= 0:
                print(f"\033[93mWarning: Ivalide 'points_per_pacgum'. Default Used \033[0m")
                return  False

        elif data_name == "points_per_super_pacgum":
            if isinstance(val, bool) or  not isinstance(val, int) or 100 < val or val <= 0:
                print(f"\033[93mWarning: Ivalide 'points_per_super_pacgum'. Default Used \033[0m")
                return  False

        elif data_name == "points_per_ghost":
            if isinstance(val, bool) or  not isinstance(val, int) or 10000 < val or val < 200:
                print(f"\033[93mWarning: Ivalide 'points_per_ghost'. Default Used \033[0m")
                return  False

        elif data_name == "seed":
            if isinstance(val, bool) or  not isinstance(val, int):
                print(f"\033[93mWarning: Ivalide 'seed'. Default Used \033[0m")
                return  False

        elif data_name == "level_max_time":
            if isinstance(val, bool) or  not isinstance(val, int) or 10000 < val or val <= 5:
                print(f"\033[93mWarning: Ivalide 'level_max_time'. Default Used \033[0m")
                return  False

        return True

    def get_curr_level_data(self) -> Dict[str, Dict]:


        """   """

        for name, val in self.default_data.copy().items():
            if name not in ["lives", "pacgum", "seed"]:
                self.default_data[name] = val + self.level_up_def
        
        s_levle: str = "level " + str(self.level)
        default_config: Dict [str, Dict] = {s_levle: self.default_data}
        config: Dict = self.config

        for lev, data in default_config.items():
            if isinstance(lev, str) and isinstance(data, Dict) and s_levle == lev:
                for name, val in data.copy().items():
                    if isinstance(config, Dict) and s_levle in config and isinstance(config[s_levle], Dict) and name in config[s_levle] and self.__is_respeceted_data(name, config[s_levle][name]):
                        data[name] = config[s_levle][name]

        self.level += 1
        self.level_up_def += 10
        self.default_data = default_config[s_levle]
        final_config: Dict[str, Dict] = {s_levle: self.default_data.copy()}
        self.default_data["seed"] = 0

        return final_config


def main():

    """   """

    # try:
    pac_obj = PacMan()

    for level, data in pac_obj.get_curr_level_data().items():
            print(level, "\n\t", data)

    for level, data in pac_obj.get_curr_level_data().items():
            print(level, "\n\t", data)

    for level, data in pac_obj.get_curr_level_data().items():
            print(level, "\n\t", data)

    # except Exception as e:

    #     _, _, tb = sys.exc_info()
    #     while tb.tb_next:
    #         tb = tb.tb_next

    #     print(f"Line: {tb.tb_lineno}")
    #     print(f"Error: {e}")


main()
