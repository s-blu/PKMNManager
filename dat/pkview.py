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

#from gi.repository import Gtk
import sqlite3
import dat.pkdao as pkdao
import re

ver = '0.5'



""" 
>>>>>>>>>
---------------------------------------------------------
------------->> Methoden des Printcommand <<------------- 
---------------------------------------------------------
>>>>>>>>>
"""

""" 
--------------------------------------------------------
------>> Methoden, die den Befehl verarbeiten <<------ 
--------------------------------------------------------
"""


""" Verarbeitet den printcommand. Ueberprueft, ob Parameter oder Pokemon angegeben wurden, fordert uU eine Pokemonangabe an und stoesst den Printvorgang an.
arguments sollte hier ein String sein, der der Konsoleneingabe des printcommands entspricht. """
def process_print_command(arguments):
    # Die erste Angabe fuehrte zum Aufruf der Methode (und ist damit pr oder zeige) und hat keine Relevanz mehr
    # Daher wird sie hier entfernt
    arguments = arguments.split(' ', 1)
    # Der Aufruf [1:] entfernt das erste von beiden Elementen aus der Liste, belässt arguments aber als Liste und 
    # wandelt es nicht in String um, wie [1] es tun würde
    arguments = arguments[1:]
    if len(arguments) > 0:
        if arguments[0].startswith('-'):
            print_pokemon_by_args(arguments[0])
        else:
            print_pokemon(arguments[0])
    else:
        pokem = input('Welches Pokemon? > ')
        if pokem == '' or pokem == 'all':
            print_pokemon_by_args('')
        else:
            print_pokemon(pokem)

""" Stösst die Ausgabe von ein, mehrere oder allen Pokemon an. Validiert Existenz und gibt ggf. Fehlermeldungen aus. """
def print_pokemon(pokem):
    if isinstance(pokem, str):
        pkms = create_list(pokem)
        
        if len(pkms) == 0 :
            print("Ungueltiges Pokemon '{0}'".format(pokem))
            return
        
        for pokemon in pkms:
            if not pkdao.valid_pk(pokemon):
                print("Ungueltiges Pokemon '{0}'".format(pokemon))
            else:
                print_output(pokemon)
                
        
    #Ist das Pokemon ein int-Wert, wurde es im vorherigen Programmverlauf bereits auf Gueltigkeit geprueft.
    elif isinstance(pokem, int):
        print_output(pokem)
  
""" Stoesst die Ausgabe der Pokemon an, auf die die Argumente passen """
def print_pokemon_by_args(arguments): 
    list = get_pklist_by_args(arguments)
    
    if len(list) > 100:
        dispall = input('Moechten Sie alle {0} Pokemon anzeigen lassen? Y/no > '.format(len(list)+1))
        if dispall == 'no' or dispall == 'n':
            return
            
    for pk in list:
        print_pokemon(pk)
        
""" Erzeugt die Ausgabe eines einzelnen Pokemon auf der Konsole. Als Argument wird Nummer oder Name des Pokemon erwartet """
def print_output(pokemon):
    pkinfo, locs = pkdao.get_pkinfo(pokemon)
            
    catch = " ( ) "
    if pkinfo[2] != 0:
        catch = "gefangen!"
    
    info = ''
    if pkinfo[3] != None:
        info = "Info: '{0}'".format(pkinfo[3])
    
    print("{0} {1},\t {2} \t {3}".format(pkinfo[0], pkinfo[1], catch, info))

    if len(locs) > 0:
        print("\t - - - - - - - - - - - - - -")
    for loc in locs:
        print("\t Fangbar in {0}, {1}".format(loc[0], loc[1]))
    if len(locs) > 0:
        print("\t - - - - - - - - - - - - - -")
        
""" 
-----------------------------------------------------------------
------>> Methoden, die die betroffenen Pokemon ermitteln <<------ 
-----------------------------------------------------------------
"""        
  
  
""" Vearbeitet die Listen oder Rangeangabe und erstellt eine Int-Range oder eine Stringliste der betroffenen Pokemonnummern bzw. -Namen anhand der uebergebenen Pokemonangaben. """  
def create_list(pks):

    pkms = []

    if re.match('[\w]+[-][\w]+', pks) != None:
        start, end = pks.split('-')
        if re.match('[0-9]+[-][0-9]+', pks) != None:
            pkms = range(int(start), int(end)+1)
        else:
            if not pkdao.valid_pk(start):
                print("Ungueltiges Pokemon '{0}'".format(start))
            elif not pkdao.valid_pk(start):
                print("Ungueltiges Pokemon '{0}'".format(end))
            else:
                start = pkdao.get_pknr(start)
                end = pkdao.get_pknr(end)
                pkms = range(int(start), int(end)+1)
    elif ',' in pks:
        pkms = pks.split(',')
        
        for i in range (0, len(pkms)):
            pk = pkms[i]
            pk = pk.strip()
            pk = pk.capitalize()
            
            pkms[i] = pk
    elif re.match('[0-9]+', pks) != None:
        pkms.append(pks)
    else:
        pkms = pkdao.get_pk_list_by_namesnippet(pks)
        
    return pkms

