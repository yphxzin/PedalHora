from flask import Flask, render_template, request

from previsao import CENARIO, CLIMAS, prever

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def inicio():
    valores = CENARIO
    resultado = erro = None
    if request.method == "POST":
        try:
            valores = (
                request.form["data"], int(request.form["hora"]),
                float(request.form["temperatura"]), int(request.form["umidade"]),
                int(request.form["vento"]), int(request.form["clima"]),
                "feriado" in request.form,
            )
            resultado = prever(*valores)
        except ValueError as exc:
            erro = str(exc)
    return render_template("index.html", valores=valores, climas=CLIMAS,
                           resultado=resultado, erro=erro)


if __name__ == "__main__":
    app.run()
