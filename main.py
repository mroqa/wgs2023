import pathlib
import os
import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objs as go

dirname = os.path.dirname(__file__)

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
    meta_tags=[
        {
            "name": "viewprot",
            "content": "width=device-width, initial-scale=1.0, shrink-to-fit=no",
        }
    ],
)
app.title = "THE WORLD DATA VISUALIZATION PRIZE"
server = app.server

years = [
    "2009",
    "2010",
    "2011",
    "2012",
    "2013",
    "2014",
    "2015",
    "2016",
    "2017",
    "2018",
    "2019",
    "2020",
    "2021",
]
sheets = [
    "GLOBAL HEALTH",
    "ENERGY",
    "QUALITY OF LIFE",
    "EDUCATION & DEVELOPMENT",
    "SUSTAINABILITY & CLIMATE",
    "ECONOMICS",
]

health = pd.read_excel("https://github.com/mroqa/wgs2023/blob/master/assets/Alldata.xlsx", sheets[0])
energy = pd.read_excel("https://github.com/mroqa/wgs2023/blob/master/assets/Alldata.xlsx", sheets[1])
quality = pd.read_excel("https://github.com/mroqa/wgs2023/blob/master/assets/Alldata.xlsx", sheets[2])
education = pd.read_excel("https://github.com/mroqa/wgs2023/blob/master/assets/Alldata.xlsx", sheets[3])
sustainability = pd.read_excel("https://github.com/mroqa/wgs2023/blob/master/assets/Alldata.xlsx", sheets[4])
economics = pd.read_excel("https://github.com/mroqa/wgs2023/blob/master/assets/Alldata.xlsx", sheets[5])

options_health = [
    {"label": "Health Expenditure", "value": "Health Expenditure"},
    {"label": "Dementia", "value": "Dementia"},
    {"label": "Smoking", "value": "Smoking"},
    {"label": "Tuberculosis", "value": "Tuberculosis"},
    {"label": "HIV-AIDS", "value": "HIV-AIDS"},
    {"label": "Polio", "value": "Polio"},
    {"label": "Malaria", "value": "Malaria"},
    {"label": "Tuberculosis", "value": "Tuberculosis"},
]
options_energy = [
    {
        "label": "Photovoltaic Solar Power (PV)",
        "value": "Photovoltaic Solar Power (PV)",
    },
    {"label": "Solar Power", "value": "Solar Power"},
    {"label": "Wind Power", "value": "Wind Power"},
    {"label": "Renewable Energy", "value": "Renewable Energy"},
]
options_quality = [
    dict(label=val, value=val) for val in quality["cause"].unique().tolist()[::-1]
]
options_edu = [
    dict(label=val, value=val) for val in education["cause"].unique().tolist()[::-1]
]
options_sustain = [
    dict(label=val, value=val)
    for val in sustainability["cause"].unique().tolist()[::-1]
]
options_eco = [
    dict(label=val, value=val) for val in economics["cause"].unique().tolist()[::-1]
]
# ---------------- Health data -------------#
deaths = health[health.data == "deaths"]
deaths = deaths.drop(["data", "metric", "10 year change"], axis=1)
deaths = deaths.melt(id_vars=["cause"])
deaths.columns = ["disease", "year", "deaths"]
deaths = deaths[deaths["deaths"].notna()]
# ---------------- Energy data -------------#
energy = energy[energy.data == "as % of global electricity production"]
energy = energy.drop(["data", "metric", "10 year change"], axis=1)
energy = energy.melt(id_vars=["cause"])
energy.columns = ["source", "year", "production"]
energy = energy[energy["production"].notna()]
# ---------------- Quality data -------------#
lifeQuality = quality[quality.data == "% of global population"]
lifeQuality = lifeQuality.drop(["data", "metric", "10 year change"], axis=1)
lifeQuality = lifeQuality.melt(id_vars=["cause"])
lifeQuality.columns = ["cause", "year", "percent"]
lifeQuality = lifeQuality[lifeQuality["percent"].notna()]
# ---------------- Education data -------------#
eduData = education[education.data == "% of global population"]
eduData = eduData.drop(["data", "metric", "10 year change"], axis=1)
eduData = eduData.melt(id_vars=["cause"])
eduData.columns = ["literacy", "year", "percent"]
eduData = eduData[eduData["percent"].notna()]
# ---------------- Climate data -------------#
sustain_climate = sustainability[sustainability.data == "planet"]
sustain_climate = sustain_climate.drop(["data", "metric", "10 year change"], axis=1)
sustain_climate = sustain_climate.melt(id_vars=["cause"])
sustain_climate.columns = ["type", "year", "percent"]
sustain_climate = sustain_climate[sustain_climate["percent"].notna()]
# ---------------- economics data -------------#
ecodata = economics[economics.data == "GDP amount per capita"]
ecodata = ecodata.drop(["data", "metric", "10 year change"], axis=1)
ecodata = ecodata.melt(id_vars=["cause"])
ecodata.columns = ["index", "year", "amount"]
ecodata = ecodata[ecodata["amount"].notna()]
# ---------------- Health-happiness capita data -------------#
health_exp = health[health.data == "current expenditure per capita"]
health_exp = health_exp.drop(["data", "metric", "10 year change"], axis=1)
health_exp = health_exp.melt(id_vars=["cause"])
health_exp.columns = ["healthTitle", "year", "health_expense"]
happiness = quality[quality.cause == "Happy Planet Index"]
happiness = happiness.drop(["data", "metric", "10 year change"], axis=1)
happiness = happiness.melt(id_vars=["cause"])
happiness.columns = ["hapTitle", "year", "happiness_index"]
ecodata02 = economics[economics.cause == "Economic Growth"]
ecodata02 = ecodata02.drop(["data", "metric", "10 year change"], axis=1)
ecodata02 = ecodata02.melt(id_vars=["cause"])
ecodata02.columns = ["economic growth", "year", "growth amount"]
data01 = pd.merge(pd.merge(health_exp, happiness, on="year"), ecodata02, on="year")
data01.drop(["healthTitle", "hapTitle", "economic growth"], axis=1, inplace=True)
# ---------------- Education girls and boys data -------------#
edu01 = education[
    (education["cause"] == "Boys Not in Primary School")
    | (education["cause"] == "Girls Not in Primary School")
    | (education["cause"] == "Children Not in Primary School")
]
edu01 = edu01.groupby(["cause"], as_index=False)[years].mean()
edu01 = pd.melt(edu01, id_vars=["cause"], var_name="year", value_name="Rate")
# print(edu01.head())
# ---------------- Sustainability data -------------#
sustain01 = sustainability.drop(["data", "metric", "10 year change"], axis=1)
sustain01 = sustain01.to_dict("records")
data_columns = list(sustain01[0].keys())
data_values = list(i[j] for j in data_columns for i in sustain01)
data_values = np.reshape(data_values, (-1, len(sustain01)))

