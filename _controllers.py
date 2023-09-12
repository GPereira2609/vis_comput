from dash import html, dcc
from app import app

import dash_bootstrap_components as dbc
import pandas as pd

df = pd.DataFrame(pd.read_csv("base.csv"))
df = df.dropna(subset="Localização")

gravidade = {
    3: ["VIOLÊNCIA CONTRA A MULHER", "DISPARO DE ARMA DE FOGO", "ESTUPRO", "MORTE A ESCLARECER", "HOMICÍDIO", 
        "TRÁFICO ", "PORTE DE ARMA"],
    2: [
        "USUÁRIO DE ENTORPECENTE", "ROUBO", "LESÃO CORPORAL", "AMEAÇA", "TENTATIVA DE FURTO", "FURTO", "FURTO QUALIFICADO",
        "TENTATIVA DE ROUBO", "LATROCINIO TENTADO", "SEQUESTRO E CÁRCERE PRIVADO", "POSSE DE ARMA DE FOGO, ACESSÓRIO OU MUNIÇÃO DE USO PERMITIDO"
    ], 
    1: [
        "PERTURBAÇÃO DO SOSSEGO OU TRABALHO ALHEIO", "PERTURBAÇÃO DA TRANQUILIDADE", "VIOLAÇÃO DE DOMICILIO", "FURTO DE COISA COMUM"
    ]
}

def mapear_gravidade(linha):
    if linha["Tipo de Ocorrência"] in gravidade[3]:
        return 3
    elif linha["Tipo de Ocorrência"] in gravidade[2]:
        return 2
    else:
        return 1

slider = [1, 2, 3]

controller = dbc.Row([
    html.Img(id="logo", src=app.get_asset_url("logo-ufal.png"), style={"width": "50%", "height": "20%"}),
    html.H4("Ocorrências na cidade de Maceió/AL", style={"margin-top": "30px"}),

    html.H5("Bairro", style={"margin-top": "5px", "margin-bottom": "10px"}),
    dcc.Dropdown(id="bairro", options=[
        {"label": i, "value": i} for i in df["Bairro"].unique().tolist()
    ], value="Todos", placeholder="Selecione um bairro"),

    html.H5("Ocorrência", style={"margin-top": "5px", "margin-bottom": "10px"}),
    dcc.Dropdown(
        id="ocorrencia", options=[
            {"label": j, "value":j} for j in df["Tipo de Ocorrência"].unique().tolist()
        ], value="Todos", placeholder="Selecione o tipo de ocorrência"
    ),

    html.H5("Gravidade da Ocorrência", style={"margin-top": "5px", "margin-bottom": "10px"}),
    dcc.Dropdown(id="gravidade", options=["Grave", "Média", "Baixa"], placeholder="Selecione uma gravidade")
])

