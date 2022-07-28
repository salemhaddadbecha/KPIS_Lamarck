import os

path_list = [
    "modules/controle_qualite",
    "modules/update_tables"
]


def format_dir(path):
    """
    Permet de formatter en ASCII tous les fichiers d'un
    dossier
    :param path:
    """
    for filename in os.listdir(path):
        file = ""
        print(os.path.join(path, filename))
        with open(os.path.join(path, filename), 'r', encoding="UTF-8") as f:
            file = f.read()

        with open(os.path.join(path, filename), 'w', encoding="UTF-8") as f:
            f.write(file.replace("é", "e").replace("è", "e").replace("ô", "o"))


for path in path_list:
    format_dir(path)
