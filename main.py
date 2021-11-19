from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("arrivals.html")
    #"<p>Hello, World!</p>"

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/add-vehicle")
def add_vehicle():
    return render_template("add-vehicle.html")

if __name__ == '__main__':
    app.run(debug=True) 