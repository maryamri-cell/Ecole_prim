from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import Annonce, Message, Devoir, Absence, RendezVous, Eleve, User
from datetime import date

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def index():
    stats = {}
    annonces = Annonce.query.order_by(Annonce.date_publication.desc()).limit(3).all()
    unread_msgs = Message.query.filter_by(destinataire_id=current_user.id, lu=False)\
                               .order_by(Message.date_envoi.desc()).limit(5).all()
    devoirs = []
    rdvs = []

    if current_user.role == 'direction':
        stats = {
            'users': User.query.count(),
            'eleves': Eleve.query.count(),
            'annonces': Annonce.query.count(),
            'messages': Message.query.count(),
        }

    elif current_user.role == 'professeur':
        stats = {
            'classes': Eleve.query.filter_by(professeur_id=current_user.id)\
                           .with_entities(Eleve.classe).distinct().count(),
            'devoirs': Devoir.query.filter_by(professeur_id=current_user.id).count(),
            'absences_today': Absence.query.filter_by(professeur_id=current_user.id)\
                                     .filter(Absence.date == date.today()).count(),
            'non_lus': len(unread_msgs),
        }
        devoirs = Devoir.query.filter_by(professeur_id=current_user.id)\
                        .filter(Devoir.date_limite >= date.today())\
                        .order_by(Devoir.date_limite).limit(3).all()

    elif current_user.role == 'parent':
        enfants = Eleve.query.filter_by(parent_id=current_user.id).all()
        classes = [e.classe for e in enfants]
        stats = {
            'enfants': len(enfants),
            'absences': Absence.query.join(Eleve).filter(Eleve.parent_id == current_user.id).count(),
            'non_lus': len(unread_msgs),
            'rdvs': RendezVous.query.filter_by(parent_id=current_user.id).count(),
        }
        if classes:
            devoirs = Devoir.query.filter(Devoir.classe.in_(classes))\
                            .filter(Devoir.date_limite >= date.today())\
                            .order_by(Devoir.date_limite).limit(3).all()

    rdvs = RendezVous.query.filter(
        ((RendezVous.parent_id == current_user.id) | (RendezVous.professeur_id == current_user.id)),
        RendezVous.statut != 'annule'
    ).order_by(RendezVous.date_heure).limit(3).all()

    return render_template('dashboard/index.html',
        stats=stats, annonces=annonces, unread_msgs=unread_msgs,
        devoirs=devoirs, rdvs=rdvs, today=date.today())
