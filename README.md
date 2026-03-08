# 🏫 EcoleCom — Version Flask (Python)

Plateforme de communication scolaire avec Flask + SQLite.
**Pas besoin de XAMPP ni de MySQL !**

---

## 🚀 Installation en 3 étapes

### Étape 1 — Installer Python
Télécharge Python sur **https://python.org** (version 3.10 ou plus)
⚠️ Coche **"Add Python to PATH"** pendant l'installation !

### Étape 2 — Lancer le projet
Double-clique sur le fichier **`lancer.bat`**

C'est tout ! Le script installe tout automatiquement.

### Étape 3 — Ouvrir dans le navigateur
```
http://localhost:5000
```

---

## 🔐 Comptes de test

| Rôle | Email | Mot de passe |
|------|-------|-------------|
| Direction | direction@ecole.ma | password |
| Professeur | prof@ecole.ma | password |
| Parent | parent@ecole.ma | password |

---

## 📁 Structure du projet

```
ecole-flask/
├── app.py              → Application Flask principale
├── models.py           → Modèles de base de données
├── requirements.txt    → Dépendances Python
├── lancer.bat          → Script de lancement Windows
│
├── routes/
│   ├── auth.py         → Connexion / déconnexion
│   ├── dashboard.py    → Tableau de bord
│   ├── messages.py     → Messagerie
│   ├── annonces.py     → Annonces
│   ├── devoirs.py      → Devoirs
│   ├── absences.py     → Absences
│   ├── rdv.py          → Rendez-vous
│   └── admin.py        → Administration
│
├── templates/          → Pages HTML (Jinja2)
└── static/             → CSS et JavaScript
```

---

## ✅ Avantages vs PHP

- ✅ Pas besoin de XAMPP
- ✅ Pas besoin de MySQL (SQLite intégré)
- ✅ Un seul fichier `lancer.bat` pour tout démarrer
- ✅ Pas de problèmes de chemins relatifs
- ✅ Base de données créée automatiquement
