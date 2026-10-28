
from flask import Flask, request, jsonify
from flask_cors import CORS
from sympy import symbols, Eq, solve, factor, expand, sympify

app = Flask(__name__)
CORS(app)

x = symbols("x")


@app.route("/")
def home():
    return "Math Assistant API is running!"


@app.route("/api", methods=["POST"])
def calculate():
    try:
        data = request.get_json(force=True)

        mode = data.get("mode", "")
        expression = data.get("expression", "")

        if mode == "equation":
            left = sympify(data["left"])
            right = sympify(data["right"])
            result = solve(Eq(left, right), x)

        elif mode == "factor":
            result = factor(sympify(expression))

        elif mode == "expand":
            result = expand(sympify(expression))

        else:
            return jsonify({"error": "Unknown operation"}), 400

        return jsonify({"result": str(result)})

    except Exception as error:
        return jsonify({"error": str(error)}), 400


if __name__ == "__main__":
    app.run()
