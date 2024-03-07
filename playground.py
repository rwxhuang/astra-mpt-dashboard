import plotly.express as px
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash import html
from dash.dependencies import Input, Output, State

df = px.data.iris()
fig = px.scatter(df, x="sepal_width", y="sepal_length")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

modal = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader("Modal Header"),
                dbc.ModalBody([
                    html.H4(id='hover_info'),
                    dcc.Graph(
                        id='modal_graph',
                        figure=fig
                    )
                ]),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close", className="ml-auto")
                ),
            ],
            id="modal",
            centered=True
        ),
    ]
)

app.layout = dbc.Container([
    dbc.Row([
        html.H2('Dash is Awesome!')
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Graph(
                id='my_graph',
                figure=fig
            )
        )
    ],justify='center'),
    modal
])

@app.callback(
    Output("modal", "is_open"),
    Output("hover_info","children"),
    [Input("my_graph", "hoverData"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(hover_data,close_button, is_open):
    if hover_data or close_button:
        x = hover_data['points'][0]['x']
        y = hover_data['points'][0]['y']
        text = "x = "+str(x)+" & y = "+str(y)
        return not is_open,text
    return is_open,None

if __name__ == "__main__":
    app.run_server(debug=True,port=8006)