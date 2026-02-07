from flask import Flask, request, jsonify

app = Flask(__name__)

# Simple car data
CARS = {
    "tesla model 3": {"fuel": "Electric", "co2": 0},
    "toyota prius": {"fuel": "Hybrid", "co2": 70},
    "toyota corolla": {"fuel": "Petrol", "co2": 120}
}

def sustainability_score(fuel, co2):
    score = 0
    if fuel == "Electric":
        score += 50
    elif fuel == "Hybrid":
        score += 30
    else:
        score += 10

    if co2 == 0:
        score += 30
    elif co2 < 80:
        score += 20
    else:
        score += 10

    return score

@app.route("/car")
def car():
    name = request.args.get("name", "").lower()

    if name in CARS:
        fuel = CARS[name]["fuel"]
        co2 = CARS[name]["co2"]
    else:
        fuel = "Petrol"
        co2 = 150

    score = sustainability_score(fuel, co2)

    if score >= 70:
        color = "Green"
    elif score >= 40:
        color = "Yellow"
    else:
        color = "Red"

    return jsonify({
        "car": name,
        "fuel_type": fuel,
        "co2_emissions": co2,
        "sustainability_score": score,
        "rating": color
    })

if __name__ == "__main__":
    app.run(debug=True)
