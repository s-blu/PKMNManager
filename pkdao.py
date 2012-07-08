#!/usr/bin/env python
# -*- coding: utf -8 -*-

#from gi.repository import Gtk
import sqlite3

conn = sqlite3.connect('../db/pkmmanager.db')
c = conn.cursor()


# Gibt die Informationen eines Pokemon in 2 Tupeln zurueck. Das erste Tupfel ist eine Liste mit Nummer, Name und Catched
# Das zweite Tupel ist eine Liste, die wiederrum Listen mit edition und location enthaehlt
def get_pkinfo(pokemon):

    #holt die nr des pokemon, falls name angegeben
    if isinstance(pokemon, str) and not pokemon.isdigit():
        pokemon = get_pknr(pokemon)
        
    
    pkinfo = []
    locs = []   
    
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

def set_c(pokemon, catch):
    #holt die nr des pokemon, falls name angegeben
    if isinstance(pokemon, str) and not pokemon.isdigit():
        pokemon = get_pknr(pokemon)
    
    inserts = (catch, pokemon)
    c.execute('update pokemon set catched=? where nr=?', inserts)
        
  
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
        
        
        
    
    
    
