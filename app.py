import dash
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input
from config import METRICS
from data_prep import join


data = join()

app = dash.Dash(__name__)
app.title = "Covid-19 Analytics"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.Img(src="/assets/header-pic.png", className="header-img"),
                html.H1(children="Covid-19 Analytics", className="header-title"),
                html.P(
                    children="Analyze the distribution of Covid-19 cases in the US",
                    className="header-description"
                ),
            ],
            className="header"
        ),

        # Menu
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="State", className="menu-title"),
                        dcc.Dropdown(
                            id="State-filter",
                            options=np.sort(data.state.unique()),
                            value="USA",
                            clearable=False,
                            className="dropdown"
                        )
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Metric", className="menu-title"),
                        dcc.Dropdown(
                            id="Metric-filter",
                            options=list(data.columns.values)[3:],
                            value="cases_avg",
                            clearable=False,
                            className="dropdown"
                        )
                    ]
                )
                ,
                html.Div(
                    children=[
                        html.Div(children="Date Range", className="menu-title"),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data.date.min().date(),
                            max_date_allowed=data.date.max().date(),
                            start_date=data.date.min().date(),
                            end_date=data.date.max().date()
                        )
                    ]
                )
            ],
            className="menu"
        ),

        # Graph
        html.Div(
            children=[
                # Graph for cases
                html.Div(
                    children=dcc.Graph(
                        id="graph",
                        config={"displayModeBar": False},
                    ),
                    className="card"
                ),

                # Graph for counties
                # html.Div(
                #     children=dcc.Graph(
                #         id="counties",
                #         config={"displayModeBar": False},
                #     ),
                #     className="card"
                # ),
            ],
            className="wrapper"
        ),
    ]
)

@app.callback(
    #[Output("cases-per-day", "figure"), Output("deaths-per-day", "figure")],
    [Output("graph", "figure")],
    [
        Input("State-filter", "value"),
        Input("Metric-filter", "value"),
        Input("date-range", "start_date"),
        Input("date-range", "end_date")
    ]
)
def update_charts(state, metric, start_date, end_date):
    mask = (
        (data.state == state)
        & (data.date >= start_date)
        & (data.date <= end_date)
    )

    filtered_data = data.loc[mask, :]
    chart_figure = {
        "data": [
            {
                "x": filtered_data["date"],
                "y": filtered_data[metric],
                "type": "lines"
            }
        ],
        "layout": {
            "title": {
                "text": f"{METRICS[metric]} for {state} state" if state != "USA" else f"{METRICS[metric]} for USA",
                "x": 0.05,
                "xanchor": "left"
            },
            # "xaxis": {"fixedrange": True},
            # "yaxis": {"fixedrange": True},
            "colorway": ["#17B897"]
        }
    }

    return [chart_figure,]

# @app.callback(
#     [Output("")]
# )

if __name__ == "__main__":
    app.run_server(debug=True, host="127.0.0.1")
