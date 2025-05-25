from flask import Flask, request, jsonify, render_template
import requests
from dotenv import load_dotenv
import os
load_dotenv()
app = Flask(__name__)

API_KEY = os.getenv("API_KEY")  # Your API Ninjas key
API_URL = "https://api.api-ninjas.com/v1/nutrition?query={}"

@app.route("/")
def index():
    return render_template("index.html")  # Loads frontend

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(force=True)
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"error": "Please enter a food item."}), 400

        headers = {"X-Api-Key": API_KEY}
        params = {"query": user_message}
        response = requests.get(API_URL, headers=headers, params=params)

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
            return jsonify({"error": "❗ API error. Please try again later."})
    except Exception as e:
        return jsonify({"error": f"❗ Error: {str(e)}"})
if __name__ == "__main__":
    app.run(debug=True)
