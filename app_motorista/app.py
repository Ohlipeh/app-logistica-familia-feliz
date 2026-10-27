import sys
import os
from flask import Flask, render_template, request, redirect, url_for

# 1. Este "truque" ensina o site a encontrar a sua pasta principal para importar o banco
pasta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(pasta_raiz)

# Agora podemos importar a nossa ponte com o Google Sheets!
from database.repositorio import ControleFrota

app = Flask(__name__)
sistema = ControleFrota()


@app.route("/")
def index():
    return render_template("index.html")


# 2. Rota de Check-in (Lida com o formulário)
@app.route("/checkin", methods=["GET", "POST"])
def checkin():
    if request.method == "POST":
        motorista = request.form.get("id_motorista")
        # O select agora envia o ID do veículo que já estava amarrado à demanda
        veiculo = request.form.get("id_veiculo")
        km = request.form.get("km_inicial")

        sistema.realizar_checkin(motorista, veiculo, km)
        return redirect(url_for("index"))

    # Busca as demandas recentes em vez dos veículos soltos
    todas_demandas = sistema.buscar_demandas_recentes()
    demandas_pendentes = []

    for d in todas_demandas:
        linha = list(d)
        # Trava de segurança para garantir 8 colunas
        while len(linha) < 8:
            linha.append("")

        if linha[7] == "Pendente":
            demandas_pendentes.append(linha)

    return render_template("checkin.html", demandas=demandas_pendentes)


# 3. Rota de Check-out (Devolução do veículo)
@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if request.method == "POST":
        veiculo = request.form.get("id_veiculo")
        km_final = request.form.get("km_final")

        # NOVO: Puxa o texto que o motorista digitou
        observacoes = request.form.get("observacoes")

        # Chama a função enviando também as observações
        sistema.realizar_checkout(veiculo, km_final, observacoes)

        return redirect(url_for("index"))

    todos_veiculos = sistema.buscar_veiculos()
    return render_template("checkout.html", veiculos=todos_veiculos)


if __name__ == "__main__":
    app.run(debug=True)
