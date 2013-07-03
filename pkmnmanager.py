#!/usr/bin/python
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
import sys, os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import dat.pkview as pkview



def __main():
    run()
    
def run():

    running = True
    print("=====================================================")
    print( 'Willkommen im Pokemonmanager V{0}!'.format(pkview.ver))
    print( 'pr/print Ausgabe der Pokemon')
    print( 'addloc/addinfo rmloc/rminfo Hinzufügen/Entfernen von Fundorten/Info')
    print( 'exit Programm beenden')
    print( 'help ausfuehrliche Hilfe'  )
    print( '=====================================================')
    
    try:
        while(running):
            func = input(' >> Was moechten Sie tun? > ')
            
            if func == 'h' or func == "help" or func == 'hilfe':
                print( '=====================================================')
                print( 'Sie befinden sich im Pokemonmanager V{0}!'.format(pkview.ver))
                print( '- - -')
                print( 'print, pr, zeige')
                print( '\t gibt Daten nach Parametern gefiltert aus. \n\t Fuer alle Pokemon bei Nachfrage Enter druecken.')
                print( '\t Fuer bestimmte Pokemon Nummer, Range oder Namen(sfragment) angeben')
                print( '\t -g/-ung alle gefangenen/ungefangenen Pokemon')
                print( '\t -info alle Pokemon mit eingetragener Info')
                print( '\t -ed<...> alle Pokemon mit angegeber Edition , z.B.: -edHG')
                print( '\t -loc<...>/-ort<...> alle Pokemon mit angegebem Fundort,\n\t z.B.: -locRoute 24')
                print( '\t Falls kein Ort angegeben, werden alle mit Ortinfo ausgegeben')
                print( '\t -rng alle Pokemon in der Zahlenrange. Start und Ende werden \n\t durch "to"  getrennt, z.B.: -rng1to150')
                print( '\t Die Parameter sind auch kombinierbar.')
                print( 'addloc, neuerort')
                print( '\t fuegt einen Fundort aus Edition und Fundort zum Pokemon hinzu.')
                print( 'rmloc, loescheort')
                print( '\t loescht einen oder alle Fundorte')
                print( 'addinfo, neueinfo ')
                print( '\t fuegt eine Notiz zum Pokemon hinzu.')
                print( 'rminfo, loescheinfo')
                print( '\t loescht die Notiz zum Pokemon.')
                print( 'setcatched, ct, gefangen ')
                print( '\t markiert ein oder mehrere Pokemon als gefangen.')
                print( 'unsetcatched, uct, ungefangen')
                print( '\t markiert ein oder mehrere Pokemon als nicht gefangen.')
                print( 'html')
                print( '\t Erstellt eine HTML-Datei mit dem Suchergebnis. \n\t Es sind die gleichen Filteroptionen wie bei print verfügbar.')
                print( 'export')
                print( '\t exportiert die Fundorte und ggf. die Infos zur Weitergabe')
                print( 'import')
                print( '\t Importiert per "export" erstellte Einträge. \n\t Eigene Einträge bleiben dabei erhalten.')
                print( 'backup')
                print( '\t Erstellt eine Backupdatei zur Wiederherstellung der Datenbank. \n\t Diese Funktion ist nicht zur Weitergabe \n\t sondern zur Sicherung der Daten gedacht.')
                print( 'restore')
                print( '\t Liest eine Backupdatei ein und fuellt die Datenbank mit diesen Daten')
                print( '\t ACHTUNG! DABEI WIRD DIE GESAMTE DATENBANK ÜBERSCHRIEBEN! \n\t Alle nicht im Backup enthaltenen Daten gehen verloren!')
                print( 'exit, beenden')
                print( '\t beendet dieses Programm')
                print( 'credits')
                print( '\t zeigt Informationen ueber dieses Programm an')
                print( '- - -')
                print( 'Mehrfachangaben durch , trennen oder Ranges angeben, z.B. 1,2,3 oder 3-77')
                print( 'Pokemon können direkt hinter dem Befehl angegeben werden')
                print( '- - -')
                print( 'Für eine ausführlichere Hilfe beachten Sie bitte die readme.txt')
                print( '=====================================================')
                
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
                print( "\33[2J")
            elif 'flausch' in func:    
                print( "Aaaaw! *flausch* <3")
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
                print( '"hilfe" hilft.')
    except KeyboardInterrupt:
        print( 'Abbruch des Programms durch Ctrl+C.')
        print( 'Das ist zwar unsanft, aber ich wuensche trotzdem einen schoenen Tag!')
        sys.exit(1)
            
run()
        
        
    
    
    
