from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Absence, Eleve
from datetime import datetime, date

absences_bp = Blueprint('absences', __name__)

@absences_bp.route('/absences')
@login_required
def index():
    if current_user.role == 'professeur':
        absences = Absence.query.filter_by(professeur_id=current_user.id)\
                          .order_by(Absence.date.desc()).all()
        eleves = Eleve.query.filter_by(professeur_id=current_user.id)\
                       .order_by(Eleve.classe, Eleve.nom).all()
    elif current_user.role == 'parent':
        absences = Absence.query.join(Eleve)\
                          .filter(Eleve.parent_id == current_user.id)\
                          .order_by(Absence.date.desc()).all()
        eleves = []
    else:
        absences = Absence.query.order_by(Absence.date.desc()).all()
        eleves = Eleve.query.all()
    return render_template('modules/absences.html', absences=absences, eleves=eleves, today=date.today())

@absences_bp.route('/absences/ajouter', methods=['POST'])
@login_required
def ajouter():
    eleve_id = request.form.get('eleve_id', type=int)
    type_ = request.form.get('type', 'absence')
    motif = request.form.get('motif', '').strip()
    date_ = None
    if request.form.get('date'):
        try:
            date_ = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
        except ValueError:
            date_ = date.today()
    else:
        date_ = date.today()
    if eleve_id:
        a = Absence(eleve_id=eleve_id, professeur_id=current_user.id,
                    type=type_, motif=motif, date=date_)
        db.session.add(a)
        db.session.commit()
        flash('Absence signalée !', 'success')
    return redirect(url_for('absences.index'))

@absences_bp.route('/absences/justifier/<int:id>', methods=['POST'])
@login_required
def justifier(id):
    a = Absence.query.get_or_404(id)
    a.justifie = True
    db.session.commit()
    flash('Absence justifiée.', 'success')
    return redirect(url_for('absences.index'))

@absences_bp.route('/absences/supprimer/<int:id>', methods=['POST'])
@login_required
def supprimer(id):
    a = Absence.query.get_or_404(id)
    db.session.delete(a)
    db.session.commit()
    flash('Absence supprimée.', 'danger')
    return redirect(url_for('absences.index'))
