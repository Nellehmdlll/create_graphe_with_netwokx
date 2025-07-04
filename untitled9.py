# -*- coding: utf-8 -*-
"""Untitled9.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1f3odjQmbc52STryE46BammAfFRliACkk
"""

import matplotlib.pyplot as plt
import networkx as nx

# Définition des tâches (durée, prédécesseurs)
tasks = [
    (2, []),        # 0 : Permis
    (7, []),        # 1 : Maçonnerie
    (3, [0, 1]),    # 2 : Charpente
    (1, [2]),       # 3 : Toiture
    (8, [0, 1]),    # 4 : Plomberie
    (2, [3, 4]),    # 5 : Façade
    (1, [3, 4]),    # 6 : Fenêtre
    (1, [3, 4]),    # 7 : Jardin
    (3, [6]),       # 8 : Plafonds
    (2, [8]),       # 9 : Peintures
    (1, [5, 9])     # 10 : Emménagement
]

# 1_Création du graphe orienté
G = nx.DiGraph()

# Ajout des nœuds et des arêtes avec durées en labels
for i, (duration, preds) in enumerate(tasks):
    G.add_node(i, label=f"T{i}\n({duration} sem)")
    for p in preds:
        G.add_edge(p, i)

# Positionnement des nœuds sans pygraphviz
pos = nx.spring_layout(G, seed=42)

# Dessin du graphe
plt.figure(figsize=(14, 8))
nx.draw(G, pos, with_labels=False, arrows=True, node_size=3000, node_color="lightgreen", edge_color="gray")
nx.draw_networkx_labels(G, pos, labels=nx.get_node_attributes(G, 'label'), font_size=10)
plt.title("Graphique du projet de M. Clément B.", fontsize=14)
plt.axis("off")
plt.tight_layout()
plt.show()

#6. Implémentation de la fonction
def project(L):
    n = len(L)
    durations = [L[i][0] for i in range(n)]
    predecessors = [L[i][1] for i in range(n)]

    # 1. Construire le graphe et le degré entrant
    from collections import defaultdict, deque

    graph = defaultdict(list)
    in_degree = [0] * n
    for i, preds in enumerate(predecessors):
        for p in preds:
            graph[p].append(i)
            in_degree[i] += 1

    # 2. Tri topologique
    queue = deque([i for i in range(n) if in_degree[i] == 0])
    topo_order = []
    while queue:
        node = queue.popleft()
        topo_order.append(node)
        for succ in graph[node]:
            in_degree[succ] -= 1
            if in_degree[succ] == 0:
                queue.append(succ)

    # 3. Date au plus tôt
    earliest = [0] * n
    for i in topo_order:
        for j in graph[i]:
            earliest[j] = max(earliest[j], earliest[i] + durations[i])

    project_duration = max(earliest[i] + durations[i] for i in range(n))
    print(earliest)

    # 4. Date au plus tard
    latest = [project_duration] * n
    for i in reversed(topo_order):
        if not graph[i]:  # tâche finale
            latest[i] = project_duration - durations[i]
        for j in graph[i]:
            latest[i] = min(latest[i], latest[j] - durations[i])
    print(latest)

    # 5. Résultat
    result = []
    for i in range(n):
        slack = latest[i] - earliest[i]
        result.append({
            "tâche": i,
            "DE (au plus tôt)": earliest[i],
            "slack (marge)": slack
        })

    return result, project_duration

#Résultat du projet
résultat, durée = project(tasks)

for r in résultat:
    print(f"Tâche {r['tâche']} : DE = {r['DE (au plus tôt)']}, Slack = {r['slack (marge)']}")
print(f"Durée minimale du projet : {durée} semaines")

