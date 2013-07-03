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
""" Dieses Modul enthaelt alle Methoden, die Datenbankzugriffe vornehmen sowie jene, die Dateien schreiben oder lesen."""
import sqlite3
import re
import dat.pkview
import codecs
import html
import cgi

conn = sqlite3.connect('db/pkmmanager.db')
c = conn.cursor()


""" 
>>>>>>>>>
--------------------------------------------------------
------>> Methoden mit Datenbankzugriff <<------ 
--------------------------------------------------------
>>>>>>>>>
"""

""" 
--------------------------------------------------------
------>> Methoden mit lesendem Datenbankzugriff <<------ 
--------------------------------------------------------
"""

""" Ueberprueft die Existenz des angegebenen Pokemonnamen oder der angegebenen Nummer. Ist es existent, wird True zurueckgegeben, false sonst """
# TODO: Ueberpruefen, ob Implementierung sinnvoll (v.a. zweiter teil)
def valid_pk(pokemon):
    #holt die nr des pokemon, falls name angegeben
    if isinstance(pokemon, str ) and not pokemon.isdigit():
        pokemon = get_pknr(pokemon)
        if not pokemon:
            return False
    
    pokemon = (pokemon,)
    #Ermittung der Pokemoninformationen
    for row in c.execute('select nr from pokemon where nr = ?', pokemon):
        return True
    
    return False

""" Gibt eine Liste mit den Nummern aller Pokemon zurueck, die das angegebenen Namensfragment enthalten """
def get_pk_list_by_namesnippet(namesnippet):
    pkmns = []
    for row in c.execute("select nr from pokemon where name like '{0}%' ".format(namesnippet)):
        pkmns.append(row[0])
    
    return pkmns
    
""" Gibt die Nummer des Pokemon mit dem angegebenen Namen. 
Ist kein Pokemon mit dem Namen vorhanden oder wurde kein String angegeben, wird None zurueckgegeben. """
def get_pknr(pokemon):
    if isinstance(pokemon, str ) and not pokemon.isdigit():
        pokemon = pokemon.capitalize()
        pokemon = (pokemon,)
        for row in c.execute('select nr from pokemon where name = ?', pokemon):
            return row[0]
            
    return None

""" Gibt die Informationen eines Pokemon in 2 Tupeln zurueck. Das erste Element ist eine Liste mit Nummer, Name und Catched
Das zweite Element ist eine Liste, die wiederrum Listen mit edition und location enthaehlt """
def get_pkinfo(pokemon):

    #holt die nr des pokemon, falls name angegeben
    if isinstance(pokemon, str ) and not pokemon.isdigit():
        pokemon = get_pknr(pokemon)

    pkinfo = []
    locs = []   
    
    #pokemon muss in ein tupel umgewandelt werden, da die execute als argument ein tupel erwartet
    pokemon = (pokemon,)
    #Ermittung der Pokemoninformationen
    for row in c.execute('select nr, name, catched, infos from pokemon where nr = ?', pokemon):

        pkinfo = [row[0], row[1], row[2], row[3]]
        
        #Ermittlung der Location-Information
        nummer = (row[0],)
        for row2 in c.execute('select edition, location from locations where nr = ?', nummer):
            locs.append([row2[0], row2[1]])
                  
    return pkinfo, locs
    
