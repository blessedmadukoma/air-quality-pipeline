import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import duckdb
import pandas as pd

with duckdb.connect("../air_quality.db", read_only=True) as db_connection:
    air_quality_df = db_connection.execute(
        "SELECT * FROM presentation.air_quality_data"
    ).fetchdf()

    daily_stats_df = db_connection.execute(
        "SELECT * FROM presentation.daily_air_quality_stats"
    ).fetchdf()

    latest_values_df = db_connection.execute(
        "SELECT * FROM presentation.latest_param_values_per_location"
    ).fetchdf()


def plot_map_figure():
    map_fig = px.scatter_mapbox(
        latest_values_df,
        lat="lat",
        lon="lon",
        hover_name="location",
        hover_data={
            "datetime": True,
            "pm10": True,
            "pm25": True,
            "so2": True,
            "lon": False,
            "lat": False
        },
        zoom=10.0
    )

    map_fig.update_layout(
        mapbox_style="open-street-map",
        height=800,
        title="Air Quality Monitoring Locations"
    )

    return map_fig


def plot_line_figure():
    line_fig = px.line(
        daily_stats_df[daily_stats_df["parameter"] ==
                       "so2"].sort_values(by="measurement_date"),
        x="measurement_date",
        y="average_value",
        title="SO2 Levels Plot Over Time"
    )

    return line_fig


def plot_box_figure():
    box_fig = px.box(
        daily_stats_df[daily_stats_df["parameter"] ==
                       "so2"].sort_values(by="weekday_number"),
        x="weekday",
        y="average_value",
        title="SO2 Levels Distribution By Week Day"
    )

    return box_fig


app = dash.Dash(__name__)


app_layout = html.Div([
    html.H1("Air Quality Dashboard"),
    dcc.Tabs([
        dcc.Tab(
            label="Sensor Locations",
            children=[
                dcc.Graph(id="map-street-view", figure=plot_map_figure())
            ]
        ),
        dcc.Tab(
            label="Parameter Plots",
            children=[
                dcc.Graph(id="line-plot", figure=plot_line_figure()),
                dcc.Graph(id="box-plot", figure=plot_box_figure())
            ]
        ),
    ])
])

# app.layout = html.Div()
app.layout = app_layout

if __name__ == "__main__":
    app.run_server(debug=True)
