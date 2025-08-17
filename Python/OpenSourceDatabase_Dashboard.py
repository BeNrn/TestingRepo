# -*- coding: utf-8 -*-
"""
Purpose:    Script for an open source database.
Created:    25.07.2025
Author:     BeNrn
Updated:    17.08.2025
"""
#https://realpython.com/python-dash/#style-your-dash-application
#https://dash.plotly.com/dash-core-components/tabs (for the tabs)
#https://dash.plotly.com/basic-callbacks for callbacks like INPUT, OUTPUT and STATE
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
#   [x] delete data by id
#   [-] add column #TODO: Not yet implemented
#   [-] remove column #TODO: Not yet implemented

#load libs
import pandas as pd
import os

from dash import Dash, Input, Output, dcc, html, dash_table, callback, ALL
#from dash.exceptions import PreventUpdate

#load paths
user_name = os.getlogin()
os.chdir(r"C:\Users\{}\Documents\Freizeit\Geschenke\2025_Toms_Pflanzendatenbank".format(user_name))
base_path = r"C:\Users\{}\Documents\Freizeit\Geschenke\2025_Toms_Pflanzendatenbank".format(user_name)
database_path = os.path.join(base_path, "openDB.csv")
    
    
def loadTable(database_path):
    """
    Load the table from CSV from disk.
    """
    #load the data
    db_df = pd.read_csv(database_path, sep = ";", dtype = {"Bild_ID" : "str"}, index_col=[0])

    #laod matching images (image name starts with Bild_ID)
    image_list = os.listdir(os.path.join(base_path, "assets"))

    image_name_list = []
    for bild_id in db_df["Bild_ID"]:
        matching_image_list = [i for i in image_list if i.startswith(str(bild_id) + "_")]
        if len(matching_image_list) == 1:
            image_name_list = image_name_list + [[i for i in image_list if i.startswith(str(bild_id) + "_")][0]]
        else:
            image_name_list = image_name_list + [None]

    #to string        
    #image_name_list = [f"{i}" for i in image_name_list]
    image_name_list = [f'<img src="/assets/{i}" height="60">' if i is not None else None for i in image_name_list]

    db_df["Bild_Name"] = image_name_list

    list_of_dict = db_df.to_dict('records')
    for index, element in enumerate(list_of_dict):
        element["ID"] = db_df.index[index]

    return db_df, list_of_dict


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
    html.H1(children="PlantDB"),
    #introduce tabs
    dcc.Tabs(id = "tabs", value = "tab_table", children=[
        dcc.Tab(label="Tabelle", value = "tab_table"),
        dcc.Tab(label="Datenänderung", value = "tab_datainput"),
        ]),
        html.Div(id="database"),
        html.Div(id="content")
    ])

#controls the tabs, based on user input
@callback(
        Output("database", 'children'),
        Input('tabs', 'value'))

def render_content(tab):
    """
    Create the layout.

    Parameters
    ----------
    tab : string
        The tab, the user clicks on.

    Returns
    -------
    None.

    """
    #freshly load the data
    db_df, list_of_dict = loadTable(database_path = database_path)
    
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
                id = "datatable",
                data = list_of_dict,
                #add id column manually
                columns = [{'name': 'ID', 'id': 'ID', 'presentation': 'markdown'}] + [{'name': col, 'id': col, 'presentation': 'markdown'} for col in db_df.columns],
                filter_action = 'native',
                style_table = {'overflowX': 'auto'},
                style_cell = {'textAlign': 'left'},
                style_data={'whiteSpace': 'normal', 'height': 'auto'},
                markdown_options={'html': True}
            )
        ])
    #tab 2
    elif tab == 'tab_datainput':
        return html.Div([
            #data row input GUI
            #-------------------
            html.H3("Zeile hinzufügen"),
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
            html.Button('Zeile hinzufügen', id = "save_button", n_clicks=0),
            html.Div(id='output1'),
            
            #row deletion GUI
            #----------------
            html.H3("Zeile löschen"),
            html.P("Bitte die ID der Zeile eingeben, die gelöscht werden soll."),
            dcc.Input(id = "row_deletion_id", type = "text", placeholder = "Zeilen ID", value = None),
            #about buttons: https://dash.plotly.com/dash-html-components/button
            html.Button('Zeile entfernen', id = 'save_button_row_deletion', n_clicks=0),
            html.Div(id = 'output2')
            
            # #column add GUI
            # #---------------
            # html.H3("Spalte hinzufügen"),
            # html.P("Bitte den neu hinzuzufügenden Feldnamen angeben."),
            # dcc.Input(id = "column_addition_id", type = "text", placeholder = "Spaltenname", value = None),
            # html.Div(id = 'output3'),
            
            # #column deletion GUI
            # #--------------------
            # html.H3("Spalte löschen"),
            # html.P("Bitte den Spaltennamen angeben, der gelöscht werden soll."),
            # dcc.Input(id = "column_deletion_id", type = "text", placeholder = "Spaltenname", value = None),
            # html.Div(id = 'output4')
            ]) 

