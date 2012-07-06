#!/usr/bin/env python
# -*- coding: utf -8 -*-

#from gi.repository import Gtk
import sqlite3
import pkdao

# Gibt ein, mehrere oder alle Pokemon mitsamt Locationinformation aus.
def print_pokemon(pokem):

    pkinfo, locs = pkdao.get_pkinfo(pokem)

    catch = "nicht gefangen."
    if pkinfo[2] != 0:
        catch = "gefangen!"
    
    info = ''
    if pkinfo[3] != None:
        info = "Info: '{0}'".format(pkinfo[3])
    
    print u"{0} {1},\t {2} \t {3}".format(pkinfo[0], pkinfo[1], catch, info)

    if len(locs) > 0:
        print "\t - - - - - - - - - - - - - -"
    for loc in locs:
        print u"\t Fangbar in {0}, {1}".format(loc[0], loc[1])
    if len(locs) > 0:
        print "\t - - - - - - - - - - - - - -"
        
        
def add_location():

    pokemon = raw_input('Pokemoninformation? > ')
    edition = raw_input('Welche Edition? > ')
    location = raw_input('Welche Location? > ')
    
    pkdao.add_loc(pokemon, edition, location)
    
    print_pokemon(pokemon)
    moreinput = raw_input("Moechten Sie mehr Daten einpflegen? yes/N > ")
    moreinput = moreinput.lower()
    
    while moreinput == 'yes' or moreinput == 'y':
        edition = raw_input('Welche Edition? > ')
        loc = raw_input('Welche Location? > ')
    
        pkdao.add_loc(pokemon, edition, loc)
        print_pokemon(pokemon)
        moreinput = raw_input("Moechten Sie mehr Daten einpflegen? yes/N > ")
        moreinput = moreinput.lower()
  
#gibt eine pokemonliste nach den uebergebenen argumenten gefiltert aus
def printa(arguments):
    arguments = arguments.split(' -')
    arguments = arguments [1:]
    
    if len(arguments) == 0:
        dispall = raw_input('Moechten Sie alle Pokemon anzeigen lassen? Y/no > ')
        if dispall == 'no' or dispall == 'n':
            return
    
    list = pkdao.get_pk(arguments)
    
    for pk in list:
        print_pokemon(pk)
    
def rm_location():
    pokemon = raw_input('Pokemoninformation? > ')
    print_pokemon(pokemon)
    print 'Spezifizieren Sie bitte den Eintrag der geloescht werden soll.'
    edition = raw_input('Loeschen: Welche Edition? > ')
    location = raw_input('Loeschen: Welche Location? > ')
    pkdao.rm_loc(pokemon, edition, location)
    print_pokemon(pokemon)
    
    morerm = raw_input("Moechten Sie mehr Daten loeschen? yes/N > ")
    morerm = morerm.lower()
    
    while morerm == 'yes' or morerm == 'y':
        edition = raw_input('Loeschen: Welche Edition? > ')
        location = raw_input('Loeschen: Welche Location? > ')
    
        pkdao.rm_loc(pokemon, edition, location)
        print_pokemon(pokemon)
        morerm = raw_input("Moechten Sie mehr Daten loeschen? yes/N > ")
        morerm = morerm.lower()

def add_info():
    pokemon = raw_input('Pokemoninformation? > ')
    info = raw_input('Info? > ')
    
    pkdao.add_info(pokemon, info)
    
def rm_info():
    pokemon = raw_input('Von welchem Pokemon wollen Sie die Info loeschen? > ')
    
    pkdao.rm_info(pokemon)
    
def set_c():
    print 'Herzlichen Glückwunsch zum Fangerfolg! :)'
    pokemon = raw_input('Pokemoninformation? (Mehrere durch Kommata trennen) > ')
    pkdao.set_c(pokemon, 1)
   
def uset_c():
    pokemon = raw_input('Pokemoninformation? (Mehrere durch Kommata trennen) > ')
    pkdao.set_c(pokemon, 0)
    
def close():
    pkdao.close()
        
        
    
    
    
