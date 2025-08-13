# -*- coding: utf-8 -*-
"""
Purpose:    Script for an open source database.
Created:    25.07.2025
Author:     BeNrn
Updated:    10.08.2025
"""
#https://realpython.com/python-dash/#style-your-dash-application
#https://dash.plotly.com/dash-core-components/tabs (for the tabs)
#start the dash Dashboard:
#   - open CMD
#   - activate python environment
#   - cd to file location of this script
#   - run > python OpenSourceDatabase_Dashboard.py
#   - open the provided URL in a browser
# 
#Functions
#   [x] Show the data table with the images
#   [x] import data (append at the bottom)
#   [-] delete data by id
#   [-] add column
#   [-] remove column

#load libs
import pandas as pd
import os

from dash import Dash, Input, Output, dcc, html, dash_table, callback, ALL

#load paths
user_name = os.getlogin()
os.chdir(r"C:\Users\{}\Documents\Freizeit\Geschenke\2025_Toms_Pflanzendatenbank".format(user_name))
base_path = r"C:\Users\{}\Documents\Freizeit\Geschenke\2025_Toms_Pflanzendatenbank".format(user_name)
database_path = os.path.join(base_path, "openDB.csv")

#load the data
db_df = pd.read_csv(database_path, sep = ";", dtype = {"Bild_ID" : "str"}, index_col=[0])

#laod matching images (image name starts with Bild_ID)
image_list = os.listdir(os.path.join(base_path, "assets"))

image_name_list = []
for bild_id in db_df["Bild_ID"]:
    image_name_list = image_name_list + [[i for i in image_list if i.startswith(str(bild_id) + "_")][0]]

image_name_list = [f"{i}" for i in image_name_list]
image_name_list = [f'<img src="/assets/{i}" height="60">' for i in image_name_list]

db_df["Bild_path"] = image_name_list

list_of_dict = db_df.to_dict('records')
for index, element in enumerate(list_of_dict):
    element["ID"] = db_df.index[index]

#start a dash instance
# suppress_callback_exceptions=True -> the line "html.Button('Speichern', id='save_button')"
# is only in the second tab, however, dash expect it to be in the initial setup
# which would lead to the creation of the save button in every tab. The option
# allows elements to not be loaded immediately
app = Dash(__name__, suppress_callback_exceptions=True)

#set the style of the webpage
#html.Div -> create a new division
app.layout = html.Div([
    #primary heading
    html.H1(children="Toms Pflanzendatenbank"),
    #introduce tabs
    dcc.Tabs(id = "tabs", value = "tab_table", children=[
        dcc.Tab(label="Tabelle", value = "tab_table"),
        dcc.Tab(label="Datenänderung", value = "tab_datainput"),
        ]),
        html.Div(id="database")
    ])

#controls the tabs, based on user input
@callback(
        Output("database", 'children'),
        Input('tabs', 'value'))

def render_content(tab):
    """
    Create the layout

    Parameters
    ----------
    tab : string
        The tab, the user clicks on.

    Returns
    -------
    None.

    """
    #tab 1
    if tab == 'tab_table':
        return html.Div([
            html.H1(children="Pflanzentabelle"),
            #add a paragraph
            html.P(
                children=(
                    "Analyze the behavior of avocado prices and the number"
                    " of avocados sold in the US between 2015 and 2018"
                ),
            ),
            #https://dash.plotly.com/datatable
            
            dash_table.DataTable( 
                data = list_of_dict,
                #add id column manually
                columns = [{'name': 'ID', 'id': 'ID', 'presentation': 'markdown'}] + [{'name': col, 'id': col, 'presentation': 'markdown'} for col in db_df.columns],
                style_table = {'overflowX': 'auto'},
                style_cell = {'textAlign': 'left'},
                style_data={'whiteSpace': 'normal', 'height': 'auto'},
                markdown_options={'html': True}
            )
        ])
    #tab 2
    elif tab == 'tab_datainput':
        return html.Div([
            #data row input
            #---------------
            html.H3("Dateneingabe"),
            html.P("Bitte die Daten eingeben, die hinzugefügt werden sollen. Die Spalte 'Bild_ID' ist ein Pflichtfeld."),
            #list comprehension for each column in the df to dynamically depict 
            # df input fields
            html.Div([
            #on inputs: https://dash.plotly.com/dash-core-components/input
            dcc.Input(id={"type" : "dynamic_input", "index" : df_col}, 
                          type = "text", 
                          placeholder = f"{df_col}",
                          value = None)
                for df_col in db_df.columns if df_col != "ID"
            ]),
            #save button
            html.Button('Speichern', id='save_button'),
            #row deletion
            #--------------
            html.H3("Zeile löschen"),
            html.P("Bitte die ID der Zeile eingeben, die gelöscht werden soll."),
            dcc.Input(id = "column_deletion_id", type = "text", placeholder = "Zeilen ID", value = None),
            #column add
            #----------
            html.H3("Spalte hinzufügen"),
            html.P("Bitte den neu hinzuzufügenden Feldnamen angeben."),
            dcc.Input(id = "column_addition_id", type = "text", placeholder = "Spaltenname", value = None),
            #column deletion
            #---------------
            html.H3("Spalte löschen"),
            html.P("Bitte den Spaltennamen angeben, der gelöscht werden soll."),
            dcc.Input(id = "column_deletion_id", type = "text", placeholder = "Spaltenname", value = None),
            
            html.Div(id = 'output')
        ]) 

#process input on the second tab
@callback(
    Output('output', 'children'),
    Input({'type': 'dynamic_input', 'index': ALL}, 'value'),
    Input('save_button', 'n_clicks')
    )

# def display_inputs(values, n_clicks):
#     # values is a list of input values in the order of inputs generated
#     return f"You entered: {values}, {n_clicks}"

def save_data(values, n_clicks):
    return "Bitte Daten eingeben."
    if n_clicks == None:
        return f"Bitte Daten eingeben.{values}"
    #field "Bild_ID" must not be empty
    elif values[db_df.columns.get_loc("Bild_ID")] is None:
        return 'Das Feld "Bild_ID" darf nicht leers sein.'
    elif values[db_df.columns.get_loc("Bild_ID")] is not None:
        #list to series and append at the end
        db_df.loc[len(db_df)] = values
        db_df.to_csv(database_path, index = "ID", sep = ";")
        return "Daten gespeichert!"
    
# @callback(
#     Output('output', 'children'),
#     Input("column_deletion_id", "value"),
#     Input("column_addition_id", "value"),
#     Input("column_deletion_id", "value"),
#     )
    
# def printData(value1, value2, value3):
#     return f"{value1}, {value2}, {value3}"

#run the app
if __name__ == "__main__":
    app.run(debug=True)