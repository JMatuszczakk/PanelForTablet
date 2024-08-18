# Flask application (app.py)
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Simulated smart home state
smart_home_state = {
    "living_room_light": False,
    "bedroom_light": False,
    "temperature": 20,
    "security_system": True
}

# Simulated security PIN (in a real system, this would be securely stored)
SECURITY_PIN = "1234"

@app.route('/')
def home():
    return render_template('home.html', state=smart_home_state)

@app.route('/toggle_light', methods=['POST'])
def toggle_light():
    room = request.json['room']
    smart_home_state[f"{room}_light"] = not smart_home_state[f"{room}_light"]
    return jsonify({"status": "success", "state": smart_home_state[f"{room}_light"]})

@app.route('/set_temperature', methods=['POST'])
def set_temperature():
    temperature = request.json['temperature']
    smart_home_state["temperature"] = temperature
    return jsonify({"status": "success", "temperature": temperature})

@app.route('/toggle_security', methods=['POST'])
def toggle_security():
    pin = request.json.get('pin')
    
    # If the system is currently armed, we need to check the PIN
    if smart_home_state["security_system"] and pin != SECURITY_PIN:
        return jsonify({"status": "error", "message": "Incorrect PIN"}), 400

    smart_home_state["security_system"] = not smart_home_state["security_system"]
    return jsonify({"status": "success", "state": smart_home_state["security_system"]})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)