line_options = [deaths, energy, lifeQuality, eduData, sustain_climate, ecodata]


def get_info(categoryId, optionName):
    data = pd.read_excel("https://github.com/mroqa/wgs2023/blob/master/assets/Alldata.xlsx", sheets[categoryId])
    data = data[data.cause == optionName]
    data = data[data.data != "as % of global electricity production"]
    data = data[data.data != "deaths"]
    return data


radio_cat = dbc.RadioItems(
    id="category",
    className="radio",
    options=[
        dict(label="GLOBAL HEALTH", value=0),
        dict(label="ENERGY", value=1),
        dict(label="QUALITY OF LIFE", value=2),
        dict(label="EDUCATION", value=3),
        dict(label="SUSTAINABILITY", value=4),
        dict(label="ECONOMICS", value=5),
    ],
    value=0,
    inline=True,
)

drop_map = dcc.Dropdown(
    id="drop_map",
    clearable=False,
    searchable=False,
    style={"margin": "4px", "box-shadow": "0px 0px #ebb36a", "border-color": "#ebb36a"},
)
# ---------------------------------------- Start the layout here-------------------------------------#
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [dbc.CardImg(src="/assets/WGS-logo-transparency.png")],
                            className="logo",
                        ),
                    ],
                    width=3,
                ),
                dbc.Col(
                    [
                        html.H2(
                            "What Just Happened in The World: A Decade in Review",
                            className="text-center",
                        ),
                    ],
                    width=9,
                ),
            ],
            className="header",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.I(className="fas fa-exclamation-circle"),
                                html.Label(
                                    "Choose a Main Topic", style={"margin": "20px"}
                                ),
                                radio_cat,
                            ]
                        )
                    ],
                    style={"padding-bottom": "15px"},
                )
            ],
            className="box",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.I(className="fas fa-line-chart"),
                                html.Label(id="title_line", style={"margin": "10px"}),
                                dcc.Graph(id="line-fig"),
                            ],
                            className="box",
                            style={"padding-bottom": "15px"},
                        ),
                    ],
                    style={"width": "50%"},
                ),
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.I(className="fas fa-exclamation-circle"),
                                        html.Label(
                                            id="choose_type", style={"margin": "10px"}
                                        ),
                                        drop_map,
                                    ],
                                    className="box",
                                    style={"padding-bottom": "15px"},
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Label(
                                                    id="info-title",
                                                    style={"margin": "10px"},
                                                ),
                                                html.Br(),
                                                html.Div(
                                                    [
                                                        html.Div(
                                                            [html.P(id="info-comment")],
                                                            className="box_info",
                                                        )
                                                    ]
                                                ),
                                            ],
                                            className="box",
                                            style={"padding-bottom": "15px"},
                                        )
                                    ]
                                ),
                            ]
                        )
                    ],
                    style={"width": "50%"},
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.I(className="fas fa-bell"),
                                html.Label(
                                    id="scatter-title", style={"margin": "10px"}
                                ),
                                dcc.Graph(id="scatter-fig"),
                            ],
                            className="box",
                            style={"padding-bottom": "15px"},
                        )
                    ],
                    style={"width": "50%"},
                ),
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.I(className="fas fa-bar-chart"),
                                html.Label(id="bar-title", style={"margin": "10px"}),
                                dcc.Graph(id="bar-fig"),
                                html.Br(),
                            ],
                            className="box",
                            style={"padding-bottom": "15px"},
                        ),
                    ],
                    style={"width": "50%"},
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.I(className="fas fa-table"),
                                html.Label(id="table-title", style={"margin": "10px"}),
                                dcc.Graph(id="table_fig"),
                            ],
                            className="box",
                            style={"padding-bottom": "15px"},
                        )
                    ],
                    style={"width": "90%"},
                ),
            ]
        ),
        # -----------------------------------Footer--------------------------------#
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Br(),
                                        html.P(
                                            [
                                                "Made with ",
                                                html.I(className="fas fa-heart"),
                                                " by ",
                                                html.A(
                                                    "Mohammed Roqa",
                                                    href="https://www.linkedin.com/in/mroqa/",
                                                    target="_blank",
                                                ),
                                            ],
                                            style={
                                                "font-size": "14px",
                                                "text-align": "center",
                                            },
                                        ),
                                    ],
                                    style={"width": "50%"},
                                ),
                                html.Div(
                                    [
                                        html.Br(),
                                        html.P(
                                            [
                                                "Sources ",
                                                html.Br(),
                                                html.A(
                                                    "Our World in Data",
                                                    href="https://ourworldindata.org/",
                                                    target="_blank",
                                                ),
                                                " - ",
                                                html.A(
                                                    "World Government Summit",
                                                    href="https://www.worldgovernmentsummit.org/home",
                                                    target="_blank",
                                                ),
                                            ],
                                            style={
                                                "font-size": "12px",
                                                "text-align": "center",
                                            },
                                        ),
                                    ],
                                    style={"width": "47%"},
                                ),
                            ],
                            className="footer",
                            style={"display": "flex"},
                        ),
                    ]
                )
            ]
        ),
    ],
    fluid=True,
    className="main",
)


