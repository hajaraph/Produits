# Gestion des Produits – API REST FastAPI

Ce projet est une API REST pour la gestion d'une base de données de produits, réalisée avec FastAPI et SQLAlchemy.

## Fonctionnalités
- Ajouter un produit
- Lister tous les produits
- Modifier un produit
- Supprimer un produit
- Afficher les produits avec le montant (prix × quantité)
- Obtenir les statistiques (montant minimal, maximal, total)

## Modèle de données Produit
- `numProduit` : identifiant (int)
- `design` : désignation (str)
- `prix` : prix unitaire (float)
- `quantite` : quantité (int)

## Exemple de JSON pour ajouter un produit
```json
{
  "numProduit": 1,
  "design": "Clavier mécanique",
  "prix": 59.99,
  "quantite": 10
}
```

## Exemple de JSON pour modifier un produit
> Pour la modification, envoyez le même format que pour l'ajout (sans changer `numProduit`).
```json
{
  "numProduit": 1,
  "design": "Clavier rétroéclairé",
  "prix": 69.99,
  "quantite": 15
}
```

## Démarrage rapide
1. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```
2. **Lancer le serveur** :
   ```bash
   uvicorn main:app --reload
   ```
3. **Accéder à la documentation interactive** :
   - Swagger UI : [http://localhost:8000/docs](http://localhost:8000/docs)
   - Redoc : [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Endpoints principaux
- `POST   /produits`           : Ajouter un produit
- `GET    /produits`           : Lister tous les produits
- `PUT    /produits/{id}`      : Modifier un produit
- `DELETE /produits/{id}`      : Supprimer un produit
- `GET    /produits/affichage` : Lister produits avec montant
- `GET    /stats`              : Statistiques (min, max, total)

## Changer la base de données
Par défaut : SQLite. Pour MySQL ou PostgreSQL, modifiez la variable `DATABASE_URL` dans `main.py`.

---

**Projet pédagogique – REST API produits (FastAPI)**
