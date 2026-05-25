from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

OPERATIONS = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a / b if b != 0 else 'Error: Division by zero',
    '%': lambda a, b: a % b if b != 0 else 'Error: Division by zero',
    '^': lambda a, b: a ** b,
}

SCIENCE_OPS = {
    'sin': lambda x: math.sin(math.radians(x)),
    'cos': lambda x: math.cos(math.radians(x)),
    'tan': lambda x: math.tan(math.radians(x)),
    'asin': lambda x: math.degrees(math.asin(x)) if -1 <= x <= 1 else 'Error: Domain',
    'acos': lambda x: math.degrees(math.acos(x)) if -1 <= x <= 1 else 'Error: Domain',
    'atan': lambda x: math.degrees(math.atan(x)),
    'log': lambda x: math.log10(x) if x > 0 else 'Error: Domain',
    'ln': lambda x: math.log(x) if x > 0 else 'Error: Domain',
    'sqrt': lambda x: math.sqrt(x) if x >= 0 else 'Error: Domain',
    'cbrt': lambda x: x ** (1/3) if x >= 0 else -((-x) ** (1/3)),
    'square': lambda x: x ** 2,
    'cube': lambda x: x ** 3,
    'exp': lambda x: math.exp(x),
    'tenx': lambda x: 10 ** x,
    'factorial': lambda x: math.factorial(x) if x >= 0 and x == int(x) else 'Error: Domain',
    'abs': lambda x: abs(x),
    'inv': lambda x: 1 / x if x != 0 else 'Error: Division by zero',
    'negate': lambda x: -x,
}

UNARY_OPS = {'square', 'cube', 'sqrt', 'cbrt', 'exp', 'tenx', 'factorial', 'abs', 'inv', 'negate'} | set(SCIENCE_OPS.keys()) - {'+', '-', '*', '/', '%', '^'}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    op = data.get('op')
    a = data.get('a')
    b = data.get('b')

    if a is None:
        return jsonify({'error': 'Missing operands'}), 400

    try:
        a = float(a)
        if b is not None and b != '':
            b = float(b)
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid number'}), 400

    if op in SCIENCE_OPS:
        result = SCIENCE_OPS[op](a)
    elif op in OPERATIONS:
        if b is None:
            return jsonify({'error': 'Missing second operand'}), 400
        result = OPERATIONS[op](a, b)
    else:
        return jsonify({'error': f'Unknown operation: {op}'}), 400

    if isinstance(result, str) and result.startswith('Error'):
        return jsonify({'error': result}), 400

    if isinstance(result, float) and (math.isinf(result) or math.isnan(result)):
        return jsonify({'error': 'Result undefined'}), 400

    return jsonify({'result': result})


if __name__ == '__main__':
    app.run(debug=True)
