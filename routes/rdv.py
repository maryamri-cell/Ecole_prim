from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, RendezVous, User, Eleve
from datetime import datetime

rdv_bp = Blueprint('rdv', __name__)

@rdv_bp.route('/rendez-vous')
@login_required
def index():
    rdvs = RendezVous.query.filter(
        (RendezVous.parent_id == current_user.id) |
        (RendezVous.professeur_id == current_user.id)
    ).order_by(RendezVous.date_heure.desc()).all()

    professeurs = []
    if current_user.role == 'parent':
        eleve_profs = Eleve.query.filter_by(parent_id=current_user.id).all()
        prof_ids = list({e.professeur_id for e in eleve_profs if e.professeur_id})
        professeurs = User.query.filter(User.id.in_(prof_ids)).all() if prof_ids else \
                      User.query.filter_by(role='professeur').all()

    return render_template('modules/rendez-vous.html', rdvs=rdvs, professeurs=professeurs)

@rdv_bp.route('/rendez-vous/ajouter', methods=['POST'])
@login_required
def ajouter():
    prof_id = request.form.get('professeur_id', type=int)
    date_heure_str = request.form.get('date_heure')
    motif = request.form.get('motif', '').strip()
    date_heure = None
    if date_heure_str:
        try:
            date_heure = datetime.fromisoformat(date_heure_str)
        except (ValueError, TypeError):
            date_heure = None
    if prof_id and date_heure:
        r = RendezVous(parent_id=current_user.id, professeur_id=prof_id,
                       date_heure=date_heure, motif=motif)
        db.session.add(r)
        db.session.commit()
        flash('Demande de rendez-vous envoyée !', 'success')
    return redirect(url_for('rdv.index'))

@rdv_bp.route('/rendez-vous/confirmer/<int:id>', methods=['POST'])
@login_required
def confirmer(id):
    r = RendezVous.query.get_or_404(id)
    r.statut = 'confirme'
    r.note_professeur = request.form.get('note', '').strip()
    db.session.commit()
    flash('Rendez-vous confirmé !', 'success')
    return redirect(url_for('rdv.index'))

@rdv_bp.route('/rendez-vous/annuler/<int:id>', methods=['POST'])
@login_required
def annuler(id):
    r = RendezVous.query.get_or_404(id)
    r.statut = 'annule'
    db.session.commit()
    flash('Rendez-vous annulé.', 'danger')
    return redirect(url_for('rdv.index'))
