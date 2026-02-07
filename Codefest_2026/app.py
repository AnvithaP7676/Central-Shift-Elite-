from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("API_NINJAS_KEY")
API_URL = "https://api.api-ninjas.com/v1/cars"

# ---------------- CO₂ LOGIC ---------------- #

def calculate_co2(car):
    # Electric vehicles
    if car["fuel_type"].lower() == "electric":
        return 0

    # VERY IMPORTANT:
    # APIs usually give MPG, not CO₂ directly.
    # We convert MPG → CO₂ using EPA standard approximation.

    mpg = car.get("combination_mpg")
    if not mpg:
        return None

    # EPA approximation: ~8,887 g CO₂ per gallon of petrol
    co2 = (8887 / mpg) * 1.609  # g/km
    return round(co2, 1)

def sustainability_score(co2):
    if co2 == 0:
        return 95
    score = 100 - (co2 / 2)
    return max(10, min(95, int(score)))

def score_color(score):
    if score <= 49:
        return "red", "High Impact"
    elif score <= 65:
        return "yellow", "Moderate Impact"
    return "green", "Low Impact"

# ---------------- ROUTE ---------------- #

@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        query = request.form["query"].strip()

        # Expect input like: "BMW 320d 2020"
        parts = query.split()
        if len(parts) < 3:
            result = {"error": "Please enter: Make Model Year"}
            return "SustainX is running"


        make = parts[0]
        year = parts[-1]
        model = " ".join(parts[1:-1])

        headers = {"X-Api-Key": API_KEY}
        params = {
            "make": make,
            "model": model,
            "year": year
        }

        response = requests.get(API_URL, headers=headers, params=params)
        data = response.json()

        if not data:
            result = {"error": "Exact car not found in database"}
            return render_template("index.html", result=result)

        car = data[0]
        co2 = calculate_co2(car)

        if co2 is None:
            result = {"error": "Emissions data unavailable for this vehicle"}
            return render_template("index.html", result=result)

        score = sustainability_score(co2)
        color, label = score_color(score)

        result = {
            "name": f"{car['make']} {car['model']} {car['year']}",
            "fuel": car["fuel_type"].title(),
            "co2": co2,
            "score": score,
            "color": color,
            "label": label,
            "source": "Exact match from live vehicle database"
        }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