""" Gibt eine Liste mit den Nummern der Pokemon zurueck, die auf die uebergebenen Argumente passen. """
def get_pk_list_by_args(args):
    g = ''
    ung = ''
    ort = ''
    info = ''
    rng = ''
    ed = ''
    loc = ''

    """ Fuer jedes Argument wird geprueft, um welches es sich handelt.
    Dann wird die vorbereitete Variable mit dem entsprechenden SQL-Abfragelement belegt, 
    welche das spaetere Ergebnis wie gewuenscht beeinflusst."""
    for arg in args:
        arg = arg.strip()
        if arg == 'g':
            g = ' catched = 1 '
        elif arg == 'ung':
            ung = ' catched = 0 '
        elif arg == 'ort' or arg == 'loc':
            ort = ' join locations on pokemon.nr = locations.nr'
        elif arg == 'info':
            info = ' infos is not null '
        elif 'rng' in arg:
            arg = arg.lstrip('rng')
            start, sep, end = arg.partition('to')
            rng = " pokemon.nr between '{0}' and '{1}' ".format(start, end)
        elif 'ed' in arg:
            ort = ' join locations on pokemon.nr = locations.nr'
            arg = arg.lstrip('ed')
            arg = arg.strip()
            ed = " locations.edition = '{0}' ".format(arg)
        elif 'loc' in arg or 'ort' in arg:
            ort = ' join locations on pokemon.nr = locations.nr'
            arg = arg.lstrip('loc')
            arg = arg.lstrip('ort')
            arg = arg.strip()
            loc = " locations.location like '%{0}%' ".format(arg)
    
    """ Falls sowohl -g als auch -ung uebergeben wurde, werden beide Variablen zurueckgesetzt, da die Ergebnismenge sonst leer waere
    (da catched nur einen Wert annehmen kann, beide jedoch und-verknuepft werden) """
    if g != '' and ung != '':
        g = ''
        ung = ''
    
    # Die Datenbankabfrage wird dann anhand der durch die Argumente vorgegebenen Fragmenten zusammengesetzt
    exc ='select pokemon.nr from pokemon'
    
    if ort != '':
        exc = exc + ort
    # Falls das Argument das erste ist, das an die Abfrage angefuegt wird, wird kein 'and' dazwischen benoetigt. 
    add_and = False;
    if g != '' or ung != '' or info != '' or ed != '' or loc != '' or rng != '':
        exc = exc + ' where '
        if g != '':
            if add_and:
                exc += ' and '
            exc += g
            add_and = True
        if ung != '':
            if add_and:
                exc += ' and '
            exc += ung
            add_and = True
        if info != '':
            if add_and:
                exc += ' and '
            exc += info
            add_and = True
        if rng != '':
            if add_and:
                exc += ' and '
            exc += rng
            add_and = True
        if ed != '':
            if add_and:
                exc += ' and '
            exc += ed
            add_and = True
        if loc != '':
            if add_and:
                exc += ' and '
            exc +=  loc
            add_and = True
            
    exc += ' order by pokemon.nr'
     
    result = []
    for row in c.execute(exc):  
        if row[0] not in result:
            result.append(row[0])
         
    return result
  
""" Gibt die Anzahl der fuer das uebergebene Pokemon hinterlegten Locationinformationen zurueck """  
def get_number_of_locs(pokemon):
    locs = 0
    #holt die nr des pokemon, falls name angegeben
    if isinstance(pokemon, str ) and not pokemon.isdigit():
        pokemon = get_pknr(pokemon)
    pokemon = (pokemon,)
    for row in c.execute('select * from locations where nr = ?', pokemon):
        locs += 1
        
    return locs
    
""" Gibt die fuer das uebergebene Pokemon hinterlegte Information zurueck """
def get_info(nr):
    for row in c.execute('select infos from pokemon where nr = ?', (nr,)):
        return row[0]

        
""" 
------------------------------------------------------------
------>> Methoden mit schreibenden Datenbankzugriff <<------ 
------------------------------------------------------------
"""


""" 
------>> Manipulation der Locationstabelle <<------ 
"""
 
 
"""Fuegt die uebergebene Edition, Locationinformation und Pokemonnummer in die Locationstabelle ein """
def add_loc(pokemon, edition, location):

    #holt die nr des pokemon, falls name angegeben
    if isinstance(pokemon, str ) and not pokemon.isdigit():
        pokemon = get_pknr(pokemon)
        
    edition = edition.upper()
    edition = edition.strip()
    location = location.strip()
    inserts = (pokemon, edition, location)
    c.execute('insert into locations (nr, edition, location) values (?,?,?)', inserts)
    
    conn.commit()
  
""" Entfernt den durch Nummer, Edition und Location spezifizierten Eintrag aus der Locationstabelle """  
def rm_loc(pokemon, edition, location):
    #holt die nr des pokemon, falls name angegeben
    if isinstance(pokemon, str ) and not pokemon.isdigit():
        pokemon = get_pknr(pokemon)
        

    inserts = (pokemon, edition, location)  
    c.execute('delete from locations where nr=? and edition=? and location=?', inserts)

    conn.commit()
 
""" Entfernt alle zu der uebergebenen Pokemonnummer gehoerenden Eintraege aus der Locationstabelle """ 
def rm_all_loc(pokemon):
    #holt die nr des pokemon, falls name angegeben
    if isinstance(pokemon, str ) and not pokemon.isdigit():
        pokemon = get_pknr(pokemon)
        

    inserts = (pokemon,)  
    c.execute('delete from locations where nr=?', inserts)

    conn.commit()

    