""" Erstellt eine Liste mit allen Pokemonnummern, auf die die Argumente passen. Bei unbekannten Parametern wird eine Fehlermeldung ausgegeben und abgebrochen. """    
def get_pklist_by_args(arguments):
    arguments = arguments.split('-')
    arguments = arguments [1:]

    for arg in arguments:
        arg = arg.strip()
        if not pkdao.is_known_arg(arg):
            print("Unbekannter Parameter '{0}'".format(arg))
            return

    return pkdao.get_pk_list_by_args(arguments)
 

""" 
>>>>>>>>>
---------------------------------------------------------
------------->> Methoden fuer addloc/rmloc <<------------- 
---------------------------------------------------------
>>>>>>>>>
"""


""" Verarbeitet den addloc-command. Wenn die direkte Pokemonangabe hinter dem Befehl fehlt, wird abgefragt. """
def process_addloc(arguments):
    arguments = arguments.split(' ', 1)
    arguments = arguments [1:]
    if len(arguments) > 0:
        add_location(arguments[0])
    else:
        pokem = input('Pokemonnr oder -name? > ')
        add_location(pokem)      
        
""" Fragt Edition und Fundort ab. Fuegt den angegebenen Pokemon eine Location, also einen Fundort, bestehend aus Edition und Fundort, hinzu """
def add_location(pokem):
    edition = input('Welche Edition? > ')
    location = input('Welche Location? > ')
    
    pkms = create_list(pokem)
    invalidpk = 0
    for pokemon in pkms:
        if not pkdao.valid_pk(pokemon):
            print("Ungueltiges Pokemon '{0}'".format(pokemon))
            invalidpk += 1
        else:
            pkdao.add_loc(pokemon, edition, location)
            
            print_pokemon(pokemon)
    if invalidpk < len(pkms):        
        moreinput = input("Moechten Sie mehr Daten einpflegen? yes/N > ")
        moreinput = moreinput.lower()
        
        while moreinput == 'yes' or moreinput == 'y':
            edition = input('Welche Edition? > ')
            loc = input('Welche Location? > ')
        
            for pokemon in pkms:
                if not pkdao.valid_pk(pokemon):
                    print("Ungueltiges Pokemon '{0}'".format(pokemon))
                else:
                    pkdao.add_loc(pokemon, edition, loc)
                    print_pokemon(pokemon)
            moreinput = input("Moechten Sie mehr Daten einpflegen? yes/N > ")
            moreinput = moreinput.lower()
  

    
""" Verarbeitet den rmloc-command. Wenn die direkte Pokemonangabe hinter dem Befehl fehlt, wird abgefragt. """
def process_rmloc(arguments):
    arguments = arguments.split(' ', 1)
    arguments = arguments [1:]
    if len(arguments) > 0:
        rm_location(arguments[0])
    else:
        pokem = input('Pokemonnr oder -name? > ')
        rm_location(pokem)      
 
""" Erfragt Informationen zu den loeschenden Locationangaben. 
Loescht die Locationangaben der uebergebenen Pokemon. 
Bei ungueltigen Pokemon oder Pokemon ohne Locationeintrag wird eine Fehlermeldung erzeugt. """
def rm_location(pokem):
    pkms = create_list(pokem)
    
    invalidpk = 0
    for pokemon in pkms:
        if not pkdao.valid_pk(pokemon):
            print("Ungueltiges Pokemon '{0}'".format(pokemon))
            invalidpk += 1
        else:
            if pkdao.get_number_of_locs(pokemon) == 0:
                print("Fuer Pokemon '{0}' existieren keine Locationangaben".format(pokemon))
                invalidpk += 1
            else:
                print_pokemon(pokemon)
    
    if invalidpk < len(pkms):
        rmall = input('Sollen alle Eintraege geloescht werden? yes/N > ')
        rmall = rmall.lower()
        if rmall == 'yes' or rmall == 'y':
            for pokemon in pkms:
                pkdao.rm_all_loc(pokemon)
                print_pokemon(pokemon)
            
        else:
            print('Spezifizieren Sie bitte den Eintrag der geloescht werden soll.')
            edition = input('Loeschen: Welche Edition? > ')
            location = input('Loeschen: Welche Location? > ')
            for pokemon in pkms:
                pkdao.rm_loc(pokemon, edition, location)
                print_pokemon(pokemon)
                          
            morerm = input("Moechten Sie mehr Daten loeschen? yes/N > ")
            morerm = morerm.lower()
            
            while morerm == 'yes' or morerm == 'y':
                edition = input('Loeschen: Welche Edition? > ')
                location = input('Loeschen: Welche Location? > ')
                for pokemon in pkms:
                    pkdao.rm_loc(pokemon, edition, location)
                    print_pokemon(pokemon)
                morerm = input("Moechten Sie mehr Daten loeschen? yes/N > ")
                morerm = morerm.lower()

                
