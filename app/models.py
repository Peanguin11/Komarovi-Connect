
from flask_login import UserMixin, LoginManager
from datetime import datetime
from uuid import uuid4

from werkzeug.security import generate_password_hash

from config import db, app


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, )
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)

    def __init__(self, username, password, role="guest"):
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role
login_manager = LoginManager(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text)
    registration_link = db.Column(db.String(500))
    location = db.Column(db.String(500))
    image = db.Column(db.String(200))
    event_date = db.Column(db.DateTime)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.id

# class AdminUser(UserMixin):
#     id = "admin"

def make_unique(string):
    ident = uuid4().__str__()
    return f"{ident}-{string}"

class News(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(80), unique= False, nullable= False)
    img = db.Column(db.String(80), unique= False, nullable= False)
    description = db.Column(db.String(80), unique= False, nullable= False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'{self.id}: {self.name}'

all_news = [
    {
        "name": "კომაროვის გუნდი ოლიმპიადაზე",
        "img": "komarovi_team.jpg",
        "description": "კომაროვის მოსწავლეებმა გაიმარჯვეს საერთაშორისო მათემატიკურ ოლიმპიადაზე.",
        "pdf": "",
        "id": 0,
    },
    {
        "name": "ახალი ბიბლიოთეკა თბილისში",
        "img": "tbilisi_library.jpg",
        "description": "თბილისში გაიხსნა თანამედროვე ბიბლიოთეკა, რომელიც ახალგაზრდებისთვის უფასოა.",
        "pdf": "",
        "id": 1,
    },
    {
        "name": "კომაროვის ექსპერიმენტული ლაბორატორია",
        "img": "komarovi_lab.jpg",
        "description": "სკოლაში შეიქმნა ახალი ფიზიკის ლაბორატორია, სადაც მოსწავლეები ექსპერიმენტებს ატარებენ.",
        "pdf": "",
        "id": 2,
    },
    {
        "name": "საქართველოს საგზაო ოლიმპიადა",
        "img": "georgia_olympiad.jpg",
        "description": "ქართველმა მოსწავლეებმა მონაწილეობა მიიღეს ეროვნულ საგზაო ოლიმპიადაში. (საგზაო ოლიმპიადა იდკ რა არი chatgpt-მ დაწერა აღწერა)",
        "pdf": "",
        "id": 3,
    },
    {
        "name": "კომაროველების საინჟინრო პროექტი",
        "img": "engineering_project.jpg",
        "description": "კომაროვის გუნდი მუშაობს ახალ ინოვაციურ საინჟინრო პროექტზე.",
        "pdf": "",
        "id": 4,
    },
    {
        "name": "თბილისის მუზეუმის ახალი ექსპოზიცია",
        "img": "tbilisi_museum.jpg",
        "description": "თბილისის მუზეუმში გაიხსნა ახალი ექსპოზიცია, რომელიც ისტორიას ასახავს.",
        "pdf": "",
        "id": 5,
    },
    {
        "name": "კომაროვის კლუბის ახალი ინიციატივა",
        "img": "komarovi_club.jpg",
        "description": "მოსწავლეებმა დაიწყეს ინიციატივა — პროგრამირების სწავლება უმცროსკლასელებისთვის.",
        "pdf": "",
        "id": 6,
    },
    {
        "name": "მთაწმინდის სამეცნიერო ფესტივალი",
        "img": "mtatsminda_festival.jpg",
        "description": "მთაწმინდაზე ჩატარდა სამეცნიერო ფესტივალი, სადაც სკოლები თავიანთ გამოგონებებს წარადგენდნენ.",
        "pdf": "",
        "id": 7,
    },
    {
        "name": "კომაროვის სპორტული შეჯიბრი",
        "img": "komarovi_sports.jpg",
        "description": "სკოლაში გაიმართა სპორტული შეჯიბრი, სადაც მონაწილეობდნენ ყველა კლასის მოსწავლეები.",
        "pdf": "",
        "id": 8,
    },
    {
        "name": "ახალი ტექნოლოგიები საქართველოს სკოლებში",
        "img": "georgia_schools.jpg",
        "description": "საქართველოს ზოგიერთ სკოლაში დაინერგა ხელოვნური ინტელექტის გამოყენება სწავლების პროცესში.",
        "pdf": "",
        "id": 9,
    },
]
all_events = [
    {
        "title": "კომაროვის სამეცნიერო კვირეული",
        "description": "მოსწავლეები წარმოადგენენ მათ მიერ ჩატარებულ ექსპერიმენტებს და კვლევებს.",
        "registration_link": "https://komarovi.ge/events/science-week",
        "location": "კომაროვის სკოლა, თბილისი",
        "image": "science_week.jpg",
    },
    {
        "title": "საქართველოს რობოტიკის ოლიმპიადა",
        "description": "ქვეყნის მასშტაბით გუნდები ეჯიბრებიან რობოტების შექმნაში და პროგრამირებაში.",
        "registration_link": "https://robotics.ge/olympiad",
        "location": "ექსპო ჯორჯია, თბილისი",
        "image": "robotics_olympiad.jpg",
    },
    {
        "title": "ინჟინერიის ღია დღე",
        "description": "კომაროვის სკოლის კლუბი ატარებს ღია შეხვედრას ინჟინერიით დაინტერესებულთათვის.",
        "registration_link": "https://komarovi.ge/events/engineering-day",
        "location": "კომაროვის ინჟინერიის ლაბორატორია",
        "image": "engineering_day.jpg",
    },
    {
        "title": "თბილისის სამეცნიერო ფესტივალი",
        "description": "თბილისში ტარდება ფესტივალი, სადაც წარმოდგენილია თანამედროვე ტექნოლოგიები და ინოვაციები.",
        "registration_link": "https://tbilisisciencefest.ge",
        "location": "მთაწმინდის პარკი",
        "image": "tbilisi_festival.jpg",
    },
    {
        "title": "კომაროვის სპორტული დღე",
        "description": "მოსწავლეები მონაწილეობენ სპორტულ შეჯიბრებში, რომლებიც მთელი სკოლის მასშტაბით ტარდება.",
        "registration_link": "https://komarovi.ge/events/sports-day",
        "location": "კომაროვის სპორტული დარბაზი",
        "image": "sports_day.jpg",
    },
    {
        "title": "სტარტაპ კონკურსი",
        "description": "ახალგაზრდა ინოვატორები თავიანთი სტარტაპ იდეებით წარდგებიან ჟიურის წინაშე.",
        "registration_link": "https://georgiastartups.ge",
        "location": "თბილისის ტექნოპარკი",
        "image": "startup_competition.jpg",
    },
    {
        "title": "კომაროვის მათემატიკის ღამე",
        "description": "ღამე, როცა მოსწავლეები გუნდებად მუშაობენ რთულ მათემატიკურ ამოცანებზე.",
        "registration_link": "https://komarovi.ge/events/math-night",
        "location": "კომაროვის საკონფერენციო დარბაზი",
        "image": "math_night.jpg",
    },
    {
        "title": "კომაროვის კოდინგის ბანაკი",
        "description": "ზაფხულის პროგრამა, სადაც მოსწავლეები სწავლობენ პროგრამირებას და გუნდურ მუშაობას.",
        "registration_link": "https://komarovi.ge/events/coding-camp",
        "location": "კომაროვის სკოლის ბანაკი, გუდაური",
        "image": "coding_camp.jpg",
    },
    {
        "title": "თბილისის ინოვაციების გამოფენა",
        "description": "ახალი პროექტების პრეზენტაცია — ტექნოლოგიები, ხელოვნება და ინოვაციები.",
        "registration_link": "https://innovationexpo.ge",
        "location": "ექსპო ჯორჯია",
        "image": "innovation_expo.jpg",
    },
    {
        "title": "კომაროვის წიგნების დღე",
        "description": "დღე, რომელიც მიძღვნილია წიგნების გაცვლასა და ლიტერატურულ დისკუსიებს.",
        "registration_link": "https://komarovi.ge/events/book-day",
        "location": "კომაროვის ბიბლიოთეკა",
        "image": "book_day.jpg",
    },
]


if __name__ == '__main__' :

    with app.app_context():
        db.create_all()
        admin = User(username='admin', password='password', role='admin')
        user = User(username='user', password='123')
        db.session.add(admin)
        db.session.add(user)
        db.session.commit()
        for news in all_news:
            new_news = News(name= news['name'],img= news['img'], description=news['description'] )
            db.session.add(new_news)
            db.session.commit()
        for event in all_events:
            new_event = Events(
                title=event['title'],
                description=event['description'],
                registration_link=event['registration_link'],
                location=event['location'],
                image=event['image']
            )
            db.session.add(new_event)

        db.session.commit()