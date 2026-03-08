from extensions import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('direction','professeur','parent','eleve'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def initiales(self):
        return (self.prenom[0] + self.nom[0]).upper()

    def role_label(self):
        labels = {'direction':'Direction','professeur':'Professeur','parent':'Parent','eleve':'Élève'}
        return labels.get(self.role, self.role)

class Eleve(db.Model):
    __tablename__ = 'eleves'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    classe = db.Column(db.String(20), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    professeur_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    parent = db.relationship('User', foreign_keys=[parent_id], backref='enfants')
    professeur = db.relationship('User', foreign_keys=[professeur_id])

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    expediteur_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    destinataire_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    sujet = db.Column(db.String(255))
    contenu = db.Column(db.Text, nullable=False)
    lu = db.Column(db.Boolean, default=False)
    date_envoi = db.Column(db.DateTime, default=datetime.utcnow)
    expediteur = db.relationship('User', foreign_keys=[expediteur_id])
    destinataire = db.relationship('User', foreign_keys=[destinataire_id])

class Annonce(db.Model):
    __tablename__ = 'annonces'
    id = db.Column(db.Integer, primary_key=True)
    auteur_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    titre = db.Column(db.String(200), nullable=False)
    contenu = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), default='general')
    date_evenement = db.Column(db.Date)
    date_publication = db.Column(db.DateTime, default=datetime.utcnow)
    auteur = db.relationship('User', foreign_keys=[auteur_id])

class Devoir(db.Model):
    __tablename__ = 'devoirs'
    id = db.Column(db.Integer, primary_key=True)
    professeur_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    classe = db.Column(db.String(20), nullable=False)
    matiere = db.Column(db.String(100))
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    date_limite = db.Column(db.Date)
    date_publication = db.Column(db.DateTime, default=datetime.utcnow)
    professeur = db.relationship('User', foreign_keys=[professeur_id])

class Absence(db.Model):
    __tablename__ = 'absences'
    id = db.Column(db.Integer, primary_key=True)
    eleve_id = db.Column(db.Integer, db.ForeignKey('eleves.id'), nullable=False)
    professeur_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.Enum('absence','retard'), nullable=False)
    motif = db.Column(db.Text)
    justifie = db.Column(db.Boolean, default=False)
    date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    eleve = db.relationship('Eleve', foreign_keys=[eleve_id])
    professeur = db.relationship('User', foreign_keys=[professeur_id])

class RendezVous(db.Model):
    __tablename__ = 'rendez_vous'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    professeur_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_heure = db.Column(db.DateTime, nullable=False)
    statut = db.Column(db.String(20), default='en_attente')
    motif = db.Column(db.Text)
    note_professeur = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    parent = db.relationship('User', foreign_keys=[parent_id])
    professeur = db.relationship('User', foreign_keys=[professeur_id])
