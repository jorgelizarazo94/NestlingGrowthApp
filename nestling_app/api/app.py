import dash
from dash import dcc, html, Input, Output, State, dash_table
import pandas as pd
import io
import base64
from nestling_app.api.translations import translations
import kaleido
import plotly.graph_objects as go
import numpy as np
import webbrowser
import threading
#from models.growth_models import fit_models, logistic, gompertz, richards, von_bertalanffy, evf
import sys
import os
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nestling_app.models.growth_models import fit_models, logistic, gompertz, richards, von_bertalanffy, evf

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

app = dash.Dash(
    __name__,
    assets_folder=resource_path("assets"),
    suppress_callback_exceptions=True
)
server = app.server


def normalize_criterion(criterion):
    return "AICc" if str(criterion or "AIC").upper() == "AICC" else "AIC"


def delta_column_name(criterion):
    return "ΔAICc" if normalize_criterion(criterion) == "AICc" else "ΔAIC"


def finite_float(value):
    try:
        numeric_value = float(value)
    except (TypeError, ValueError):
        return None
    return numeric_value if np.isfinite(numeric_value) else None


def calculate_aicc(aic, params, sample_size):
    aic_value = finite_float(aic)
    if aic_value is None:
        return None

    parameter_count = len(params)
    denominator = sample_size - parameter_count - 1
    if denominator <= 0:
        return None

    return finite_float(
        aic_value + (2 * parameter_count * (parameter_count + 1)) / denominator
    )


def format_table_value(value):
    numeric_value = finite_float(value)
    return round(numeric_value, 4) if numeric_value is not None else "N/A"


def annotated_results(results, sample_size):
    annotations = []
    for result in results or []:
        if len(result) >= 8:
            model_name, params, aic, aicc, bic, k_value, t_value, _ = result[:8]
        else:
            model_name, params, aic, bic, k_value, t_value, _ = result
            aicc = calculate_aicc(aic, params, sample_size)
        annotations.append({
            "result": result,
            "Modelo": model_name,
            "Parámetros": str(params),
            "AIC": finite_float(aic),
            "AICc": finite_float(aicc),
            "BIC": finite_float(bic),
            "k": finite_float(k_value),
            "T": finite_float(t_value),
        })
    return annotations


def results_dataframe(results, criterion, sample_size, variable=None):
    annotations = annotated_results(results, sample_size)
    if not annotations:
        return pd.DataFrame()

    best_aic = min(
        (result["AIC"] for result in annotations if result["AIC"] is not None),
        default=None
    )
    best_aicc = min(
        (result["AICc"] for result in annotations if result["AICc"] is not None),
        default=None
    )

    metric = normalize_criterion(criterion)
    annotations.sort(
        key=lambda result: result[metric]
        if result[metric] is not None
        else float("inf")
    )

    records = []
    for result in annotations:
        delta_aic = (
            result["AIC"] - best_aic
            if result["AIC"] is not None and best_aic is not None
            else None
        )
        delta_aicc = (
            result["AICc"] - best_aicc
            if result["AICc"] is not None and best_aicc is not None
            else None
        )

        record = {
            "Modelo": result["Modelo"],
            "Parámetros": result["Parámetros"],
            "AIC": format_table_value(result["AIC"]),
            "AICc": format_table_value(result["AICc"]),
            "BIC": format_table_value(result["BIC"]),
            "k": format_table_value(result["k"]),
            "T": format_table_value(result["T"]),
            "ΔAIC": format_table_value(delta_aic),
            "ΔAICc": format_table_value(delta_aicc),
        }
        if variable is not None:
            record["Variable"] = variable
        records.append(record)

    return pd.DataFrame(records)


def model_table_columns(lang, criterion, include_variable=False):
    t = translations.get(lang, translations["en"])
    delta_col = delta_column_name(criterion)
    columns = [
        {"name": t.get("model_column", "Model"), "id": "Modelo"},
        {"name": t.get("parameters_column", "Parameters"), "id": "Parámetros"},
        {"name": "AIC", "id": "AIC"},
        {"name": "AICc", "id": "AICc"},
        {"name": "BIC", "id": "BIC"},
        {"name": "k", "id": "k"},
        {"name": "T", "id": "T"},
        {"name": delta_col, "id": delta_col},
    ]
    if include_variable:
        columns.append({"name": t.get("variable_column", "Variable"), "id": "Variable"})
    return columns


def records_for_columns(records, columns):
    if not records or not columns:
        return records
    column_ids = [column["id"] for column in columns if column.get("id")]
    return [
        {column_id: record.get(column_id) for column_id in column_ids}
        for record in records
    ]


