from flask import Flask, render_template, url_for, flash, session, request, redirect
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from forms import AdminLogin, NewEvent, NewProject
from werkzeug.utils import secure_filename
from flask import current_app
from uuid import uuid4
import os
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'password'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///komarovi.db'
app.config['SECRET_KEY'] = '5792318bb0b13ce0c67dfde280ba245'
db = SQLAlchemy(app)
migrate = Migrate(app,db)

login_manager = LoginManager(app)
login_manager.login_view = 'adminlogin' 

def make_unique(string):
    ident = uuid4().__str__()
    return f"{ident}-{string}"


class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text)
    registration_link = db.Column(db.String(500))
    location = db.Column(db.String(500))
    image = db.Column(db.String(200))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.id

class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text)
    funding_goal = db.Column(db.Integer, nullable=False, default=0)
    current_amount = db.Column(db.Integer, nullable=False, default=0)
    image = db.Column(db.String(200))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Project %r>' % self.id

class AdminUser(UserMixin):
    id = "admin" 
@login_manager.user_loader
def load_user(user_id):
    if user_id == "admin":
        return AdminUser()
    return None

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html', current_page='home')

@app.route("/news")
def news():
    return render_template('news.html', current_page='news')

@app.route("/events")
def events():
    allEvents = Events.query.order_by(Events.date_added)
    return render_template('events.html', current_page='events', events=allEvents)

@app.route("/events/<int:id>")
def event(id):
    event = Events.query.get_or_404(id)
    return render_template('event.html', event=event)

@app.route("/projects")
def projects():
    allProjects = Projects.query.order_by(Projects.date_added)
    return render_template('projects.html', current_page='projects', projects=allProjects)

@app.route("/projects/<int:id>")
def project(id):
    project = Projects.query.get_or_404(id)
    return render_template('project.html', project=project)

@app.route("/projects/donate/<int:id>", methods=['POST'])
def donate(id):
    project = Projects.query.get_or_404(id)
    amount = int(request.form.get("amount", 0))  # donation amount from form
    if amount > 0:
        project.current_amount += amount
        db.session.commit()
    return redirect(url_for('project', id=id))

@app.route("/adminpanel")
@login_required
def adminpanel():
    return render_template('adminpanel.html')

@app.route("/adminpanel/events", methods=['GET', 'POST'])
@login_required
def add_events():
    form = NewEvent()
    allEvents = Events.query.order_by(Events.date_added)
    if form.validate_on_submit():
        filename = None
        if form.image.data:

            filename = secure_filename(form.image.data.filename)
            filename = make_unique(filename)
            upload_path = os.path.join(current_app.root_path, 'static/uploads', filename)
            form.image.data.save(upload_path)


        event = Events(
            title=form.title.data,
            description=form.description.data,
            registration_link=form.registration_link.data,
            location=form.location.data,
            image=filename  
        )

        db.session.add(event)
        db.session.commit()

        return redirect(url_for('add_events'))

    return render_template('add_events.html', form=form, events=allEvents)

@app.route("/adminpanel/events/update/<int:id>", methods=['GET', 'POST'])
@login_required
def update_event(id):
    event = Events.query.get_or_404(id)
    filename=None
    form = NewEvent()
    if form.validate_on_submit():
        if form.image.data:

            filename = secure_filename(form.image.data.filename)
            filename = make_unique(filename)
            upload_path = os.path.join(current_app.root_path, 'static/uploads', filename)
            form.image.data.save(upload_path)
        event.title = form.title.data
        event.description=form.description.data
        event.registration_link=form.registration_link.data
        event.location=form.location.data
        event.image=filename
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('events'))
    form.title.data = event.title
    form.description.data=event.description
    form.registration_link.data = event.registration_link
    form.location.data=event.location
    form.image.data=event.image
    return render_template('update_events.html', form=form, event=event)

@app.route("/adminpanel/events/delete/<int:id>", methods=['GET', 'POST'])
@login_required
def delete_event(id):
    event_to_delete = Events.query.get_or_404(id)
    try:
        if event_to_delete.image:
            image_path = os.path.join(
                current_app.root_path, "static/uploads", event_to_delete.image
            )
            if os.path.exists(image_path):
                os.remove(image_path)

        db.session.delete(event_to_delete)
        db.session.commit()
        form = NewEvent()
        allEvents = Events.query.order_by(Events.date_added)
        return render_template('add_events.html', form=form, events=allEvents)
    except: 
        flash("error")

@app.route("/adminpanel/projects", methods=['GET', 'POST'])
@login_required
def add_projects():
    form = NewProject()
    allProjects = Projects.query.order_by(Projects.date_added)
    if form.validate_on_submit():
        filename = None
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            filename = make_unique(filename)
            upload_path = os.path.join(current_app.root_path, 'static/uploads', filename)
            form.image.data.save(upload_path)

        project = Projects(
            title=form.title.data,
            description=form.description.data,
            funding_goal=form.funding_goal.data,
            image=filename  
        )

        db.session.add(project)
        db.session.commit()

        return redirect(url_for('add_projects'))

    return render_template('add_projects.html', form=form, projects=allProjects)


@app.route("/adminpanel/projects/update/<int:id>", methods=['GET', 'POST'])
@login_required
def update_project(id):
    project = Projects.query.get_or_404(id)
    filename = None
    form = NewProject()
    if form.validate_on_submit():
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            filename = make_unique(filename)
            upload_path = os.path.join(current_app.root_path, 'static/uploads', filename)
            form.image.data.save(upload_path)

        project.title = form.title.data
        project.description = form.description.data
        project.funding_goal = form.funding_goal.data
        if filename:
            project.image = filename

        db.session.add(project)
        db.session.commit()
        return redirect(url_for('projects'))

    # Pre-fill form
    form.title.data = project.title
    form.description.data = project.description
    form.funding_goal.data = project.funding_goal
    form.image.data = project.image
    return render_template('update_projects.html', form=form, project=project)


@app.route("/adminpanel/projects/delete/<int:id>", methods=['GET', 'POST'])
@login_required
def delete_project(id):
    project_to_delete = Projects.query.get_or_404(id)
    try:
        if project_to_delete.image:
            image_path = os.path.join(
                current_app.root_path, "static/uploads", project_to_delete.image
            )
            if os.path.exists(image_path):
                os.remove(image_path)

        db.session.delete(project_to_delete)
        db.session.commit()
        form = NewProject()
        allProjects = Projects.query.order_by(Projects.date_added)
        return render_template('add_projects.html', form=form, projects=allProjects)
    except:
        flash("error")


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    form = AdminLogin()
    if form.validate_on_submit():
        if form.username.data == ADMIN_USERNAME and form.password.data == ADMIN_PASSWORD:
            user = AdminUser()
            login_user(user) 
            flash('Logged in successfully', 'success')
            return redirect(url_for('adminpanel'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('adminlogin.html', title='Register', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'info')
    return redirect(url_for('home'))



if __name__ == "__main__":
    app.run(debug=True)