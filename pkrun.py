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
            print 'printpokemon oder prp gibt die Daten zum uebergebenen Pokemon aus'
            print 'print oder pr gibt die Daten gemaess der Parameter aus. Ohne Parameter werden alle Pokemon ausgegeben.'
            print '\t -g gibt alle gefangenen Pokemon aus'
            print '\t -ung gibt alle ungefangenen Pokemon aus'
            print '\t -ort gibt alle Pokemon mit Fundorten aus'
            print '\t -info gibt alle Pokemon mit Info aus'
            print '\t Die Parameter sind auch kombinierbar. print -ung -ort gibt also alle ungefangenen Pokemon mit Fundorten aus'
            print 'addlocation oder addloc fuegt Fundorte zum Pokemon hinzu.'
            print 'exit beendet dieses Programm'
        elif func == 'exit':
            running = False
            pkview.close()
        elif 'print' in func or func == 'prp':
            pokem = raw_input('Welches Pokemon? > ')
            pkview.print_pokemon(pokem)
        elif 'addloc' in func:
            pkview.add_location()
        elif 'print' in func or 'pr' in func:
            pkview.printa(func)
        else:
            print 'Tippen sie h oder help oder hilfe fuer eine Erklaerung der Funktionalitaet ein'
            
run()
        
        
    
    
    
