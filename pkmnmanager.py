#!/usr/bin/python
# -*- coding: utf-8 -*-
#Copyright 2012-2013 sam@s-blu.de
#Diese Datei ist Teil von PKMNManager.

#PKMNManager ist Freie Software: Sie koennen es unter den Bedingungen
#der GNU General Public License, wie von der Free Software Foundation,
#Version 3 der Lizenz oder (nach Ihrer Option) jeder spaeteren
#veroeffentlichten Version, weiterverbreiten und/oder modifizieren.

#PKMNManager wird in der Hoffnung, dass es nuetzlich sein wird, aber
#OHNE JEDE GEWaeHRLEISTUNG, bereitgestellt; sogar ohne die implizite
#Gewaehrleistung der MARKTFaeHIGKEIT oder EIGNUNG FueR EINEN BESTIMMTEN ZWECK.
#Siehe die GNU General Public License fuer weitere Details.

#Sie sollten eine Kopie der GNU General Public License zusammen mit diesem
#Programm erhalten haben. Wenn nicht, siehe <http://www.gnu.org/licenses/>.


import sqlite3
import dat.pkview as pkview
import sys


def __main():
    run()
    
def run():

    running = True
    print '====================================================='
    print 'Willkommen im Pokemonmanager V{0}!'.format(pkview.ver)
    print 'prp/print Ausgabe der Pokemon'
    print 'addloc/info rmloc/info Aendern von Fundorten und Info'
    print 'exit Programm beenden'
    print 'help ausfuehrliche Hilfe'  
    print 'Bitte keine Umlaute benutzen.'
    print '====================================================='
    
    try:
        while(running):
            func = raw_input(' >> Was moechten Sie tun? > ')
            
            if func == 'h' or func == "help" or func == 'hilfe':
                print '================================================'
                print 'Sie befinden sich im Pokemonmanager V{0}!'.format(pkview.ver)
                print '- - -'
                print 'print, pr, zeige'
                print '\t gibt die Daten gemaess der Parameter aus. Fuer alle Pokemon bei Nachfrage Enter druecken.'
                print '\t -g gibt alle gefangenen Pokemon aus'
                print '\t -ung gibt alle ungefangenen Pokemon aus'
                print '\t -info gibt alle Pokemon mit Info aus'
                print '\t -ed gibt alle Pokemon mit angegeber Edition aus, z.B.: -edHG'
                print '\t -loc oder -ort gibt alle Pokemon mit angegebem Fundort (falls angegeben, sonst alle) aus, z.B.: -locRoute 24'
                print '\t -rng gibt alle Pokemon in der angegebenen Zahlenrang aus. Start und Endwert werden durch "to" getrennt, z.B.: -rng1to150'
                print '\t Die Parameter sind auch kombinierbar. print -ung -ort gibt also alle ungefangenen Pokemon mit Fundorten aus'
                print '\t Es ist auch moeglich, nach Anfangsfragmenten zu suchen, also zb. nach allen Pokemon, die mit "Pan" anfangen, dafuer einfach pr Pan eingeben'
                print 'addloc, neuerort'
                print '\t fuegt einen oder mehrere Fundorte, bestehens aus Edition und Fundort, zum Pokemon hinzu.'
                print 'rmloc, loescheort'
                print '\t loescht ein spezifischen oder alle Fundorte'
                print 'addinfo, neueinfo '
                print '\t fuegt eine Notiz/Information zum Pokemon hinzu.'
                print 'rminfo, loescheinfo'
                print '\t loescht die Notiz/Information zum Pokemon.'
                print 'setcatched, ct, gefangen '
                print '\t markiert ein oder mehrere Pokemon als gefangen.'
                print 'unsetcatched, uct, ungefangen'
                print '\t markiert ein oder mehrere Pokemon als nicht gefangen.'
                print 'export'
                print '\t exportiert die Fundortinformationen und wahlweise die Infoeintraege zur Weitergabe'
                print 'import'
                print '\t Importiert per Export erstellte Fundort und evt. Infoeintraege. Eigene Eintraege bleiben dabei erhalten'
                print 'backup'
                print '\t Erstellt eine Backupdatei zur Wiederherstellung der Datenbank. Diese Funktion ist nicht zur Weitergabe sondern zur Sicherung der Daten gedacht.'
                print '\t Per Backup erstellte Dateien sind nicht per Import einpflegbar!'
                print 'restore'
                print '\t Liest eine Backupdatei ein und fuellt die Datenbank mit diesen Daten'
                print '\t ACHTUNG! DABEI WIRD DIE GESAMTE DATENBANK UEBERSCHRIEBEN! Alle nicht im Backup enthaltenen Daten gehen verloren!'
                print 'exit, beenden'
                print '\t beendet dieses Programm'
                print 'credits'
                print '\t zeigt Informationen ueber dieses Programm an'
                print '- - -'
                print 'Mehrfachangaben durch , trennen oder Ranges angeben, z.B. 3-77'
                print 'Pokemon koennen nach Eingabe des Befehls oder direkt hinter den Befehl geschrieben werden'
                print '================================================'
                
            elif func == 'exit' or func == 'beenden':
                running = False
                pkview.close()
            elif 'zeige' in func or 'pr' in func:
                pkview.process_print_command(func)
            elif 'addloc' in func or 'neuerort' in func:
                pkview.process_addloc(func)
            elif 'removeloc' in func or 'rmloc' in func or 'loescheort' in func:
                pkview.process_rmloc(func)
            elif 'addinfo' in func or 'neueinfo' in func:
                pkview.process_addinfo(func)
            elif 'removeinfo' in func or 'rminfo' in func or 'loescheinfo' in func:
                pkview.process_rminfo(func)
            elif 'unsetcatch' in func or 'uct' in func or 'ungefangen' in func:
                pkview.process_ct_uct(func, 0)
            elif 'setcatch' in func or 'ct'in func or 'gefangen' in func:
                pkview.process_ct_uct(func, 1)
            elif 'credit' in func:
                pkview.credit()
            elif 'clear' in func:
                print "\33[2J"
            elif 'flausch' in func:    
                print "Aaaaw! *flausch* <3"
            elif 'add_pk' == func:
                nachfr = raw_input('>>')
                if nachfr == 'add_pk':
                    nr = raw_input('nr? > ')
                    name = raw_input('name? > ')
                    pkview.add_pk(nr, name)
            elif 'backup' == func:
                pkview.backup()
            elif 'restore' == func:
                pkview.restore()
            elif 'export' == func:
                pkview.export()
            elif 'import' == func:
                pkview.import_file()
            elif 'html' in func:
                pkview.create_html(func)
            else:
                print '"hilfe" hilft.'
    except KeyboardInterrupt:
        print 'Abbruch des Programms durch Ctrl+C.'
        print 'Das ist zwar unsanft, aber ich wuensche trotzdem einen schoenen Tag!'
        sys.exit(1)
            
run()
        
        
    
    
    
