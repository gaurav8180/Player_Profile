import os
import google.generativeai as genai
import json
from flask import Flask, render_template, request, jsonify

# Initialize the Flask application
app = Flask(__name__)

# Configuring the API key
os.environ["GOOGLE_AI_STUDIO"] = "AIzaSyDSg-yazQLiFuT63PyIFqlOQ-g-jX-LenE"
genai.configure(api_key=os.environ["GOOGLE_AI_STUDIO"])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the player's name from the form input
        player_name = request.form.get("player_name")

        if not player_name:
            return "Error: No player name provided", 400
        
        # Using Gemini model with JSON output configuration
        model = genai.GenerativeModel(
            "gemini-1.5-flash",
            generation_config={"response_mime_type": "application/json"}
        )

        # Generating the prompt with the player's name
        prompt = f"""
        Generate a detailed JSON profile for the athlete named "{player_name}". 
        Include the following details:
        - Full Name
        - Date of Birth
        - Nationality
        - Sport and Discipline
        - Team and Position
        - Notable Events (Name, Date, Location, Level, and Result)
        - Career Statistics (Wins, Personal Bests, World Ranking)
        - Achievements
        - Health and Fitness (Injury History and Fitness Data)
        - Performance Analytics (Strengths and Weaknesses)
        - Media Links (e.g., interviews, social media)
        - Quotes
        - Upcoming Goals (Event and Goal)
        - Medal Tally:
            - National: (Gold, Silver, Bronze, Total, Associated Events with Details)
            - International: (Gold, Silver, Bronze, Total, Associated Events with Details)
        Use this JSON schema:
        AthleteProfile = {{
          "athlete": {{
            "fullName": str,
            "dateOfBirth": str,
            "nationality": str,
            "sport": str,
            "discipline": str,
            "team": str,
            "position": str,
            "events": list[Event],
            "statistics": Statistics,
            "achievements": list[str],
            "healthAndFitness": HealthAndFitness,
            "performanceAnalytics": PerformanceAnalytics,
            "media": list[Media],
            "quotes": list[str],
            "upcomingGoals": list[Goal],
            "medalTally": {{
              "national": {{
                "gold": int,
                "silver": int,
                "bronze": int,
                "total": int,
                "events": list[EventDetail]
              }},
              "international": {{
                "gold": int,
                "silver": int,
                "bronze": int,
                "total": int,
                "events": list[EventDetail]
              }}
            }}
          }}
        }}

        EventDetail = {{
          "eventName": str,
          "date": str,
          "location": str,
          "level": str,
          "result": str
        }}

        Statistics = {{
          "wins": int,
          "personalBests": list[str],
          "worldRanking": int
        }}

        HealthAndFitness = {{
          "injuryHistory": list[str],
          "fitnessData": dict
        }}

        PerformanceAnalytics = {{
          "strengths": list[str],
          "weaknesses": list[str]
        }}

        Media = {{
          "mediaType": str,
          "mediaLink": str
        }}

        Goal = {{
          "event": str,
          "goal": str
        }}
        """

        # Generate the JSON profile
        try:
            response = model.generate_content(prompt)
            athlete_data = json.loads(response.text)  # Parse response.text as JSON

            # Now you can access 'athlete_data' as a dictionary
            athlete = athlete_data.get("athlete", {})

            if not athlete:
                return "Error: Athlete data not found", 400

            return render_template("profile.html", athlete=athlete)
        except Exception as e:
            return f"Error generating athlete profile: {str(e)}", 500

    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
