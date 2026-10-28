
from flask import Flask, request, jsonify
from flask_cors import CORS
from sympy import (
    symbols,
    Eq,
    solve,
    factor,
    expand,
    sympify
)

app = Flask(__name__)
CORS(app)

# Variable used in the mathematical expressions
x = symbols("x")

# Limit the length of expressions sent to the API
MAX_EXPRESSION_LENGTH = 300


def parse_expression(value):
    """Validate and convert a text expression into a SymPy expression."""

    if not isinstance(value, str):
        raise ValueError("L'expression doit être du texte.")

    value = value.strip()

    if not value:
        raise ValueError("Veuillez saisir une expression.")

    if len(value) > MAX_EXPRESSION_LENGTH:
        raise ValueError("L'expression est trop longue.")

    # Allow x^2 to represent x**2
    expression = sympify(
        value,
        locals={"x": x},
        convert_xor=True
    )

    return expression


@app.route("/", methods=["GET"])
def home():
    return "Math Assistant API is running!"


@app.route("/api/calculate", methods=["POST"])
def calculate():
    try:
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({
                "success": False,
                "error": "Les données envoyées sont invalides.",
                "steps": []
            }), 400

        mode = data.get("mode", "")

        # Solve an equation
        if mode == "equation":
            left = parse_expression(data.get("left", ""))
            right = parse_expression(data.get("right", ""))

            equation = Eq(left, right)
            solutions = solve(equation, x)

            return jsonify({
                "success": True,
                "title": "Résolution de l'équation",
                "answer": [str(solution) for solution in solutions],
                "steps": [
                    f"Membre de gauche : {left}",
                    f"Membre de droite : {right}",
                    f"Équation obtenue : {equation}",
                    f"Solutions : {solutions}"
                ]
            })

        # Factor an expression
        elif mode == "factor":
            expression = parse_expression(
                data.get("expression", "")
            )

            result = factor(expression)

            return jsonify({
                "success": True,
                "title": "Factorisation",
                "answer": str(result),
                "steps": [
                    f"Expression initiale : {expression}",
                    f"Expression factorisée : {result}"
                ]
            })

        # Expand an expression
        elif mode == "expand":
            expression = parse_expression(
                data.get("expression", "")
            )

            result = expand(expression)

            return jsonify({
                "success": True,
                "title": "Développement",
                "answer": str(result),
                "steps": [
                    f"Expression initiale : {expression}",
                    f"Expression développée : {result}"
                ]
            })

        return jsonify({
            "success": False,
            "error": "Opération inconnue. Choisissez une opération valide.",
            "steps": []
        }), 400

    except Exception:
        return jsonify({
            "success": False,
            "error": (
                "Impossible de traiter cette expression. "
                "Vérifiez sa syntaxe mathématique."
            ),
            "steps": []
        }), 400


if __name__ == "__main__":
    app.run()
