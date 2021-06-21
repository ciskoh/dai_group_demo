"""
This module creates the dashboard sourcing data from assets/runner_db.db
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from pandas import DataFrame, read_sql_query
from sqlite3 import connect
import plotly.express as px
from config import config

# ----- DASH APP -----------

external_stylesheets = ['assets/stylesheet.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# server = app.server  # TODO: check this setting fror aws+docker deployment

# Define app layout
app.layout = html.Div([
    # Header
    html.H1(className='h1', children='Zurich Marathon 2014-2018 data exploration'),
    html.Div(className="h1", children='Interactive visualisation of runners participating to the Zurich marathon '),
    html.Div(children=[
        # TODO check possible output/value type
        dcc.Dropdown(id="selector1",
                     options=[{'label': f"{r[0]} to {r[1]}", 'value': f"{r[0]},{r[1]}"} for r in config.runner_groups],
                     value='0 to 100',
                     placeholder="Select age group",
                     multi=False,  # TODO: change to multiselector
                     clearable=True,
                     className='Selector'
                     ),
        dcc.Dropdown(id="selector2",
                     options=[{'label': y, 'value': y} for y in config.years],
                     value='All years',
                     placeholder="Select a year",
                     multi=False,  # TODO: change to multiselector
                     clearable=True,
                     className='Selector'
                     ), ]
    ),
    # separation line
    html.Hr(),

    # First plot

    html.Div(id="plot", children=dcc.Graph(id="fig1_c1"),
             className="pretty_container",
             style={'display': 'inline-block'}),

    # TODO: add data_table below
    html.Div(children=dcc.Graph(id="fig1_c2"),
             className="pretty_container",
             style={'display': 'inline-block'}),

    html.Aside(className=".sidebar a",
               children='Made by Matteo Jucker Riva \u00A9 for DAI Group')
])

#TODO adapt for multiple selectors
def filter_age_group(age_group=None) -> str:
    """adds age_group filter to sql_query"""

    if age_group:
        start_age = age_group.split(",")[0]
        end_age = age_group.split(",")[1]
        sel1_output = f" run_year - Age_year >= {start_age} AND run_year - Age_year <= {end_age} "
        return sel1_output

def filter_year(race_year=None) -> str:
    """adds marathon year filter to sql_query"""
    if race_year:
        sel2_output = f"run_year={race_year}"
        return sel2_output


def create_sql_query(table_name, sel1_output=None, sel2_output=None) -> str:
    """creates the sql_query"""
    sql_query = f"SELECT * from {table_name}"
    if all([sel1_output, sel2_output]):
        sql_query += f" WHERE {sel1_output} AND {sel2_output}"
    elif any([sel1_output, sel2_output]):
        sql_query += f" WHERE " + "".join([filt for filt in [sel1_output, sel2_output] if filt])
    return sql_query


def query_data(sql_query, connection) -> DataFrame:
    """sources the data from runner database returning a dataframe"""
    return read_sql_query(sql_query, connection)

def fetch_data_wrapper(sel1, sel2, db_file_path) -> DataFrame:
    """wrapper function to get data and return a dataframe"""
    conn = connect(db_file_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_name = cursor.fetchall()[0][0]

    sel1_output = filter_age_group(sel1)
    sel2_output = filter_year(sel2)

    sql_query = create_sql_query(table_name, sel1_output, sel2_output)
    return query_data(sql_query, conn)

def add_age_group(df, age_groups) -> DataFrame:
    """ adds age group column to dataframe for plotting"""
    df['age_series'] = df['run_year'].astype(int)-df['Age_year'].astype(int)

    age_groups_dict = {i: age_groups[i] for i in range(0, len(age_groups))}
    df['age_group'] = [k for i in df['age_series'] for k,v in age_groups_dict.items() if v[0]<= i <=v[1] ]
    return df

@app.callback(Output('plot', 'figure'),
              [Input('selector1', 'value'),
               Input('selector2', 'value')])
def update_plot(sel1, sel2, config=config):
    filtered_df = fetch_data_wrapper(sel1, sel2, config.db_file_path)
    df_with_age_group = add_age_group(filtered_df, config.runner_groups)

    fig = px.histogram(df_with_age_group, x="run_year", color="age_group")
    return fig

if __name__ == '__main__':
    # TODO: catch exception by creating database
    conn = connect(config.db_file_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_name = cursor.fetchall()[0][0]
    sel1_output= filter_age_group("0,100")
    sel2_output = filter_year("2015")
    sql_query = create_sql_query(table_name)

    # without pandas
    filtered_df = query_data(sql_query, conn)
    completed_df = add_age_group(filtered_df, config.runner_groups)

    # run app
    app.run_server(debug=True)