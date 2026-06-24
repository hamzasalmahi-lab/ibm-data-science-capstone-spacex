"""
SpaceX Falcon 9 — Launch Records Dashboard (Plotly Dash)

Run:
    python spacex_dash_app.py
Then visit http://127.0.0.1:8050 in a browser.
"""

import pandas as pd
import dash
from dash import html, dcc, Input, Output
import plotly.express as px


# ----- Data ------------------------------------------------------------------
spacex_df = pd.read_csv("../data/spacex_launch_dash.csv")
max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()
launch_sites = sorted(spacex_df["Launch Site"].unique())


# ----- App layout ------------------------------------------------------------
app = dash.Dash(__name__)
app.title = "SpaceX Launch Records Dashboard"

app.layout = html.Div(children=[
    html.H1("SpaceX Launch Records Dashboard",
            style={"textAlign": "center", "color": "#0B1F3A",
                   "fontFamily": "Calibri, Arial, sans-serif"}),

    # Site dropdown ----------------------------------------------------------
    dcc.Dropdown(
        id="site-dropdown",
        options=[{"label": "All Sites", "value": "ALL"}]
                + [{"label": s, "value": s} for s in launch_sites],
        value="ALL",
        placeholder="Select a launch site",
        searchable=True,
    ),
    html.Br(),

    # Pie chart: total successful launches share ----------------------------
    html.Div(dcc.Graph(id="success-pie-chart")),
    html.Br(),

    # Payload range slider ---------------------------------------------------
    html.P("Payload mass (kg):"),
    dcc.RangeSlider(
        id="payload-slider",
        min=0, max=10000, step=1000,
        value=[min_payload, max_payload],
        marks={i: f"{i}" for i in range(0, 10001, 2500)},
    ),

    # Scatter: payload vs outcome -------------------------------------------
    html.Div(dcc.Graph(id="success-payload-scatter-chart")),
])


# ----- Pie chart callback ----------------------------------------------------
@app.callback(
    Output("success-pie-chart", "figure"),
    Input("site-dropdown",      "value"),
)
def update_pie(site):
    if site == "ALL":
        df = spacex_df[spacex_df["class"] == 1]
        fig = px.pie(df, names="Launch Site",
                     title="Total Successful Launches by Site")
    else:
        df = spacex_df[spacex_df["Launch Site"] == site]
        counts = df["class"].value_counts().reset_index()
        counts.columns = ["class", "count"]
        counts["class"] = counts["class"].map({1: "Success", 0: "Failure"})
        fig = px.pie(counts, names="class", values="count",
                     title=f"Total Launch Outcomes for site {site}")
    return fig


# ----- Scatter callback ------------------------------------------------------
@app.callback(
    Output("success-payload-scatter-chart", "figure"),
    [Input("site-dropdown",   "value"),
     Input("payload-slider", "value")],
)
def update_scatter(site, payload_range):
    low, high = payload_range
    df = spacex_df[(spacex_df["Payload Mass (kg)"] >= low) &
                   (spacex_df["Payload Mass (kg)"] <= high)]
    if site != "ALL":
        df = df[df["Launch Site"] == site]
    fig = px.scatter(df, x="Payload Mass (kg)", y="class",
                     color="Booster Version Category",
                     title=("Payload vs. Outcome — All Sites" if site == "ALL"
                            else f"Payload vs. Outcome — {site}"))
    return fig


# ----- Entry point -----------------------------------------------------------
if __name__ == "__main__":
    app.run_server(debug=False)
