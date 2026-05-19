from flask import Flask, render_template, redirect, jsonify
from flask import session as flask_session

from data import db_session
from data.posts import Post
from data.users import User

from forms.login import LoginForm
from forms.register import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'

db_session.global_init("db/music.db")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()

        user = db_sess.query(User).filter(User.email == form.email.data).first()

        if user and user.check_password(form.password.data):
            flask_session["user_id"] = user.id
            return redirect("/")

        return "Неверный логин или пароль"

    return render_template("login.html", form=form)


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()

        if db_sess.query(User).filter(User.email == form.email.data).first():
            return "Такой пользователь уже есть"

        user = User(
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)

        db_sess.add(user)
        db_sess.commit()

        return redirect("/login")

    return render_template("register.html", form=form)


# ---------------- HOME ----------------
@app.route("/")
def index():
    db_sess = db_session.create_session()
    posts = db_sess.query(Post).all()

    return render_template(
        "index.html",
        posts=posts,
        user_id=flask_session.get("user_id")
    )


# ---------------- ADD POST ----------------
@app.route("/add_post", methods=["GET", "POST"])
def add_post():
    from forms.post import PostForm

    form = PostForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()

        post = Post(
            title=form.title.data,
            content=form.content.data,
            author=form.author.data,
            user_id=flask_session.get("user_id")
        )

        db_sess.add(post)
        db_sess.commit()

        return redirect("/")

    return render_template("add_post.html", form=form)


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    flask_session.pop("user_id", None)
    return redirect("/")


# ---------------- API ----------------
@app.route("/api/posts")
def api_posts():
    db_sess = db_session.create_session()
    posts = db_sess.query(Post).all()

    return jsonify([
        {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "author": post.author,
            "user_id": post.user_id
        }
        for post in posts
    ])

@app.route("/post_delete/<int:post_id>")
def delete_post(post_id):
    db_sess = db_session.create_session()

    user_id = flask_session.get("user_id")
    if not user_id:
        return redirect("/login")

    post = db_sess.query(Post).filter(Post.id == post_id).first()

    if not post:
        return redirect("/")

    # если у поста есть владелец — проверяем
    if getattr(post, "user_id", None):
        if post.user_id != user_id:
            return "❌ Нельзя удалять чужие посты"

    db_sess.delete(post)
    db_sess.commit()

    return redirect("/")

if __name__ == "__main__":
    app.run(port=8080, host="127.0.0.1")
