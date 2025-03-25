import dash
from dash import dcc, html, Input, Output, State, dash_table
import pandas as pd
import io
import base64

import kaleido
import plotly.graph_objects as go
import numpy as np
#from models.growth_models import fit_models, logistic, gompertz, richards, von_bertalanffy, evf
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.growth_models import fit_models, logistic, gompertz, richards, von_bertalanffy, evf

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([

    html.Div([
        html.Img(src="/assets/Logo.png",
                 style={'height': '60px', 'margin-top': '30px', 'margin-left': '20px'}),
        html.Img(src="/assets/nestlings.jpg",
                 style={'height': '110px', 'margin-top': '30px', 'margin-right': '20px'})
    ], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center'}),

    dcc.Upload(
        id='upload-data',
        children=html.Button('📂 Upload CSV File *Subir Archivo CSV*',
                             style={'backgroundColor': '#535AA6', 'color': 'white', 'borderRadius': '5px'}),
        multiple=False
    ),
    html.Div(id='upload-status', style={'marginTop': '10px',
                                        'color': 'green',
                                        'fontWeight': 'bold'}),

    dcc.Store(id='stored-data'),
# hi -
    dcc.Tabs([
        dcc.Tab(label='Weight Analysis *Análisis de Peso*', children=[
            html.Br(),

            html.Label("Select Day Column *Seleccionar Día*:",
                       style={'fontSize': '16px', 'fontWeight': 'bold', 'color': '#535AA6'}),
            dcc.Dropdown(id='day-dropdown-weight', placeholder="Select a column for Day",
                         style={'width': '50%', 'max-width': '400px'}),

            html.Label("Select Weight Column *Seleccionar Peso*:",
                       style={'fontSize': '16px', 'fontWeight': 'bold', 'color': '#535AA6', 'margin-top': '20px'}),
            dcc.Dropdown(id='weight-dropdown', placeholder="Select a column for Weight",
                         style={'width': '50%', 'max-width': '400px'}),

            html.Br(),
            # Primer botón (Weight Analysis)
            html.Button("Analyze Weight *Analizar Peso*",
                        id="analyze-weight", n_clicks=0,
                        style={
                            'backgroundColor': '#535AA6',
                            'color': 'white',
                            'borderRadius': '8px',
                            'padding': '12px',
                            'fontSize': '20px',
                            'fontWeight': 'bold'
            }),

            html.Br(),

            dcc.Graph(id='weight-graph'),

            html.Button("📤 Export Graph *Exportar Gráfica*", id="export-graph-button", n_clicks=0,
                        style={'backgroundColor': '#E28342', 'color': 'white', 'borderRadius': '5px',
                               'padding': '8px'}),
            dcc.Download(id="download-graph"),

            html.H3("Model Results *Resultados de Modelos*", style={'textAlign': 'center', 'color': '#2E86C1'}),

            dash_table.DataTable(
                id='model-results-table',
                columns=[
                    {"name": "Modelo", "id": "Modelo"},
                    {"name": "Parámetros", "id": "Parámetros"},
                    {"name": "AIC", "id": "AIC"},
                    {"name": "BIC", "id": "BIC"},
                    {"name": "k", "id": "k"},
                    {"name": "T", "id": "T"},
                    {"name": "ΔAIC", "id": "ΔAIC"}
                ],
                style_table={'overflowX': 'auto'},
                style_header={'backgroundColor': '#535AA6', 'color': 'white', 'fontWeight': 'bold'},
                style_cell={'textAlign': 'center'},
                sort_action="native",
                export_format="csv"
            ),

            html.Br(),
            html.Button("📥 Export Results *Exportar Resultados*", id="export-button", n_clicks=0,
                        style={'backgroundColor': '#E28342', 'color': 'white', 'borderRadius': '5px',
                               'padding': '10px'}),
            dcc.Download(id="download-dataframe-csv")
        ]),

        dcc.Tab(label='Wing & Tarsus Analysis *Análisis Ala y Tarso*', children=[
            html.Br(),
            html.Label("Select Day Column *Seleccionar Dia*:",
                       style={'fontSize': '16px', 'fontWeight': 'bold', 'color': '#535AA6'}),
            dcc.Dropdown(id='day-dropdown-wing', style={'width': '50%', 'max-width': '400px'}), #535AA6

            html.Label("Select Wing Column *Ala*:",
                       style={'fontSize': '16px', 'fontWeight': 'bold', 'color': '#535AA6'}),
            dcc.Dropdown(id='wing-dropdown', style={'width': '50%', 'max-width': '400px'}),

            html.Label("Select Tarsus Column *Tarso*:",
                       style={'fontSize': '16px', 'fontWeight': 'bold', 'color': '#535AA6'}),
            dcc.Dropdown(id='tarsus-dropdown', style={'width': '50%', 'max-width': '400px'}),

            html.Button("Analyze Wing & Tarsus *Analizar Ala y Tarso*",
                        id="analyze-wing-tarsus", n_clicks=0,
                        style={
                            'backgroundColor': '#535AA6',
                            'color': 'white',
                            'borderRadius': '8px',
                            'padding': '12px',
                            'fontSize': '20px',
                            'fontWeight': 'bold'
            }),

            dcc.Graph(id='wing-graph'),

            html.Button("📤 Export Graph Wing & Tarsus *Exportar Gráfica Ala y Tarso*",
            id="export-graph-wing-tarsus-button", n_clicks=0,
            style={'backgroundColor': '#E28342', 'color': 'white', 'borderRadius': '5px', 'padding': '8px'}),
            dcc.Download(id="download-graph-wing-tarsus"),

            html.H3("Model Results Wing & Tarsus *Resultado Modelo Alas & Tarso", style={'textAlign': 'center', 'color': '#535AA6'}),

            dash_table.DataTable(
                id='model-results-table-wing-tarsus',
                columns=[
                    {"name": "Modelo", "id": "Modelo"},
                    {"name": "Parámetros", "id": "Parámetros"},
                    {"name": "AIC", "id": "AIC"},
                    {"name": "BIC", "id": "BIC"},
                    {"name": "k", "id": "k"},
                    {"name": "T", "id": "T"},
                    {"name": "ΔAIC", "id": "ΔAIC"},
                    {"name": "Variable", "id": "Variable"},
                ],
                style_table={'overflowX': 'auto'},
                style_header={'backgroundColor': '#535AA6', 'color': 'white', 'fontWeight': 'bold'},
                style_cell={'textAlign': 'center'},
                sort_action="native",
                export_format="csv"
            ),

            html.Br(),
            html.Button("📥 Export Results Ala y Tarso", id="export-wing-tarsus-button",
                        style={'backgroundColor': '#E28342', 'color': 'white', 'padding': '8px'}),
            dcc.Download(id="download-wing-tarsus-csv")
        ]),
    ]),
])

@app.callback(
    [Output('stored-data', 'data'),
     Output('day-dropdown-weight', 'options'),
     Output('weight-dropdown', 'options'),
     Output('day-dropdown-wing', 'options'),
     Output('wing-dropdown', 'options'),
     Output('tarsus-dropdown', 'options'),
     Output('upload-status', 'children')],
    Input('upload-data', 'contents'),
)
def load_data(contents):
    if not contents:
        return None, [], [], [], [], [], ""

    content_type, content_string = contents.split(',')
    decoded = io.BytesIO(base64.b64decode(content_string))
    df = pd.read_csv(decoded)

    options = [{'label': col, 'value': col} for col in df.columns]

    return df.to_json(date_format='iso', orient='split'), options, options, options, options, options, "✅ CSV uploaded successfully!"


# Callback para análisis de peso #d
# Callback para peso con tabla incluida y formato original
@app.callback(
    [Output('weight-graph', 'figure'),
     Output('model-results-table', 'data')],
    Input('analyze-weight', 'n_clicks'),
    [State('day-dropdown-weight', 'value'),
     State('weight-dropdown', 'value'),
     State('stored-data', 'data')]
)
def analyze_weight(n_clicks, day_col, weight_col, json_data):
    if n_clicks == 0 or json_data is None:
        return go.Figure(), []

    df = pd.read_json(json_data, orient='split')
    x_data = df[day_col]
    y_data = df[weight_col]

    best_model, results = fit_models(x_data, y_data)

    if best_model is None:
        return go.Figure(), []

    model_name, best_params, _, _, _, _, _ = best_model
    model_func = {
        "Logistic": logistic,
        "Gompertz": gompertz,
        "Richards": richards,
        "Von Bertalanffy": von_bertalanffy,
        "Extreme Value Function": evf
    }[model_name]

    x_fit = np.linspace(x_data.min(), x_data.max(), 100)
    y_fit = model_func(x_fit, *best_params)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_data, y=y_data, mode='markers',
        marker=dict(size=6, color='gray', opacity=0.7),  # ✅ Color gris original
        name="Observed Data"
    ))

    fig.add_trace(go.Scatter(
        x=x_fit, y=y_fit, mode='lines',
        line=dict(color='black', width=2),  # ✅ Línea negra original
        name="Trend"
    ))

    # ✅ Restaurar estilo original solicitado por usuario
    fig.update_layout(
        xaxis=dict(tickmode='linear', dtick=1),
        xaxis_title="Days After Hatching",
        yaxis_title="Weight",
        template="simple_white",
        font=dict(size=14, color="black"),
        legend=dict(x=0, y=1, bgcolor="rgba(255,255,255,0.5)"),
        showlegend=True
    )

    results_df = pd.DataFrame(results, columns=["Modelo", "Parámetros", "AIC", "BIC", "k", "T", "ΔAIC"])
    results_df["Parámetros"] = results_df["Parámetros"].astype(str)

    return fig, results_df.to_dict('records')

