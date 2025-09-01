# -*- coding: utf-8 -*-
"""
Purpose:    Script for an open source database.
Created:    25.07.2025
Author:     BeNrn
Updated:    20.08.2025
"""
#Sources
#-------
#https://realpython.com/python-dash/#style-your-dash-application
#https://dash.plotly.com/dash-core-components/tabs (for the tabs)
#https://dash.plotly.com/basic-callbacks for callbacks like INPUT, OUTPUT and STATE
#https://www.w3schools.com/css/css_comments.asp about CSS components
# The font is from: https://fonts.google.com/specimen/Mozilla+Headline

#How to start
#-------------
#start the dash Dashboard:
#   - open CMD
#   - activate python environment
#   - cd to file location of this script
#   - run > python OpenSourceDatabase_Dashboard.py
#   - open the provided URL in a browser

#Functionalities
#----------------
#   [x] Show the data table with the images
#   [x] import data (append at the bottom)
#   [x] delete data by id
#   [-] add column #TODO: Not yet implemented
#   [-] remove column #TODO: Not yet implemented

#load libs
#---------
import pandas as pd
import os
from dash import Dash, Input, Output, dcc, html, dash_table, callback, ALL

#load paths
#-----------
base_path = os.path.dirname(__file__)
database_path = os.path.join(base_path, "openDB.csv")
    
def loadTable(database_path):
    """
    Load the table from CSV from disk.

    database_path -- string
        Path to the csv file
    Returns: the loaded pandas df, a dict of the dataframe in a list with added column id
    """
    #load the data
    db_df = pd.read_csv(database_path, sep = ";", na_values = "None", index_col=[0])

    #load matching images, if no image is provided return None 
    image_html_list = [i if str(i) != "nan" else None for i in list(db_df["Bild_Name"])]
    
    #for depiction in table (nan -> None, rest stays the same)
    db_df["Bild_Name"] = image_html_list

    #provide df as dict for dash table input
    list_of_dict_db = db_df.to_dict("records")
    for index, element in enumerate(list_of_dict_db):
        element["Zeilennummer"] = db_df.index[index]

    return db_df, list_of_dict_db


#define a style sheet (text style)
#----------------------------------
#source: https://fonts.google.com/specimen/Mozilla+Headline
external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?family=Mozilla+Headline:wght@200..700&display=swap"
        ),
        "rel": "stylesheet",
    },
]
#start a dash instance
#-----------------------
# suppress_callback_exceptions = True -> the line "html.Button("Speichern", id = "save_button")"
# is only in the second tab, however, dash expect it to be in the initial setup
# which would lead to the creation of the save button in every tab. The option
# allows elements to not be loaded immediately
app = Dash(__name__, suppress_callback_exceptions = True, external_stylesheets = external_stylesheets)

#Title appears in the browser tab
app.title = "PlantDB"

#set the basic strucutre of the webpage
#---------------------------------------
#html.Div -> create a new division
app.layout = html.Div([
    html.Div(className = "header", children = [
        #primary heading
        html.H1(children = "🌿 PlantDB", className = "header-title", style = {'font-family': 'Mozilla Headline, sans-serif'}),
        html.Div([
            #add a paragraph
            html.P(children = ("Open Source Pflanzen-Datenbank"), className = "text-center", style = {'font-family': 'Mozilla Headline, sans-serif'}),
            html.A("📃 Anleitung", href="/assets/Anleitung_PlantDB.pdf", target="_blank", className = "text-right", style = {'font-family': 'Mozilla Headline, sans-serif', 'color': 'rgb(100, 154, 117)'})
        ], className = "column"),
        html.Div([
            #keep the center empty
            html.P("", className = "text-center"),
            html.P("Created by Benno 2025", className = "text-right", style = {'font-family': 'Mozilla Headline, sans-serif', 'margin-top': '10px', 'color': 'rgb(100, 154, 117)'})
        ], className = "column")
    ]),
    #introduce tabs
    html.Div(className = "sub-header1", children = [
        dcc.Tabs(id = "tabs", value = "tab_table", children = [
            dcc.Tab(label="Tabelle", value = "tab_table", className="tab-style", selected_className = "selected-tab-style", style = {'font-family': 'Mozilla Headline, sans-serif'}), #color can not be changed here, overwritte by CSS
            dcc.Tab(label="Datenänderung", value = "tab_datainput", className="tab-style", selected_className = "selected-tab-style", style = {'font-family': 'Mozilla Headline, sans-serif'}), #color can not be changed here, overwritte by CSS
        ]),
        html.Div(id = "database"),
        html.Div(id = "content")
    ])])

#controls the tabs, based on user input
@callback(
        Output("database", "children"),
        Input("tabs", "value"))

