# -*- coding: utf-8 -*-
"""
Purpose:    Read, process and write VCF contact file to readable text file.
Created:    28.01.2024
Author:     BeNrn
"""

#set paths
#---------
vcfPath = r"C:\Users\tamta\Documents\Kontakte_SamsungHandy_05092022.vcf"
outFile = r"C:\Users\tamta\Documents\test.txt"

#load data
#----------
with open(vcfPath, "r") as vcfFile:
    data = vcfFile.readlines()

#remove unnecessary data and reformat
#------------------------------------
#reversed() is used, because remove() will remove items from the list and will
# alter all subsequent indices. Thus, iterating from behind, the change in the 
# index will only affect alrady passed items
for element in reversed(data):
    if not element.startswith(("N:", "TEL", "ADR", "BDAY", "NOTE")):
        data.remove(element)

#list to string
data = str(data)

#clean up
data = data.replace(r"\n", "")
data = data[1:-1]
data = data.replace(r"N:", "+++NAME;")
data = data.replace("'", "")

#create list with entries for each contact
data = data.split("+++")
data = data[1:]

#iterate over each contact
#-------------------------
for element in data:
    #bit of processing
    fullName = telephoneNumber = address = birthdayFull = note =  None
    #split up the different entries
    contactEntries = element.split(",")
            
    #cover multiple telephone numbers
    telephoneNumber = list()
        
    for entry in contactEntries:
        #split up the contact entry parts
        entryParts = entry.split(";")
        if entryParts[0].strip() == "NAME":
            #NAME:<Nachname>;<Vorname>;<zusätzliche Vornamen>;<Präfix>;<Suffix>
            fullName = entryParts[2] + " " + entryParts[3] + " " + entryParts[1]
            fullName = fullName.replace("  ", " ") #cover missing middle name
        if entryParts[0].strip() == "TEL":
            #TEL:<Typ>:<Nummer>
            telephoneNumber = telephoneNumber + [entryParts[1]]
        if entryParts[0].strip().startswith("ADR"):
            #ADR:<POBOX>;<EXT>;<STREET>:<LOCALITY>;<REGION>;<PLZ>;<country>
            if entryParts[2].startswith("ENCODING"):
                #addressString = "=4E=65=75=73=74=C3=A4=64=74=65=72=20=4D=61=72=6B=74=20=35;=48=69=6C=64=65=73=68=65=69=6D;;=33=31=31=33=34;"
                addressString = entryParts[-1] 
                addressString = addressString.replace("=", " ")
                addressParts = addressString.split(";")
                
                for index, element in enumerate(addressParts):
                    addressParts[index] = bytearray.fromhex(element).decode()
                
                address = addressParts
            elif entryParts[2].startswith("CHARSET"):
                addressString = entryParts[5:]
                addressString = ",".join(addressString)
                addressString = addressString.replace("=", " ")
                addressParts = addressString.split(",")
                
                for index, element in enumerate(addressParts):
                    addressParts[index] = bytearray.fromhex(element).decode()
                
                address = addressParts
            else:
                address = entryParts[1] + " " + entryParts[3] + " " + entryParts[6] + " " + entryParts[4]
                address = [address.strip()]
        if entryParts[0].strip().startswith("BDAY"):
            #BDAY:<YEAR>-<MONTH>;<DAY>
            birthday = entryParts[0].split(":")[1]
            birthday = birthday.split("-")
            birthdayFull = birthday[-1] + "." + birthday[2] + "." + birthday[0]
        if entryParts[0].strip().startswith("NOTE"):
            if len(entryParts) > 1 and entryParts[1].startswith("ENCODING"):
                noteString = entryParts[-1].split(":")[1] 
                noteString = noteString.replace("=", " ")
                noteParts = noteString.split(";")
                
                for index, element in enumerate(noteParts):
                    noteParts[index] = bytearray.fromhex(element).decode()
                
                note = "NOTE:" + noteParts[0]
                
            else:
                note = entryParts[0].strip()
                
            
    #write to file
    #-------------
    with open(outFile, "a") as file:
        if fullName is not None:
            file.write(fullName + "\n")
        if telephoneNumber is not None:
            file.write("\n".join(telephoneNumber) + "\n")
        if address is not None:
            file.write(address[0] + "\n")
        if birthdayFull is not None:
            file.write(birthdayFull + "\n")
        if note is not None:
            file.write(note + "\n")
        
        file.write("--------\n") 
