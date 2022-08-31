import pandas as pd

def join():
    states_data = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/rolling-averages/us-states.csv")
    us_data = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/rolling-averages/us.csv")

    states_data.drop(['geoid'], axis=1, inplace=True)
    us_data.rename(columns={"geoid":"state"}, inplace=True)

    data = pd.concat([states_data, us_data])
    data["date"] = pd.to_datetime(data["date"], format="%Y-%m-%d")
    data.sort_values("date", inplace=True)

    return data
