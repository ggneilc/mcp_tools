from flask import Flask, request, jsonify, abort, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, instance_relative_config=True)

# ensure instance folder is created
os.makedirs(app.instance_path, exist_ok=True)
db_path = os.path.join(app.instance_path, 'blog.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Models ---
class Post(db.Model):
    id      = db.Column(db.Integer, primary_key=True)
    title   = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tags    = db.Column(db.String(200), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "tags": [t.strip() for t in self.tags.split(",")] if self.tags else []
        }

# Create tables if they don’t exist
with app.app_context():
    db.create_all()

# --- Routes ---
@app.route('/')
def home():
    posts = [p.to_dict() for p in Post.query.order_by(Post.id.desc()).limit(5).all()]
    return render_template('index.html', posts=posts)

@app.route("/posts", methods=["GET"])
def list_posts():
    posts = Post.query.all()
    return jsonify([p.to_dict() for p in posts])

@app.route("/posts/<int:post_id>", methods=["GET"])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)


@app.route("/posts/<int:post_id>", methods=["PUT"])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    data = request.get_json() or {}

    title = data.get("title")
    content = data.get("content")
    tags = data.get("tags")

    # If nothing to update, return 400
    if title is None and content is None and tags is None:
        abort(400, "At least one of title, content, or tags must be provided.")

    if title is not None:
        post.title = title
    if content is not None:
        post.content = content
    if tags is not None:
        # Normalize tags: accept list/tuple or comma string
        if isinstance(tags, (list, tuple)):
            post.tags = ",".join(tags)
        else:
            post.tags = str(tags)

    db.session.commit()
    return jsonify(post.to_dict()), 200

@app.route("/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return '', 204

@app.route("/posts", methods=["POST"])
def create_post():
    data = request.get_json() or {}
    title   = data.get("title")
    content = data.get("content")
    tags    = data.get("tags", [])

    if not title or not content:
        abort(400, "Both title and content are required.")

    # Store tags as comma-separated string
    tags_str = ",".join(tags) if isinstance(tags, (list, tuple)) else str(tags)

    post = Post(title=title, content=content, tags=tags_str)
    db.session.add(post)
    db.session.commit()

    return jsonify(post.to_dict()), 201

if __name__ == "__main__":
    app.run(debug=True)