""" 
>>>>>>>>>
------------------------------------------------------------
------------->> Methoden fuer addinfo/rminfo <<------------- 
------------------------------------------------------------
>>>>>>>>>
"""


""" Verarbeitet den addinfo-command. Wenn die direkte Pokemonangabe hinter dem Befehl fehlt, wird abgefragt. """   
def process_addinfo(arguments):
    arguments = arguments.split(' ', 1)
    arguments = arguments [1:]
    if len(arguments) > 0:
        set_info(arguments[0])
    else:
        pokem = input('Pokemonnr oder -name? > ')
        set_info(pokem) 

""" Erfragt die einzutragende Information, traegt sie fuer die uebergebenen Pokemon ein und gibt bei ungueltigen Pokemon eine Fehlermeldung zurueck"""
def set_info(pokem):
    info = input('Info? > ')
    pkms = create_list(pokem)
    
    for pokemon in pkms:
        if not pkdao.valid_pk(pokemon):
            print("Ungueltiges Pokemon '{0}'".format(pokemon))
        else:
            pkdao.set_info(pokemon, info)
            print_pokemon(pokemon)
    
""" Verarbeitet den rminfo-command. Wenn die direkte Pokemonangabe hinter dem Befehl fehlt, wird abgefragt. """   
def process_rminfo(arguments):
    # Die erste Angabe fuehrte zum Aufruf der Methode (und ist damit pr oder zeige) und hat keine Relevanz mehr
    # Daher wird sie hier entfernt
    arguments = arguments.split(' ', 1)
    # Der Aufruf [1:] entfernt das erste von beiden Elementen aus der Liste, belässt arguments aber als Liste und 
    # wandelt es nicht in String um, wie [1] es tun würde
    arguments = arguments[1:]
    if len(arguments) > 0:
        rm_info(arguments[0])
    else:
        pokem = input('Von welchem Pokemon wollen Sie die Info loeschen? > ')
        rm_info(pokem) 
  
""" Loescht die Information der uebergebenen Pokemon. Ist ein Pokemon ungueltig, wird eine Fehlermeldung zurueckgegebe. """  
def rm_info(pokem):
    pkms = create_list(pokem)
    for pokemon in pkms:
        if not pkdao.valid_pk(pokemon):
            print("Ungueltiges Pokemon '{0}'".format(pokemon))
        else:
            pkdao.rm_info(pokemon)
            print_pokemon(pokemon)
  
""" 
>>>>>>>>>
------------------------------------------------------
------------->> Methoden fuer ct / uct <<------------- 
------------------------------------------------------
>>>>>>>>>
"""
  
  
""" Verarbeitet den ct- und uct-command. Wenn die direkte Pokemonangabe hinter dem Befehl fehlt, wird abgefragt. """    
def process_ct_uct(arguments, catched):
    arguments = arguments.split(' ', 1)
    arguments = arguments [1:]
    if len(arguments) > 0:
        set_c(arguments[0], catched)
    else:
        pokem = input('Pokemonnr oder -name? > ')
        set_c(pokem, catched) 
  
""" Setzt den Catchwert der uebergebenen Pokemon auf 1 fuer gefangen oder 0 fuer ungefangen """
def set_c(pokem, catched):
    if catched == 1:
        print('Herzlichen Glueckwunsch zum Fangerfolg! :)')
    pkms = create_list(pokem)
    
    for pokemon in pkms:
        if not pkdao.valid_pk(pokemon):
            print("Ungueltiges Pokemon '{0}'".format(pokemon))
        else:
            pkdao.set_c(pokemon, catched)
            print_pokemon(pokemon)
            
           
""" 
>>>>>>>>>
-----------------------------------------------------------
------------->> Methoden zum Dateischreiben <<------------- 
-----------------------------------------------------------
>>>>>>>>>
"""            
 
""" Fragt den Dateinamen fuer die Backupdatei nach und stoesst das Dateischreiben an. """ 
def backup():
    filename = input('Wie soll die Backupdatei heissen? > ')
    pkdao.create_backup(filename)
  
