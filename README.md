## 🧠 Core – Lancement et coordination des benchmarks

Le module `Core` constitue le **point d’entrée principal du projet**. Il orchestre les opérations suivantes :

- Génération de jeux de données synthétiques dans des bases SQLite.
- Exécution des algorithmes de skyline sur ces données.
- Mesure des temps d’exécution.
- Export des résultats pour visualisation (ex. TikZ pour LaTeX).

### 📌 Composants principaux

| Élément            | Description                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| `AppRun`           | Classe utilitaire pour interagir avec les bases de données (création, sélection, mock). |
| `create_tables()`  | Génère plusieurs bases de données de test avec différentes tailles.         |
| `compare_all()`    | Lance une série de tests comparatifs sur plusieurs algorithmes et enregistre les performances. |
| `data_normalizer()`| Formate les données de performance pour les exporter sous forme de graphiques. |


## 🛠️ Utils – Outils auxiliaires

### `ComputerStats.py` – Analyse des ressources système

Ce module fournit une vue d’ensemble du matériel utilisé pendant les benchmarks :

- **RAM** :
  - Quantité totale
  - Mémoire utilisée
  - Mémoire libre
- **Processeur (CPU)** :
  - Nombre de cœurs logiques et physiques
  - Fréquences min/max/actuelle
  - Pourcentage d'utilisation
- **Carte graphique (GPU)** :
  - Nom, charge, mémoire (libre/utilisée/totale), température (si disponible)

Utilise :
- [`psutil`](https://pypi.org/project/psutil/)
- [`GPUtil`](https://pypi.org/project/GPUtil/)
- [`tabulate`](https://pypi.org/project/tabulate/)

📌 Affiche les informations sous forme de tableaux lisibles directement en terminal.

### `DataParser.py` – Conversion des données SQL en dictionnaire Python

Ce module permet de convertir les résultats d'une requête SQL en un dictionnaire Python, facilitant ainsi l'accès aux données.

- **Entrée** :
  - Liste de tuples où chaque tuple représente une ligne de données SQL, avec l'ID comme premier élément et les autres éléments comme valeurs associées.
  
- **Sortie** :
  - Dictionnaire où chaque clé est l'ID d'une ligne et chaque valeur est un tuple contenant les autres éléments de cette ligne.

Utilise :
- Aucune bibliothèque externe spécifique, seulement des fonctionnalités de base de Python.

📌 Permet de manipuler les résultats SQL sous forme de dictionnaire, facilitant l'analyse et l'accès rapide aux données.

### `DisplayHelpers.py` – Affichage coloré et structuré

Ce module offre des fonctions pour afficher des messages colorés dans le terminal et structurer les données de manière lisible.

- **Fonctions** :
  - `print_color(color, text)` : Imprime un texte dans une couleur spécifique.
  - `print_green(text)` : Affiche le texte en vert.
  - `print_red(text)` : Affiche le texte en rouge.
  - `beauty_print(title, data)` : Affiche un titre et structure les données (liste, dictionnaire, etc.) de manière lisible.

Utilise :
- [`colorama`](https://pypi.org/project/colorama/)

📌 Facilite l'affichage visuel des résultats, avec des couleurs et une structure adaptée pour les logs et rapports dans le terminal.

### `Helpers.py` – Algorithme DP-IDP et gestion des relations

Ce module contient des classes et fonctions pour exécuter l'algorithme **DP-IDP**, gérer des relations entre les données, et offrir des utilitaires pour la conversion de fichiers entre Python 2 et Python 3.

- **Classes** :
  - `DP_IDP_ALL` : Implémente l'algorithme DP-IDP pour comparer des entités à travers des matrices de relations.
  - `Ranking` : Optimise le tri des éléments dans un classement en utilisant un `OrderedDict`.
  
- **Fonctions** :
  - `python2_to_python3_folders` : Génère la commande pour convertir un dossier de fichiers Python 2 en Python 3.
  - `menu` : Affiche un menu d'initialisation pour générer des enregistrements dans la base de données.

📌 Utilise :
- `sqlite3` : Pour l'interaction avec la base de données.
- `numpy` : Pour la manipulation des données numériques.
- `colorama` : Pour l'affichage coloré dans la console.


### `TimeCalc.py` – Calcul et formatage du temps d'exécution

Ce module contient la classe **TimeCalc** qui mesure et formate le temps d'exécution d'un algorithme, tout en calculant le temps moyen par échantillon.

- **Classe `TimeCalc`** :
  - Mesure le temps d'exécution d'un algorithme.
  - Calcule le temps moyen par échantillon.
  - Formate le temps en heures, minutes et secondes pour une lisibilité optimale.

- **Méthodes** :
  - `format_time(time_to_format)` : Formate un temps en secondes dans un format lisible (heures, minutes, secondes).
  - `get_formated_data()` : Retourne une chaîne contenant les données formatées sur l'exécution.
  - `stop()` : Arrête le chronomètre, calcule le temps d'exécution total et le temps moyen par échantillon.

📌 Utilise :
- `time` : Pour mesurer les temps d'exécution.



