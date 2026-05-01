# CyberForum 赛博论坛

> 现代化响应式论坛系统，基于 Flask + SQLite + Nginx，支持暗色黑客主题。

![CyberForum](https://img.shields.io/badge/CyberForum-Python%20%F0%9F%90%8D-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 目录

- [特性](#特性)
- [技术栈](#技术栈)
- [快速部署](#快速部署)
- [手动部署](#手动部署)
- [配置说明](#配置说明)
- [使用指南](#使用指南)
- [目录结构](#目录结构)
- [故障排查](#故障排查)

---

## 特性

- ✅ **响应式设计** — 完美适配桌面端和移动端
- 🎨 **赛博朋克主题** — 暗色模式 + 霓虹光晕 + 扫描线效果
- 👤 **用户系统** — 注册、登录、个人资料、头像上传
- 📝 **帖子系统** — 发帖、评论、置顶、Markdown 支持
- 🔐 **管理员后台** — 用户管理、帖子管理、内容审核
- 📁 **图片上传** — 支持 PNG/JPG/GIF/WEBP，自动裁剪头像
- 🐳 **Docker 部署** — 一键启动，开箱即用

---

## 技术栈

| 组件 | 技术 |
|------|------|
| 后端 | Python 3.11 + Flask |
| 数据库 | SQLite（Flask-SQLAlchemy） |
| 用户认证 | Flask-Login |
| 图片处理 | Pillow |
| Web 服务器 | Nginx（反向代理） |
| 容器化 | Docker + Docker Compose |

---

## 快速部署

### 前置要求

- Linux 服务器（物理机 / 虚拟机 / NAS）
- 已安装 **Docker** 和 **Docker Compose**
- 端口 **3050**（HTTP）和 **3051**（HTTPS，已配置但未启用）

### 部署步骤

**1. 克隆项目**

```bash
git clone https://github.com/Connor888t/CyberForum.git
cd CyberForum
```

**2. 一键启动**

```bash
docker-compose up -d
```

**3. 访问论坛**

```
http://你的服务器IP:3050
```

**4. 登录管理员账号**

```
用户名: admin
密码:   admin123
```

> ⚠️ 首次登录后请立即修改管理员密码！

---

## 手动部署

如果不使用 Docker，需要手动安装依赖：

### 环境要求

- Python 3.9+
- Nginx
- 目录权限：uploads/ 和 avatars/ 需要写权限

### 安装步骤

```bash
# 1. 安装依赖
pip install flask flask-sqlalchemy flask-login pillow

# 2. 创建必要目录
mkdir -p uploads avatars

# 3. 启动 Flask
cd app
python app.py

# 4. Nginx 反向代理（参考 nginx/nginx.conf）
```

---

## 配置说明

### 环境变量

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `SECRET_KEY` | `cyberpunk-secret-key` | Flask 密钥，用于会话加密 |
| `FLASK_ENV` | `production` | 运行环境 |

在 `docker-compose.yml` 中修改：

```yaml
environment:
  - SECRET_KEY=你的随机密钥
  - FLASK_ENV=production
```

### 端口配置

默认端口映射：

| 容器内端口 | 宿主机端口 | 说明 |
|-----------|-----------|------|
| 80 | 3050 | HTTP |
| 443 | 3051 | HTTPS（需配置 SSL 证书）|

修改 `docker-compose.yml` 中的 `ports` 部分即可更换端口。

### SSL/HTTPS 配置

1. 准备 SSL 证书文件：
   ```bash
   mkdir -p ssl
   # 放入 your-domain.crt 和 your-domain.key
   ```

2. 编辑 `nginx/nginx.conf` 取消 SSL 相关注释

3. 修改 `docker-compose.yml` 中 nginx 的端口映射

---

## 使用指南

### 普通用户

| 操作 | 说明 |
|------|------|
| 注册账号 | 点击右上角「注册」，填写用户名、邮箱、密码 |
| 登录 | 使用注册账号登录 |
| 修改头像 | 登录后点击用户名 → 个人资料 → 上传头像 |
| 浏览帖子 | 首页展示所有帖子，点击标题进入详情 |
| 发帖 | 点击「发布帖子」，填写标题和内容 |
| 评论 | 在帖子详情页底部发表评论 |

### 管理员

访问 `http://你的IP:3050/admin`

| 功能 | 说明 |
|------|------|
| 用户管理 | 查看所有用户、删除用户 |
| 帖子管理 | 查看/删除所有帖子、置顶帖子 |
| 系统面板 | 论坛数据统计 |

---

## 目录结构

```
CyberForum/
├── app/
│   ├── __init__.py          # Flask 应用工厂
│   ├── app.py               # 主入口、蓝图注册、路由
│   ├── models.py            # 数据库模型（User/Post/Comment）
│   ├── auth/                # 认证模块（登录/注册/个人资料）
│   │   └── __init__.py
│   ├── posts/               # 帖子模块（发帖/查看/评论）
│   │   └── __init__.py
│   └── admin/               # 管理后台模块
│       └── __init__.py
├── templates/               # Jinja2 模板
│   ├── base.html            # 基础模板（导航/页脚/样式）
│   ├── index.html           # 首页
│   ├── auth/                # 认证相关页面
│   ├── posts/               # 帖子相关页面
│   └── admin/               # 管理后台页面
├── static/
│   ├── css/style.css         # 样式文件
│   └── images/               # 默认头像等静态资源
├── nginx/
│   └── nginx.conf            # Nginx 配置
├── uploads/                  # 用户上传的图片（不纳入 Git）
├── avatars/                  # 用户头像（不纳入 Git）
├── docker-compose.yml        # 容器编排配置
└── .gitignore               # Git 忽略规则
```

> `uploads/`、`avatars/` 和 `instance/` 目录不纳入 Git 版本控制。

---

## 故障排查

### 容器启动失败

```bash
# 查看容器日志
docker logs cyberforum
docker logs cyberforum-nginx

# 重启容器
docker-compose restart
```

### 502 Bad Gateway

通常是 Flask 容器未启动或崩溃：

```bash
docker ps | grep cyberforum
docker logs cyberforum --tail 20
```

### 图片无法上传

检查目录权限：

```bash
docker exec cyberforum ls -la /app/uploads
# 如果权限不足：
chmod 777 uploads avatars
```

### 权限问题（403 Forbidden）

参考：[docker-flask-nginx-permissions](https://github.com/Connor888t/CyberForum/wiki/docker-flask-nginx-permissions)

Nginx 以 `nginx` 用户运行，无法读取 Flask 写的文件。解决方法：

```python
import os
os.chmod(filepath, 0o644)  # 确保文件对所有用户可读
```

### 初始化管理员账号未创建

手动创建：

```python
# 进入容器
docker exec -it cyberforum sh

# 在 Python shell 中执行
python
from app import app, db
from models import create_default_admin
with app.app_context():
    db.create_all()
    create_default_admin()
    print("管理员创建成功")
```

---

## 许可证

MIT License — 可以自由使用、修改和分发。
