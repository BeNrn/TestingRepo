# -*- coding: utf-8 -*-
"""
Purpose:    Logging basics.
Created:    23.02.2024
Author:     BeNrn
"""
#import libs
#------------
import logging

#set logging
#------------
#logging message
formatter = logging.Formatter("%(message)s")
#file handler
fileHandler = logging.FileHandler(r"C:\temp\loggingtext.log", "a")
#set formatter
fileHandler.setFormatter(formatter)

#stream handler
streamHandler = logging.StreamHandler()
streamHandler.setFormatter(formatter)

#clear potentially opened loggers
#root logger
log = logging.getLogger()
#remove all old handlers
for hdlr in log.handlers[:]:
    #check if hdlr is of class stream or file handler
    if isinstance(hdlr, logging.FileHandler) or isinstance(hdlr, logging.StreamHandler):
        log.removeHandler(hdlr)

#add new handler
log.addHandler(fileHandler)
log.addHandler(streamHandler) #write output to console and logfile
log.setLevel(logging.INFO)

#do the work
#------------

#test logging
logging.info("Test logging.")