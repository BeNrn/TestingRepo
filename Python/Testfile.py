# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 20:31:00 2022

@author: Ben

Testing for course AutomateTheBoringStuff
"""
#General
#--------
#stop the program when it get to this part
import sys
sys.exit()

#print() returns a None value. Thus:
a = print() 
a == None

#print command has optional keyword arguments as well. Like:
print("Hello", "you", sep = "__", end = "")
print("Newline")

#Globald and local scope
#-----------------------
#variables in a function only exists within a function (local scope). They will 
#   be forgotten when the function is terminated
#variables outside a function exists everywhere but in the function (global scope)
var_a = 10
print(var_a)

def sum_up():
    var_a = 2
    var_a + 2
    
print(var_a)

#global variable can be used in functions. Python will search for them if no 
#   local variable with the called name exists in the function. Like:
    
varB = 10

def sum_up(number):
    number = varB + 12
    print(number)

sum_up(varB)

#variable in a function can be defined as global, even if it is assigned within
# a function, using the "global" statement

def sum_up():
    global number
    number = 10
    
sum_up()
print(number)

#Try and Except Statements
#-------------------------
#to define which response should be given by which error, the errortype can be
#   defined in the except statement

def divideBy(number):
    try:
        return 10/number
    except ZeroDivisionError:
        print("Division by zero is not allowed.")
    except TypeError:
        print("You did not enter a number.")
        
divideBy(2)
divideBy(0)   
divideBy("f")   

#using except without an error type will cover all errors
def divideBy(number):
    try:
        return 10/number
    except:
        print("Something went wrong.")
        
divideBy(2)
divideBy(0)   
divideBy("f")
