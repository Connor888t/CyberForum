from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, User, Post, Comment

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/panel')
@login_required
def panel():
    if current_user.username != 'admin':
        flash('无权访问', 'error')
        return redirect(url_for('index'))
    stats = {
        'users': User.query.count(),
        'posts': Post.query.count(),
        'comments': Comment.query.count()
    }
    return render_template('admin/panel.html', stats=stats)

@admin_bp.route('/users')
@login_required
def users():
    if current_user.username != 'admin':
        flash('无权访问', 'error')
        return redirect(url_for('index'))
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/posts')
@login_required
def posts():
    if current_user.username != 'admin':
        flash('无权访问', 'error')
        return redirect(url_for('index'))
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('admin/posts.html', posts=posts)

