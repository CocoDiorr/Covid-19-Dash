import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px


data = pd.read_csv("States.csv")
data = data.query("state=='California'")
data["date"] = pd.to_datetime(data["date"], format="%Y-%m-%d")
data.sort_values("date", inplace=True)

app = dash.Dash(__name__)

# Making the figure
fig = px.line(data,
             x="date",
             y=["cases", "deaths"],
             title="Total number of cases and deaths of Covid-19",
             color_discrete_sequence=["red", "black"],
             log_y=True,
             )
# Changing the axes' and legend's titles
fig.update_layout(xaxis_title="Date",
                  yaxis_title="Number",
                  legend_title="",
                  font=dict(
                      family="Courier New, monospace",
                      size=18,
                  )
                  )

app.layout = html.Div(
    children=[
        html.H1(children="Covid-19 Analytics",),
        html.P(
            children="Analyze the distribution of Covid-19 cases in the US",
        ),
        dcc.Graph(
            figure=fig
        )
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True, host="127.0.0.1")
