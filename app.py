import dash
from dash import dcc, html, dash_table
import pandas as pd
import plotly.express as px

# Data
df_kpi = pd.read_csv("data/kpis.csv")
df_transactions = pd.read_csv("data/transactions.csv")
df_monthly = pd.read_csv("data/monthly_earnings.csv")
df_status = pd.read_csv("data/sale_status.csv")
df_daily = pd.read_csv("data/daily_sales.csv")

# Dash App
app = dash.Dash(__name__)

# KPIs-Cards
kpi_cards = [
    html.Div(
        [
            html.H4(row["Field"]),
            html.H2(f"${row['Value']:,.0f}"),
            html.P(
                f"{row['Change']}%",
                style={"color": "limegreen" if float(row["Change"]) >= 0 else "tomato"},
            ),
        ],
        style={
            "background": "#23233e",
            "padding": "1rem 6rem",
            "borderRadius": "18px",
            "margin": "0 0.7rem",
            "color": "white",
        },
    )
    for _, row in df_kpi.iterrows()
]

# Monatliche Einnahmen
fig_earnings = px.line(
    df_monthly,
    x="Month",
    y=["Current_Income", "Last_Month_Income"],
    labels={"value": "Income", "variable": "Legend"},
    color_discrete_map={"Current_Income": "blue", "Last_Month_Income": "red"},
    template="plotly_dark",
)

# Transactions
transaction_table = dash_table.DataTable(
    columns=[{"name": i, "id": i} for i in df_transactions.columns],
    data=df_transactions.to_dict("records"),
    style_cell={"backgroundColor": "#23233e", "color": "white"},
    style_header={"backgroundColor": "#1a1c2b", "color": "white"},
)

# Daily-Sales Bar
fig_daily = px.bar(
    df_daily,
    x="Day",
    y="Sales",
    labels={"Sales": "Sales", "Day": "Day"},
    text_auto=True,
    template="plotly_dark",
)
fig_daily.update_traces(marker_line_width=0)
fig_daily.update_layout(
    plot_bgcolor="#23233e",
    paper_bgcolor="#23233e",
    font_color="white",
    margin=dict(t=30, l=0, r=0, b=0),
)

# Sales-Donut
fig_status = px.pie(
    df_status,
    names="Status",
    values="Count",
    hole=0.5,
    color_discrete_sequence=px.colors.sequential.RdBu,
)
fig_status.update_traces(
    textinfo="label+percent", marker=dict(line=dict(color="#181b2a", width=2))
)
fig_status.update_layout(
    plot_bgcolor="#23233e",
    paper_bgcolor="#23233e",
    font_color="white",
    margin=dict(t=30, l=0, r=0, b=0),
    showlegend=True,
)


# Layout
app.layout = html.Div(
    [
        html.H1("Sales Dashboard", style={"color": "white"}),
        html.Div(kpi_cards, style={"display": "flex"}),
        html.Div(
            [
                dcc.Graph(figure=fig_earnings, config={"displayModeBar": False}),
                html.Div(
                    [
                        dcc.Graph(figure=fig_status, config={"displayModeBar": False}),
                        dcc.Graph(figure=fig_daily, config={"displayModeBar": False}),
                    ],
                    style={"display": "flex", "gap": "2rem", "padding": "1.5rem 0"},
                ),
            ],
            style={"margin": "2rem 0"},
        ),
        html.Div([transaction_table], style={"margin": "2rem 0"}),
    ],
    style={
        "background": "#181b2a",
        "padding": "2rem",
        "margin": "-0.5rem",
        "minHeight": "100vh",
        "box-sizing": "border-box",
    },
)

if __name__ == "__main__":
    app.run(debug=True)