#data row input processing
#-------------------------
@callback(
    Output('output1', 'children'),
    Output('save_button', 'n_clicks'), #reset the button, everytime it was clicked by returnin 0 as a second value, reassigning it to n_clicks
    Input({'type': 'dynamic_input', 'index': ALL}, 'value'),
    Input("save_button", 'n_clicks')
    #State('datatable', 'data'),
    )

# def display_inputs(values, n_clicks):
#     # values is a list of input values in the order of inputs generated
#     return f"You entered: {values}, {n_clicks}"

def save_data(values:list, btn1_clicks:int) -> str:
    """
    Appends the input data to the dataframe and overwrite csv.
    
    values:list
        Contains the values entered by the user in the form of [value1, value2, ...]
    btn1_clicks:int
        Number of clicks. Is None by default.
    """
    #freshly load the data
    db_df, list_of_dict = loadTable(database_path = database_path)
    
    #return f"Output 1: Bitte Daten eingeben.{values},{btn1_clicks}."
    if btn1_clicks == 0:
        return "Output 1: Bitte Daten eingeben.", 0
    #field "Bild_ID" must not be empty
    #elif btn1_clicks > 0 and values[db_df.columns.get_loc("Bild_ID")] is None:
    #    #raise PreventUpdate
    #    return 'Output 1: Das Feld "Bild_ID" darf nicht leers sein.', 0, no_update
    #at least one value must be entered
    elif btn1_clicks > 0 and values != [None for i in range(len(values))]: #and values[db_df.columns.get_loc("Bild_ID")] is not None:
        #Bild_Name input (picture name) to valid path
        values[db_df.columns.get_loc("Bild_Name")] == f'<img src="/assets/{values[db_df.columns.get_loc("Bild_Name")]}" height="60">'
        #'<img src="/assets/1_Gänseblümchen.jpg" height="60">'
        #append list at the end end and export to csv
        db_df.loc[len(db_df)] = values
        db_df.to_csv(database_path, index = "ID", sep = ";")
        return "Output 1: Zeile hinzugefügt!", 0

#data row deletion processing
#-------------------------
@app.callback(
    Output('output2', 'children'),
    Output('save_button_row_deletion', 'n_clicks'), #reset the button, everytime it was clicked by returnin 0 as a second value, reassigning it to n_clicks
    Input('row_deletion_id', 'value'),
    Input('save_button_row_deletion', 'n_clicks')
    )

def deleteRow(value:list, btn2_clicks:int) -> str:
    """
    Parameters
    ----------
    value : list
        DESCRIPTION.
    btn2_clicks : int
        DESCRIPTION.

    Returns
    -------
    str
        DESCRIPTION.
    """
    #freshly load the data
    db_df, list_of_dict = loadTable(database_path = database_path)
    
    if btn2_clicks == 0:
        return "Output 2: Bitte Zeilen-ID eingeben, die gelöscht werden soll.", 0
    elif btn2_clicks > 0 and value is None:
        return 'Output 2: Bitte eine valide Zahl eingeben.', 0
    elif btn2_clicks > 0 and not value.isdigit():
        return 'Output 2: Bitte eine valide Zahl eingeben.', 0
    elif btn2_clicks > 0 and value.isdigit():
        db_df = db_df.drop(index = int(value))
        db_df.to_csv(database_path, index = "ID", sep = ";")
        return 'Output 2: Zeile gelöscht!', 0

# #data column addition processing
# #------------------------------
# @app.callback(
#     Output('output3', 'children'),
#     Input('column_addition_id', 'value')
# )
# def columnAddition(value):
    
#     return f'Output 3: {value}'

# #data column deletion processing
# #--------------------------------
# @app.callback(
#     Output('output4', 'children'),
#     Input('column_deletion_id', 'value')
# )
# def update_output_4(value):
#     return f'Output 4: {value}'
    
#run the app
if __name__ == "__main__":
    app.run(debug=True)