app.layout = html.Div([

            html.Div([
                html.A(
                    html.Img(
                        src="/assets/logo.png",
                        style={'height': '60px', 'margin-top': '30px', 'margin-left': '20px'}
                    ),
                    href="https://wildlabs.net",
                    target="_blank"
                ),
                html.Div([
                    html.Div(id="published-in-label",
                             style={'fontSize': '14px', 'fontWeight': 'bold', 'color': '#535AA6',
                                    'textAlign': 'center', 'marginBottom': '4px'}),
                    html.A(
                        html.Img(
                            src="/assets/sage_avian.svg",
                            alt="Sage Avian Biology",
                            style={
                                'height': '140px',
                                'width': '460px',
                                'objectFit': 'contain'
                            }
                        ),
                        href="https://journals.sagepub.com/home/avb",
                        target="_blank",
                        rel="noopener noreferrer"
                    )
                ], style={'textAlign': 'center', 'marginTop': '24px'}),
                html.Img(
                    src="/assets/nestlings.jpg",
                    style={'height': '110px', 'margin-top': '30px', 'margin-right': '20px'}
                )
            ], style={
                'display': 'flex',
                'justifyContent': 'space-between',
                'alignItems': 'center'
            }),

        html.Div([
            html.Label(id="language-selector-label", style={'margin-left': '20px'}),
            dcc.Dropdown(
                id='language-selector',
                options=[
                    {'label': '🇬🇧 English', 'value': 'en'},
                    {'label': '🇪🇸 Español', 'value': 'es'},
                    {'label': '🇵🇹 Português', 'value': 'pt'}
                ],
                value='es',
                clearable=False,
                style={'width': '200px', 'margin': '10px 0 30px 20px'}
            ),
            html.Label(id="label-information-criterion", style={'margin-left': '20px'}),
            dcc.Dropdown(
                id='criterion-selector',
                options=[
                    {'label': 'AIC', 'value': 'AIC'},
                    {'label': 'AICc (muestra pequeña)', 'value': 'AICc'}
                ],
                value='AIC',
                clearable=False,
                style={'width': '240px', 'margin': '10px 0 30px 20px'}
            ),
            dcc.Store(id='selected-language', data='es')
        ]),

    dcc.Upload(
        id='upload-data',
        children=html.Button('📂 Upload CSV File *Subir Archivo CSV*',
                             style={'backgroundColor': '#535AA6', 'color': 'white', 'borderRadius': '5px'}),
        multiple=False
    ),
    html.Div(id='upload-button-placeholder', style={'marginTop': '10px',
                                        'color': 'green',
                                        'fontWeight': 'bold'}),

    dcc.Store(id='stored-data'),
# hi -
    dcc.Tabs([
        dcc.Tab(id='tab-weight', children=[
            html.Br(),

            html.Label(id="label-select-day-weight",
                       style={'fontSize': '16px', 'fontWeight': 'bold', 'color': '#535AA6'}),
            dcc.Dropdown(id='day-dropdown-weight', placeholder="Select a column for Day",
                         style={'width': '50%', 'max-width': '400px'}),

            html.Label(id="label-select-weight",
                       style={'fontSize': '16px', 'fontWeight': 'bold', 'color': '#535AA6', 'margin-top': '20px'}),
            dcc.Dropdown(id='weight-dropdown', placeholder="Select a column for Weight",
                         style={'width': '50%', 'max-width': '400px'}),

            html.Label("Select Y-axis Unit:", style={'margin-left': '20px'}),
            dcc.Dropdown(
                id='unit-selector-weight',
                options=[
                    {'label': 'g', 'value': 'g'},
                    {'label': 'kg', 'value': 'kg'},
                    {'label': 'lb', 'value': 'lb'},
                    {'label': 'oz', 'value': 'oz'}
                ],
                value='g',
                clearable=False,
                style={'width': '150px', 'margin-left': '20px'}
            ),

            html.Br(),
            # Primer botón (Weight Analysis)
            html.Button(id="analyze-weight", n_clicks=0,
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

            html.Button( id="export-graph-button", n_clicks=0,
                        style={'backgroundColor': '#E28342', 'color': 'white', 'borderRadius': '5px',
                               'padding': '8px'}),
            dcc.Download(id="download-graph"),

            html.H3(id="h3-model-results", style={'textAlign': 'center', 'color': '#2E86C1'}),

            dash_table.DataTable(
                id='model-results-table',
                columns=model_table_columns('es', 'AIC'),
                style_table={'overflowX': 'auto'},
                style_header={'backgroundColor': '#535AA6', 'color': 'white', 'fontWeight': 'bold'},
                style_cell={'textAlign': 'center'},
                sort_action="native",
                export_format="csv"
            ),

            html.Br(),
            html.Button( id="export-button", n_clicks=0,
                        style={'backgroundColor': '#E28342', 'color': 'white', 'borderRadius': '5px',
                               'padding': '10px'}),
            dcc.Download(id="download-dataframe-csv")
        ]),

        dcc.Tab(id='tab-wing', label='tab-wing', children=[
            html.Br(),
            html.Label(id="label-select-day-wing",
                       style={'fontSize': '16px', 'fontWeight': 'bold', 'color': '#535AA6'}),
            dcc.Dropdown(id='day-dropdown-wing', style={'width': '50%', 'max-width': '400px'}), #535AA6

            html.Label(id="label-select-wing",
                       style={'fontSize': '16px', 'fontWeight': 'bold', 'color': '#535AA6'}),
            dcc.Dropdown(id='wing-dropdown', style={'width': '50%', 'max-width': '400px'}),

            html.Label(id="label-select-tarsus",
                       style={'fontSize': '16px', 'fontWeight': 'bold', 'color': '#535AA6'}),
            dcc.Dropdown(id='tarsus-dropdown', style={'width': '50%', 'max-width': '400px'}),

            html.Label("Select Y-axis Unit:", style={'margin-left': '20px'}),
            dcc.Dropdown(
                id='unit-selector-wing',
                options=[
                    {'label': 'mm', 'value': 'mm'},
                    {'label': 'cm', 'value': 'cm'},
                    {'label': 'inch', 'value': 'inch'}
                ],
                value='mm',
                clearable=False,
                style={'width': '150px', 'margin-left': '20px'}
            ),

            html.Button(id="analyze-wing-tarsus", n_clicks=0,
                        style={
                            'backgroundColor': '#535AA6',
                            'color': 'white',
                            'borderRadius': '8px',
                            'padding': '12px',
                            'fontSize': '20px',
                            'fontWeight': 'bold'
            }),

            dcc.Graph(id='wing-graph'),

            html.Button(
            id="export-graph-wing-tarsus-button", n_clicks=0,
            style={'backgroundColor': '#E28342', 'color': 'white', 'borderRadius': '5px', 'padding': '8px'}),
            dcc.Download(id="download-graph-wing-tarsus"),

            html.H3(id="h3-model-results-wing", style={'textAlign': 'center', 'color': '#535AA6'}),

            dash_table.DataTable(
                id='model-results-table-wing-tarsus',
                columns=model_table_columns('es', 'AIC', include_variable=True),
                style_table={'overflowX': 'auto'},
                style_header={'backgroundColor': '#535AA6', 'color': 'white', 'fontWeight': 'bold'},
                style_cell={'textAlign': 'center'},
                sort_action="native",
                export_format="csv"
            ),

            html.Br(),
            html.Button(id="export-wing-tarsus-button",
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
     Output('upload-button-placeholder', 'children')],
    [Input('upload-data', 'contents'),
     State('selected-language', 'data')]
)
def load_data(contents, lang):
    if not contents:
        return None, [], [], [], [], [], ""

    content_type, content_string = contents.split(',')
    decoded = io.BytesIO(base64.b64decode(content_string))
    df = pd.read_csv(decoded)

    options = [{'label': col, 'value': col} for col in df.columns]
    message = translations[lang]['upload_success']

    return (
        df.to_json(date_format='iso', orient='split'),
        options,
        options,
        options,
        options,
        options,
        message
    )

@app.callback(
    Output('h3-model-results-wing', 'children'),
    Input('selected-language', 'data')
)
def update_model_results_wing_title(lang):
    t = translations[lang]
    return t.get('model_results_wing', 'Model Results Wing & Tarsus')


@app.callback(
    [Output('language-selector-label', 'children'),
     Output('label-information-criterion', 'children'),
     Output('criterion-selector', 'options'),
     Output('published-in-label', 'children'),
     Output('model-results-table', 'columns'),
     Output('model-results-table-wing-tarsus', 'columns')],
    [Input('selected-language', 'data'),
     Input('criterion-selector', 'value')]
)
def update_criterion_and_publication_labels(lang, criterion):
    t = translations.get(lang, translations["en"])
    return (
        t.get('language_label', '🌍 Language / Idioma / Língua:'),
        t.get('information_criterion', 'Information criterion'),
        [
            {'label': t.get('aic_option', 'AIC'), 'value': 'AIC'},
            {'label': t.get('aicc_option', 'AICc (small sample)'), 'value': 'AICc'},
        ],
        t.get('published_in', 'published in'),
        model_table_columns(lang, criterion),
        model_table_columns(lang, criterion, include_variable=True),
    )


# Callback para análisis de peso #d
# Callback para peso con tabla incluida y formato original
@app.callback(
    [Output('weight-graph', 'figure'),
     Output('model-results-table', 'data')],
    [Input('analyze-weight', 'n_clicks'),
     Input('criterion-selector', 'value')],
    [State('day-dropdown-weight', 'value'),
     State('weight-dropdown', 'value'),
     State('stored-data', 'data'),
     State('unit-selector-weight', 'value')]
)
def analyze_weight(n_clicks, criterion, day_col, weight_col, json_data, unit):
    if n_clicks == 0 or json_data is None or not day_col or not weight_col:
        return go.Figure(), []

    df = pd.read_json(json_data, orient='split')
    df_clean = df[[day_col, weight_col]].dropna()

    if df_clean.empty:
        print("⚠️ Dataset is empty after removing NaNs.")
        return go.Figure(), []

    x_data = df_clean[day_col]
    y_data = df_clean[weight_col]

    if len(df_clean) < 3:
        print(f"⚠️ No hay suficientes datos. Solo {len(df_clean)} filas.")
        return go.Figure(), []

    best_model, results = fit_models(x_data, y_data, criterion=criterion)
    if best_model is None:
        return go.Figure(), []

    model_name, best_params, *_ = best_model
    model_func = {
        "Logistic": logistic,
        "Gompertz": gompertz,
        "Richards": richards,
        "Von Bertalanffy": von_bertalanffy,
        "Extreme Value Function": evf
    }[model_name]

    x_fit = np.linspace(x_data.min(), x_data.max(), 80)
    y_fit = model_func(x_fit, *best_params)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_data, y=y_data, mode='markers',
        marker=dict(size=6, color='gray', opacity=0.7),
        name="Observed Data"
    ))
    fig.add_trace(go.Scatter(
        x=x_fit, y=y_fit, mode='lines',
        line=dict(color='black', width=2),
        name="Trend"
    ))

    tick_spacing = 1 if len(x_data.unique()) <= 12 else int(len(x_data.unique()) // 10)

    fig.update_layout(
        xaxis=dict(
            range=[x_data.min(), x_data.max()],  # eje X exacto sin margen
            tickmode='linear',
            dtick=tick_spacing,
            title="Days After Hatching"
        ),
        yaxis_title=f"Weight ({unit})",
        template="simple_white",
        font=dict(size=14, color="black"),
        legend=dict(x=0, y=1, bgcolor="rgba(255,255,255,0.5)"),
        showlegend=True
    )

    results_df = results_dataframe(results, criterion, len(df_clean))

    return fig, results_df.to_dict('records')

@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("export-button", "n_clicks"),
    State("model-results-table", "data"),
    State("model-results-table", "columns"),
    prevent_initial_call=True
)
def export_results(n_clicks, table_data, columns):
    if not table_data:
        return dash.no_update
    results_df = pd.DataFrame(records_for_columns(table_data, columns))
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
    [Output('export-graph-button', 'children'),
     Output('export-button', 'children'),
     Output('export-graph-wing-tarsus-button', 'children'),
     Output('export-wing-tarsus-button', 'children')],
    Input('selected-language', 'data')
)
def update_export_buttons(lang):
    t = translations[lang]
    return (
        t.get('export_graph', '📤 Export Graph'),
        t.get('export_results', '📥 Export Results'),
        t.get('export_graph_wing', '📤 Export Graph Wing & Tarsus'),
        t.get('export_results_wing', '📥 Export Results Wing & Tarsus'),
    )


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

@app.callback(
    [Output('tab-weight', 'label'),
     Output('tab-wing', 'label')],
    Input('selected-language', 'data')
)
def update_tab_labels(lang):
    t = translations[lang]
    return t['weight_tab'], t['wing_tab']


# Callback para análisis de ala y tarso
@app.callback(
    Output("download-wing-tarsus-csv", "data"),
    Input("export-wing-tarsus-button", "n_clicks"), # ✅ Corregido
    State("model-results-table-wing-tarsus", "data"),
    State("model-results-table-wing-tarsus", "columns"),
    prevent_initial_call=True
)
def export_wing_tarsus_results(n_clicks, data, columns):
    if not data:
        return dash.no_update
    df = pd.DataFrame(records_for_columns(data, columns))
    return dcc.send_data_frame(df.to_csv, "wing_tarsus_results.csv", index=False)



@app.callback(
    [Output('analyze-weight', 'children'),
     Output('upload-data', 'children'),
     Output('analyze-wing-tarsus', 'children')],
    Input('selected-language', 'data')
)
def update_labels(lang):
    t = translations[lang]
    return (
        t['analyze_weight'],
        html.Button(t['upload_btn'], style={
            'backgroundColor': '#535AA6', 'color': 'white', 'borderRadius': '5px'
        }),
        t['analyze_wing_tarsus']
    )

@app.callback(
    Output('h3-model-results', 'children'),
    Input('selected-language', 'data')
)
def update_model_results_title(lang):
    t = translations[lang]
    return t.get('model_results', 'Model Results')

@app.callback(
    [Output('wing-graph', 'figure'),
     Output('model-results-table-wing-tarsus', 'data')],
    [Input('analyze-wing-tarsus', 'n_clicks'),
     Input('criterion-selector', 'value')],
    [State('day-dropdown-wing', 'value'),
     State('wing-dropdown', 'value'),
     State('tarsus-dropdown', 'value'),
     State('stored-data', 'data'),
     State('unit-selector-wing', 'value')],
    prevent_initial_call=True
)

def analyze_wing_tarsus(n_clicks, criterion, day_col, wing_col, tarsus_col, json_data, unit):
    if n_clicks == 0 or json_data is None or not day_col or not wing_col or not tarsus_col:
        return go.Figure(), []

    df = pd.read_json(json_data, orient='split')
    df_clean = df[[day_col, wing_col, tarsus_col]].dropna()
    if df_clean.empty:
        return go.Figure(), []

    x_data = df_clean[day_col]
    x_fit = np.linspace(x_data.min(), x_data.max(), 30)  # puedes reducir de 100 a 80

    combined_results = []
    fig = go.Figure()

    # Ala
    y_wing = df_clean[wing_col]
    best_model_wing, results_wing = fit_models(x_data, y_wing, criterion=criterion)
    if best_model_wing:
        model_name_w, params_w, *_ = best_model_wing
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

        combined_results.append(
            results_dataframe(results_wing, criterion, len(df_clean), variable='Wing')
        )

    # Tarso
    y_tarsus = df_clean[tarsus_col]
    best_model_tarsus, results_tarsus = fit_models(x_data, y_tarsus, criterion=criterion)
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

        combined_results.append(
            results_dataframe(results_tarsus, criterion, len(df_clean), variable='Tarsus')
        )

    if not combined_results:
        return fig, []

    combined_results_df = pd.concat(combined_results, ignore_index=True)

    # Estilo gráfico final
    tick_spacing = 1 if len(x_data.unique()) <= 12 else int(len(x_data.unique()) // 10)

    fig.update_layout(
        xaxis=dict(
            range=[x_data.min(), x_data.max()],  # 🚨 aquí obligamos el eje X exacto sin margen
            tickmode='linear',
            dtick=tick_spacing,
            title="Days After Hatching"
        ),
        yaxis_title=f"Measurement ({unit})",
        template="simple_white",
        font=dict(size=14, color="black"),
        legend=dict(x=0.05, y=0.95, bgcolor="rgba(255,255,255,0.5)")
    )

    return fig, combined_results_df.to_dict('records')

@app.callback(
    Output('selected-language', 'data'),
    Input('language-selector', 'value')
)
def store_language(lang_value):
    return lang_value

@app.callback(
    [Output('label-select-day-weight', 'children'),
     Output('label-select-weight', 'children'),
     Output('label-select-day-wing', 'children'),
     Output('label-select-wing', 'children'),
     Output('label-select-tarsus', 'children')],
    Input('selected-language', 'data')
)
def update_dropdown_labels(lang):
    t = translations[lang]
    return (
        t.get('select_day', 'Select Day Column'),
        t.get('select_weight', 'Select Weight Column'),
        t.get('select_day', 'Select Day Column'),  # usado también en tab-wing
        t.get('select_wing', 'Select Wing Column'),
        t.get('select_tarsus', 'Select Tarsus Column')
    )


def open_browser():
    webbrowser.open_new("http://127.0.0.1:8050")

def main():
    threading.Timer(1, open_browser).start()
    try:
        app.run(debug=False)
    except AttributeError:
        app.run_server(debug=False)

if __name__ == '__main__':
    main()
