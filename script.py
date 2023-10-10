import networkx as nx
from tabulate import tabulate


def pretraitement(path_fic):
    tab = {}
    for lines in path_fic:
        values = lines.split()
        task = int(values[0])
        duration = int(values[1])
        predecessors = list(map(int, values[2:]))
        tab[task] = {"duration": duration,
                     "predecessors": predecessors, "successors": []}
    return tab


def calculate_successors(tab):
    # Crée un graphe dirigé
    G = nx.DiGraph()

    # Ajoute les tâches et les arêtes au graphe
    for task, data in tab.items():
        G.add_node(task, duration=data["duration"])
        G.add_edges_from([(predecessor, task)
                         for predecessor in data["predecessors"]])

    # Calcule les successeurs directs de chaque tâche et les stocke dans le dictionnaire "successors"
    for task in tab.keys():
        tab[task]["successors"] = list(G.successors(task))


def create_square_empty_matrix(n):
    matrice = []
    for i in range(n):
        ligne = ['*'] * n
        matrice.append(ligne)
    return matrice


def show_matrix(matrix):
    for ligne in matrix:
        print(ligne)


def add_element_matrix(matrix, line, colon, p):
    matrix[line][colon] = p


if __name__ == '__main__':
    nom_fichier = input(
        "Tapez le nom du fichier de contraintes (exemple : fichier.txt) :")

    # Vérifie que le nom du fichier se termine par ".txt"
    if nom_fichier[-4:] == ".txt":
        try:
            with open(nom_fichier, 'r') as fic:
                tab = pretraitement(fic)
                calculate_successors(tab)
                n = len(tab)

                # Crée un tableau à partir des données pour l'affichage
                tableau = [[task, data["duration"], " ".join(map(str, data["predecessors"])), " ".join(
                    map(str, data["successors"]))] for task, data in tab.items()]

                # Affiche le tableau
                print(tabulate(tableau, headers=[
                      "Tâche", "Durée", "Prédécesseurs", "Successeurs"], tablefmt="grid"))

                # Creation de la matrice
                m = create_square_empty_matrix(n + 2)

                # Remplissage de la matrice en fonction des prérequis
                for task, data in tab.items():
                    # Si la tâche n'a aucun prédécesseur, alors la première colonne est 0
                    if not data["predecessors"]:
                        add_element_matrix(m, 0, task, 0)

                    # Si la tâche a des successeurs, alors remplir la matrice avec les poids des successeurs
                    for successor in data["successors"]:
                        add_element_matrix(m, task, successor, data["duration"])

                # Affichage de la matrice
                show_matrix(m)

        except EOFError:
            print("Le fichier n'a pas été trouvé.")
