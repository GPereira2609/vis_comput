from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

from _controllers import *
from _map import *
from _histogram import *

from app import app

server = app.server

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([controller], md=3),
        dbc.Col([map, hist], md=9)
    ])
], fluid=True)


# ==============
# Callbacks
# ==============
@app.callback(
        Output("hist", "figure"),
        Output("map", "figure"),
        Input("bairro", "value"),
        Input("gravidade", "value"),
        Input("ocorrencia", "value")
)
def update_hist(bairro, grav, ocorrencia):
    # Tratamentos 
    df_dto = df.copy()
    g_factor = 3
    df_dto[["latitude", "longitude"]] = df_dto["Localização"].str.split(",", expand=True)
    df_dto["latitude"] = df_dto["latitude"].astype(float)
    df_dto["longitude"] = df_dto["longitude"].astype(float)
    
    def remover_outliers(df_dto):
        df = df_dto.copy()
        # Outliers de latitude
        df = df[df["latitude"] <= -9.480295]
        df = df[df["latitude"] >= -9.753285]
        # Outliers de longitude
        df = df[df["longitude"] <= -35.69725]
        df = df[df["longitude"] >= -35.95904]

        return df
    
    df_dto = remover_outliers(df_dto)

    
    if bairro is not None:
        if bairro != "Todos":
            df_dto = df_dto[df_dto["Bairro"] == bairro]

    if ocorrencia is not None:
        if ocorrencia != "Todos":
            df_dto = df_dto[df_dto["Tipo de Ocorrência"] == ocorrencia]

    df_dto["Gravidade"] = df_dto.apply(mapear_gravidade, axis=1)
    if grav is not None:
        if grav == "Grave":
            g_factor = 3
        elif grav == "Média":
            g_factor = 2
        else:
            g_factor = 1
        print(g_factor)
        df_dto = df_dto[df_dto["Gravidade"] == g_factor]
        
    # Histograma
    hist_fig = px.histogram(df_dto, x="Tipo de Ocorrência", opacity=.75)
    hist_layout = go.Layout(
        margin=go.layout.Margin(l=10, r=0, t=0, b=50),
        showlegend=False,
        template="plotly_dark",
        paper_bgcolor="rgba(0, 0, 0, 0)"
    )
    hist_fig.layout = hist_layout 

    # Mapa
    px.set_mapbox_access_token(open("keys/mapbox_key").read())

    
    # Ponto zero de Maceió
    mean_lat, mean_lon = -9.665328194281061, -35.73591296335011
        
    
    map_fig = px.scatter_mapbox(df_dto, lat="latitude", lon="longitude", size="Gravidade", zoom=10, opacity=.4)
    map_fig.update_layout(mapbox=dict(center=go.layout.mapbox.Center(lat=mean_lat, lon=mean_lon)),
            template="plotly_dark", paper_bgcolor="rgba(0, 0, 0, 0)",
            margin=go.layout.Margin(l=10, r=10, t=10, b=10))

    return hist_fig, map_fig

if __name__ == "__main__":
    app.run_server(debug=False)