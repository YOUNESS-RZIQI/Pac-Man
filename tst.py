from typing import List, Dict, Set, Tuple, Any

class ConfigFileTools:

    """   """

    def is_comment(self, line: str) -> bool:

        """   """

        if line and line[0] == "#":
             return True
        elif line and len(line) >= 2 and line[:2] == "//":
             return True
        else:
             return False

    def clean_from_comments(self, path: str) -> Dict[str, str | List[str]]:

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
                             config += line
                return {"config": config, "comments": comments}
                    
        except PermissionError:
            raise PermissionError("Permission Error for Reading"
                                  f" Configuration file: {path}")


config_file_obj = ConfigFileTools()

dct = config_file_obj.clean_from_comments("/home/yrziqi/Pac-Man/configuration.json")

print(dct["comments"])