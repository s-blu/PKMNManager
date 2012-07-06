#!/usr/bin/env python

#from gi.repository import Gtk
import sqlite3

conn = sqlite3.connect('pokedex.db')
c = conn.cursor()

def print_pokemon(pokemon):
    if isinstance(pokemon, str) and not pokemon.isdigit():
        pokemon = pokemon.capitalize()
        pokemon = (pokemon,)
        for row_name in c.execute('select nr from pokemon where name = ?', pokemon):
            pokemon = row_name[0]
            
            
    pokemon = (pokemon,)    
    for row in c.execute('select nr, name, catched from pokemon where nr = ?', pokemon):

        catch = ",\t not catched."
        if row[2] != 0:
            catch = ",\t catched!"

        print str(row[0]) + " " + row[1] + catch
        
        nummer = (row[0],)
        for row2 in c.execute('select edition, location from locations where nr = ?', nummer):
            print "\t Catchable in {0}, {1}".format(row2[0], row2[1])
    
def add_location(pokemon, edition, location):
    
    
    if isinstance(pokemon, str) and not pokemon.isdigit():
        pokemon = (pokemon,)
        for row in c.execute('select nr from pokemon where name = ?', pokemon):
            pokemon = row[0]
    
    inserts = (pokemon, edition, location)
    c.execute('insert into locations (nr, edition, location) values (?,?,?)', inserts)
    
    print_pokemon(pokemon)
    moreinput = raw_input("Moechten Sie mehr Daten einpflegen? yes/N > ")
    moreinput = moreinput.lower()
    
    if moreinput == 'yes' or moreinput == 'y':
        addlocp(pokemon)
    else:
        okay = raw_input("Sollen die Angaben gespeichert werden? Y/no > ")
        okay = okay.lower()
        
        if okay != "no" and okay != "n":
            conn.commit()
        
def addloc():
    pokemon = raw_input('Pokemoninformation? > ')
    edition = raw_input('Welche Edition? > ')
    loc = raw_input('Welche Location? > ')
    
    add_location(pokemon, edition, loc)
    
def addlocp(pokemon):
    edition = raw_input('Welche Edition? > ')
    loc = raw_input('Welche Location? > ')
    
    add_location(pokemon, edition, loc)
    
def prp():
    pokem = raw_input('Welches Pokemon? > ')
    print_pokemon(pokem)
    
def run():
    running = True
    while(running):
        func = raw_input('Was moechten Sie tun? > ')
        
        if func == 'h' or func == "help" or func == 'hilfe':
            print 'Sie befinden sich im Pokemonmanager V0.001!'
            print 'print_pokemon oder prp gibt die Daten zur uebergebenen pokemonnr aus'
            print 'add_location der addloc fuegt die location in der uebergebenen edition zum pokemon hinzu.'
            print 'exit beendet dieses Programm'
        elif func == 'exit':
            running = False
        elif 'print_pokemon' in func or func == 'prp':
            prp()
        elif 'add_location' in func or func == 'addloc':
            addloc()
        else:
            print 'Tippen sie h oder help oder hilfe fuer eine Erklaerung der Funktionalitaet ein'
            
run()
        
        
    
    
    
