from flask import Flask, render_template, request
from lexer import lexer

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    tokens = []
    error = None

    if request.method == 'POST':

        code = request.form['code']

        if len(code) > 4000:
            error = "Limite máximo de 4000 caracteres excedido."
            return render_template(
                'index.html',
                tokens=[],
                error=error,
                code=code
            )

        try:
            tokens = lexer(code)

        except Exception as e:
            error = str(e)

    return render_template(
        'index.html',
        tokens=tokens,
        error=error
    )

if __name__ == '__main__':
    app.run(debug=True)