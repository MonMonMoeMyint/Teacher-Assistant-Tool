from flask import Flask, request, jsonify
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

FIXED_OPENAPI_JSON = {
    "openapi": "3.1.0",
    "info": {
        "title": "Cause-Effect Finder API",
        "description": "API to find cause-effect relationships.",
        "version": "1.0.0"
    },
    "servers": [
        {
            "url": "https://teacher-assistant-tool-production.up.railway.app"
        }
    ],
    "paths": {
        "/get_cause_effect": {
            "post": {
                "summary": "Find cause-effect relationships based on input",
                "operationId": "getCauseEffect",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "query": { "type": "string" }
                                },
                                "required": ["query"]
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {
                                        "$ref": "#/components/schemas/CauseEffectResponse"
                                    }
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "Bad request (missing or invalid query parameter)"
                    },
                    "404": {
                        "description": "No relevant results found"
                    }
                }
            }
        }
    },
    "components": {
        "schemas": {
            "CauseEffectResponse": {
                "type": "object",
                "properties": {
                    "cause": { "type": "string" },
                    "effect": { "type": "string" },
                    "advice": { "type": "string" }
                }
            }
        }
    }
}


# Load dataset from Google Drive (provide your shared link ID)
google_drive_id = os.getenv("GOOGLE_DRIVE_FILE_ID")
url = f"https://drive.google.com/uc?id={google_drive_id}"
data = pd.read_csv(url)  # Load CSV dataset

# Endpoint 1: Search Cause-Effect Data
@app.route('/get_cause_effect', methods=['POST'])
def get_cause_effect():
    user_input = request.json.get('query', '').lower()  # Teacher's input
    if not user_input:
        return jsonify({'error': 'Query is required'}), 400

    # Filter dataset for matches
    matches = data[data['cause'].str.contains(user_input, case=False, na=False)]
    if matches.empty:
        return jsonify({'message': 'No relevant results found'}), 404

    # Return top results
    response = matches[['cause', 'effect']].to_dict(orient='records')
    return jsonify({'results': response})

# Endpoint 2: Serve OpenAPI JSON
@app.route('/openapi.json', methods=['GET'])
def openapi():
    return jsonify(FIXED_OPENAPI_JSON)

if __name__ == '__main__':
    app.run(debug=True)
