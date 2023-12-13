import os
from configparser import ConfigParser


def config(
    filename: str = "database.ini",
    section: str = "postgresql",
):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    parser = ConfigParser()
    parser.read(os.path.join(dir_path, filename))

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            "Section {0} not found in the {1} file".format(section, filename)
        )

    return db
