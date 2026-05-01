import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Post, Comment, create_default_admin
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'cyberpunk-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cyberforum.db'
app.config['UPLOAD_FOLDER'] = '/app/uploads'
app.config['AVATAR_FOLDER'] = '/app/avatars'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ============== 蓝图注册 ==============

from auth import auth_bp
from posts import posts_bp
from admin import admin_bp

app.register_blueprint(auth_bp)
app.register_blueprint(posts_bp)
app.register_blueprint(admin_bp)

# ============== 路由 ==============

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.pinned.desc(), Post.created_at.desc()).paginate(page=page, per_page=20)
    return render_template('index.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/avatars/<filename>')
def serve_avatar(filename):
    return send_from_directory(app.config['AVATAR_FOLDER'], filename)

@app.route('/upload/avatar', methods=['POST'])
@login_required
def upload_avatar():
    if 'avatar' not in request.files:
        flash('没有选择文件', 'error')
        return redirect(url_for('auth.profile', username=current_user.username))
    file = request.files['avatar']
    if file.filename == '':
        flash('没有选择文件', 'error')
        return redirect(url_for('auth.profile', username=current_user.username))
    if file and allowed_file(file.filename):
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f'user_{current_user.id}_avatar.{ext}'
        filepath = os.path.join(app.config['AVATAR_FOLDER'], filename)
        # 裁剪为正方形头像
        try:
            img = Image.open(file)
            size = min(img.size)
            left = (img.size[0] - size) // 2
            top = (img.size[1] - size) // 2
            img = img.crop((left, top, left + size, top + size))
            img = img.resize((200, 200), Image.LANCZOS)
            img.save(filepath, quality=85)
            os.chmod(filepath, 0o644)  # 确保nginx可读
        except Exception as e:
            flash(f'图片处理失败: {str(e)}', 'error')
            return redirect(url_for('auth.profile', username=current_user.username))
        # 更新数据库
        current_user.avatar = f'/avatars/{filename}'
        db.session.commit()
        flash('头像更新成功！', 'success')
    else:
        flash('不支持的文件格式，请上传 png/jpg/gif/webp 图片', 'error')
    return redirect(url_for('auth.profile', username=current_user.username))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ============== 启动 ==============

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_default_admin()
    app.run(host='0.0.0.0', port=5000, debug=False)
