from models.admin import Admin
from services.report_service import ReportService
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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
        service = ReportService()
        
        res = service.report_lost_item_service(request.form["item"], request.form["name"],
        request.form['trip-start'])
        
        return redirect(url_for("success_page", result=res["message"]))

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


if __name__ == '__main__':
    app.run(debug=True)
    