""" 
------>> Manipulation der Pokemontabelle <<------ 
"""    
    
""" Fuegt die ubergebene Information bei der uebergebenen Nummer ein. Eventuell vorhandene Eintraege werden dabei ueberschrieben. """    
def set_info(pokemon, info):
    #holt die nr des pokemon, falls name angegeben
    if isinstance(pokemon, str ) and not pokemon.isdigit():
        pokemon = get_pknr(pokemon)
    inserts = (info, pokemon)
    c.execute('update pokemon set infos=? where nr=?', inserts)

    conn.commit()
 
""" Loescht die fuer das uebergebene Pokemon hinterlegte Information, indem sie mit null ueberschrieben wird """ 
def rm_info(pokemon):
    set_info(pokemon, None) 

""" Setzt den Catchwert des uebergebenen Pokemons (Nr oder Name) auf den uebergebenen Wert, wobei dieser 0 fuer ungefangen oder 1 fuer gefangen entsprechen sollte. """
def set_c(pokemon, catch):
    #holt die nr des pokemon, falls name angegeben
    if isinstance(pokemon, str ) and not pokemon.isdigit():
        pokemon = get_pknr(pokemon)
    """ Falls ein String angegeben wird, wird '0' als 0 (ungefangen) und '1' als 1 (gefangen) interpretiert. 
    Alles andere fuehrt zu einem Verlassen der Methode, damit der Wert nicht geaendert wird. """
    if isinstance(catch, str ) and not catch.isdigit():
        if catch == '1':
            catch = 1
        elif catch == '0':
            catch = 0;
        else:
            return
            
    inserts = (catch, pokemon)
    c.execute('update pokemon set catched=? where nr=?', inserts)
    
    conn.commit()

""" Fuegt ein neues Pokemon mit Nummer und Name in die Datenbank ein.

Die Methode ist zum Debuggen da - im Normalfall sollte ein Einfuegen von Pokemondaten nicht noetig sein.
Zur Aktivierung add_pk in die Konsole eingeben, auf >>> erneut add_pk, dann Nummer und Pokemonname  """
def add_pk(nr, name):
    inserts = (nr, name)
    c.execute('insert into pokemon (nr, name) values (?,?)', inserts)
        
    conn.commit()    
    

""" 
------>> Manipulation beider Tabellen <<------ 
"""

  
"""Liest die Informationen der Backupdatei ein, loescht vorhandene Informationen aus der Datenbank 
und traegt die eingelesenen Informationen ein. """
#TODO: Nur in der backupdatei vorhandene Nummern werden resettet. Eventuell komplettes Leerraeumen der DB einpflegen?
def restore(filename):
    if not check_if_restorefile(filename):
        return
    file = open(filename, "r")
    #Die erste Zeile dient zur Kennzeichnung des Dateityps und ist ohne informatielle Relevanz
    file.readline()
    while (True): 
        line = file.readline()
        if (re.match(r"[0-9]+ [01]", line) != None):
            #Die erste Informationszeile enthaelt die Pokedexnummer sowie den Catchstatus
            nr, catched = line.split(" ")
            catched = catched.strip()
            set_c(nr, catched)
            # Gibt der View Rueckmeldung, welche Pokemoninformationen gerade verarbeitet werden.
            dat.pkview.announce_restore_state(nr)
            
            line = file.readline()
            #Die zweite Zeile enthaelt die Info oder ist leer, falls keine Info eingetragen war
            info = line.strip()
            rm_info(nr)
            if info != '':
                set_info(nr, info)
            rm_all_loc(nr)
            #Alle darauffolgenden eingerueckten Zeilen enthalten Edition und Fundort
            line = file.readline()
            while (re.match(r"\t .*", line) != None):
                loc = line.strip()
                ed, loc = loc.split(' ', 1)
                add_loc(nr, ed, loc)
                line = file.readline()
        # Ist die Line komplett leer, ist die Datei zuende und die Schleife wird abgebrochen.
        elif not line:
            break
        #Sollte eine Zeile nicht als Pokemonidentifikation validiert werden koennen (kein Einsteigen in das if) wird die naechste 
        #Zeile eingelesen und die fehlerhafte Zeile ignoriert, damit es zu keiner Endlosschleife kommt.
        else:
            line = file.readline()
            
    file.close()
    conn.commit()

