from flask import render_template, url_for, flash, redirect, request, abort
from solstice import app, db, bcrypt
from solstice.models import User, Project, Forum
from solstice.forms import RegistrationForm, LoginForm, UpdateAccountForm, ProjectForm
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image
import secrets
import os

projects = [
    {
        'id': 17,
        'nick': 'Ivan Paljetak',
        'pfp': 'https://yt3.ggpht.com/ytc/AAUvwng5jRdtCNaiyXmRiBMrlJnEcIxnISVC8N_Na-Fb=s88-c-k-c0x00ffffff-no-rj',
        'content': 'First post content',
        'score': 47,
        'replies': 6
    },
    {
        'id': 18,
        'nick': 'Ivan Paljetak #2',
        'pfp': 'https://yt3.ggpht.com/ytc/AAUvwng5jRdtCNaiyXmRiBMrlJnEcIxnISVC8N_Na-Fb=s88-c-k-c0x00ffffff-no-rj',
        'content': 'Second post content',
        'score': 31,
        'replies': 4
    }
]

topics = [
    {
        'id': 1,
        'nick': 'Algebra'
    },
    {
        'id': 1,
        'nick': 'Grammar'
    },
    {
        'id': 1,
        'nick': 'Microbiology'
    },
    {
        'id': 1,
        'nick': 'Programming'
    },
    {
        'id': 1,
        'nick': 'Geometry'
    }
]

forums = [
    {
        'id': 19,
        'nick': 'Ivan Paljetak',
        'pfp': 'https://yt3.ggpht.com/ytc/AAUvwng5jRdtCNaiyXmRiBMrlJnEcIxnISVC8N_Na-Fb=s88-c-k-c0x00ffffff-no-rj',
        'dir': 'Math',
        'dir_c': 'primary',
        'content': 'An example post hahahahahahahaha lol this is just an example lollllll',
        'score': 157,
        'replies': 8,

        'id2': 20,
        'nick2': 'I.P',
        'pfp2': 'unknown',
        'content2': 'This is an example reponse to the question asked.',
        'score2': 204
    },
    {
        'id': 21,
        'nick': 'Ivan Paljetak',
        'pfp': 'https://yt3.ggpht.com/ytc/AAUvwng5jRdtCNaiyXmRiBMrlJnEcIxnISVC8N_Na-Fb=s88-c-k-c0x00ffffff-no-rj',
        'dir': 'Science',
        'dir_c': 'danger',
        'content': 'An example post hahahahahahahaha lol this is just an example lollllll',
        'score': 157,
        'replies': 8,

        'id2': 22,
        'nick2': 'I.P',
        'pfp2': 'unknown',
        'content2': 'This is an example reponse to the question asked.',
        'score2': 204
    }
]

#########################
## REQUIRED APP ROUTES ##
#########################

@app.route("/")
@app.route("/feed")
def home():
    if current_user.is_authenticated:
        projects = Project.query.all()
        return render_template('home.html', projects=projects, topics=topics, forums=forums)
    else:
        return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            redir = request.args.get("next")
            return redirect(redir) if redir else redirect(url_for("home"))
        else:
            flash("Incorrect credentials.")
    return render_template('login.html', title='Sign in', form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created. Please log in.")
        return redirect(url_for("login"))
    return render_template('register.html', title='Register', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/projects")
@login_required
def proj():
    return render_template('projects.html', projects=projects, title='Projects')

@app.route("/forums")
@login_required
def forum():
    return render_template('forums.html', forums=forums, title='Forums')

@app.route("/search")
@login_required
def search():
    return render_template('search.html', title='Search')

@app.route("/exclusive")
@login_required
def exclusive():
    return render_template('news.html', forums=forums, title='News')

@app.route("/user")
@login_required
def user():
    return render_template('user.html', title='User')

@app.route("/me", methods=["GET", "POST"])
@login_required
def me():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_pic(form.picture.data)
            current_user.pfp = picture_file
            print(current_user.pfp)
        current_user.name = form.name.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Account successfully updated.")
        return redirect(url_for("me"))
    elif request.method == "GET":
        form.name.data = current_user.name
        form.username.data = current_user.username
        form.email.data = current_user.email
    img_file = url_for("static", filename="img/pfp/" + current_user.pfp)
    return render_template('account.html', title='Account', img_file=img_file, form=form)

@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    project = ProjectForm()
    if project.validate_on_submit():
        post = Project(content=project.content.data, survey=project.survey.data, project_uploader=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Project added.")
        return redirect(url_for("home"))
    return render_template('upload.html', title='Upload to Solstice', project=project)

@app.route("/upload/forum", methods=["GET", "POST"])
@login_required
def upload_forum():
    project = ProjectForm()
    if project.validate_on_submit():
        post = Project(content=project.content.data, survey=project.survey.data, project_uploader=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Project added.")
        return redirect(url_for("home"))
    return render_template('upload2.html', title='Upload to Solstice', project=project)

@app.route("/project/<project_id>")
@login_required
def project(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('project.html', project=project, title="Project")

@app.route("/project/<project_id>/edit", methods=["GET", "POST"])
@login_required
def update_project(project_id):
    post = Project.query.get_or_404(project_id)
    if post.project_uploader != current_user:
        abort(403)
    form = ProjectForm()
    if request.method == "GET":
        form.content.data = post.content
        form.survey.data = post.survey
    elif form.validate_on_submit:
        post.content = form.content.data
        post.survey = form.survey.data
        db.session.commit()
        flash("Project updated.")
        return redirect(url_for("project", project_id=post.id))
    return render_template('upload.html', title='Edit Project', project=form)

@app.route("/project/<project_id>/delete", methods=["GET", "POST"])
@login_required
def delete_project(project_id):
    post = Project.query.get_or_404(project_id)
    if post.project_uploader != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Project deleted.")
    return redirect(url_for("home"))


#######################
## IMAGE PROCCESSING ##
#######################


def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

def crop_max_square(pic):
    return crop_center(pic, min(pic.size), min(pic.size))

def save_pic(fpic):
    print("recieved.")
    hex = secrets.token_hex(16)
    _, fext = os.path.splitext(fpic.filename)
    filename = hex + fext
    file_path = os.path.join(app.root_path, "static/img/pfp", filename)
    i = crop_max_square(Image.open(fpic)).resize((72, 72))
    i.save(file_path)
    return filename
