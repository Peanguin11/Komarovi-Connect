from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html', current_page='home')

@app.route("/news")
def news():
    return render_template('news.html', current_page='news')

@app.route("/events")
def events():
    return render_template('events.html', current_page='events')

@app.route("/projects")
def projects():
    return render_template('donations.html', current_page='projects')

if __name__ == "__main__":
    app.run(debug=True)