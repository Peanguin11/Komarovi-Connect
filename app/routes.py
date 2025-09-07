

from flask import  render_template, url_for, flash, redirect,  current_app, request
from flask_login import  login_user, login_required, logout_user
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from forms import *
from config import app, db, ADMIN_PASSWORD, ADMIN_USERNAME
import os
from models import make_unique,  Events, News, Projects, login_manager, User #, AdminUser


@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html', current_page='home')



@app.route("/events")
def events():
    allEvents = Events.query.order_by(Events.date_added.desc()).all()
    return render_template('events.html', current_page='events', events=allEvents)

@app.route("/events/<int:id>")
def event(id):
    event = Events.query.get_or_404(id)
    return render_template('event.html', event=event)

@app.route("/projects")
def projects():
    allProjects = Projects.query.order_by(Projects.date_added)
    return render_template('projects.html', current_page='projects', projects=allProjects,)

@app.route("/projects/<int:id>")
def project(id):
    project = Projects.query.get_or_404(id)
    return render_template('project.html', project=project)

@app.route("/adminpanel")
@login_required
def adminpanel():
    return render_template('adminpanel.html')

@app.route("/adminpanel/events", methods=['GET', 'POST'])
@login_required
def add_events():
    form = NewEvent()
    allEvents = Events.query.order_by(Events.date_added.desc())
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
            event_date = form.event_date.data,
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
        if event.image:
            image_path = os.path.join(
                current_app.root_path, "static/uploads", event.image
            )
            if os.path.exists(image_path):
                os.remove(image_path)
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            filename = make_unique(filename)
            upload_path = os.path.join(current_app.root_path, 'static/uploads', filename)
            form.image.data.save(upload_path)
        event.title = form.title.data
        event.description=form.description.data
        event.registration_link=form.registration_link.data
        event.event_date=form.event_date.data
        event.location=form.location.data
        event.image=filename
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('events'))
    form.title.data = event.title
    form.description.data=event.description
    form.registration_link.data = event.registration_link
    form.event_date.data = event.event_date
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
        return redirect(url_for('add_events'))
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
    
@app.route("/donate/<int:id>", methods=['GET', 'POST'])
def donate(id):
    project = Projects.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            amount = int(request.form.get('amount', 0))
            if amount > 0:
                project.current_amount += amount
                db.session.commit()
                flash(f'Thank you for your donation of {amount}!', 'success')
            else:
                flash('Please enter a valid donation amount.', 'error')
        except ValueError:
            flash('Please enter a valid donation amount.', 'error')
        
        return redirect(url_for('project', id=id))
    
    return render_template('donations.html', project=project)

# @app.route("/adminlogin", methods=['GET', 'POST'])
# def adminlogin():
#     form = AdminLogin()
#     if form.validate_on_submit():
#         if form.username.data == ADMIN_USERNAME and form.password.data == ADMIN_PASSWORD:
#             user = AdminUser()
#             login_user(user)
#             flash('Logged in successfully', 'success')
#             return redirect(url_for('adminpanel'))
#         else:
#             flash('Invalid username or password', 'danger')
#     return render_template('adminlogin.html', title='Register', form=form)
#
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'info')
    return redirect(url_for('home'))




# @login_manager.user_loader
# def load_user(user_id):
#     if user_id == "admin":
#         return AdminUser()
#     return None


@app.route('/news')
def all_news():
    page = request.args.get('page', 1, type=int)
    per_page = 6
    all_news = News.query.order_by(News.date_added.desc()).paginate(page=page, per_page=per_page)
    before_str = request.args.get("before")
    query = News.query

    # Filter: before
    if before_str:
        try:
            before_date = datetime.strptime(before_str, "%Y-%m-%d")
            next_day = before_date + timedelta(days=1)
            query = query.filter(News.date_added < next_day)
        except ValueError:
            pass

    # Sort newest first + paginate
    all_news = query.order_by(News.date_added.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    # Render template
    return render_template(
        "all_news.html",
        all_news=all_news,
        before=before_str,
        current_page="news",
    )



@app.route('/add_news', methods=["GET", "POST"])
def add_news():
    form = Addnewsform()

    if request.method == "POST":
        file_img = request.files['img']
        filename = None
        if file_img:
            filename = secure_filename(file_img.filename)
            filename = make_unique(filename)
            images_folder = os.path.join(current_app.root_path, 'static/uploads')
            os.makedirs(images_folder, exist_ok=True)
            file_img.save(os.path.join(images_folder, filename))

        news = News(name=form.name.data, img=filename, description=form.description.data)
        db.session.add(news)
        db.session.commit()

        return redirect("/")
    return render_template('add_news.html', form=form)




@app.route('/opened_news/<int:news_id>')
def opened_news(news_id):
    selected_news= News.query.get_or_404(news_id)
    return render_template('opened_news.html', selected_news=selected_news)



@app.route('/delete/<int:id>', methods=["GET", "POST"])
def delete(id):
    selected_news = News.query.get_or_404(id)

    if selected_news.img:
        image_path = os.path.join(current_app.root_path, "static/uploads", selected_news.img)
        if os.path.exists(image_path):
            os.remove(image_path)

    db.session.delete(selected_news)
    db.session.commit()
    return redirect(url_for('all_news'))





@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
        return redirect("/")
    return render_template('login.html', form=form)


@app.route('/update_news/<int:id>', methods=["GET", "POST"])
@login_required
def update_news(id):
    news_item = News.query.get_or_404(id)
    form = Addnewsform()
    filename = news_item.img

    if form.validate_on_submit():
        if form.img.data:
            if news_item.img:
                old_image_path = os.path.join(current_app.root_path, 'static/uploads', news_item.img)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)

            file_img = form.img.data
            filename = secure_filename(file_img.filename)
            filename = make_unique(filename)
            images_folder = os.path.join(current_app.root_path, 'static/uploads')
            os.makedirs(images_folder, exist_ok=True)
            file_img.save(os.path.join(images_folder, filename))

        news_item.name = form.name.data
        news_item.description = form.description.data
        news_item.img = filename

        db.session.commit()
        return redirect("/news")

    form.name.data = news_item.name
    form.description.data = news_item.description

    return render_template('update_news.html', form=form, news=news_item)
@app.route("/adminpanel/news")
@login_required
def admin_news():
    all_news = News.query.order_by(News.id).all()
    return render_template('admin_news.html', all_news=all_news)




