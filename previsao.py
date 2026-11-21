"""Entradas compartilhadas entre o treinamento e o produto."""
from datetime import date
from functools import lru_cache
from pathlib import Path

import keras
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parent
CLIMAS = {
    1: "Céu limpo ou parcialmente nublado",
    2: "Nublado ou com neblina",
    3: "Chuva ou neve leve",
}
CENARIO = ("2012-10-16", 17, 22.0, 55, 14, 1, False)


def preparar(dados):
    """Usa somente calendário e condições meteorológicas."""
    datas = pd.to_datetime(dados["dteday"])
    hora = dados["hr"].to_numpy()
    mes = datas.dt.month.to_numpy() - 1
    angulo_hora = 2 * np.pi * hora / 24
    angulo_mes = 2 * np.pi * mes / 12
    return np.column_stack([
        np.sin(angulo_hora), np.cos(angulo_hora),
        np.sin(angulo_mes), np.cos(angulo_mes),
        np.eye(24)[hora],
        np.eye(7)[datas.dt.dayofweek.to_numpy()],
        dados[["workingday", "temp", "hum", "windspeed"]].to_numpy(),
        dados["weathersit"].eq(2),
        dados["weathersit"].ge(3),
    ]).astype("float32")


@lru_cache(maxsize=1)
def carregar_modelo():
    return keras.models.load_model(RAIZ / "modelo" / "pedalhora.keras", compile=False)


def prever(data, hora, temperatura, umidade, vento, clima, feriado=False):
    """Retorna a quantidade estimada para a próxima hora do cenário informado."""
    dia = date.fromisoformat(data)
    if not date(2011, 1, 1) <= dia <= date(2012, 12, 31):
        raise ValueError("Selecione uma data entre 2011 e 2012.")
    if not 0 <= hora <= 23 or clima not in CLIMAS:
        raise ValueError("Informe uma hora entre 0 e 23 e uma condição de clima válida.")
    if not (0 <= temperatura <= 41 and 0 <= umidade <= 100 and 0 <= vento <= 67):
        raise ValueError("Confira os limites de temperatura, umidade e vento.")
    dados = pd.DataFrame([{
        "dteday": pd.Timestamp(dia),
        "hr": int(hora),
        "temp": temperatura / 41,
        "hum": umidade / 100,
        "windspeed": vento / 67,
        "weathersit": clima,
        "workingday": int(dia.weekday() < 5 and not feriado),
    }])
    resultado = keras.ops.convert_to_numpy(carregar_modelo()(preparar(dados), training=False))
    return max(0, round(float(resultado[0, 0])))
