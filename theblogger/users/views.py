from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, logout_user, current_user, login_required
from theblogger import db
from theblogger.models import User, BlogPost
from theblogger.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from theblogger.users.picture_handler import add_profile_pic

users = Blueprint("users", __name__)


# Registration view for new users
@users.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Thanks for registering! Have fun blogging")
        return redirect(url_for("users.login"))
    return render_template("register.html", form=form)


# Log in view
@users.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # if email doesn't exist render error page
        if user is None:
            return render_template("error_pages/unregistered_acc.html")

        # checking if the user provided the correct password
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash("Successfully logged in!")
            # registering the requested page that prompted the log in
            next = request.args.get("next")
            # setting next as home page if no next page was requested
            if next == None or not next[0] == "/":
                next = url_for("core.index")
            # redirecting the user to next page
            return redirect(next)
    return render_template("login.html", form=form)


# logging out the user and redirecting them to home page
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("core.index"))


# User account page
@users.route("/account", methods=["GET", "POST"])
@login_required  # the user has to be logged in to view their account
def account():
    form = UpdateUserForm()

    if form.validate_on_submit():
        # if the user has uplaoded picture the following is executed
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data, username)
            # setting the profile image of the user
            current_user.profile_image = pic
        # if the user has changed their username
        if form.username:
            current_user.username = form.username.data
        # if the user has changed their email
        if form.email:
            current_user.email = form.email.data

        # commit the changes made by the user to the db
        db.session.commit()
        flash("User Account has been Updated!")
        return redirect(url_for("users.account"))

    # show the user info if they're not posting any changes
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    # selecting the profile image
    profile_image = url_for(
        "static", filename="profile_pics"+current_user.profile_image)

    return render_template("account.html", profile_image=profile_image, form=form)


# Use posts view
@users.route("/<username>")
def user_posts(username):
    # using pages to go through the user's posts
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(
        BlogPost.date.desc()).paginate(page=page, per_page=5)
    return render_template("user_blog_posts.html", blog_posts=blog_posts, user=user)
