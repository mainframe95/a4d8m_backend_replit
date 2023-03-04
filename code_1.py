

with open('fichier.txt', 'r') as fichier:
    lignes = fichier.readlines()

nouvelles_lignes = []

for ligne in lignes:
    if "Enregistrement " not in ligne:
        nouvelles_lignes.append(ligne)

with open('result.txt', 'w') as fichier:
    for ligne in nouvelles_lignes:
        fichier.write(ligne)

# lignes = []
# # Ouvrir le fichier texte en mode lecture
# with open("fichier.txt", "r") as fichier:
#     # Lire toutes les lignes dans une liste
#     lignes = fichier.readlines()

# # Supprimer les lignes souhaitées
# lignes_supprimer = [2, 5, 7]  # Les lignes 2, 5 et 7 vont être supprimées
# for index in sorted(lignes_supprimer, reverse=True):
#     del lignes[index]

# # Ouvrir le fichier texte en mode écriture
# with open("resuilt.txt", "w") as fichier:
#     # Écrire les lignes restantes dans le fichier
#     for ligne in lignes:
#         fichier.write(ligne)
