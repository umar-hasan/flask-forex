from forex_python.converter import CurrencyRates, CurrencyCodes
from flask import Flask, request, render_template, redirect, url_for, flash

app = Flask(__name__)
app.config["SECRET_KEY"] = "12345"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():
    c = CurrencyRates()
    con_from = request.form["convert-from"]
    con_to = request.form["convert-to"]
    err_flashes = 0
    try:
        c.get_rates(con_from)
    except:
        flash(f"{con_from} is not a valid currency.", "error")
        err_flashes = err_flashes + 1
    try:
        c.get_rates(con_to)
    except:
        flash(f"{con_to} is not a valid currency.", "error")
        err_flashes = err_flashes + 1
    try:
        float(request.form["amount"])
    except:
        flash("Invalid amount entered.", "error")
        err_flashes = err_flashes + 1

    if err_flashes > 0:
        return redirect(url_for("home"))

    sym = CurrencyCodes().get_symbol(request.form["convert-to"])
    amt = round(c.convert(con_from, con_to, float(request.form["amount"])), 2)
    flash(f"{sym}{amt}", "conversion")
    return redirect(url_for("home"))
