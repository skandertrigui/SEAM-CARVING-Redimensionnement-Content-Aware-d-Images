# Documentation Technique : Redimensionnement d'Image par Seam Carving

Ce document détaille la logique de travail, la méthodologie et les fondements théoriques (Théorie des Graphes) du projet de redimensionnement d'image sensible au contenu.

## 1. Introduction au Seam Carving

Le Seam Carving, ou découpage de coutures, est une technique de redimensionnement d'image qui préserve le contenu important. Contrairement au redimensionnement traditionnel (par mise à l'échelle ou recadrage), cette méthode identifie et supprime des chemins de pixels (coutures) ayant la plus faible importance visuelle.

---

## 2. Modélisation par la Théorie des Graphes

Le problème du Seam Carving est intrinsèquement lié à la recherche de chemin optimal dans un graphe.

### 2.1 Représentation en Graphe
Une image de taille $H \times W$ est modélisée comme un Graphe Orienté Acyclique (DAG) :
* **Nœuds :** Chaque pixel $(i, j)$ de l'image est un nœud du graphe.
* **Arêtes :** Pour une couture verticale, un pixel $(i, j)$ est connecté aux pixels $(i+1, j-1)$, $(i+1, j)$, et $(i+1, j+1)$ de la ligne suivante.
* **Poids :** Le poids de chaque nœud (ou arête) est déterminé par une fonction d'énergie.

### 2.2 Recherche du Chemin Critique
Trouver la couture optimale revient à trouver le chemin de poids minimal entre la ligne supérieure et la ligne inférieure de l'image. Comme le graphe est un DAG, nous utilisons la Programmation Dynamique (plus performante que Dijkstra dans ce cas spécifique) pour calculer les coûts cumulés de manière linéaire $\mathcal{O}(H \times W)$.

---

## 3. Fonction d'Énergie et Importance Visuelle

L'énergie d'un pixel détermine son "poids" dans le graphe.

### 3.1 Énergie Classique (Backward Energy)
Traditionnellement, on utilise le gradient de l'image (dérivée spatiale) :

$$E(i,j) = \left(\frac{\partial I}{\partial x}\right)^2 + \left(\frac{\partial I}{\partial y}\right)^2$$

Les pixels avec des changements de couleur brusques (bords) ont une énergie élevée et sont préservés.

### 3.2 Énergie Prospective (Forward Energy) - Notre Implémentation
L'énergie prospective ne regarde pas seulement l'état actuel des pixels, mais l'impact de leur suppression sur l'image future. Elle calcule le coût des nouveaux gradients créés par la suppression d'une couture.
* **Avantage :** Réduit considérablement les distorsions visuelles et les artefacts, en particulier sur les textures complexes.

---

## 4. Logique de Travail et Méthodologie

### 4.1 Calculateur de Couture Matriciel
Pour garantir une exécution rapide, nous avons vectorisé l'algorithme :
* Utilisation de **NumPy** pour traiter les lignes de pixels en parallèle.
* Calcul de la matrice des coûts cumulés $M(i,j)$ où chaque cellule contient le coût minimal pour atteindre ce pixel depuis le haut.

### 4.2 Lissage Spatial
Pour éviter que les coutures ne soient trop accidentées (*jagged*), nous appliquons un filtre de lissage sur la carte d'énergie. Cela stabilise les chemins et produit des résultats visuellement plus naturels ("plus ajustés").

---

## 5. Architecture du Projet

Le projet est structuré de manière modulaire :
* `cli_auto.py` : Interface utilisateur simplifiée.
* `resizer.py` : Orchestrateur principal.
* `matrix_seam.py` : Algorithmique de recherche de chemin optimal.
* `forward_energy.py` : Calcul de la fonction d'énergie multi-canal.
* `image_utils.py` : Manipulations bas niveau des pixels.

---

## 6. Résultats (Avant / Après)

Voici un aperçu de la réduction de dimension obtenue grâce à l'algorithme de Seam Carving :

![Résultat Seam Carving Avant Après](Capture%20d’écran%202026-01-19%20222036.png)

---

## 7. Conclusion

L'utilisation de la théorie des graphes permet de transformer un problème de design visuel en un problème d'optimisation mathématique rigoureux. Grâce à la modélisation en DAG et à l'utilisation de la Forward Energy, ce projet offre une solution robuste et performante pour l'adaptation de contenu d'image.
