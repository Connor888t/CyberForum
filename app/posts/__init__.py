import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db, Post, Comment
from datetime import datetime

posts_bp = Blueprint('posts', __name__)

@posts_bp.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        image = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                filename = secure_filename(file.filename)
                unique_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_name)
                file.save(filepath)
                os.chmod(filepath, 0o644)  # 修复权限让nginx可读
                image = f"/uploads/{unique_name}"
        post = Post(title=title, content=content, author=current_user, image=image)
        db.session.add(post)
        db.session.commit()
        flash('帖子发布成功', 'success')
        return redirect(url_for('index'))
    return render_template('posts/create.html')

@posts_bp.route('/post/<int:post_id>')
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/view.html', post=post)

@posts_bp.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user.username != 'admin' and post.author != current_user:
        flash('无权删除此帖子', 'error')
        return redirect(url_for('index'))
    if post.image:
        try:
            os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], os.path.basename(post.image)))
        except: pass
    db.session.delete(post)
    db.session.commit()
    flash('帖子已删除', 'success')
    return redirect(url_for('index'))

@posts_bp.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    post = Post.query.get_or_404(post_id)
    content = request.form.get('content')
    comment = Comment(content=content, post=post, author=current_user)
    db.session.add(comment)
    db.session.commit()
    flash('评论已发布', 'success')
    return redirect(url_for('posts.view_post', post_id=post_id))

@posts_bp.route('/post/<int:post_id>/pin', methods=['POST'])
@login_required
def pin_post(post_id):
    if current_user.username != 'admin':
        flash('无权操作', 'error')
        return redirect(url_for('index'))
    post = Post.query.get_or_404(post_id)
    post.pinned = not post.pinned
    db.session.commit()
    flash('置顶状态已切换', 'success')
    return redirect(url_for('index'))
