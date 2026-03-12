from __future__ import annotations

from flask import Flask, jsonify, request

from engine import normalize_datetime_payload, time_remaining_payload
from schemas import validate_request

app = Flask(__name__)

@app.get('/')
def home():
    return {
        "service": "Time-Date-Utilities-Microservice",
        "status": "running",
        "endpoints": [
            "GET /health",
            "POST /normalize-datetime",
            "POST /time-remaining"
        ]
    }, 200

@app.get('/health')
def health():
    return jsonify({'status': 'ok'}), 200


@app.post('/normalize-datetime')
def normalize_datetime():
    payload = request.get_json(silent=True)
    ok, result = validate_request('normalize-datetime', payload)
    if not ok:
        return jsonify(result), 400
    return jsonify(normalize_datetime_payload(result)), 200


@app.post('/time-remaining')
def time_remaining():
    payload = request.get_json(silent=True)
    ok, result = validate_request('time-remaining', payload)
    if not ok:
        return jsonify(result), 400
    return jsonify(time_remaining_payload(result)), 200


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5002, debug=True)
