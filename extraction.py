from tabulate import tabulate


def sup_doublon(list):
    tab = []
    list_elmt = []
    for elmt in list:
        if elmt not in tab:
            tab.append(elmt)
            list_elmt.append(elmt)
    return list_elmt


def pretraitement(path_fic):
    tab = {}
    for lines in path_fic:
        values = lines.split()
        actual = int(values[0])
        previous = list(map(int, values[1:]))
        previous = sup_doublon(previous)
        tab[actual] = previous
    return tab


if __name__ == '__main__':
    nom_fichier = input(
        "Tapez le nom du fichier de contraintes (exemple : fichier.txt) :")
    if nom_fichier[-4:] == ".txt":
        try:
            with open(nom_fichier, 'r') as fic:
                tab = pretraitement(fic)
                # Conversion dic to list of list
                tableau = [[nœud, " ".join(map(str, précédents))]
                           for nœud, précédents in tab.items()]
                print(tabulate(tableau, headers=[
                      "Noeud", "Noeuds Précédents"], tablefmt="grid"))
        except EOFError:
            print("Le fichier n'a pas été trouvé.")
