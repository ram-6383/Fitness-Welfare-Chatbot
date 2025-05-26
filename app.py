from flask import Flask, request, jsonify, render_template
import requests
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

# Load API keys from .env
NUTRITION_API_KEY = os.getenv("API_KEY")
EXERCISE_API_KEY = os.getenv("EXERCISE_API_KEY")  # Add this to your .env
HOSPITAL_API_KEY = os.getenv("HOSPITAL_API_KEY")  # Add this to your .env

# API endpoints
NUTRITION_API_URL = "https://api.api-ninjas.com/v1/nutrition"
EXERCISE_API_URL = "https://api.api-ninjas.com/v1/exercises"
HOSPITAL_API_URL = "https://api.api-ninjas.com/v1/hospitals"

@app.route("/")
def index():
    return render_template("index.html")

# Nutrition route
@app.route("/chat", methods=["POST"])
def nutrition_chat():
    try:
        data = request.get_json(force=True)
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"error": "Please enter a food item."}), 400

        headers = {"X-Api-Key": NUTRITION_API_KEY}
        params = {"query": user_message}
        response = requests.get(NUTRITION_API_URL, headers=headers, params=params)

        if response.status_code == 200:
            results = response.json()
            if results:
                food = results[0]
                return jsonify({
                    "name": food.get("name", "Unknown").capitalize(),
                    "calories": f"🔥 {food.get('calories', 'N/A')}",
                    "protein_g": f"💪 {food.get('protein_g', 'N/A')}",
                    "fat_total_g": f"🥓 {food.get('fat_total_g', 'N/A')}",
                    "fat_saturated_g": f"{food.get('fat_saturated_g', 'N/A')}",
                    "carbohydrates_total_g": f"🍞 {food.get('carbohydrates_total_g', 'N/A')}",
                    "sugar_g": f"🍬 {food.get('sugar_g', 'N/A')}",
                    "fiber_g": f"🌾 {food.get('fiber_g', 'N/A')}",
                    "sodium_mg": f"🧂 {food.get('sodium_mg', 'N/A')}",
                    "potassium_mg": f"🍌 {food.get('potassium_mg', 'N/A')}",
                    "cholesterol_mg": f"💉 {food.get('cholesterol_mg', 'N/A')}"
                })
            else:
                return jsonify({"error": "❓ Food not found. Try a different item."})
        else:
            return jsonify({"error": "❗ Nutrition API error. Please try again later."})
    except Exception as e:
        return jsonify({"error": f"❗ Error: {str(e)}"})


@app.route("/exercise", methods=["POST"])
def exercise_lookup():
    try:
        data = request.get_json(force=True)
        query = data.get("muscle", "").strip().lower()
        print(f"Muscle received: {query}")

        if not query:
            return jsonify({"error": "Please specify a muscle or body part."}), 400

        headers = {"X-Api-Key": EXERCISE_API_KEY}
        params = {"muscle": query}
        response = requests.get("https://api.api-ninjas.com/v1/exercises", headers=headers, params=params)

        print("Status Code:", response.status_code)
        print("API Response:", response.text)

        if response.status_code == 200:
            results = response.json()
            if results:
                exercises = [
                    f"🏋️ {ex.get('name')} — Equipment: {ex.get('equipment')}, Type: {ex.get('type')}"
                    for ex in results[:5]
                ]
                return jsonify({"exercises": exercises})
            else:
                return jsonify({"error": "❓ No exercises found for that muscle group."})
        else:
            return jsonify({"error": "❗ Exercise API error."})
    except Exception as e:
        return jsonify({"error": f"❗ Error: {str(e)}"})

# Hospital route
@app.route("/hospitals", methods=["POST"])
def hospital_lookup():
    try:
        data = request.get_json(force=True)
        user_city = data.get("city", "").strip()

        if not user_city:
            return jsonify({"error": "Please enter a city name."}), 400

        headers = {"X-Api-Key": HOSPITAL_API_KEY}
        params = {"city": user_city}
        response = requests.get("https://api.api-ninjas.com/v1/hospitals", headers=headers, params=params)

        if response.status_code == 200:
            results = response.json()
            if results:
                hospitals = [
                    f"🏥 {h.get('name', 'Unknown')} — {h.get('address', 'N/A')}, {h.get('city', '')}, {h.get('state', '')}"
                    for h in results[:5]
                ]
                return jsonify({"hospitals": hospitals})
            else:
                return jsonify({"error": "❓ No hospitals found for the given city."})
        else:
            return jsonify({"error": "❗ Hospital API error. Please try again later."})
    except Exception as e:
        return jsonify({"error": f"❗ Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
