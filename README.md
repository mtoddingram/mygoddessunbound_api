✨ MyGoddessUnknown Astrological API ✨<div align="center"><pre>)  (  ((   )  ))  (  (..|         ||    * |||/     ./   * * *//__</pre></div><div align="center"><strong>A high-precision, modern astrological calculation engine.</strong></div><div align="center"><img src="https://www.google.com/search?q=https://img.shields.io/badge/python-3.11%2B-blue.svg" alt="Python Version"><img src="https://www.google.com/search?q=https://img.shields.io/badge/framework-Flask-black.svg" alt="Flask"><img src="https://www.google.com/search?q=https://img.shields.io/badge/astronomy-Skyfield-orange.svg" alt="Skyfield"><img src="https://www.google.com/search?q=https://img.shields.io/badge/license-MIT-green.svg" alt="License"></div>🔮 Core MissionThe MyGoddessUnknown API provides developers with hyper-accurate, foundational astrological data for any moment in time. Built on modern astronomical libraries used by researchers, this backend service is the solid bedrock for applications that require reliable celestial calculations. It's designed to be the engine that powers the MyGoddessUnknown front-end and its specialized Agentic AI workflows.🌟 FeaturesAstronomical Precision: Leverages the Skyfield library and the official JPL DE421 Ephemeris for calculations that meet modern scientific standards.Complete Natal Data: Calculates the ecliptic longitudes for all major celestial bodies (Sun, Moon, and planets).Chart Angles: Computes the precise degrees of the Ascendant (ASC) and Midheaven (MC), the core axes of the horoscope.House Calculation: Implements the Placidus house system, the most widely used system in Western astrology, to calculate all 12 house cusps.Robust & Scalable: Built with a clean Flask architecture, ready for containerization and deployment.🛠️ Technology StackBackend: Python 3Framework: FlaskCore Calculation Library: SkyfieldNumerical Processing: NumPyTimezone Handling: pytz🚀 Getting StartedFollow these instructions to get the API server running on your local machine for development and testing.PrerequisitesPython 3.10+pip and venv for package managementInstallation & SetupClone the repository:git clone [https://github.com/your-username/mygoddessunknown_api.git](https://github.com/your-username/mygoddessunknown_api.git)
cd mygoddessunknown_api
Create and activate a Python virtual environment:# Create the environment
python3 -m venv venv

# Activate it (macOS/Linux)
source venv/bin/activate

# Activate it (Windows)
.\venv\Scripts\activate
Install the required dependencies:pip install -r requirements.txt
(Note: If you don't have a requirements.txt file yet, you can create one with pip freeze > requirements.txt after installing Flask, Skyfield, NumPy, and pytz.)Run the application:python run.py
The server will start on http://127.0.0.1:5000. On the first run, Skyfield will automatically download the necessary ephemeris files into the /data directory. This is a one-time process.📡 API Documentation/horoscopeThis is the primary endpoint for calculating a full natal chart.Method: POSTContent-Type: application/jsonRequest PayloadThe request body must be a JSON object with the following structure:KeyTypeDescriptionExamplebirth_dateStringThe birth date in YYYY-MM-DD format."1992-08-17"birth_timeStringThe birth time in HH:MM:SS format (24-hour)."14:23:00"birth_timezoneStringThe official IANA timezone name."America/New_York"latitudeNumberThe geographic latitude (-90 to 90).40.7128longitudeNumberThe geographic longitude (-180 to 180).-74.0060Example curl Requestcurl -X POST [http://127.0.0.1:5000/horoscope](http://127.0.0.1:5000/horoscope) \
-H "Content-Type: application/json" \
-d '{
    "birth_date": "1992-08-17",
    "birth_time": "14:23:00",
    "birth_timezone": "America/New_York",
    "latitude": 40.7128,
    "longitude": -74.0060
}'
Success Response (200 OK)A successful request returns a JSON object containing the calculated chart data.data.bodies: An object where each key is a celestial body and its value is an object containing its ecliptic longitude.data.angles: An object containing the longitudes for the Ascendant and Midheaven.data.houses: An array of 12 numbers representing the longitude of each house cusp, starting with the 1st house.{
  "status": "success",
  "data": {
    "bodies": {
      "Sun": {"longitude": 144.81},
      "Moon": {"longitude": 313.45},
      "...": "..."
    },
    "angles": {
      "ascendant": {"longitude": 204.21},
      "midheaven": {"longitude": 118.94}
    },
    "houses": [
      204.21, 235.91, 270.21, 298.94,
      324.49, 347.5, 24.21, 55.91,
      90.21, 118.94, 144.49, 167.5
    ]
  }
}
Error Response (400 Bad Request)If the request is missing fields or contains invalid data (e.g., a bad timezone), the API will return an error.{
  "status": "error",
  "message": "Invalid timezone specified."
}
🌱 Future DevelopmentThis API is the foundational layer. Future enhancements planned include:Calculation of aspects (conjunctions, trines, squares, etc.) between planets.Support for additional house systems (e.g., Whole Sign, Koch).Inclusion of other astrological points like Chiron and the Lunar Nodes.Transit calculations to compare current planetary positions to the natal chart.🤝 ContributingContributions are welcome! Please feel free to submit a pull request or open an issue for any bugs or feature requests.📜 LicenseThis project is licensed under the MIT License. See the LICENSE file for details.