""" Liest und verarbeitet die Informationen aus der uebergebenen, per Export erstellten Datei. """
def import_data(filename):
    file = open(filename, "r")
    ifinfos = file.readline()
    ifinfos = ifinfos.strip()
    # Entspricht die erste Zeile weder True noch False, ist dies keine valide Exportdatei und es wird abgebrochen.
    if not ifinfos == "True" and not ifinfos == "False":
        return None;
    line = file.readline()
    pkmns = []
    while (True): 
        # Die Reihenfolge der Daten ist: Nummer \n Info \n Edition und Location (mehrfach)
        if (re.match(r"[0-9]+", line) != None):  
            #Die Nummer wird fuer die folgenden Abfragen ausgelesen und gespeichert
            nr = line.strip()
            pkmns.append(nr)
            line = file.readline()
            # Falls es sich um einen Export mit Info handelt, ist die folgende Zeile die Info
            if ifinfos == "True":
                info = line.strip()
                # Falls eine Info angegeben, wird sie durch ein // getrennt an die bestehende angehaengt
                if info != '':
                    info = (get_info(nr) if get_info(nr) != None else "") + " // " + info
                    set_info(nr, info)
                line = file.readline()
            # Alle folgenden Editionen und Locations werden ausgelesen und eingetragen
            while (re.match(r"\t .*", line) != None):
                loc = line.strip()
                ed, loc = loc.split(' ', 1)
                add_loc(nr, ed, loc)
                line = file.readline()
        #Bricht die Schleife beim Dateiende ab
        elif not line:
            break
        #Sollte eine Zeile nicht als Pokemonidentifikation validiert werden koennen (kein Einsteigen in das if) wird die naechste 
        #Zeile eingelesen und die fehlerhafte Zeile ignoriert, damit es zu keiner Endlosschleife kommt.
        else:
            line = file.readline()
    file.close()
    conn.commit()
    return pkmns;
    
    
""" 
>>>>>>>>>
------------------------------------------------------------------------
------>> Validierende/Ueberpruefende Methoden (ohne DB-Zugriff) <<------ 
------------------------------------------------------------------------
>>>>>>>>>
"""


""" Ueberprueft, ob das uebergebene Argument bekannt, also valide ist. 
Falls ja, wird True zurueckgegeben, sonst False. """
def is_known_arg(arg):
    valid = False
    if arg == 'g':
        valid = True
    elif arg == 'ung':
        valid = True
    elif 'ort' in arg:
        valid = True
    elif arg == 'info':
        valid = True
    elif 'rng' in arg:
        valid = True
    elif 'ed' in arg:
        valid = True
    elif 'loc' in arg:
        valid = True
        
    return valid
 
""" Ueberprueft anhand der ersten Zeile, ob die Datei eine per Backuperstellte Backupdatei ist. """ 
def check_if_restorefile(filename):
    file = open(filename, "r")
    firstline = file.readline()
    if (firstline == '\t rst \t \t\n'):
        return True
    else:
        return False


""" 
>>>>>>>>>
---------------------------------------------
------>> Datei schreibende Methoden <<------ 
---------------------------------------------
>>>>>>>>>
"""


""" Erstellt eine Backupdatei, in der alle in der Datenbank gespeicherten, vom User eintragbaren Informationen + 
der Pokemonnummer als Identifier enthalten sind. Sie eignet sich daher zur vollstaendigen Wiederherstellung der Datenbank """
def create_backup(filename):
    # Holt alle PKMN mit Nr, Catched und Info
    pkmns = []
    for row in c.execute('select distinct pokemon.nr, pokemon.catched, pokemon.infos from pokemon order by pokemon.nr'):
        info = ("" if row[2] == None else row[2])
        pkmns.append([row[0], row[1], info])
    backup = open(filename, "w")
    # Die erste Zeile dient zur Identifizierung der Datei und wird beim Wiedereinlesen ueberprueft
    backup.write('\t rst \t \t\n')
    for pkmn in pkmns:
        backup.write(u"{0} {1}\n\t{2}\n".format(pkmn[0], pkmn[1], pkmn[2]))
        for row in c.execute('select edition, location from locations where nr = ?', (pkmn[0],)):
            backup.write(u"\t {0} {1}\n".format(row[0], row[1]))
        backup.write(u" \n")
    backup.close()
    
