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


def is_neg_duration(tab):
    for task, data in tab.items():
        if data["duration"] < 0:
            return True
    return False


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


def calculate_ranks(tab):
    n = len(tab)
    ranks = [-1] * (n + 1)

    def fct_rang(S):
        if ranks[S] != -1:
            return ranks[S]

        if not tab[S]["predecessors"]:
            ranks[S] = 0
            return 0

        maxRangPred = -1
        for X in tab[S]["predecessors"]:
            rangPred = fct_rang(X)
            if rangPred > maxRangPred:
                maxRangPred = rangPred

        ranks[S] = maxRangPred + 1
        return ranks[S]

    for task in tab.keys():
        fct_rang(task)

    return ranks[1:]

def calculate_tot(tab):
    n = len(tab)
    tot = [-1] * (n + 1)
    tot[0] = 0

    nbc = 1
    while nbc < n:
        for i in range(1, n + 1):
            if tot[i] == -1 and all(tot[j] > -1 for j in tab[i]["predecessors"]):
                if tab[i]["predecessors"]:
                    tot[i] = max(tot[j] + tab[j]["duration"] for j in tab[i]["predecessors"])
                else:
                    tot[i] = 0
                nbc += 1

    return tot[1:]



def calculate_tard(tab, tot, d=float('inf')):
    n = len(tab)
    tard = [float('inf')] * (n + 1)

    if n == 0:
        return tard[1:]
    
    tard[n] = tot[n - 1] if d == float('inf') else d

    visited = set()
    stack = [n]

    while stack:
        current_task = stack[-1]

        if current_task not in visited and all(tard[j] < float('inf') for j in tab[current_task]["successors"]):
            visited.add(current_task)
            stack.extend(tab[current_task]["predecessors"])
        else:
            stack.pop()

            if tard[current_task] == float('inf'):
                tard[current_task] = min(tard[j] - tab[current_task]["duration"] for j in tab[current_task]["successors"])

    return tard[1:]




def calculate_margins(tot, tard):
    return [tard[i] - tot[i] for i in range(len(tot))]


def find_critical_path(tab, tot, tard):
    return [i for i in range(1, len(tot) + 1) if tot[i - 1] == tard[i - 1]]



if __name__ == '__main__':
    while(1) :
        nom_fichier = input(
            "\nTapez le nom du fichier de contraintes (exemple : fichier.txt) ou 'Q' pour quitter :")
        
        if nom_fichier == 'Q' or nom_fichier == 'q':
            print("Merci à bientôt !")
            exit(1)
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
                        continue
                    if (len(end_point) == 0):
                        print("Il n'y a pas de point de sortie")
                        print("Ce n'est pas un graphe d’ordonnancement")
                        continue
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

                    if (is_neg_duration(tab)):
                        print("Le graphe possède des arcs négatifs")
                        print("Ce n'est pas un graphe d’ordonnancement")
                        continue
                    else:
                        print("Il n'y a pas d'arcs négatifs")

                    print("\n")

                    print("Nous vérifions s'il y a un cycle ... \n")

                    if (cycle == False):
                        print("Le graphe est cyclique")
                        print("Ce n'est pas un graphe d’ordonnancement")
                        continue
                    else:
                        print("Il n'y a pas de cycle")

                    print("C’est un graphe d’ordonnancement\n")

                    print("Commençons ...")

                    # Calcul des rangs
                    ranks = calculate_ranks(tab)

                    # Affichage des rangs sous forme de tableau
                    rank_table = [[task, rank]
                                for task, rank in enumerate(ranks, start=1)]
                    print("\nRangs des sommets :\n")
                    print(tabulate(rank_table, headers=[
                        "Sommet", "Rang"], tablefmt="grid"))
                    
                    # Calcul des dates au plus tôt
                    tot_dates = calculate_tot(tab)
                    print("\nDates au plus tôt :", tot_dates)

                    # Calcul des dates au plus tard
                    tard_dates = calculate_tard(tab, tot_dates)
                    print("\nDates au plus tard :", tard_dates)

                    # Calcul des marges totales
                    margins = calculate_margins(tot_dates, tard_dates)
                    print("\nMarges totales :", margins)

                    # Identification du chemin critique
                    critical_path = find_critical_path(tab, tot_dates, tard_dates)
                    print("\nChemin critique :", critical_path)

            except EOFError:
                
                print("Un problème est survenu. Veuillez réessayer.")
                continue
            
            except FileNotFoundError:
                print(f"Le fichier {nom_fichier} n'a pas été trouvé. Veuillez réessayer.")
                continue