""" Macht Confirmnachfrage und validiert die Backupdatei. Macht ggf. Fehlermeldung, stoesst sonst den Restorevorgang an. """
def restore():
    confirm = input('Sind Sie sich sicher, das sie die Datenbank wiederherstellen wollen? \n Alle Daten, die nicht in der Backupdatei enthalten sind, gehen verloren! \n Die Wiederherstellung nimmt einige Zeit in Anspruch. \n Tippen Sie YES, wenn sie sich sicher sind. > ')
    if confirm == 'YES':
        filename = input('Aus welcher Datei soll die Datenbank wiederhergestellt werden? > ')
        if (check_filename(filename)):
            if (pkdao.check_if_restorefile(filename)):
                pkdao.restore(filename)
            else:
                print('Diese Datei ist keine Backupdatei. Bitte beachten Sie, das nur Dateien, die mit dem Befehl backup erstellt wurden, verwendet werden duerfen')
        else: 
            print('Die uebergebene Datei ist nicht existent')
    else:
        print('Eingabe entspricht nicht YES, Wiederherstellungsvorgang wird abgebrochen.')

""" Fragt nach, ob Infos mit exportiert werden sollen und stoesst das Dateischreiben an. """   
#TODO: Dateinamenabfrage     
def export(): 
    info = input('Moechten Sie die Infos mit exportieren? Y/no > ').lower()
    if info == 'no' or info == 'n':
        pkdao.export(False)
    else:
        pkdao.export(True)
    print("Export war erfolgreich!")
""" Fragt Dateinamen, aus dem importiert werden soll, nach, ueberpruft dessen Gueltigkeit und stoesst den Import an. Stoesst ausserdem bei Erfolg die 
Ausgabe der durch den Importvorgang betroffenen Pokemon an. """ 
def import_file():
    file = input('Aus welcher Datei soll importiert werden? > ')
    if (check_filename(file)):
        print('Bitte warten....')
        success = pkdao.import_data(file)
        if (success != None):
            print('Import war erfolgreich!')
            for pk in success:
                print_output(pk)
        else:
            print('Der Import konnte nicht durchgefuehrt werden.')
    else:
        print('Die uebergebene Datei ist nicht existent')

""" Gibt die betroffenen Pokemon aus und ueberprueft, ob die Abfrage leer ist. Falls nicht, wird eine Bestaetigung erbeten und das Dateischreiben angestossen. """
def create_html(arguments):
    list = get_pklist_by_args(arguments)
    if len(list) == 0:
        print("Diese Abfrage enhaelt keine Ergebnisse. HTML wird nicht erstellt.")
        return;
    process_print_command(arguments)
    htmlconfirm = input('Moechten Sie diese Abfrage als HTML speichern? Y/no > ').lower()
    if htmlconfirm != 'n' and htmlconfirm != 'no':
        pkdao.create_html(list, arguments)        

        
""" 
>>>>>>>>>
--------------------------------------------------------------------
------------->> Validierende Methoden, sonstige Ausgaben <<------------- 
--------------------------------------------------------------------
>>>>>>>>>
"""  

""" Ueberprueft, ob die Datei mit uebergebenen Namen existiert und sich oeffnen laesst. """         
def check_filename(name):
    try: 
        file = open(name, "r") 
        file.close()
        return True;
    except IOError:
        return False;


""" Ermoeglicht eine Konsolenangabe, wie weit der Restoreprozess ist. Wird aus pkdao aufgerufen. """        
def announce_restore_state(nr):
    print('Wiederherstellung laeuft... Pokemon Nr. {0}'.format(nr))

""" Fuegt ein neues Pokemon mit Nummer und Name in die Datenbank ein.

Die Methode ist zum Debuggen da - im Normalfall sollte ein Einfuegen von Pokemondaten nicht noetig sein.
Zur Aktivierung add_pk in die Konsole eingeben, auf >>> erneut add_pk, dann Nummer und Pokemonname  """    
def add_pk(nr, name):
    pkdao.add_pk(nr, name)
    
""" Verarbeitet den Befehl credit und gibt die Credits aus. """    
def credit():
    print( '- - - Credits - - -')
    print( 'Pokemonmanager V{0}'.format(ver))
    print( 'Dient zur Unterstuetzung beim Komplettieren des eigenen Pokedex')
    print( 'Dies ist kein Pokedex! Sondern ein Fundort/Info/Gefangen-nichtgefangen Manager')
    print( 'Neuste unterstuetzte Pokemonversion: schwarz/weiss')
    print( 'Geschrieben von Sam B. <sam(at)s-blu.de>')
    print( 'Anfang Juli 2012 gestartetes Projekt in Python')
    print( 'Ein sparkling Flausch an Tsurai fuers Testen <3')
    print( '- - - - - - - - -')
    
def close():
    pkdao.close()
        
        
    
    
    
