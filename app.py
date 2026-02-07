from flask import Flask, render_template, request

app = Flask(__name__)

def co2_per_km(fuel):
    mapping = {
        "Petrol": 180,
        "Diesel": 150,
        "Hybrid": 90,
        "Electric": 0
    }
    return mapping.get(fuel, 160)

def estimate_daily_co2(fuel, hours, avg_speed=40):
    km_driven = hours * avg_speed  # Assuming avg speed of 40 km/h
    co2 = co2_per_km(fuel) * km_driven
    return round(co2, 1)


def calculate_score(co2):
    if co2 == 0:
        return 95
    score = 100 - (co2 / 50)  # Lower CO₂ → higher score
    return max(10, min(95, int(score)))

def color_index(score):
    if score <= 49:
        return "red", "High CO₂ impact"
    elif score <= 65:
        return "yellow", "Moderate CO₂ impact"
    else:
        return "green", "Low CO₂ impact"


@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        brand = request.form["brand"].strip()
        fuel = request.form["fuel"]
        hours = float(request.form["hours"])

        co2 = estimate_daily_co2(fuel, hours)
        score = calculate_score(co2)
        color, explanation = color_index(score)

        result = {
            "brand": brand,
            "fuel": fuel,
            "hours": hours,
            "co2": co2,
            "score": score,
            "color": color,
            "explanation": explanation,
            "source": "Estimated from driving habits"
        }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
