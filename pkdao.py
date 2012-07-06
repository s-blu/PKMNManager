#!/usr/bin/env python

#from gi.repository import Gtk
import sqlite3

conn = sqlite3.connect('../db/pokedex.db')
c = conn.cursor()


# Gibt die Informationen eines Pokemon in 2 Tupeln zurueck. Das erste Tupfel ist eine Liste mit Nummer, Name und Catched
# Das zweite Tupel ist eine Liste, die wiederrum Listen mit edition und location enthaehlt
def get_pkinfo(pokemon):

    # Falls Name angegeben wurde, wird die Nummer ermittelt
    if isinstance(pokemon, str) and not pokemon.isdigit():
        pokemon = pokemon.capitalize()
        pokemon = (pokemon,)
        for row_name in c.execute('select nr from pokemon where name = ?', pokemon):
            pokemon = row_name[0]
            
            
    pokemon = (pokemon,)
    #Ermittung der Pokemoninformationen
    for row in c.execute('select nr, name, catched from pokemon where nr = ?', pokemon):

        pkinfo = [row[0], row[1], row[2]]
        
        #Ermittlung der Location-Information
        locs = []
        nummer = (row[0],)
        for row2 in c.execute('select edition, location from locations where nr = ?', nummer):
            locs.append([row2[0], row2[1]]
                  
    return pkinfo, locs
 
#fuegt die edition und location zum pokemon hinzu 
def add_loc(pokemon, edition, location):

    if isinstance(pokemon, str) and not pokemon.isdigit():
        pokemon = (pokemon,)
        for row in c.execute('select nr from pokemon where name = ?', pokemon):
            pokemon = row[0]
    
    inserts = (pokemon, edition, location)
    c.execute('insert into locations (nr, edition, location) values (?,?,?)', inserts)
    
    
    conn.commit()
    
def close():
    conn.commit()
    c.close()
    conn.close()
        
        
        
    
    
    