### End of the layout here ###

# ------------------------------------------------------ Callbacks ------------------------------------------------------
#
@app.callback(
    [
        Output("title_line", "children"),
        Output("line-fig", "figure"),
        Output("drop_map", "options"),
        Output("drop_map", "value"),
        Output("choose_type", "children"),
    ],
    Input("category", "value"),
)
def line_chart(category_select):
    ################## Category Plot ##################
    # global line_fig, comment, options_return, type_chosen

    df = line_options[category_select]

    if category_select == 0:
        title = "Total Deaths per year by a disease"
        fig_line = px.line(
            data_frame=df,
            x=df["year"],
            y=df["deaths"],
            color="disease",
            template="ggplot2",
            labels={
                "deaths": "Number of people died",
                "year": "Year",
                "disease": "Disease",
            },
            markers=True,
        )
        fig_line.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="right", x=1)
        )

    elif category_select == 1:
        title = "Total % of global electricity produced by each source"
        fig_line = px.line(
            data_frame=df,
            x=df["year"],
            y=df["production"],
            color="source",
            template="ggplot2",
            labels={"production": "% of Global Electricity Production", "year": "Year"},
            markers=True,
        )
        fig_line.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="right", x=1)
        )
    elif category_select == 2:
        title = "Total % of life qualities in the last 10 years"
        fig_line = px.line(
            data_frame=df,
            x=df["year"],
            y=df["percent"],
            color="cause",
            template="ggplot2",
            labels={"cause": "Facility", "year": "Year", "percent": "Total %"},
            markers=True,
        )
        fig_line.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="right", x=1)
        )
    elif category_select == 3:
        title = "Total global literacy in the last 10 years"
        fig_line = px.line(
            data_frame=df,
            x=df["year"],
            y=df["percent"],
            color="literacy",
            labels={
                "literacy": "Literacy",
                "year": "Year",
                "percent": "% Total Literacy",
            },
            markers=True,
        )
        fig_line.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="right", x=1)
        )
    elif category_select == 4:
        title = "Total sustainability and climate change over the last 10 years"
        fig_line = px.line(
            data_frame=df,
            x=df["year"],
            y=df["percent"],
            color="type",
            labels={"type": "Action", "year": "Year", "percent": "Total % Change"},
            markers=True,
        )
        fig_line.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="right", x=1)
        )
    else:
        title = "The world GDP per capita change in the last 10 years"
        fig_line = px.line(
            data_frame=df,
            x=df["year"],
            y=df["amount"],
            color="index",
            labels={"amount": "$ Change", "year": "Year"},
            markers=True,
        )
        fig_line.update_layout(
            legend=dict(orientation="h", yanchor="bottom", y=1.1, xanchor="right", x=1)
        )
    # ----------------------------------- Dropdown Bar -------------------------------------#
    if category_select == 0:
        options_return = options_health
        type_chosen = "Choose a health problem"
    elif category_select == 1:
        options_return = options_energy
        type_chosen = "Choose an energy source"
    elif category_select == 2:
        options_return = options_quality
        type_chosen = "Choose quality of life option:"
    elif category_select == 3:
        options_return = options_edu
        type_chosen = "Choose education option:"
    elif category_select == 4:
        options_return = options_sustain
        type_chosen = "Choose climate and sustainability option:"
    else:
        options_return = options_eco
        type_chosen = "Choose economics option:"
    return (
        title,
        fig_line,
        options_return,
        options_return[0]["value"],
        type_chosen,
    )
