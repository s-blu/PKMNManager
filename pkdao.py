#!/usr/bin/env python

#from gi.repository import Gtk
import sqlite3

conn = sqlite3.connect('../db/pokedex.db')
c = conn.cursor()


# Gibt die Informationen eines Pokemon in 2 Tupeln zurueck. Das erste Tupfel ist eine Liste mit Nummer, Name und Catched
# Das zweite Tupel ist eine Liste, die wiederrum Listen mit edition und location enthaehlt
def get_pkinfo(pokemon):

    #holt die nr des pokemon, falls name angegeben
    if isinstance(pokemon, str) and not pokemon.isdigit():
        pokemon = get_pknr(pokemon)
            
            
    pokemon = (pokemon,)
    #Ermittung der Pokemoninformationen
    for row in c.execute('select nr, name, catched, infos from pokemon where nr = ?', pokemon):

        pkinfo = [row[0], row[1], row[2], row[3]]
        
        #Ermittlung der Location-Information
        locs = []
        nummer = (row[0],)
        for row2 in c.execute('select edition, location from locations where nr = ?', nummer):
            locs.append([row2[0], row2[1]])
                  
    return pkinfo, locs
    
def get_pk(args):
    g = ''
    ung = ''
    ort = ''
    info = ''

    for arg in args:
        if arg == 'g':
            g = ' catched = 1 '
        elif arg == 'ung':
            ung = ' catched = 0 '
        elif arg == 'ort':
            ort = ' join locations on pokemon. nr = locations.nr'
        elif arg == 'info':
            info = ' infos is not null '
            
    if g != '' and ung != '':
        g = ''
        ung = ''
    
    exc ='select pokemon.nr from pokemon'
    
    if ort != '':
        exc = exc + ort
    
    if g != '' or ung != '' or info != '':
        exc = exc + ' where '
        if g != '':
            exc += g
        if ung != '':
            exc += ung 
        if info != '':
            if ung != '' or g != '':
                exc += ' and ' + info
            else:
                exc += info
    
    result = set()
    for row in c.execute(exc):  
        result.add(row[0])
        
    return result
 
#fuegt die edition und location zum pokemon hinzu 
def add_loc(pokemon, edition, location):

    #holt die nr des pokemon, falls name angegeben
    if isinstance(pokemon, str) and not pokemon.isdigit():
        pokemon = get_pknr(pokemon)
    
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
  
def add_info(pokemon, info):
    #holt die nr des pokemon, falls name angegeben
    if isinstance(pokemon, str) and not pokemon.isdigit():
        pokemon = get_pknr(pokemon)
    
    inserts = (info, pokemon)
    c.execute('update pokemon set infos=? where nr=?', inserts)

    conn.commit()
  
def rm_info(pokemon):
    add_info(pokemon, None)    
  
def get_pknr(pokemon):
    if isinstance(pokemon, str) and not pokemon.isdigit():
        pokemon = pokemon.capitalize()
        pokemon = (pokemon,)
        for row in c.execute('select nr from pokemon where name = ?', pokemon):
            return row[0]
  
def close():
    conn.commit()
    c.close()
    conn.close()
        
        
        
    
    
    
