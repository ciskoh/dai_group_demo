"""
This module creates the dashboard sourcing data from assets/runner_db.db
"""

import dash
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from pandas import DataFrame, read_sql_query
from sqlite3 import connect
import plotly.express as px

from config import config
from modules import create_runner_db

# ----- DASH APP -----------

external_stylesheets = ['assets/stylesheet.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# server = app.server  # TODO: check this setting fror aws+docker deployment

# Define app layout
app.layout = html.Div([
    # Header
    html.H1(className='h1', children='Zurich Marathon 2014-2018 data exploration'),
    html.H2(className="h1", children='Interactive visualisation of runners participating to the Zurich marathon '),
    html.Div(children=[
        dcc.Dropdown(id="selector1",
                     options=[{'label': f"{r[0]} to {r[1]}", 'value': f"{r[0]} to {r[1]}"} for r in config.age_groups],
                     value='0 to 100',
                     placeholder="Select age group",
                     multi=True,
                     clearable=True,
                     className='Selector'
                     ),
        dcc.Dropdown(id="selector2",
                     options=[{'label': y, 'value': y} for y in config.years],
                     value='',
                     placeholder="Select a year",
                     multi=True,
                     clearable=True,
                     className='Selector'
                     ), ]
    ),
    # separation line
    html.Hr(),

    # First plot

    html.Div(id="plot",
             children=[
                 html.H3(className="plot_title", children="Plot of runners per race year and age group"),
                 dcc.Graph(id="fig1")],
             className="pretty_container"),

    html.Div(children=[html.H3(className="plot_title", children="Table of runners data"),
                       dt.DataTable(id="fig2", columns=[{"name": i, "id": i, 'presentation': 'markdown'} for i in config.field_names])],
             className="pretty_container"
             ),
    html.Hr(),
    html.Aside(className=".sidebar a",
               children='Made by Matteo Jucker Riva \u00A9 for DAI Group')
])

# ----- FUNCTIONS-----

def filter_age_group(age_groups=None) -> str:
    """adds age_group filter to sql_query"""
    if isinstance(age_groups, list) and (any(age_groups)):
        sel1_output = ""
        for age_group in age_groups:
            start_age, end_age = age_group.split(" to ")
            sel1_output += f" Run_year - Age_year BETWEEN {start_age} AND {end_age} OR"
        return sel1_output[:-3]  # removes final or


def filter_year(race_year=None) -> str:
    """adds marathon year filter to sql_query"""
    if race_year:
        if not isinstance(race_year, list):
            race_year = [race_year]
        sel2_output = f"Run_year IN ({', '.join([str(ry) for ry in race_year])})"
        return sel2_output


def create_sql_query(table_name, sel1_output=None, sel2_output=None) -> str:
    """creates the sql_query"""
    sql_query = f"SELECT * from {table_name}"
    if all([sel1_output, sel2_output]):
        sql_query += f" WHERE ({sel1_output}) AND ({sel2_output})"
    elif any([sel1_output, sel2_output]):
        sql_query += f" WHERE " + "".join([filt for filt in [sel1_output, sel2_output] if filt])
    return sql_query


def query_data(sql_query, connection) -> DataFrame:
    """sources the data from runner database returning a dataframe"""
    return read_sql_query(sql_query, connection)


def fetch_data_wrapper(sel1, sel2, db_file_path) -> DataFrame:
    """wrapper function gets data and returns a dataframe"""
    try:
        conn = connect(db_file_path)
    except ConnectionError:
        create_runner_db(config)
    finally:
        conn = connect(db_file_path)

    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_name = cursor.fetchone()[0]
    sel1_output = filter_age_group(sel1)
    sel2_output = filter_year(sel2)

    sql_query = create_sql_query(table_name, sel1_output, sel2_output)
    return query_data(sql_query, conn)


def add_age_group(df, age_groups) -> DataFrame:
    """ adds age group column to dataframe for plotting"""
    df['age_series'] = df['Run_year'].astype(int) - df['Age_year'].astype(int)

    age_groups_dict = {i: age_groups[i] for i in range(0, len(age_groups))}
    df['age_group'] = [f"{v[0]} to {v[1]}" for i in df['age_series'] for v in age_groups_dict.values() if
                       v[0] <= i <= v[1]]
    return df

# CALLBACKS
@app.callback(Output("fig1", 'figure'),
              [Input('selector1', 'value'),
               Input('selector2', 'value')])
def update_plot(sel1, sel2, config=config):
    filtered_df = fetch_data_wrapper(sel1, sel2, config.db_file_path)
    # filtered_df['Run_year']=filtered_df['Run_year']
    df_with_age_group = add_age_group(filtered_df, config.age_groups)
    fig = px.histogram(df_with_age_group,
                       x="Run_year",
                       color="age_group",
                       category_orders={"age_group": [f"{v[0]} to {v[1]}" for v in config.age_groups]},
                       range_x=[min(config.years), max(config.years)]
                       )
    fig.update_layout(xaxis = dict(
        tickmode = 'linear',
        dtick = 1
    ))
    return fig


def display_links(df):
    """makes links clickable in the data table"""
    links = df['Run_link'].to_list()
    rows = []
    for x in links:
        link = '[' + x + '](' + str(x) + ')'
        rows.append(link)
    return rows


@app.callback(Output("fig2", 'data'),
              [Input('selector1', 'value'),
               Input('selector2', 'value')])
def update_data_table(sel1, sel2, config=config):
    filtered_df = fetch_data_wrapper(sel1, sel2, config.db_file_path)
    df_with_age_group = add_age_group(filtered_df, config.age_groups)
    df_with_age_group['Run_link'] = display_links(df_with_age_group)
    return df_with_age_group.to_dict('records')


if __name__ == '__main__':

    # run app
    (app.run_server(host='0.0.0.0', port=8050, debug=True))

