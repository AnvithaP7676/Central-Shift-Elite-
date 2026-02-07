from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

def estimate_car(car_name):
    name = car_name.lower()

    if any(x in name for x in ["tesla", "ev", "electric"]):
        return "Electric", 0

    if "hybrid" in name:
        return "Hybrid", 60

    if "diesel" in name:
        return "Diesel", 140


    return "Petrol", 180


def score_car(fuel, co2):
    score = 100

    if fuel == "Electric":
        score -= 0
    elif fuel == "Hybrid":
        score -= 25
    elif fuel == "Petrol":
        score -= 45
    elif fuel == "Diesel":
        score -= 55

    score -= co2 // 4
    return max(0, min(100, score))


def rating_and_reason(score):
    if score >= 66:
        return (
            "Green",
            "This car has low emissions and better efficiency, making it environmentally friendly."
        )
    elif score >= 50:
        return (
            "Yellow",
            "This car has moderate emissions. It is acceptable but not fully sustainable."
        )
    else:
        return (
            "Red",
            "This car produces high emissions and has a strong negative impact on the environment."
        )


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    car = data.get("car", "").strip()

    if car == "":
        return jsonify({"error": "No car name entered"}), 400

    fuel, co2 = estimate_car(car)
    score = score_car(fuel, co2)
    rating, reason = rating_and_reason(score)

    return jsonify({
        "app": "SustainX",
        "car": car.title(),
        "fuel": fuel,
        "co2": co2,
        "score": score,
        "rating": rating,
        "reason": reason
    })


if __name__ == "__main__":
    app.run(debug=True)



