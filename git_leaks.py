import json
import sys
from git import Repo
import signal
import re


REPO_DIR = './skale-manager'                            # Repositorio
KEY_WORDS = ['leak', 'secret', 'crash', 'error']


def gest_excepcion(signal, frame):
    # Gestión de excpeiciones 
    print("\nHA HABIDO UNA EXCPECIÓN")
    print("SE VHA SALIDO DEL PROGRAMA\n")
    sys.exit(1)


def extract(REPO_DIR):
    
    repo = Repo(REPO_DIR)           # Se extrae el repositorio

    return repo


def transform(repo, KEY_WORDS):
    commits = list(repo.iter_commits())         # Se sacan los commits del repo
    leaks = []                                  # Aquí almacenamos los leaks

    for commit in commits:
        for pal in KEY_WORDS:
            # Se buscan las palabras claves en los commits
            if re.search(pal, commit.message, re.IGNORECASE):
                leaks.append([commit, pal])

    return leaks


def load(leaks):
    contador = 1
    # Se va a presentar cada commit con un número
    for commit in leaks:
        mensaje = re.sub(r"\n", "", commit[0].message)
        print(
            f'{contador} - Commit {commit[1]} -> {commit[0]} {mensaje}\n')    # Se imprime nº, palabra clave encontrada y commit
        contador += 1


def load_json(leaks):
    # Como Json funciona por diccionarios creamos un diccionario: clave es el id, valores lista con mensaje
    dict_leaks = {}
    i = 1
    for commit in leaks:
        dict_leaks[i] = [str(commit[0]), str(commit[0].message), commit[1]]
        i += 1

    with open('git_leaks.json', 'w') as file:
        json.dump(dict_leaks, file, indent=2)

    print(dict_leaks)


if __name__ == '__main__':
    # En caso de que se genere una expeción CTRL + C
    signal.signal(signal.SIGINT, gest_excepcion)

    repo = extract(REPO_DIR)
    leaks = transform(repo, KEY_WORDS)
    load(leaks)
    exit()
