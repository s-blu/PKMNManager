#!/usr/bin/env python
# -*- coding: utf -8 -*-
#Copyright 2012 sam@s-blu.de
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
import re

conn = sqlite3.connect('db/pkmmanager.db')
c = conn.cursor()


# Gibt die Informationen eines Pokemon in 2 Tupeln zurueck. Das erste Tupfel ist eine Liste mit Nummer, Name und Catched
# Das zweite Tupel ist eine Liste, die wiederrum Listen mit edition und location enthaehlt
def get_pkinfo(pokemon):

    #holt die nr des pokemon, falls name angegeben
    if isinstance(pokemon, str) and not pokemon.isdigit():
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
    
def valid_pk(pokemon):
    #holt die nr des pokemon, falls name angegeben
    if isinstance(pokemon, str) and not pokemon.isdigit():
        pokemon = get_pknr(pokemon)
        if pokemon == False:
            return False
    
    pokemon = (pokemon,)
    #Ermittung der Pokemoninformationen
    for row in c.execute('select nr from pokemon where nr = ?', pokemon):
        return True
    
    return False
   
#prueft, ob uebergebene argumente existieren   
def get_pk_is_known_arg(arg):
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
    
#gibt eine liste aller pokemon mit angegebenen namensfragment  
def get_pk_by_name(pokemon):
    pkmns = []
    #pokemon = (pokemon,)
    for row in c.execute("select nr from pokemon where name like '{0}%' ".format(pokemon)):
        pkmns.append(row[0])
    
    return pkmns
    
#gibt eine liste aller pokemon, die auf die uebergebenen parameter passen
def get_pk(args):
    g = ''
    ung = ''
    ort = ''
    info = ''
    rng = ''
    ed = ''
    loc = ''

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
    
    if g != '' and ung != '':
        g = ''
        ung = ''
    
    exc ='select pokemon.nr from pokemon'
    
    if ort != '':
        exc = exc + ort
    ad = False;
    if g != '' or ung != '' or info != '' or ed != '' or loc != '' or rng != '':
        exc = exc + ' where '
        if g != '':
            if ad:
                exc += ' and '
            exc += g
            ad = True

        if ung != '':
            if ad:
                exc += ' and '
            exc += ung
            ad = True
        if info != '':
            if ad:
                exc += ' and '
            exc += info
            ad = True
        if rng != '':
            if ad:
                exc += ' and '
            exc += rng
            ad = True
        if ed != '':
            if ad:
                exc += ' and '
            exc += ed
            ad = True
        if loc != '':
            if ad:
                exc += ' and '
            exc +=  loc
            ad = True
            
    exc += ' order by pokemon.nr'
     
    result = []
    for row in c.execute(exc):  
        if row[0] not in result:
            result.append(row[0])
         
    return result
 
#fuegt die edition und location zum pokemon hinzu 
def add_loc(pokemon, edition, location):

    #holt die nr des pokemon, falls name angegeben
    if isinstance(pokemon, str) and not pokemon.isdigit():
        pokemon = get_pknr(pokemon)
        
    edition = edition.upper()
    edition = edition.strip()
    location = location.strip()
    inserts = (pokemon, edition, location)
    c.execute('insert into locations (nr, edition, location) values (?,?,?)', inserts)
    
    conn.commit()
    
def rm_loc(pokemon, edition, location):
    #holt die nr des pokemon, falls name angegeben
    if isinstance(pokemon, str) and not pokemon.isdigit():
        pokemon = get_pknr(pokemon)
        

    inserts = (pokemon, edition, location)  
    c.execute('delete from locations where nr=? and edition=? and location=?', inserts)

    conn.commit()
    
def have_locs(pokemon):
    locs = 0
    #holt die nr des pokemon, falls name angegeben
    if isinstance(pokemon, str) and not pokemon.isdigit():
        pokemon = get_pknr(pokemon)
    pokemon = (pokemon,)
    for row in c.execute('select * from locations where nr = ?', pokemon):
        locs += 1
        
    return locs
        

def rm_all_loc(pokemon):
    #holt die nr des pokemon, falls name angegeben
    if isinstance(pokemon, str) and not pokemon.isdigit():
        pokemon = get_pknr(pokemon)
        

    inserts = (pokemon,)  
    c.execute('delete from locations where nr=?', inserts)

    conn.commit()
  
def add_info(pokemon, info):
    #holt die nr des pokemon, falls name angegeben
    if isinstance(pokemon, str) and not pokemon.isdigit():
        pokemon = get_pknr(pokemon)
    
    inserts = (info, pokemon)
    c.execute('update pokemon set infos=? where nr=?', inserts)

    conn.commit()
  
def rm_info(pokemon):
    add_info(pokemon, None) 

# Setzt den Catchwert des uebergebenen Pokemons (Nr oder Name) auf den uebergebenen Wert
def set_c(pokemon, catch):
    #holt die nr des pokemon, falls name angegeben
    if isinstance(pokemon, str) and not pokemon.isdigit():
        pokemon = get_pknr(pokemon)
    if not catch.isdigit():
        if catch == '0':
            catch = 0;
        else:
            catch = 1;
    inserts = (catch, pokemon)
    c.execute('update pokemon set catched=? where nr=?', inserts)
    
    conn.commit()

