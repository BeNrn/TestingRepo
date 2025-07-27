# -*- coding: utf-8 -*-
"""
Purpose:    Script for an open source database.
Created:    25.07.2025
Author:     BeNrn
"""
#abstract
# 1. Images are stored in an image directory and are connected using an id 
#    naming. The naming follows: "ID_Name.jpg"
# 2. The data itself is stored in a CSV file.
# 3. Uploads are performed using an excel file.
# 4. Exports of the database are done to PDF format.
# 5. Information are retrieved in a python context window.

#load libs
import pandas as pd
import os
import reportlab

#https://www.geeksforgeeks.org/python/creating-pdf-documents-with-python/
#https://docs.reportlab.com/rml/userguide/Chapter_1_Introduction/
#from reportlab.pdfgen import canvas
#from reportlab.pdfbase.ttfonts import TTFont
#from reportlab.pdfbase import pdfmetrics

from reportlab import platypus
from reportlab.lib import colors

#set current working directory and define as base path
user_name = os.getlogin()
os.chdir(r"C:\Users\{}\Documents\Freizeit\Geschenke\2025_Toms_Pflanzendatenbank".format(user_name))
base_path = r"C:\Users\{}\Documents\Freizeit\Geschenke\2025_Toms_Pflanzendatenbank".format(user_name)
database_path = os.path.join(base_path, "openDB.csv")

#load functions
def uploadFiles(input_path):
    """
    Parameters
    ----------
    input_path : TYPE
        DESCRIPTION.

    Returns
    -------
    Writes df to disk..

    """
    df = pd.read_excel(input_path)
    if not os.path.exists(database_path):
        df.to_csv(database_path, sep = ";", index = False)
    else:
        db_df = pd.read_csv(database_path, sep = ";")
        db_df = pd.concat([db_df, df], axis = 0, ignore_index=True)
        db_df.to_csv(database_path, sep = ";", index = False)
        
def deleteEntries(axis, delete_number):
    """
    Parameters
    ----------
    axis : TYPE
        DESCRIPTION.
    delete_number : TYPE
        DESCRIPTION.

    Returns
    -------
    Writes df to disk.

    """    
    delete_start = int(delete_number.split(":")[0])
    delete_end = int(delete_number.split(":")[1])+1
    
    db_df = pd.read_csv(database_path, sep = ";")
    if axis == "ZEILE":
        db_df = db_df.drop([delete_start,delete_end])
    else:
        delete_list = list(range(delete_start, delete_end))
        db_df.drop(db_df.columns[delete_list],axis=1,inplace=True)
    
    db_df.to_csv(database_path, sep = ";", index = False)
    
def dfToPDF(elements_to_return):
    if elements_to_return == "ALLE":
        db_df = pd.read_csv(database_path, sep = ";")
        data = db_df.values.tolist()
        header = [list(db_df.columns)]
        list_of_lists = header + data
        pdf_table = platypus.tables.Table(list_of_lists)
        
        pdf_table.setStyle(platypus.TableStyle([('BACKGROUND',(0,0),(-1,0),colors.grey), # Kopfzeile grau hinterlegen
                                                          ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke) # Textfarbe in Kopfzeile
                                                          ]))
        
       # ('ALIGN', (0, 0), (-1, -1), 'CENTER'),               # Zentrieren
       # ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),     # Schriftart Kopfzeile
       # ('BOTTOMPADDING', (0, 0), (-1, 0), 12),              # Abstand unten Kopfzeile
       # ('BACKGROUND', (0, 1), (-1, -1), colors.beige),      # Hintergrund für restliche Zeilen
       # ('GRID', (0, 0), (-1, -1), 1, colors.black),         # Tabellenrahmen
        
        #creating a pdf object
        doc = platypus.SimpleDocTemplate(os.path.join(base_path, "report.pdf"), pagesize = reportlab.lib.pagesizes.A4)
        
        styles = reportlab.lib.styles.getSampleStyleSheet() # vordefinierte Textstile
        
        heading = platypus.Paragraph("Report", styles['Title'])
        linie = platypus.HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.grey)
        
        elements = [heading, linie, platypus.Spacer(1, 20), pdf_table, platypus.PageBreak()] 
        
        image_list = os.listdir(os.path.join(base_path, "Bilder"))
        
        for entry in data:
            list_of_lists_single = header + [entry]
            pdf_table_single = platypus.tables.Table(list_of_lists_single)
            pdf_table_single.setStyle(platypus.TableStyle([('BACKGROUND',(0,0),(-1,0),colors.grey), ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke)]))
            
            image_name = [i for i in image_list if i.startswith(str(entry[-1]) + "_")][0]
            
            image = platypus.Image(os.path.join("Bilder", image_name))  # Pfad anpassen
            elements = elements + [pdf_table_single, platypus.Spacer(1, 20), image, platypus.PageBreak()]
            
            if entry == data[-1]:
                elements = elements[:-1]#remove last page break
        
        doc.build(elements)
        
    elif elements_to_return == "AUSWAHL":
        print("Bisher noch nicht eingebaut.")
        #TODO
    elif elements_to_return == "FILTER":
        print("Bisher noch nicht eingebaut.")
        #TODO
        


#set stopper to allow the user to stop the application.
stopper = False

while not stopper:
    user_input = input("Was willst du machen? (UPLOAD / DELETE / REPORT / STOP): ")
    
    if user_input == "UPLOAD":
        excel_name = input("- Wenn der Dateiname von 'Upload.xlsx' abweicht, gib ihn bitte an, ansonsten drücke bitte einfach ENTER: ")
        
        if excel_name != "":
            input_path = os.path.join(os.getcwd(), excel_name)
        else:
            input_path = os.path.join(os.getcwd(), "Upload.xlsx")
        
        uploadFiles(input_path = input_path)
    
    if user_input == "DELETE": #TODO: beim löschen die struktur anzeigen und die einträge anzeigen, die gelöscht werden würden mit nochmaliger bestätigung erfragen
        axis = input("- Willst du eine/mehrere Zeilen oder Spalten löschen? (ZEILE / SPALTE): ")
        delete_number = input("- Welche Einträge möchtest du löschen? (Start:Ende): ")
        
        deleteEntries(axis = axis, delete_number = delete_number)
        
    if user_input == "REPORT":
        elements_to_return = input("- Welche Elemente sollen wiedergegeben werden? (ALLE / AUSWAHL / FILTER): ")
        
        dfToPDF(elements_to_return = elements_to_return)
        
    if user_input == "STOP":
        stopper = True
    
    