@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("export-button", "n_clicks"),
    State("model-results-table", "data"),
    prevent_initial_call=True
)
def export_results(n_clicks, table_data):
    if not table_data:
        return dash.no_update
    results_df = pd.DataFrame(table_data)
    return dcc.send_data_frame(results_df.to_csv, "model_results.csv", index=False)

@app.callback(
    Output("download-graph", "data"),
    Input("export-graph-button", "n_clicks"),
    State("weight-graph", "figure"),
    prevent_initial_call=True
)
def export_graph(n_clicks, figure):
    if not figure:
        return dash.no_update
    img_bytes = go.Figure(figure).to_image(format="png", scale=3)
    return dcc.send_bytes(img_bytes, "graph_export.png")

@app.callback(
    Output("download-graph-wing-tarsus", "data"),
    Input("export-graph-wing-tarsus-button", "n_clicks"),
    State("wing-graph", "figure"),
    prevent_initial_call=True
)
def export_graph_wing_tarsus(n_clicks, figure):
    if not figure:
        return dash.no_update
    img_bytes = go.Figure(figure).to_image(format="png", scale=3)
    return dcc.send_bytes(img_bytes, "wing_tarsus_graph.png")


# Callback para análisis de ala y tarso
@app.callback(
    Output("download-wing-tarsus-csv", "data"),
    Input("export-wing-tarsus-button", "n_clicks"), # ✅ Corregido
    State("model-results-table-wing-tarsus", "data"),
    prevent_initial_call=True
)
def export_wing_tarsus_results(n_clicks, data):
    if not data:
        return dash.no_update
    df = pd.DataFrame(data)
    return dcc.send_data_frame(df.to_csv, "wing_tarsus_results.csv", index=False)


