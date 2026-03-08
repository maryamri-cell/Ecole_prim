from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Message, User

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('/messagerie')
@login_required
def index():
    msgs = Message.query.filter(
        (Message.expediteur_id == current_user.id) |
        (Message.destinataire_id == current_user.id)
    ).order_by(Message.date_envoi.desc()).all()

    selected = None
    msg_id = request.args.get('id', type=int)
    if msg_id:
        selected = Message.query.get(msg_id)
        if selected and selected.destinataire_id == current_user.id:
            selected.lu = True
            db.session.commit()

    users = User.query.filter(User.id != current_user.id).order_by(User.role, User.nom).all()
    return render_template('modules/messagerie.html', msgs=msgs, selected=selected, users=users)

@messages_bp.route('/messagerie/envoyer', methods=['POST'])
@login_required
def envoyer():
    dest_id = request.form.get('destinataire_id', type=int)
    sujet = request.form.get('sujet', '').strip()
    contenu = request.form.get('contenu', '').strip()
    if dest_id and contenu:
        msg = Message(expediteur_id=current_user.id, destinataire_id=dest_id,
                      sujet=sujet, contenu=contenu)
        db.session.add(msg)
        db.session.commit()
        flash('Message envoyé !', 'success')
    return redirect(url_for('messages.index'))
