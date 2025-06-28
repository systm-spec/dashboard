import dash
from dash import dcc, html, dash_table
import pandas as pd
import plotly.express as px

# Dash App
app = dash.Dash(__name__)

# Data
df_kpi = pd.read_csv("data/kpis.csv")
df_transactions = pd.read_csv("data/transactions.csv")
df_monthly = pd.read_csv("data/monthly_earnings.csv")
df_status = pd.read_csv("data/sale_status.csv")
df_daily = pd.read_csv("data/daily_sales.csv")

# Colors
PRIMARY = "#6c63ff"
ACCENT = "#ef476f"
PANEL = "#23233e"
BG = "#181b2a"

# KPIs-Cards
kpi_cards = [
    html.Div(
        [
            html.H4(row["Field"], style={"color": PRIMARY, "margin": "0"}),
            html.H2(f"${row['Value']:,.0f}", style={"margin": "0.2em 0"}),
            html.P(
                f"{row['Change']}%",
                style={
                    "color": ACCENT if float(row["Change"]) < 0 else PRIMARY,
                    "fontWeight": "bold",
                    "fontSize": "1.1em",
                },
            ),
        ],
        style={
            "background": PANEL,
            "padding": "1rem 3rem",
            "borderRadius": "18px",
            "margin": "0 0.7rem",
            "color": "white",
            "boxShadow": "0 2px 12px 0 rgba(40,40,80,0.15)",
            "minWidth": "180px",
            "textAlign": "center",
        },
    )
    for _, row in df_kpi.iterrows()
]

# Monatliche Einnahmen
fig_earnings = px.line(
    df_monthly,
    x="Month",
    y=["Current_Income", "Last_Month_Income"],
    labels={"value": "Einnahmen", "variable": "Legende"},
    color_discrete_map={"Current_Income": PRIMARY, "Last_Month_Income": ACCENT},
    template="plotly_dark",
)
fig_earnings.update_layout(
    title_text="Monatliche Einnahmen (aktuell vs. Vormonat)",
    title_font_size=22,
    title_font_color=PRIMARY,
    legend_title_text="",
    plot_bgcolor=PANEL,
    paper_bgcolor=PANEL,
    font_color="white",
    margin=dict(t=50, l=20, r=20, b=30),
)

# Transactions
transaction_table = dash_table.DataTable(
    columns=[{"name": i, "id": i} for i in df_transactions.columns],
    data=df_transactions.to_dict("records"),
    style_cell={"backgroundColor": PANEL, "color": "white", "fontSize": "1.03em"},
    style_header={
        "backgroundColor": PRIMARY,
        "color": "white",
        "fontWeight": "bold",
        "fontSize": "1.08em",
        "border": "none",
    },
    style_data={"border": "none"},
    style_as_list_view=True,
    style_table={"borderRadius": "10px", "overflow": "hidden"},
)

# Daily-Sales Bar
fig_daily = px.bar(
    df_daily,
    x="Day",
    y="Sales",
    labels={"Sales": "Verkäufe", "Day": "Wochentag"},
    text_auto=True,
    template="plotly_dark",
    color_discrete_sequence=[PRIMARY],
)
fig_daily.update_traces(marker_line_width=0)
fig_daily.update_layout(
    title_text="Tägliche Verkäufe",
    plot_bgcolor=PANEL,
    paper_bgcolor=PANEL,
    font_color="white",
    margin=dict(t=50, l=0, r=0, b=0),
    title_font_color=PRIMARY,
)

# Sales-Donut
fig_status = px.pie(
    df_status,
    names="Status",
    values="Count",
    hole=0.5,
    color_discrete_sequence=[PRIMARY, ACCENT, "#00bcd4"],
)
fig_status.update_traces(
    textinfo="label+percent",
    marker=dict(line=dict(color=BG, width=2)),
    pull=[0.05, 0, 0],
)
fig_status.update_layout(
    title_text="Verkaufsstatus",
    plot_bgcolor=PANEL,
    paper_bgcolor=PANEL,
    font_color="white",
    margin=dict(t=50, l=0, r=0, b=0),
    showlegend=False,
    title_font_color=PRIMARY,
)

# Layout
app.layout = html.Div(
    [
        html.H1(
            "Sales Dashboard",
            style={
                "color": PRIMARY,
                "fontWeight": "bold",
                "fontSize": "2.7em",
                "marginBottom": "1.4rem",
                "letterSpacing": "2px",
            },
        ),
        html.Div(kpi_cards, style={"display": "flex", "gap": "1.5rem"}),
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
        html.H3(
            "Transaktionshistorie", style={"color": PRIMARY, "marginBottom": "1rem"}
        ),
        html.Div([transaction_table], style={"margin": "2rem 0"}),
        html.Div(
            "© 2025 Felix Auls | Data Analyst Portfolio",
            style={
                "color": "#555a7a",
                "textAlign": "center",
                "marginTop": "3rem",
                "fontSize": "1em",
            },
        ),
    ],
    style={
        "background": BG,
        "padding": "2.5rem 2rem",
        "margin": "-0.5rem",
        "minHeight": "100vh",
        "box-sizing": "border-box",
        "fontFamily": "Segoe UI, Arial, sans-serif",
    },
)

if __name__ == "__main__":
    app.run(debug=True)
