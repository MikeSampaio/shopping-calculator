from flask import Flask, render_template, request
from supermarket_calculator_web import (calculate_discount_web, calculate_tax_web, price_converter_web, packagepricepound_web,
                                         price_100g_converter_web, price_lb_to_g_web, product_comparison_web, update_exchange_rate_online)
app = Flask(__name__)

from datetime import datetime, timedelta

@app.context_processor
def inject_exchange_rate():

    from supermarket_calculator_web import (
        exchange_rate,
        last_exchange_update,
        update_exchange_rate_online)

    if (
        last_exchange_update is None
        or datetime.now() - last_exchange_update
            > timedelta(hours=1)):
        update_exchange_rate_online()

    from supermarket_calculator_web import (exchange_rate, last_exchange_update)

    return {"exchange_rate": round(exchange_rate, 4), 
            "exchange_time": last_exchange_update.strftime("%d/%m/%Y %H:%M") 
                              if last_exchange_update
                              else "Unknown"}

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/discount", methods = ["GET", "POST"])
def discount():
    discount = None
    money_saved_cad = None
    money_saved_eur = None
    message = None
    error = None
    try:
        if request.method == "POST":
            regular_price = float(request.form["regular_price"])
            sale_price = float(request.form["sale_price"])

            print("Regular:", regular_price)
            print("Sale:", sale_price)
            discount, money_saved_cad, money_saved_eur, message = calculate_discount_web(regular_price,sale_price)
            print(discount)

    except ValueError as e:
        error = str(e)

    return render_template("index.html", discount = discount, money_saved_cad = money_saved_cad, money_saved_eur = money_saved_eur, message = message, error = error)


@app.route("/tax", methods=["GET", "POST"])
def tax():

    price_with_tax_cad = None
    price_with_tax_eur = None
    tax_amount_cad = None
    tax_amount_eur = None
    error = None

    if request.method == "POST":
        try:
            price_cad = float(request.form["price_cad"])

            (price_with_tax_cad,price_with_tax_eur, tax_amount_cad,tax_amount_eur) = calculate_tax_web(price_cad)
        except ValueError as e:
            error = str(e)
    return render_template("tax.html",price_with_tax_cad=price_with_tax_cad,price_with_tax_eur=price_with_tax_eur,
                           tax_amount_cad=tax_amount_cad,tax_amount_eur=tax_amount_eur, error = error)
        
@app.route("/converter", methods=["GET", "POST"])
def converter():

    price_cad = None
    price_eur = None
    error = None

    try:
        if request.method == "POST":
            price_cad = float(request.form["price_cad"])
            price_cad, price_eur = price_converter_web(price_cad)
    
    except ValueError as e:
        error = str(e)

    return render_template(
        "converter.html",
        price_cad=price_cad,
        price_eur=price_eur, error = error)



@app.route("/package", methods=["GET", "POST"])
def package():

    results = None
    error = None

    try:
        if request.method == "POST":

            unit = request.form["unit"]
            weight = float(request.form["weight"])
            package_price_cad = float(request.form["package_price_cad"])

            results = packagepricepound_web(
                unit,
                weight,
                package_price_cad)
    except ValueError as e:
        error = str(e)

    return render_template(
        "package.html",
        results=results, error = error)

@app.route("/100g", methods=["GET", "POST"])
def converter_100g():

    results = None
    error = None
    
    try:
        if request.method == "POST":

            priceper100g = float(
                request.form["priceper100g"])

            results = price_100g_converter_web(
                priceper100g)
    except ValueError as e:
        error = str(e)

    return render_template(
        "100g.html",
        results=results, error=error)

@app.route("/lbtog", methods=["GET", "POST"])
def lbtog():

    package_price_cad = None
    package_price_eur = None
    error = None

    try:
        if request.method == "POST":

            weight_g = float(request.form["weight_g"])

            price_per_lb_cad = float( request.form["price_per_lb_cad"])

            (package_price_cad,package_price_eur) = price_lb_to_g_web(weight_g,price_per_lb_cad)
    except ValueError as e:
        error = str(e)

    return render_template(
        "lbtog.html",
        package_price_cad=package_price_cad,
        package_price_eur=package_price_eur, error = error)

@app.route("/compare", methods=["GET", "POST"])
def compare():

    results = None
    error = None
    
    if request.method == "POST":

        try:

            results = product_comparison_web(

                request.form["name_a"],
                float(request.form["weight_a"]),
                float(request.form["price_a"]),

                request.form["name_b"],
                float(request.form["weight_b"]),
                float(request.form["price_b"]))
        except ValueError as e:
            error = str(e)

    return render_template(
        "compare.html",
        results=results, error=error)

import os
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT", 5000)))