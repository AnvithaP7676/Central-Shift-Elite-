from flask import Flask, request, jsonify

app = Flask(__name__)

# -------------------------
# Simple car database
# -------------------------
CAR_DATABASE = {
    "tesla model 3": {
        "fuel": "Electric",
        "co2": 0,
        "range": 490
    },
    "toyota prius": {
        "fuel": "Hybrid",
        "co2": 70,
        "range": 900
    },
    "toyota corolla": {
        "fuel": "Petrol",
        "co2": 120,
        "range": 650
    }
}

# -------------------------
# Sustainability logic
# -------------------------
def calculate_score(car):
    score = 0

    if car["fuel"] == "Electric":
        score += 50
    elif car["fuel"] == "Hybrid":
        score += 30
    else:
        score += 10

    if car["co2"] == 0:
        score += 30
    elif car["co2"] < 80:
        score += 20
    else:
        score += 10

    if car["range"] > 400:
        score += 20

    return min(score, 100)

def score_color(score):
    if score >= 70:
        return "Green"
    elif score >= 40:
        return "Yellow"
    else:
        return "Red"

# -------------------------
# Routes
# -------------------------
@app.route("/")
def home():
    return "CodeFest Sustainable Car API is running!"

@app.route("/car")
def car():
    name = request.args.get("name", "").lower()

    if name in CAR_DATABASE:
        car_data = CAR_DATABASE[name]
    else:
        # default if car not found
        car_data = {
            "fuel": "Petrol",
            "co2": 150,
            "range": 500
        }

    score = calculate_score(car_data)
    color = score_color(score)

    return jsonify({
        "car_name": name,
        "fuel_type": car_data["fuel"],
        "co2_emissions": car_data["co2"],
        "range_km": car_data["range"],
        "sustainability_score": score,
        "rating_color": color
    })

if __name__ == "__main__":
    app.run(debug=True)
