
from flask import Flask, request, jsonify
from flask_cors import CORS
from sympy import (
    symbols,
    Eq,
    solve,
    factor,
    expand,
    sympify,
    solve_univariate_inequality
)

app = Flask(__name__)
CORS(app)

# Variable used in mathematical expressions
x = symbols("x")

# Maximum allowed expression length
MAX_EXPRESSION_LENGTH = 300


def parse_expression(value):
    """Validate and convert text into a SymPy expression."""

    if not isinstance(value, str):
        raise ValueError("L'expression doit être du texte.")

    value = value.strip()

    if not value:
        raise ValueError("Veuillez saisir une expression.")

    if len(value) > MAX_EXPRESSION_LENGTH:
        raise ValueError("L'expression est trop longue.")

    return sympify(
        value,
        locals={"x": x},
        convert_xor=True
    )


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

        # 1. Solve an equation
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

        # 2. Solve an inequality
        elif mode == "inequality":
            expression = parse_expression(
                data.get("expression", "")
            )

            # The input must be a relational inequality.
            if not getattr(expression, "is_Relational", False):
                raise ValueError(
                    "Saisissez une inéquation avec <, >, <= ou >=."
                )

            result = solve_univariate_inequality(
                expression,
                x,
                relational=True
            )

            return jsonify({
                "success": True,
                "title": "Résolution de l'inéquation",
                "answer": str(result),
                "steps": [
                    f"Inéquation saisie : {expression}",
                    f"Ensemble des solutions : {result}"
                ]
            })

        # 3. Factor an expression
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

        # 4. Expand an expression
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
                "Vérifiez sa syntaxe mathématique et les signes utilisés."
            ),
            "steps": []
        }), 400


if __name__ == "__main__":
    app.run()
