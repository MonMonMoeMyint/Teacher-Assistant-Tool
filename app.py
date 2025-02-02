from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load dataset from Google Drive (provide your shared link ID)
google_drive_id = "YOUR_GOOGLE_DRIVE_FILE_ID"
url = f"https://drive.google.com/uc?id={google_drive_id}"
data = pd.read_csv(url)  # Load CSV dataset


@app.route("/get_cause_effect", methods=["POST"])
def get_cause_effect():
    query = request.json.get("query")  # Teacher's input
    if not query:
        return jsonify({"error": "Query is required"}), 400

    # Filter dataset for matches
    matches = data[data["cause"].str.contains(query, case=False, na=False)]
    if matches.empty:
        return jsonify({"message": "No relevant results found"}), 404

    # Return top results
    response = matches[["cause", "effect"]].to_dict(orient="records")
    return jsonify({"results": response})