@app.callback(
    [Output('wing-graph', 'figure'),
     Output('model-results-table-wing-tarsus', 'data')],
    Input('analyze-wing-tarsus', 'n_clicks'),
    [State('day-dropdown-wing', 'value'),
     State('wing-dropdown', 'value'),
     State('tarsus-dropdown', 'value'),
     State('stored-data', 'data')],
    prevent_initial_call=True
)
def analyze_wing_tarsus(n_clicks, day_col, wing_col, tarsus_col, json_data):
    if json_data is None:
        return go.Figure(), []

    df = pd.read_json(json_data, orient='split')
    df_clean = df[[day_col, wing_col, tarsus_col]].dropna()

    x_data = df_clean[day_col]
    x_fit = np.linspace(x_data.min(), x_data.max(), 50)  # puedes reducir de 100 a 80

    combined_results = []
    fig = go.Figure()

    # Ala
    y_wing = df_clean[wing_col]
    best_model_wing, results_wing = fit_models(x_data, y_wing)
    if best_model_wing:
        model_name_w, params_w, _, _, _, _, _ = best_model_wing
        model_func_w = {
            "Logistic": logistic, "Gompertz": gompertz, "Richards": richards,
            "Von Bertalanffy": von_bertalanffy, "Extreme Value Function": evf
        }[model_name_w]


        y_fit_wing = model_func_w(x_fit, *params_w)


        fig.add_trace(go.Scatter(
            x=x_data, y=y_wing, mode='markers',
            marker=dict(color='black', opacity=0.7),
            name='Wing Data'
        ))
        fig.add_trace(go.Scatter(
            x=x_fit, y=y_fit_wing, mode='lines',
            line=dict(color='black'),
            name=f'Wing Fit ({model_name_w})'
        ))

        df_wing = pd.DataFrame(results_wing, columns=["Modelo", "Parámetros", "AIC", "BIC", "k", "T", "ΔAIC"])
        df_wing['Variable'] = 'Wing'

    # Tarso
    y_tarsus = df_clean[tarsus_col]
    best_model_tarsus, results_tarsus = fit_models(x_data, y_tarsus)
    if best_model_tarsus:
        model_name_t, params_t, *_ = best_model_tarsus
        model_func_t = {
            "Logistic": logistic, "Gompertz": gompertz, "Richards": richards,
            "Von Bertalanffy": von_bertalanffy, "Extreme Value Function": evf
        }[model_name_t]

        y_fit_tarsus = model_func_t(x_fit, *params_t)

        fig.add_trace(go.Scatter(
            x=x_data, y=y_tarsus, mode='markers',
            marker=dict(color='gray', opacity=0.7),
            name='Tarsus Data'
        ))
        fig.add_trace(go.Scatter(
            x=x_fit, y=y_fit_tarsus, mode='lines',
            line=dict(color='gray', width=2),
            name=f'Tarsus Fit ({model_name_t})'
        ))

        df_tarsus = pd.DataFrame(results_tarsus, columns=["Modelo", "Parámetros", "AIC", "BIC", "k", "T", "ΔAIC"])
        df_tarsus['Variable'] = 'Tarsus'

    combined_results_df = pd.concat([df_wing, df_tarsus], ignore_index=True)
    combined_results_df["Parámetros"] = combined_results_df["Parámetros"].astype(str)

    # Estilo gráfico final
    fig.update_layout(
        xaxis=dict(tickmode='linear', dtick=1, title="Days After Hatching"),
        yaxis_title="Measurement",
        template="simple_white",
        font=dict(size=14, color="black"),
        legend=dict(x=0.05, y=0.95, bgcolor="rgba(255,255,255,0.5)")
    )

    return fig, combined_results_df.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=False)