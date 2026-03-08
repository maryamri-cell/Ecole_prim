from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from models import db, User, Eleve

admin_bp = Blueprint('admin', __name__)

def direction_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_user.role != 'direction':
            flash('Accès non autorisé.', 'danger')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated

@admin_bp.route('/admin/utilisateurs')
@login_required
@direction_required
def users():
    all_users = User.query.order_by(User.role, User.nom).all()
    return render_template('admin/users.html', users=all_users)

@admin_bp.route('/admin/utilisateurs/ajouter', methods=['POST'])
@login_required
@direction_required
def add_user():
    nom = request.form.get('nom', '').strip()
    prenom = request.form.get('prenom', '').strip()
    email = request.form.get('email', '').strip()
    role = request.form.get('role', 'parent')
    password = request.form.get('password', 'ecole2024')
    if nom and prenom and email:
        if User.query.filter_by(email=email).first():
            flash('Cet email existe déjà.', 'danger')
        else:
            u = User(nom=nom, prenom=prenom, email=email, role=role,
                     mot_de_passe=generate_password_hash(password))
            db.session.add(u)
            db.session.commit()
            flash('Utilisateur créé !', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/admin/utilisateurs/supprimer/<int:id>', methods=['POST'])
@login_required
@direction_required
def del_user(id):
    if id == current_user.id:
        flash('Vous ne pouvez pas supprimer votre propre compte.', 'danger')
        return redirect(url_for('admin.users'))
    u = User.query.get_or_404(id)
    db.session.delete(u)
    db.session.commit()
    flash('Utilisateur supprimé.', 'danger')
    return redirect(url_for('admin.users'))

@admin_bp.route('/admin/eleves')
@login_required
@direction_required
def eleves():
    all_eleves = Eleve.query.order_by(Eleve.classe, Eleve.nom).all()
    parents = User.query.filter_by(role='parent').order_by(User.nom).all()
    profs = User.query.filter_by(role='professeur').order_by(User.nom).all()
    classes = ['CP-A','CP-B','CE1-A','CE1-B','CE2-A','CE2-B','CM1-A','CM1-B','CM2-A','CM2-B']
    return render_template('admin/eleves.html', eleves=all_eleves,
                           parents=parents, profs=profs, classes=classes)

@admin_bp.route('/admin/eleves/ajouter', methods=['POST'])
@login_required
@direction_required
def add_eleve():
    nom = request.form.get('nom', '').strip()
    prenom = request.form.get('prenom', '').strip()
    classe = request.form.get('classe', '').strip()
    parent_id = request.form.get('parent_id', type=int) or None
    prof_id = request.form.get('professeur_id', type=int) or None
    if nom and prenom and classe:
        e = Eleve(nom=nom, prenom=prenom, classe=classe,
                  parent_id=parent_id, professeur_id=prof_id)
        db.session.add(e)
        db.session.commit()
        flash('Élève ajouté !', 'success')
    return redirect(url_for('admin.eleves'))

@admin_bp.route('/admin/eleves/supprimer/<int:id>', methods=['POST'])
@login_required
@direction_required
def del_eleve(id):
    e = Eleve.query.get_or_404(id)
    db.session.delete(e)
    db.session.commit()
    flash('Élève supprimé.', 'danger')
    return redirect(url_for('admin.eleves'))
