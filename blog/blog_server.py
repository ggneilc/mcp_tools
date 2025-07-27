# app.py
from flask import Flask, request, jsonify, abort, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Use a local SQLite database file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
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
    posts = [p.to_dict() for p in Post.query.all()]
    return render_template('index.html', posts=posts)

@app.route("/posts", methods=["GET"])
def list_posts():
    posts = Post.query.all()
    return jsonify([p.to_dict() for p in posts])

@app.route("/posts/<int:post_id>", methods=["GET"])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

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
