
from flask import Flask, request, jsonify
from flask_cors import CORS
from sympy import symbols, Eq, solve, factor, expand, sympify

app = Flask(__name__)
CORS(app)

x = symbols("x")


@app.route("/")
def home():
    return "Math Assistant API is running!"


@app.route("/api/calculate", methods=["POST"])
def calculate():
    try:
        data = request.get_json(force=True)
        mode = data.get("mode", "")

        if mode == "equation":
            left = sympify(data.get("left", ""), locals={"x": x})
            right = sympify(data.get("right", ""), locals={"x": x})
            solutions = solve(Eq(left, right), x)

            return jsonify({
                "success": True,
                "title": "حل المعادلة",
                "answer": [str(s) for s in solutions],
                "steps": [
                    f"الطرف الأيسر: {left}",
                    f"الطرف الأيمن: {right}",
                    f"الحلول: {solutions}"
                ]
            })

        elif mode == "factor":
            expression = sympify(
                data.get("expression", ""), locals={"x": x}
            )
            result = factor(expression)

            return jsonify({
                "success": True,
                "title": "تحليل التعبير",
                "answer": str(result),
                "steps": [
                    f"التعبير الأصلي: {expression}",
                    f"بعد التحليل: {result}"
                ]
            })

        elif mode == "expand":
            expression = sympify(
                data.get("expression", ""), locals={"x": x}
            )
            result = expand(expression)

            return jsonify({
                "success": True,
                "title": "نشر التعبير",
                "answer": str(result),
                "steps": [
                    f"التعبير الأصلي: {expression}",
                    f"بعد النشر: {result}"
                ]
            })

        return jsonify({
            "success": False,
            "error": "عملية غير معروفة",
            "steps": []
        }), 400

    except Exception:
        return jsonify({
            "success": False,
            "error": "تعذر معالجة التعبير. تحقق من كتابته.",
            "steps": []
        }), 400


if __name__ == "__main__":
    app.run()