#erstellt eine backupdatei mit allen wichtigen daten    
def create_backup(filename):
    # Holt alle PKMN mit Nr, Catched und Info
    pkmns = []
    for row in c.execute('select distinct pokemon.nr, pokemon.catched, pokemon.infos from pokemon order by pokemon.nr'):
        info = ("" if row[2] == None else row[2])
        pkmns.append([row[0], row[1], info])
    #oeffnet die datei und screibt die infos und locations
    backup = open(filename, "w")
    backup.write('\t rst \t \t\n')
    for pkmn in pkmns:
        backup.write(u"{0} {1}\n\t{2}\n".format(pkmn[0], pkmn[1], pkmn[2]))
        for row in c.execute('select edition, location from locations where nr = ?', (pkmn[0],)):
            backup.write(u"\t {0} {1}\n".format(row[0], row[1]))
        backup.write(u" \n")
    backup.close()

def check_if_restorefile(filename):
    file = open(filename, "r")
    firstline = file.readline()
    if (firstline == '\t rst \t \t\n'):
        return True
    else:
        return False

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
            print 'Wiederherstellung laeuft... Pokemon Nr. {0}'.format(nr) #AUSGABE AN UI!
            
            line = file.readline()
            #Die zweite Zeile enthaelt die Info oder ist leer, falls keine Info eingetragen war
            info = line.strip()
            rm_info(nr)
            if info != '':
                add_info(nr, info)
            rm_all_loc(nr)
            #Alle darauffolgenden eingerueckten Zeilen enthalten Edition und Fundort
            line = file.readline()
            while (re.match(r"\t .*", line) != None):
                loc = line.strip()
                ed, loc = loc.split(' ', 1)
                add_loc(nr, ed, loc)
                line = file.readline()
        elif not line:
            break
        else:
            line = file.readline()
    file.close()
    conn.commit()

def get_info(nr):
    for row in c.execute('select infos from pokemon where nr = ?', (nr,)):
        return row[0]
    
def import_data(filename):
    file = open(filename, "r")
    ifinfos = file.readline()
    ifinfos = ifinfos.strip()
    #Die erste Zeile enthaelt die Information, ob der Export mit oder ohne Info erfolgte
    if ifinfos == "True":
        line = file.readline()
        pkmns = []
        while (True): 
            # Die Reihenfolge der Daten ist: Nummer \n Info \n Edition und Location (mehrfach)
            if (re.match(r"[0-9]+", line) != None):
                #Die Nummer wird fuer die folgenden Abfragen ausgelesen und gespeichert
                nr = line.strip()
                pkmns.append(nr)
                line = file.readline()
                info = line.strip()
                # Falls eine Info angegeben, wird sie durch ein // getrennt an die bestehende angehaengt
                if info != '':
                    info = (get_info(nr) if get_info(nr) != None else "") + " // " + info
                    add_info(nr, info)
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
            else:
                line = file.readline()
        file.close()
        conn.commit()
        return pkmns;
    elif ifinfos == "False":
        pkmns = []
        line = file.readline()
        while (True):   
            if (re.match(r"[0-9]+", line) != None):
                nr = line.strip()
                pkmns.append(nr)
                line = file.readline()
                while (re.match(r"\t .*", line) != None):
                    loc = line.strip()
                    ed, loc = loc.split(' ', 1)
                    add_loc(nr, ed, loc)
                    line = file.readline()
            elif not line:
                break
            else:
                line = file.readline()
        file.close()
        conn.commit()
        return pkmns;
    else:
        return None;
    
#erstellt eine exportdatei mit oder ohne Infos und Locationinformationen    
def export(info):
    # jenachdem, ob die info mitgespeichert wird, werdena ndere informationen gelesen und geschrieben
    if (info):
        q = 'select distinct pokemon.nr, pokemon.infos from pokemon join locations on pokemon.nr = locations.nr order by pokemon.nr'
        # Holt alle PKMN mit Nr und Info, fuer die Locations gespeichert sind
        pkmns = []
        for row in c.execute(q):
            info = ("" if row[1] == None else row[1])
            pkmns.append([row[0], info])
        #oeffnet die datei und screibt die infos und locations
        backup = open("pkmnmanager-export", "w")
        #vermerkt, das dies eine export mit infos ist
        backup.write(u"True\n")
        for pkmn in pkmns:
            backup.write(u"{0}\n \t{1} \n".format(pkmn[0], pkmn[1]))
            for row in c.execute('select edition, location from locations where nr = ?', (pkmn[0],)):
                backup.write(u"\t {0} {1}\n".format(row[0], row[1]))
        backup.close()
    else:
        q = 'select distinct pokemon.nr from pokemon join locations on pokemon.nr = locations.nr order by pokemon.nr'
        # Holt alle PKMN mit Nr, fuer die Locations gespeichert sind
        pkmns = []
        for row in c.execute(q):
            pkmns.append(row[0])
        #oeffnet die datei und screibt die infos und locations
        backup = open("pkmnmanager-export", "w")
        #vermerkt, das dies eine export ohne infos ist
        backup.write(u"False\n")
        for pkmn in pkmns:
            backup.write(u"{0}\n".format(pkmn))
            for row in c.execute('select edition, location from locations where nr = ?', (pkmn,)):
                backup.write(u"\t {0} {1}\n".format(row[0], row[1]))
        backup.close()

 
# Gibt die Nummer des Pokemon, wenn der Name angeben wurde
def get_pknr(pokemon):
    if isinstance(pokemon, str) and not pokemon.isdigit():
        pokemon = pokemon.capitalize()
        pokemon = (pokemon,)
        for row in c.execute('select nr from pokemon where name = ?', pokemon):
            return row[0]
            
    return False

# Debug. Zum Aktivieren "add_pk" eingeben, enter "add_pk", nr und name    
def add_pk(nr, name):
    inserts = (nr, name)
    c.execute('insert into pokemon (nr, name) values (?,?)', inserts)
        
    conn.commit()
    
def close():
    conn.commit()
    c.close()
    conn.close()
        
        
        
    
    
    
