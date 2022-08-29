import dash
from dash import dcc
from dash import html
# import dash_core_components as dcc
# import dash_html_components as html
import pandas as pd
#import plotly.express as px
import numpy as np
from dash.dependencies import Output, Input
from config import METRICS


data = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/rolling-averages/us-states.csv")
#data = data.query("state=='California'")
data["date"] = pd.to_datetime(data["date"], format="%Y-%m-%d")
data.sort_values("date", inplace=True)

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
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="State", className="menu-title"),
                        dcc.Dropdown(
                            id="State-filter",
                            options=np.sort(data.state.unique()),
                            value="California",
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

                # Graph for deaths per day
                # html.Div(
                #     children=dcc.Graph(
                #         id="deaths-per-day",
                #         config={"displayModeBar": False},
                #     ),
                #     className="card"
                # )
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
                "text": f"{METRICS[metric]} for {state} state",
                "x": 0.05,
                "xanchor": "left"
            },
            # "xaxis": {"fixedrange": True},
            # "yaxis": {"fixedrange": True},
            "colorway": ["#17B897"]
        }
    }

    # deaths_chart_figure = {
    #     "data": [
    #         {
    #             "x": filtered_data["date"],
    #             "y": filtered_data["deaths"],
    #             "type": "lines"
    #         }
    #     ],
    #     "layout": {
    #         "title": {
    #             "text": f"Number of deaths per day for {state} state",
    #             "x": 0.05,
    #             "xanchor": "left"
    #         },
    #         "colorway": ["black"]
    #     }
    # }

    #return cases_chart_figure, deaths_chart_figure
    return [chart_figure,]

if __name__ == "__main__":
    app.run_server(debug=True, host="127.0.0.1")
