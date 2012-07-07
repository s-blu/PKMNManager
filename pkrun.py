#!/usr/bin/env python
# -*- coding: utf -8 -*-


import sqlite3
import pkview
import sys


def __main():
    run()
    
def run():

    running = True
    print '====================================================='
    print 'Willkommen im Pokemonmanager V0.3!'
    print 'prp/print Ausgabe der Pokemon'
    print 'addloc/info rmloc/info Aendern von Fundorten und Info'
    print 'exit beendet das Programm'
    print 'help bringt Sie zur ausfuehrlichen Hilfe.'  
    print '====================================================='
    
    try:
        while(running):
            func = raw_input('Was moechten Sie tun? > ')
            
            if func == 'h' or func == "help" or func == 'hilfe':
                print 'Sie befinden sich im Pokemonmanager V0.3!'
                print '- - -'
                print '"printpokemon" oder "prp" gibt die Daten zum uebergebenen Pokemon aus'
                print '"print" oder "pr" gibt die Daten gemaess der Parameter aus. Ohne Parameter werden alle Pokemon ausgegeben.'
                print '\t -g gibt alle gefangenen Pokemon aus'
                print '\t -ung gibt alle ungefangenen Pokemon aus'
                print '\t -ort gibt alle Pokemon mit Fundorten aus'
                print '\t -info gibt alle Pokemon mit Info aus'
                print '\t Die Parameter sind auch kombinierbar. print -ung -ort gibt also alle ungefangenen Pokemon mit Fundorten aus'
                print '"addlocation" oder "addloc" fuegt Fundorte zum Pokemon hinzu.'
                print '"removelocation" oder "rmloc" loescht ein spezifischen Fundort wieder.'
                print '"addinfo"  fuegt eine Notiz/Information zum Pokemon hinzu.'
                print '"removeinformation" oder "rminfo" loescht die Notiz/Information zum Pokemon.'
                print '"setcatched" oder "ct" markiert ein oder mehrere Pokemon als gefangen.'
                print '"unsetcatched" oder "uct" markiert ein oder mehrere Pokemon als nicht gefangen.'
                print '"exit" beendet dieses Programm'
                print '"credits" zeigt Informationen ueber dieses Programm an'
                print '- - -'
                print 'Mehrfachangaben durch , trennen oder Ranges angeben, z.B. 3-77'
                print 'Pokemon koennen nach Eingabe des Befehls oder direkt hinter den Befehl geschrieben werden'
                
            elif func == 'exit':
                running = False
                pkview.close()
            elif 'printp' in func or 'prp' in func:
                pkview.prp(func)
            elif 'addloc' in func:
                pkview.addloc(func)
            elif 'print' in func or 'pr' in func:
                pkview.printa(func)
            elif 'removeloc' in func or 'rmloc' in func:
                pkview.rmloc(func)
            elif 'addinfo' in func:
                pkview.addinf(func)
            elif 'removeinfo' in func or 'rminfo' == func:
                pkview.rminf(func)
            elif 'setcatch' in func or 'ct' == func:
                pkview.ct(func)
            elif 'unsetcatch' in func or 'uct' == func:
                pkview.uct(func)
            elif 'credit' in func:
                pkview.credit()
            elif 'clear' in func:
                print "\33[2J"
            elif 'flausch' in func:    
                print "Aaaaw! *flausch* <3"
            else:
                print 'Tippen sie "h"/"help"/"hilfe" fuer eine Erklaerung der Funktionalitaet ein'
    except KeyboardInterrupt:
        print 'Abbruch des Programms durch Ctrl+C.'
        print 'Das ist zwar unsanft, aber ich wuensche trotzdem einen schoenen Tag!'
        sys.exit(1)
            
run()
        
        
    
    
    
