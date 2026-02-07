<!DOCTYPE html>
<html>
<head>
  <title>SustainX</title>
  <style>
    body {
      font-family: Arial;
      background: #0f172a;
      color: white;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
    }
    .card {
      background: #020617;
      padding: 30px;
      border-radius: 12px;
      width: 350px;
      text-align: center;
      box-shadow: 0 0 20px rgba(0,0,0,0.5);
    }
    input {
      width: 100%;
      padding: 10px;
      border-radius: 6px;
      border: none;
      margin-bottom: 10px;
    }
    button {
      width: 100%;
      padding: 10px;
      background: #22c55e;
      border: none;
      border-radius: 6px;
      font-size: 16px;
      cursor: pointer;
    }
    button:hover {
      background: #16a34a;
    }
    .result {
      margin-top: 15px;
      font-size: 15px;
    }
  </style>
</head>

<body>
  <div class="card">
    <h2>SustainX</h2>
    <p>Enter any car name</p>

    <input id="carName" placeholder="e.g. Tesla Model Z">
    <button onclick="checkCar()">Check Sustainability</button>

    <div class="result" id="result"></div>
  </div>

<script>
function checkCar() {
  const car = document.getElementById("carName").value;

  if (car.trim() === "") {
    document.getElementById("result").innerText = "Please enter a car name";
    return;
  }

  fetch("/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ car: car })
  })
  .then(response => response.json())
  .then(data => {
    if (data.error) {
      document.getElementById("result").innerText = data.error;
      return;
    }

    document.getElementById("result").innerHTML = `
      <p><b>Car:</b> ${data.car}</p>
      <p><b>Fuel:</b> ${data.fuel}</p>
      <p><b>CO₂:</b> ${data.co2} g/km</p>
      <p><b>Score:</b> ${data.score}/100</p>
      <p><b>Rating:</b> ${data.rating}</p>
    `;
  })
  .catch(err => {
    document.getElementById("result").innerText = "Error connecting to server";
    console.error(err);
  });
}
</script>
</body>
</html>
