#!/usr/bin/env python

#from gi.repository import Gtk
import sqlite3
import pkview


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
            pkview.close()
        elif 'print_pokemon' in func or func == 'prp':
            pkview.print_pokemon()
        elif 'add_location' in func or func == 'addloc':
            pkview.add_location()
        else:
            print 'Tippen sie h oder help oder hilfe fuer eine Erklaerung der Funktionalitaet ein'
            
run()
        
        
    
    
    
