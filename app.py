from models.admin import Admin
from services.report_service import ReportService
from flask import Flask, render_template, request, redirect, url_for, session


app = Flask(__name__)
app.secret_key = "4eea59adc2bb4495b02f81616e3b2a8a80b97bcb0080cb00f1eaedf2be76b4a9"


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template('index.html')

@app.route('/handle-buttons', methods=["GET", "POST"])
def handle_buttons():

    clicked_button = request.form.get('action')

    if clicked_button == "lost_page":
        return redirect(url_for('lost_item'))

    elif clicked_button == "found_page":
        return redirect(url_for('found_item'))

    return redirect('/')

@app.route('/lost_item', methods=['GET', 'POST'])
def lost_item():

    if request.method == "POST":

        session["lost_item"] = {
            "item": request.form["item"],
            "name": request.form["name"],
            "date": request.form["trip-start"]
        }

        return redirect(url_for("details"))

    return render_template("lost_item.html")

@app.route('/found_item', methods=['GET', 'POST'])
def found_item():
    res = None
    if request.method == "POST":

        service = ReportService()

        res = service.claim_item_service(request.form["item"], request.form["name"], request.form['trip-start'])
    
        return redirect(url_for("search_item", result=res["message"]))
    return render_template("found_item.html")

@app.route('/success_page')
def success_page():
    result = request.args.get("result")
    return render_template("success_page.html", result=result)

@app.route('/search_item')
def search_item():
    result = request.args.get("result")
    return render_template("search_item.html", result=result)

@app.route("/details", methods=["GET", "POST"])
def details():

    if request.method == "POST":

        lost_item = session.get("lost_item")

        if not lost_item:
            return redirect(url_for("lost_item"))

        service = ReportService()

        res = service.report_lost_item_service(
            lost_item["item"],
            lost_item["name"],
            lost_item["date"],
            request.form["color"],
            request.form["size"],
            request.form["shape"]
        )

        session.pop("lost_item", None)

        return redirect(
            url_for("success_page", result=res["message"])
        )

    return render_template("details.html")

if __name__ == '__main__':
    app.run(debug=True)
    