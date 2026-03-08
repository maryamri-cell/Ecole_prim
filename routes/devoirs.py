from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Devoir, Eleve
from datetime import date

devoirs_bp = Blueprint('devoirs', __name__)

@devoirs_bp.route('/devoirs')
@login_required
def index():
    if current_user.role == 'professeur':
        devoirs = Devoir.query.filter_by(professeur_id=current_user.id)\
                        .order_by(Devoir.date_publication.desc()).all()
    elif current_user.role == 'parent':
        classes = [e.classe for e in Eleve.query.filter_by(parent_id=current_user.id).all()]
        devoirs = Devoir.query.filter(Devoir.classe.in_(classes))\
                        .order_by(Devoir.date_limite).all() if classes else []
    else:
        devoirs = Devoir.query.order_by(Devoir.date_publication.desc()).all()
    return render_template('modules/devoirs.html', devoirs=devoirs, today=date.today())

@devoirs_bp.route('/devoirs/ajouter', methods=['POST'])
@login_required
def ajouter():
    if current_user.role != 'professeur':
        flash('Accès non autorisé.', 'danger')
        return redirect(url_for('devoirs.index'))
    titre = request.form.get('titre', '').strip()
    classe = request.form.get('classe', '').strip()
    matiere = request.form.get('matiere', '').strip()
    description = request.form.get('description', '').strip()
    date_limite = None
    if request.form.get('date_limite'):
        try:
            date_limite = datetime.strptime(request.form.get('date_limite'), '%Y-%m-%d').date()
        except ValueError:
            date_limite = None
    if titre and classe:
        d = Devoir(professeur_id=current_user.id, titre=titre, classe=classe,
                   matiere=matiere, description=description, date_limite=date_limite)
        db.session.add(d)
        db.session.commit()
        flash('Devoir publié !', 'success')
    return redirect(url_for('devoirs.index'))

@devoirs_bp.route('/devoirs/supprimer/<int:id>', methods=['POST'])
@login_required
def supprimer(id):
    d = Devoir.query.get_or_404(id)
    if d.professeur_id != current_user.id:
        flash('Accès non autorisé.', 'danger')
        return redirect(url_for('devoirs.index'))
    db.session.delete(d)
    db.session.commit()
    flash('Devoir supprimé.', 'danger')
    return redirect(url_for('devoirs.index'))
