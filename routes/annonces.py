from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Annonce
from datetime import datetime, date

annonces_bp = Blueprint('annonces', __name__)

@annonces_bp.route('/annonces')
@login_required
def index():
    type_filter = request.args.get('type', '')
    query = Annonce.query
    if type_filter:
        query = query.filter_by(type=type_filter)
    annonces = query.order_by(Annonce.date_publication.desc()).all()
    return render_template('modules/annonces.html', annonces=annonces, type_filter=type_filter)

@annonces_bp.route('/annonces/ajouter', methods=['POST'])
@login_required
def ajouter():
    if current_user.role != 'direction':
        flash('Accès non autorisé.', 'danger')
        return redirect(url_for('annonces.index'))
    titre = request.form.get('titre', '').strip()
    contenu = request.form.get('contenu', '').strip()
    type_ = request.form.get('type', 'general')
    date_evt = None
    if request.form.get('date_evenement'):
        try:
            date_evt = datetime.strptime(request.form.get('date_evenement'), '%Y-%m-%d').date()
        except ValueError:
            date_evt = None
    if titre and contenu:
        a = Annonce(auteur_id=current_user.id, titre=titre, contenu=contenu,
                    type=type_, date_evenement=date_evt)
        db.session.add(a)
        db.session.commit()
        flash('Annonce publiée !', 'success')
    return redirect(url_for('annonces.index'))

@annonces_bp.route('/annonces/supprimer/<int:id>', methods=['POST'])
@login_required
def supprimer(id):
    if current_user.role != 'direction':
        flash('Accès non autorisé.', 'danger')
        return redirect(url_for('annonces.index'))
    a = Annonce.query.get_or_404(id)
    db.session.delete(a)
    db.session.commit()
    flash('Annonce supprimée.', 'danger')
    return redirect(url_for('annonces.index'))