""" Erstellt eine Exportdatei mit allen Pokemonnummern, die min. eine Location gespeichert haben und allen hinterlegten Locations. 
Je nach uebergebenen Wert werden zu diesen Pokemon die Informationen ebenfalls exportiert. """  
#TODO: Im Falle des Mitexports von Informationen auch Pokemon ohne Location aber mit Info mitexportieren
#TODO: Nur bestimmte Pokemon (per Range) exportieren?
def export(filename, info):
    # jenachdem, ob die info mitgespeichert wird, werden andere informationen gelesen und geschrieben
    if (info):
        q = 'select distinct pokemon.nr, pokemon.infos from pokemon join locations on pokemon.nr = locations.nr order by pokemon.nr'
        # Holt alle PKMN mit Nr und Info, fuer die Locations gespeichert sind
        pkmns = []
        for row in c.execute(q):
            info = ("" if row[1] == None else row[1])
            pkmns.append([row[0], info])
        #oeffnet die datei und schreibt die infos und locations
        backup = open(filename, "w")
        #vermerkt, das dies eine export mit infos ist
        backup.write("True\n")
        for pkmn in pkmns:
            backup.write("{0}\n \t{1} \n".format(pkmn[0], pkmn[1]))
            for row in c.execute('select edition, location from locations where nr = ?', (pkmn[0],)):
                backup.write("\t {0} {1}\n".format(row[0], row[1]))
        backup.close()
    else:
        q = 'select distinct pokemon.nr from pokemon join locations on pokemon.nr = locations.nr order by pokemon.nr'
        # Holt alle PKMN mit Nr, fuer die Locations gespeichert sind
        pkmns = []
        for row in c.execute(q):
            pkmns.append(row[0])
        #oeffnet die datei und screibt die infos und locations
        backup = open(filename, "w")
        #vermerkt, das dies eine export ohne infos ist
        backup.write("False\n")
        for pkmn in pkmns:
            backup.write("{0}\n".format(pkmn))
            for row in c.execute('select edition, location from locations where nr = ?', (pkmn,)):
                backup.write("\t {0} {1}\n".format(row[0], row[1]))
        backup.close()

 

"""Erstellt eine HTML, die in formatierter Weise das Ergebnis der print Abfrage enthaelt """
def create_html(pkmns, args):
    
    args = args.split('-')
    #args = args [1:]
    filename = "pokemon"
    for arg in args:
        filename += "_{0}".format(arg)
    filename += ".html"
    file = codecs.open(filename, "w", encoding="utf-8")
    file.writelines(("<!doctype html> \n","<html> \n","<head><link href='dat/style.css' type='text/css' rel='stylesheet'></head> \n","<body> \n"))
    for pk in pkmns:
        pkinfos, locs = get_pkinfo(pk)
        name = make_html_compatible(pkinfos[1])
        catch = "1.png" if pkinfos[2] == 1 else "0.png"
        file.write("<h1><img src='dat/{2}' alt='{3}' class='ct'> {0} {1}</h1>\n".format(pkinfos[0], name, catch, pkinfos[2]))
        if pkinfos[3] != None:
            info = make_html_compatible(pkinfos[3])
            file.write("\t<div class='info'><span class='infoi'>i</span> {0} </div>\n".format(info))
        if get_number_of_locs(pkinfos[0]) > 0:
            file.write("\t<table class='locs'>\n")
            for loc in locs:
                ed = make_html_compatible(loc[0])
                loc = make_html_compatible(loc[1])
                file.write("\t\t<tr><td><b>{0}</b> </td><td>{1}</td></tr>\n".format(ed, loc))
            file.write("\t</table>\n")
    file.writelines(("</body> \n", "</html>"))
    file.close()

def make_html_compatible(string):
    string = cgi.escape(string).encode('ascii', 'xmlcharrefreplace')
    string = string.decode('unicode-escape')

    
    return string

""" 
>>>>>>>>>
-----------------------------------------------
------>> Datenbankverwaltende Methoden <<------ 
-----------------------------------------------
>>>>>>>>>
"""
    
    
    
def close():
    conn.commit()
    c.close()
    conn.close()
        
        
        
    
    
    
