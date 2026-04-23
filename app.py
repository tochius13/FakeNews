from flask import Flask, jsonify, request
from claims import extract_claims
from verify import verify_claims
from scoring import calculate_score

app = Flask(__name__)

@app.get("/")
def home():
    return jsonify({"message": "API running"})

@app.post("/fact-check")
def fact_check():
    try:
        body = request.get_json(silent=True) or {}
        text = body.get("text", "")
        file_type = body.get("file_type", "text")

        if not isinstance(text, str) or not text.strip():
            return jsonify({"error": "Missing or empty 'text' field"}), 400

        claims = extract_claims(text)
        results = verify_claims(claims)
        truth_score = calculate_score(results)

        return jsonify({
            "file_type": file_type,
            "truth_score": truth_score,
            "claims_checked": len(results),
            "claims": results
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)