# -*- coding: utf-8 -*-
"""
Purpose:    Script for an open source database.
Created:    25.07.2025
Author:     BeNrn
"""
#https://realpython.com/python-dash/#style-your-dash-application
#https://dash.plotly.com/dash-core-components/tabs (for the tabs)
#start the dash Dashboard:
#   - open CMD
#   - activate python environment
#   - cd to file location of this script
#   - run > python OpenSourceDatabase_Dashboard.py
#   - open the provided URL in a browser

#load libs
import pandas as pd
import os

from dash import Dash, Input, Output, dcc, html, dash_table, callback

#load paths
user_name = os.getlogin()
os.chdir(r"C:\Users\{}\Documents\Freizeit\Geschenke\2025_Toms_Pflanzendatenbank".format(user_name))
base_path = r"C:\Users\{}\Documents\Freizeit\Geschenke\2025_Toms_Pflanzendatenbank".format(user_name)
database_path = os.path.join(base_path, "openDB.csv")

#load the data
db_df = pd.read_csv(database_path, sep = ";")

#laod matching images (image name starts with Bild_ID)
image_list = os.listdir(os.path.join(base_path, "assets"))

image_name_list = []
for bild_id in db_df["Bild_ID"]:
    image_name_list = image_name_list + [[i for i in image_list if i.startswith(str(bild_id) + "_")][0]]

image_name_list = [f"{i}" for i in image_name_list]
image_name_list = [f'<img src="/assets/{i}" height="60">' for i in image_name_list]

db_df["Bild_path"] = image_name_list

#start a dash instance
app = Dash(__name__)

#set the style of the webpage
#html.Div -> create a new division
app.layout = html.Div([
    #primary heading
    html.H1(children="Toms Pflanzendatenbank"),
    #introduce tabs
    dcc.Tabs(id = "tabs", value = "tab_table", children=[
        dcc.Tab(label="Tabelle", value = "tab_table"),
        dcc.Tab(label="Dateneingabe", value = "tab_datainput"),
        ]),
        html.Div(id="database")
    ])

#controls the tabs, based on user input
@callback(Output("database", 'children'),
              Input('tabs', 'value'))

def render_content(tab):
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
                data = db_df.to_dict('records'),
                columns = [{'name': col, 'id': col, 'presentation': 'markdown'} for col in db_df.columns],
                style_table = {'overflowX': 'auto'},
                style_cell = {'textAlign': 'left'},
                style_data={'whiteSpace': 'normal', 'height': 'auto'},
                markdown_options={'html': True}
            )
        ])
    elif tab == 'tab_datainput':
        return html.Div([
            html.H3("Dateneingabe"),
            #list(db_df) -> hier für jede Überschrift einen Block einfügen
            dcc.Input(id='input-name', type='text', placeholder='Name'),
        ])

#run the app
if __name__ == "__main__":
    app.run(debug=True)
    
    
    
    
#Dateneingabe in Dash: 
# - Input-Komponenten wie `dcc.Input`, `dcc.Dropdown` oder `dash_table.DataTable` (editierbar!)


# ## ✅ **Variante 1: Dateneingabe mit `dcc.Input` Feldern**

# Benutzer gibt Daten ein, klickt auf einen Button, und die Eingabe wird zu einer Tabelle hinzugefügt.

# ### 🧪 Beispiel:

# ```python
import dash
from dash import dcc, html, Input, Output, State
import dash_table
import pandas as pd

# Start-Daten
df = pd.DataFrame(columns=["Name", "Alter", "Beruf"])

# App initialisieren
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H2("Person hinzufügen"),

    # Eingabefelder
    dcc.Input(id='input-name', type='text', placeholder='Name'),
    dcc.Input(id='input-age', type='number', placeholder='Alter'),
    dcc.Input(id='input-job', type='text', placeholder='Beruf'),
    html.Button('Hinzufügen', id='add-button', n_clicks=0),
    
    html.Hr(),

    # Tabelle zur Anzeige
    dash_table.DataTable(
        id='data-table',
        columns=[{'name': col, 'id': col} for col in df.columns],
        data=df.to_dict('records')
    )
])

# Callback zum Hinzufügen von Daten
@app.callback(
    Output('data-table', 'data'),
    Input('add-button', 'n_clicks'),
    State('input-name', 'value'),
    State('input-age', 'value'),
    State('input-job', 'value'),
    State('data-table', 'data'),
    prevent_initial_call=True
)
def add_row(n_clicks, name, age, job, current_data):
    if name and age and job:
        current_data.append({'Name': name, 'Alter': age, 'Beruf': job})
    return current_data

if __name__ == '__main__':
    app.run_server(debug=True)
# ```

# ---

# ## ✅ **Variante 2: Direkt editierbare `DataTable`**

# Du kannst die `DataTable` direkt **editierbar** machen:

# ```python
# dash_table.DataTable(
#     id='editable-table',
#     columns=[{'name': col, 'id': col, 'editable': True} for col in df.columns],
#     data=df.to_dict('records'),
#     editable=True
# )
# ```

# → Änderungen werden direkt in der Tabelle gemacht. Du kannst mit einem Callback auch speichern, verarbeiten oder validieren, wenn sich die Daten ändern.

# ---

# ## ✅ Was du noch hinzufügen könntest:

# * Validierung der Eingaben (z. B. kein leeres Feld zulassen)
# * Zurücksetzen der Eingabefelder nach dem Absenden
# * Speicherung in einer Datei oder Datenbank

# Möchtest du eins davon auch sehen?
