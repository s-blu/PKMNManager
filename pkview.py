#!/usr/bin/env python
# -*- coding: utf -8 -*-

#from gi.repository import Gtk
import sqlite3
import pkdao

def prp(arguments):
    arguments = arguments.split(' ')
    arguments = arguments [1:]
    if len(arguments) > 0:
        print_pokemon(arguments[0])
    else:
        pokem = raw_input('Welches Pokemon? > ')
        print_pokemon(pokem)

# Gibt ein, mehrere oder alle Pokemon mitsamt Locationinformation aus.
def print_pokemon(pokem):

    pkinfo, locs = pkdao.get_pkinfo(pokem)
    

    catch = "( )"
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

    pokem = raw_input('Pokemonnr oder -name? > ')
    edition = raw_input('Welche Edition? > ')
    location = raw_input('Welche Location? > ')
    
    pkms = pokem.split(',')
    
    for pokemon in pkms:
        if not pkdao.valid_pk(pokemon):
            print "Ungueltiges Pokemon '{0}'".format(pokemon)
        else:
            pkdao.add_loc(pokemon, edition, location)
            
            print_pokemon(pokemon)
            
    moreinput = raw_input("Moechten Sie mehr Daten einpflegen? yes/N > ")
    moreinput = moreinput.lower()
    
    while moreinput == 'yes' or moreinput == 'y':
        edition = raw_input('Welche Edition? > ')
        loc = raw_input('Welche Location? > ')
    
        for pokemon in pkms:
            if not pkdao.valid_pk(pokemon):
                print "Ungueltiges Pokemon '{0}'".format(pokemon)
            else:
                pkdao.add_loc(pokemon, edition, loc)
                print_pokemon(pokemon)
        moreinput = raw_input("Moechten Sie mehr Daten einpflegen? yes/N > ")
        moreinput = moreinput.lower()
  
#gibt eine pokemonliste nach den uebergebenen argumenten gefiltert aus
def printa(arguments):
    arguments = arguments.split(' -')
    arguments = arguments [1:]

    list = pkdao.get_pk(arguments)
    
    if len(list) > 100:
        dispall = raw_input('Moechten Sie alle {0} Pokemon anzeigen lassen? Y/no > '.format(len(list)))
        if dispall == 'no' or dispall == 'n':
            return
            
    for pk in list:
        print_pokemon(pk)
    
def rm_location():
    pokem = raw_input('Pokemonnr oder -name? > ')
    
    pkms = pokem.split(',')
    
    for pokemon in pkms:
        if not pkdao.valid_pk(pokemon):
            print "Ungueltiges Pokemon '{0}'".format(pokemon)
        else:
            print_pokemon(pokemon)
            
    rmall = raw_input('Sollen alle Eintraege geloescht werden? yes/N > ')
    rmall = rmall.lower()
    if rmall == 'yes' or rmall == 'y':
        for pokemon in pkms:
            pkdao.rm_all_loc(pokemon)
            print_pokemon(pokemon)
        
    else:
        print 'Spezifizieren Sie bitte den Eintrag der geloescht werden soll.'
        edition = raw_input('Loeschen: Welche Edition? > ')
        location = raw_input('Loeschen: Welche Location? > ')
        for pokemon in pkms:
            pkdao.rm_loc(pokemon, edition, location)
            print_pokemon(pokemon)
            
    if rmall != 'yes' and rmall != 'y':          
        morerm = raw_input("Moechten Sie mehr Daten loeschen? yes/N > ")
        morerm = morerm.lower()
        
        while morerm == 'yes' or morerm == 'y':
            edition = raw_input('Loeschen: Welche Edition? > ')
            location = raw_input('Loeschen: Welche Location? > ')
            for pokemon in pkms:
                pkdao.rm_loc(pokemon, edition, location)
                print_pokemon(pokemon)
            morerm = raw_input("Moechten Sie mehr Daten loeschen? yes/N > ")
            morerm = morerm.lower()

def add_info():
    pokem = raw_input('Pokemonnr oder -name? > ')
    info = raw_input('Info? > ')
    pkms = pokem.split(',')
    
    for pokemon in pkms:
        if not pkdao.valid_pk(pokemon):
            print "Ungueltiges Pokemon '{0}'".format(pokemon)
        else:
            pkdao.add_info(pokemon, unicode(info))
            print_pokemon(pokemon)
    
def rm_info():
    pokem = raw_input('Von welchem Pokemon wollen Sie die Info loeschen? > ')
    pkms = pokem.split(',')
    
    for pokemon in pkms:
        if not pkdao.valid_pk(pokemon):
            print "Ungueltiges Pokemon '{0}'".format(pokemon)
        else:
            pkdao.rm_info(pokemon)
            print_pokemon(pokemon)
    
def set_c():
    print 'Herzlichen Glueckwunsch zum Fangerfolg! :)'
    pokem = raw_input('Pokemonnr oder -name? > ')
    pkms = pokem.split(',')
    
    for pokemon in pkms:
        if not pkdao.valid_pk(pokemon):
            print "Ungueltiges Pokemon '{0}'".format(pokemon)
        else:
            pkdao.set_c(pokemon, 1)
            print_pokemon(pokemon)
   
def uset_c():
    pokem = raw_input('Pokemonnr oder -name? > ')
    pkms = pokem.split(',')
    
    for pokemon in pkms:
        if not pkdao.valid_pk(pokemon):
            print "Ungueltiges Pokemon '{0}'".format(pokemon)
        else:
            pkdao.set_c(pokemon, 0)
            print_pokemon(pokemon)
    
def close():
    pkdao.close()
        
        
    
    
    