#returns the content based on the selected tabs
def render_content(tab):
    """
    Create the layout.

    tab : string
        The tab, the user clicks on.
    Returns: None.
    """
    #freshly load the data
    db_df, list_of_dict_db = loadTable(database_path = database_path)
    
    #tab 1
    if tab == "tab_table":
        return html.Div([
                    html.Div([
                        html.H1(children = "Datenübersicht und Filterung", style = {'font-family': 'Mozilla Headline, sans-serif', 'color': 'rgb(100, 154, 117)'})
                    ], className = "sub-header2"),
                    html.Div([
                        #https://dash.plotly.com/datatable
                        #https://dash.plotly.com/datatable/style
                        dash_table.DataTable( 
                            id = "datatable",
                            data = list_of_dict_db,
                            #add id column manually
                            style_header = {'fontWeight': 'bold', 'backgroundColor': 'rgb(58, 88, 67)','color': 'rgb(236, 236, 232)', "textAlign": "center", "fontSize": "18px"},
                            columns = [{"name": "Zeilennummer", "id": "Zeilennummer", "presentation": "markdown"}] + [{"name": col, "id": col, "presentation": "markdown"} for col in db_df.columns],
                            fixed_rows = {'headers': True, "data": 0}, #fixate header row
                            #one column different from the others
                            #style_data_conditional=[{
                            #    "if": {"column_id": "Zeilennummer"},   # 3. Zeile (Index 2)
                            #    "fontSize": "10px",
                            #    "padding": "2px 5px", #oben, rechts, unten, links
                            #    "height": "50px",
                            #    "textAlign": "center"
                            #}],
                            style_cell = {"minHeight": "30px", "height": "auto", "lineHeight": "15px", "textAlign": "center", 'verticalAlign': 'middle', 'backgroundColor': 'rgb(34, 37, 34)', 'color': 'rgb(236, 236, 232)'},
                            filter_action = "native",
                            style_table = {"overflowX": "scroll", 'heigth' : '90vh', 'maxHeight': '90vh', 'display': 'auto'},
                            style_data = {"whiteSpace": "normal", "height": "auto"},
                            style_cell_conditional=[{'if': {'column_id': "Zeilennummer"}, 'width': '130px'}], #first column is smaller (for some reasons)
                            #table should fill full screen
                            css = [{"selector": "table", "rule": "width: 100%;"},{"selector": ".dash-spreadsheet.dash-freeze-top, .dash-spreadsheet .dash-virtualized", "rule": "max-height: 1000px;"}],
                            markdown_options = {"html": True}
                        )
                    ], className = "sub-header1")
        ])
    #tab 2
    elif tab == "tab_datainput":
        return html.Div([
                    html.Div([
                        html.H1(children = "Zeilen anfügen oder löschen", style = {'font-family': 'Mozilla Headline, sans-serif', 'color': 'rgb(100, 154, 117)'})
                    ], className = "sub-header2"),
                    html.Div([
                        #data row input GUI
                        #-------------------
                        html.H2("Pflanze einsetzen", style = {'font-family': 'Mozilla Headline, sans-serif', 'color': 'rgb(207, 207, 207)'}),
                        html.P('Bitte die Daten eingeben, die hinzugefügt werden sollen.', style = {'font-family': 'Mozilla Headline, sans-serif', 'color': 'rgb(207, 207, 207)'}),
                        #list comprehension for each column in the df to dynamically depict 
                        # df input fields
                        html.Div([
                        #on inputs: https://dash.plotly.com/dash-core-components/input
                        dcc.Input(id = {"type" : "dynamic_input", "index" : df_col}, 
                                    type = "text", 
                                    placeholder = f"{df_col}",
                                    value = None,
                                    style = {'margin-bottom': '10px'})
                            for df_col in db_df.columns if df_col != "Zeilennummer"
                        ]),
                        
                        #save button
                        html.Button("Zeile hinzufügen", id = "save_button", n_clicks=0, style = {'font-family': 'Mozilla Headline, sans-serif'}),
                        html.Div(id = "output1"),
                        
                        #row deletion GUI
                        #----------------
                        html.Br(),
                        html.H2("Pflanze kompostieren", style = {'font-family': 'Mozilla Headline, sans-serif', 'color': 'rgb(207, 207, 207)'}),
                        html.P("Bitte die Zeilennummer der Zeile eingeben, die gelöscht werden soll.", style = {'font-family': 'Mozilla Headline, sans-serif', 'color': 'rgb(207, 207, 207)'}),
                        html.Div([
                            dcc.Input(id = "row_deletion_id", type = "text", placeholder = "Zeilen ID", value = None, style = {'margin-bottom': '10px'})
                        ]),
                        #about buttons: https://dash.plotly.com/dash-html-components/button
                        html.Button("Zeile entfernen", id = "save_button_row_deletion", n_clicks=0, style = {'font-family': 'Mozilla Headline, sans-serif'}),
                        html.Div(id = "output2")
                        
                        # #column add GUI
                        # #---------------
                        # html.H3("Spalte hinzufügen"),
                        # html.P("Bitte den neu hinzuzufügenden Feldnamen angeben."),
                        # dcc.Input(id = "column_addition_id", type = "text", placeholder = "Spaltenname", value = None),
                        # html.Div(id = "output3"),
                        
                        # #column deletion GUI
                        # #--------------------
                        # html.H3("Spalte löschen"),
                        # html.P("Bitte den Spaltennamen angeben, der gelöscht werden soll."),
                        # dcc.Input(id = "column_deletion_id", type = "text", placeholder = "Spaltenname", value = None),
                        # html.Div(id = "output4")
                    ], className = "sub-header2")
        ]) 

