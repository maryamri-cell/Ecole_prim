from flask import Flask
from flask_login import current_user
from extensions import db, login_manager
import os


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ecole-secret-key-2024'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecole.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Veuillez vous connecter.'

    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.messages import messages_bp
    from routes.annonces import annonces_bp
    from routes.devoirs import devoirs_bp
    from routes.absences import absences_bp
    from routes.rdv import rdv_bp
    from routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(messages_bp)
    app.register_blueprint(annonces_bp)
    app.register_blueprint(devoirs_bp)
    app.register_blueprint(absences_bp)
    app.register_blueprint(rdv_bp)
    app.register_blueprint(admin_bp)

    @app.context_processor
    def inject_helpers():
        def unread_count():
            if current_user.is_authenticated:
                from models import Message
                return Message.query.filter_by(destinataire_id=current_user.id, lu=False).count()
            return 0
        return dict(unread_count=unread_count)

    with app.app_context():
        db.create_all()
        seed_data()

    return app

def seed_data():
    from models import User, Eleve, Annonce, Devoir
    from werkzeug.security import generate_password_hash
    from datetime import date, timedelta

    if User.query.first():
        return

    direction = User(nom='Admin', prenom='Direction', email='direction@ecole.ma',
                     mot_de_passe=generate_password_hash('password'), role='direction')
    prof = User(nom='Benali', prenom='Ahmed', email='prof@ecole.ma',
                mot_de_passe=generate_password_hash('password'), role='professeur')
    parent = User(nom='Alami', prenom='Fatima', email='parent@ecole.ma',
                  mot_de_passe=generate_password_hash('password'), role='parent')
    db.session.add_all([direction, prof, parent])
    db.session.flush()

    e1 = Eleve(nom='Alami', prenom='Youssef', classe='CM2-A', parent_id=parent.id, professeur_id=prof.id)
    e2 = Eleve(nom='Alami', prenom='Sara', classe='CE1-B', parent_id=parent.id, professeur_id=prof.id)
    db.session.add_all([e1, e2])

    a1 = Annonce(auteur_id=direction.id, titre='Bienvenue sur EcoleCom !',
                 contenu='Bienvenue sur la plateforme de communication de notre école.', type='general')
    a2 = Annonce(auteur_id=direction.id, titre='Réunion parents-professeurs',
                 contenu='Une réunion est prévue le 15 du mois prochain.', type='reunion')
    db.session.add_all([a1, a2])

    d1 = Devoir(professeur_id=prof.id, classe='CM2-A', matiere='Mathématiques',
                titre='Exercices fractions', description='Faire les exercices 1 à 5 page 48.',
                date_limite=date.today() + timedelta(days=7))
    d2 = Devoir(professeur_id=prof.id, classe='CM2-A', matiere='Français',
                titre='Rédaction vacances', description='Écrire 10 lignes sur vos vacances.',
                date_limite=date.today() + timedelta(days=5))
    db.session.add_all([d1, d2])
    db.session.commit()

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