# ------------------------ Callback for bar figure --------------------------------------#
@app.callback(
    [
        Output("bar-title", "children"),
        Output("bar-fig", "figure"),
        Output("info-title", "children"),
        Output("info-comment", "children"),
    ],
    [Input("drop_map", "value"), Input("category", "value")],
)
def update_map(dropdown_value, categoryId):
    ################## incidence datset ##################
    fact_title = "Some facts about " + dropdown_value
    record = get_info(categoryId, dropdown_value)

    if categoryId == 0:
        dict = record.to_dict(orient="list")
        if "".join(map(str, dict["cause"])) == "Health Expenditure":
            info = [
                html.Br(),
                html.I(className="fas fa-lightbulb"),
                " Did you know that:",
                html.Br(),
                html.Hr(),
                "".join(map(str, dict["cause"]))
                + " was "
                + "".join(map(str, dict["2009"]))
                + " in 2009 and "
                + "".join(map(str, dict["2021"]))
                + " in 2021 "
                + "".join(map(str, dict["metric"]))
                + " ",
                html.Br(),
                html.Br(),
                "".join(map(str, dict["cause"]))
                + " has been changed in 10 years to "
                + "".join(map(str, dict["10 year change"])),
                html.Br(),
                html.Br(),
            ]
        elif "".join(map(str, dict["data"])) == "incidence":
            info = [
                html.Br(),
                html.I(className="fas fa-lightbulb"),
                " Did you know that:",
                html.Br(),
                html.Hr(),
                "".join(map(str, dict["cause"]))
                + " has "
                + "".join(map(str, dict["2009"]))
                + " incidents in 2009 and "
                + "".join(map(str, dict["2021"]))
                + " in 2021 "
                + "".join(map(str, dict["metric"]))
                + " ",
                html.Br(),
                html.Br(),
                "".join(map(str, dict["cause"]))
                + " has been changed in 10 years to "
                + "".join(map(str, dict["10 year change"])),
                html.Br(),
                html.Br(),
            ]
        else:
            info = "Sorry! no data available in this section"
    elif categoryId == 1:
        record = record.head(1)
        dict = record.to_dict(orient="list")
        info = [
            html.Br(),
            html.I(className="fas fa-lightbulb"),
            " Did you know that:",
            html.Br(),
            html.Hr(),
            "".join(map(str, dict["cause"]))
            + " has a "
            + "".join(map(str, dict["data"]))
            + " of "
            + "".join(map(str, dict["2009"]))
            + "".join(map(str, dict["metric"]))
            + " in 2009 and "
            + "".join(map(str, dict["2021"]))
            + "".join(map(str, dict["metric"]))
            + " in 2021",
            html.Br(),
            html.Br(),
            "".join(map(str, dict["cause"]))
            + " has been changed in 10 years to "
            + "".join(map(str, dict["10 year change"])),
            html.Br(),
            html.Br(),
        ]
    elif categoryId == 2:
        record = record.head(1)
        dict = record.to_dict(orient="list")
        info = [
            html.Br(),
            html.I(className="fas fa-lightbulb"),
            " Did you know that:",
            html.Br(),
            html.Hr(),
            "".join(map(str, dict["cause"]))
            + " has a "
            + "".join(map(str, dict["data"]))
            + " of "
            + "".join(map(str, dict["2009"]))
            + "".join(map(str, dict["metric"]))
            + " in 2009 and "
            + "".join(map(str, dict["2021"]))
            + "".join(map(str, dict["metric"]))
            + " in 2021",
            html.Br(),
            html.Br(),
            "".join(map(str, dict["cause"]))
            + " has been changed in 10 years to "
            + "".join(map(str, dict["10 year change"])),
            html.Br(),
            html.Br(),
        ]
    elif categoryId == 3:
        record = record.head(1)
        dict = record.to_dict(orient="list")
        info = [
            html.Br(),
            html.I(className="fas fa-lightbulb"),
            " Did you know that:",
            html.Br(),
            html.Hr(),
            "".join(map(str, dict["cause"]))
            + " has a "
            + "".join(map(str, dict["data"]))
            + " of "
            + "".join(map(str, dict["2009"]))
            + "".join(map(str, dict["metric"]))
            + " in 2009 and "
            + "".join(map(str, dict["2021"]))
            + "".join(map(str, dict["metric"]))
            + " in 2021",
            html.Br(),
            html.Br(),
            "".join(map(str, dict["cause"]))
            + " has been changed in 10 years to "
            + "".join(map(str, dict["10 year change"])),
            html.Br(),
            html.Br(),
        ]
    elif categoryId == 4:
        record = record.head(1)
        dict = record.to_dict(orient="list")
        info = [
            html.Br(),
            html.I(className="fas fa-lightbulb"),
            " Did you know that:",
            html.Br(),
            html.Hr(),
            "".join(map(str, dict["cause"]))
            + " has a "
            + "".join(map(str, dict["data"]))
            + " of "
            + "".join(map(str, dict["2009"]))
            + "".join(map(str, dict["metric"]))
            + " in 2009 and "
            + "".join(map(str, dict["2021"]))
            + "".join(map(str, dict["metric"]))
            + " in 2021",
            html.Br(),
            html.Br(),
            "".join(map(str, dict["cause"]))
            + " has been changed in 10 years to "
            + "".join(map(str, dict["10 year change"])),
            html.Br(),
            html.Br(),
        ]
    elif categoryId == 5:
        record = record.head(1)
        dict = record.to_dict(orient="list")
        info = [
            html.Br(),
            html.I(className="fas fa-lightbulb"),
            " Did you know that:",
            html.Br(),
            html.Hr(),
            "".join(map(str, dict["cause"]))
            + " has a "
            + "".join(map(str, dict["data"]))
            + " of "
            + "".join(map(str, dict["2009"]))
            + "".join(map(str, dict["metric"]))
            + " in 2009 and "
            + "".join(map(str, dict["2021"]))
            + "".join(map(str, dict["metric"]))
            + " in 2021",
            html.Br(),
            html.Br(),
            "".join(map(str, dict["cause"]))
            + " has been changed in 10 years to "
            + "".join(map(str, dict["10 year change"])),
            html.Br(),
            html.Br(),
        ]
    else:
        info = "Data is not available, please try again later."

    title = "This graph shows health expedenture per capita, happiness and economic growth relationship"
    ################## Bar Plot ##################
    fig_bar = px.bar(
        data01,
        x="year",
        y="health_expense",
        hover_data=["happiness_index", "growth amount"],
        color="growth amount",
        opacity=0.9,
        labels={
            "health_expense": "Health Expedentre per Capita",
            "growth amount": "Economic Growth",
        },
        height=400,
        color_continuous_scale=px.colors.sequential.Cividis_r,
    )
    # px.colors.sequential.Viridis
    # px.colors.diverging.BrBG
    return (
        title,
        fig_bar,
        fact_title,
        info,
    )


