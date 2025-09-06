

from flask import  render_template, url_for, flash, redirect,  current_app, request
from flask_login import  login_user, login_required, logout_user
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from forms import *
from config import app, db, ADMIN_PASSWORD, ADMIN_USERNAME
import os
from models import make_unique,  Events, News, login_manager, User #, AdminUser


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
    return render_template('donations.html', current_page='projects')

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
        return render_template('add_events.html', form=form, events=allEvents)
    except:
        flash("error")

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
    all_news = News.query.all()
    print(all_news)
    return render_template('all_news.html', all_news=all_news, current_page='news')



@app.route('/add_news', methods=["GET", "POST"])
def add_news():
    form = Addnewsform()

    if request.method == "POST":
        file_img = request.files['img']
        images_folder = os.path.join(app.root_path, 'static/images')
        os.makedirs(images_folder, exist_ok=True)
        file_img.save(os.path.join(images_folder, file_img.filename))

        news = News(name=form.name.data, img=file_img.filename, description=form.description.data)
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
    db.session.delete(selected_news)
    db.session.commit()
    return redirect("/news")




@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
        return redirect("/")
    return render_template('login.html', form=form)




