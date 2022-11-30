#from git_leaks import KEY_WORDS, REPO_DIR
import git_leaks as gl
import json


def load_json(leaks):
    # Como Json funciona por diccionarios creamos un diccionario: clave es el id, valores lista con mensaje
    dict_leaks = {}
    i = 1
    for commit in leaks:
        dict_leaks[i] = [str(commit[0]), str(commit[0].message), commit[1]]
        i += 1

    with open('git_leaks.json', 'w') as file:
        json.dump(dict_leaks, file, indent=2)

    print('Se han cargado los datos en un fichero json')


if __name__ == "__main__":
    #REPO_DIR = './skale-manager'
    #KEY_WORDS = ['leak', 'secret', 'crash', 'error']
    directorio = gl.REPO_DIR
    palabras = gl.KEY_WORDS

    repo = gl.extract(directorio)
    leaks = gl.transform(repo, palabras)
    load_json(leaks)