#data row input processing
#-------------------------
@callback(
    Output("output1", "children"),
    Output("save_button", "n_clicks"), #reset the button, everytime it was clicked by returnin 0 as a second value, reassigning it to n_clicks
    Input({"type": "dynamic_input", "index": ALL}, "value"),
    Input("save_button", "n_clicks")
    )

# def display_inputs(values, n_clicks):
#     # values is a list of input values in the order of inputs generated
#     return f"You entered: {values}, {n_clicks}"

def save_data(values:list, btn1_clicks:int) -> str:
    """
    Appends the input data to the dataframe and overwrite csv.
    
    values -- list
        Contains the values entered by the user in the form of [value1, value2, ...]
    btn1_clicks -- int
        Number of clicks. Is None by default.
    Returns: string, n_clicks were set to 0 again.
    """
    #freshly load the data
    db_df, list_of_dict_db = loadTable(database_path = database_path)
    
    #initial setup
    if btn1_clicks == 0:
        return html.P("Bitte Daten eingeben.", style = {'color': 'rgb(207, 207, 207)'}), 0
    #at least one value must be entered
    elif btn1_clicks > 0 and values != [None for i in range(len(values))]:
        #Bild_Name input (picture name) to valid path
        if values[db_df.columns.get_loc("Bild_Name")] != None:
            #add .jpg if it was not provided
            if values[db_df.columns.get_loc("Bild_Name")].endswith(".jpg"):
                values[db_df.columns.get_loc("Bild_Name")] = f'<img src="/assets/{values[db_df.columns.get_loc("Bild_Name")]}" height="100">'
            else:
                values[db_df.columns.get_loc("Bild_Name")] = f'<img src="/assets/{values[db_df.columns.get_loc("Bild_Name")]}.jpg" height="100">'
        #final setup: "<img src="/assets/1_Gänseblümchen.jpg" height="100">"
        #append list as last row to df and export to csv
        db_df.loc[len(db_df)] = values
        db_df.to_csv(database_path, index = "Zeilennummer", sep = ";")
        return html.P("Zeile hinzugefügt!", style = {'color': 'rgb(207, 207, 207)'}), 0

#data row deletion processing
#-------------------------
@app.callback(
    Output("output2", "children"),
    Output("save_button_row_deletion", "n_clicks"), #reset the button, everytime it was clicked by returnin 0 as a second value, reassigning it to n_clicks
    Input("row_deletion_id", "value"),
    Input("save_button_row_deletion", "n_clicks")
    )

def deleteRow(value:list, btn2_clicks:int) -> str:
    """
    Deletes the row with the inserted column id.
    value -- string
        The column id that should be deleted.
    btn2_clicks -- int
        Number of clicks. Is None by default.
    Returns: string, n_clicks were set to 0 again. 
    """
    #freshly load the data
    db_df, list_of_dict_db = loadTable(database_path = database_path)
    
    if btn2_clicks == 0:
        return html.P("Bitte Zeilen-ID eingeben, die gelöscht werden soll.", style = {'color': 'rgb(207, 207, 207)'}), 0
    elif btn2_clicks > 0 and value is None:
        return html.P("Bitte eine valide Zahl eingeben.", style = {'color': 'rgb(207, 207, 207)'}), 0
    elif btn2_clicks > 0 and not value.isdigit():
        return html.P("Bitte eine valide Zahl eingeben.", style = {'color': 'rgb(207, 207, 207)'}), 0
    elif btn2_clicks > 0 and value.isdigit():
        db_df = db_df.drop(index = int(value))
        db_df.to_csv(database_path, index = "Zeilennummer", sep = ";")
        return html.P("Zeile gelöscht!", style = {'color': 'rgb(207, 207, 207)'}), 0

#TODO: Not yet implemented.
# #data column addition processing
# #------------------------------
# @app.callback(
#     Output("output3", "children"),
#     Input("column_addition_id", "value")
# )
# def columnAddition(value):
    
#     return f"Output 3: {value}"

# #data column deletion processing
# #--------------------------------
# @app.callback(
#     Output("output4", "children"),
#     Input("column_deletion_id", "value")
# )
# def update_output_4(value):
#     return f"Output 4: {value}"
    
#run the app
if __name__ == "__main__":
    app.run(debug = True) #TODO: set to True, if in development or debug