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


def calculate_successors_cycle(tab, graph):
    # Crée un graphe dirigé

    # Ajoute les tâches et les arêtes au graphe
    for task, data in tab.items():
        graph.add_node(task, duration=data["duration"])
        graph.add_edges_from([(predecessor, task)
                              for predecessor in data["predecessors"]])

    # Calcule les successeurs directs de chaque tâche et les stocke dans le dictionnaire "successors"
    for task in tab.keys():
        tab[task]["successors"] = list(graph.successors(task))

    return nx.is_directed_acyclic_graph(graph)


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


if __name__ == '__main__':
    nom_fichier = input(
        "Tapez le nom du fichier de contraintes (exemple : fichier.txt) :")

    # Vérifie que le nom du fichier se termine par ".txt"
    if nom_fichier[-4:] == ".txt":
        try:
            with open(nom_fichier, 'r') as fic:
                G = nx.DiGraph()
                tab = pretraitement(fic)
                cycle = calculate_successors_cycle(tab, G)
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

                print("\n")

                # Afficher les arcs
                print("Arcs du graphe :\n")

                for edge in G.edges():
                    source, target = edge
                    # Utilisez la durée du nœud cible comme poids
                    duration = G.nodes[source]["duration"]
                    print(f"{source} -> {target} = {duration}")
                
                print("\n")

                # Vérification des conditions :
                print("Vérifions que le graphe vérifie les conditions :\n")
                # Existence de points d'entrées et de sorties

                if (len(enter_points) == 0):
                    print("Il n'y a pas de point d'entrée")
                    print("Ce n'est pas un graphe d’ordonnancement")
                    exit(1)
                if (len(end_point) == 0):
                    print("Il n'y a pas de point de sortie")
                    print("Ce n'est pas un graphe d’ordonnancement")
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

                print("\n")

                print("Nous vérifions s'il y a un cycle ... \n")

                if (cycle == False):
                    print("Le graphe est cyclique")
                    print("Ce n'est pas un graphe d’ordonnancement")
                    exit(1)
                else:
                    print("Il n'y a pas de cycle")

                print("C’est un graphe d’ordonnancement\n")

                print("Commençons ")

        except EOFError:
            print("Le fichier n'a pas été trouvé.")