# ------------------------ Callback for bar figure --------------------------------------#
@app.callback(
    [
        Output("scatter-title", "children"),
        Output("scatter-fig", "figure"),
        Output("table_fig", "figure"),
        Output("table-title", "children"),
    ],
    [Input("category", "value")],
)
def scatter_plot(catId):
    ################## incidence datset ##################
    title = "This Animated graph shows movement Gap in Primary School"
    # print(catId)
    table_title = "The table shows sustainability and climate data in a decade"

    ################## Scatter Plot ##################
    fig_scatter = px.scatter(
        edu01,
        x="Rate",
        y="cause",
        color="cause",
        animation_frame="year",
        title="Gender Gap in primary school",
        range_x=[0, 12],
        labels={"Rate": "% of Gender of Primary School Age", "cause": "Gender"},
        template="ggplot2",
    )
    fig_scatter.update_layout(
        title={"x": 0.5, "xanchor": "center", "font": {"size": 14}},
        xaxis=dict(title=dict(font=dict(size=14))),
        yaxis={"title": {"text": None}},
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1),
    )
    fig_scatter.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1500
    fig_scatter.layout.updatemenus[0].buttons[0].args[1]["transition"][
        "duration"
    ] = 1500
    fig_scatter.data[0].name = "School Boys"
    fig_scatter.data[1].name = "School Children"
    fig_scatter.data[2].name = "School Girls"
    fig_scatter.data[0]["marker"].update(size=18)
    fig_scatter.data[1]["marker"].update(size=18)
    fig_scatter.data[2]["marker"].update(size=18)
    fig_scatter.data[0]["marker"].update(color="#F4D03F")
    fig_scatter.data[1]["marker"].update(color="#34495E")
    fig_scatter.data[2]["marker"].update(color="rgb(66, 165, 245)")

    for x in fig_scatter.frames:
        x.data[0]["marker"]["color"] = "#F4D03F"
        x.data[1]["marker"]["color"] = "#34495E"
        x.data[2]["marker"]["color"] = "rgb(66, 165, 245)"

    return (
        title,
        fig_scatter,
        go.Figure(
            data=[
                go.Table(
                    header=dict(
                        values=data_columns,
                        fill_color="rgb(239, 243, 255)",
                        line_color="rgb(239, 243, 255)",
                        align="left",
                    ),
                    cells=dict(
                        values=data_values,
                        fill_color=[
                            "rgb(239, 243, 255)",
                            "rgb(187, 222, 251)",
                            "rgb(144, 202, 249)",
                            "rgb(100, 181, 246)",
                            "rgb(66, 165, 245)",
                            "rgb(33, 150, 243)",
                            "rgb(30, 136, 229)",
                            "rgb(25, 118, 210)",
                            "rgb(30, 136, 229)",
                            "rgb(33, 150, 243)",
                            "rgb(66, 165, 245)",
                            "rgb(100, 181, 246)",
                            "rgb(144, 202, 249)",
                            "rgb(187, 222, 251)",
                        ],
                        line_color=[
                            "rgb(239, 243, 255)",
                            "rgb(187, 222, 251)",
                            "rgb(144, 202, 249)",
                            "rgb(100, 181, 246)",
                            "rgb(66, 165, 245)",
                            "rgb(33, 150, 243)",
                            "rgb(30, 136, 229)",
                            "rgb(25, 118, 210)",
                            "rgb(30, 136, 229)",
                            "rgb(33, 150, 243)",
                            "rgb(66, 165, 245)",
                            "rgb(100, 181, 246)",
                            "rgb(144, 202, 249)",
                            "rgb(187, 222, 251)",
                        ],
                        align="left",
                    ),
                )
            ]
        ),
        table_title,
    )


if __name__ == '__main__':
    app.run_server(debug=True)
