import networkx as nx
from tabulate import tabulate
import pandas as pd


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
    df = pd.DataFrame(matrix)
    print(df)


def add_element_matrix(matrix, line, colon, p):
    matrix[line][colon] = p


def is_connexe(a_matrix, enter):
    n = len(a_matrix)

    def dfs(node, visited):
        visited[node] = True
        for neighbor in range(n):
            if m[node][neighbor] == 1 and not visited[neighbor]:
                dfs(neighbor, visited)

    visited = [False] * n

    dfs(enter, visited)

    if all(visited):
        return True
    else:
        return False


# Utilisation de Bellman-Ford


def is_cyclic(a_matrix):
    # Nombre de sommets dans le graphe
    n = len(a_matrix)

    # Initialiser les distances à l'infini et la source à 0
    distances = [float('inf')] * n
    distances[0] = 0

    # Itérer sur tous les sommets
    for i in range(n - 1):
        for u in range(n):
            for v in range(n):
                if a_matrix[u][v] != 0 and distances[u] + a_matrix[u][v] < distances[v]:
                    distances[v] = distances[u] + a_matrix[u][v]

    # Vérifier la présence de cycles
    for i in range(n):
        for v in range(n):
            if a_matrix[i][v] != 0 and distances[i] + a_matrix[i][v] < distances[v]:
                return True  # Cycle détecté

    return False  # Aucun cycle détecté


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
                enter_points = []
                end_point = []
                # Remplissage de la matrice en fonction des prérequis
                for task, data in tab.items():
                    # Si la tâche n'a aucun prédécesseur, alors la première colonne est 0
                    if not data["predecessors"]:
                        add_element_matrix(m, 0, task, 0)
                        enter_points.append(task)

                    # Si la tâche a des successeurs, alors remplir la matrice
                    # avec les poids des successeurs
                    if not data["successors"]:
                        end_point.append(task)

                    for successor in data["successors"]:
                        add_element_matrix(
                            m, task, successor, data["duration"])

                # Affichage de la matrice
                print("\n")
                show_matrix(m)

                # Vérification des conditions :

                # Existence de points d'entrées et de sorties

                if (len(enter_points) == 0):
                    print("Il n'y a pas de point d'entrée")
                    exit(1)
                if (len(end_point) == 0):
                    print("Il n'y a pas de point de sortie")
                    exit(1)
                if (len(enter_points) == 1):
                    print("Le point d'entrée est : ", enter_points)
                elif (len(enter_points) > 1):
                    print("Les points d'entrées sont ", enter_points)
                if (len(end_point) == 1):
                    print("Le point de sortie est : ", end_point)
                else:
                    print("Les points de sorties sont ", end_point)

                # Verification des cycles

                if (is_connexe(m, enter_points[0]) == False):
                    print("Le graphe n'est pas connexe")
                    exit(1)

                if (is_cyclic(m)):
                    print("Le graphe est cyclique")
                    exit(1)

                print("C’est un graphe d’ordonnancement")

        except EOFError:
            print("Le fichier n'a pas été trouvé.")
