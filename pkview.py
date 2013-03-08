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
import pkdao
import re

ver = '0.4.1'

#Validiert die Existenz des Pokemon. Ist es existent, wird der Name ohne Leerzeichen und mit grossen Anfangsbuchstaben
# (Datenbankkonform) zurueckgegeben
def valid_pk(pk):
    if not pkdao.valid_pk(pk):
        return False
    else:
        return pk
        
def create_list(pks):

    pkms = []

    if re.match('[\w]+[-][\w]+', pks) != None:
        start, sep, end = pks.partition('-')
        if re.match('[0-9]+[-][0-9]+', pks) != None:
            pkms = range(int(start), int(end)+1)
        else:
            if not pkdao.valid_pk(start):
                print "Ungueltiges Pokemon '{0}'".format(start)
            elif not pkdao.valid_pk(start):
                print "Ungueltiges Pokemon '{0}'".format(end)
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
        pkms = pkdao.get_pk_by_name(pks)
        
    return pkms
    
# Ermoeglicht den Aufruf von print_pokemon mit direkt angegebenen Parametern. Fehlt die direkte Angabe, wird abgefragt.
def prp(arguments):
    arguments = arguments.split(' ', 1)
    arguments = arguments [1:]
    if len(arguments) > 0:
        if arguments[0].startswith('-'):
            printa(arguments[0])
        else:
            print_pokemon(arguments[0])
    else:
        pokem = raw_input('Welches Pokemon? > ')
        if pokem == '' or pokem == 'all':
            printa('')
        else:
            print_pokemon(pokem)

# Gibt ein, mehrere oder alle Pokemon mitsamt Locationinformation aus.
def print_pokemon(pokem):

    if isinstance(pokem, str):
        
        pkms = create_list(pokem)
        
        if len(pkms) == 0 :
            print "Ungueltiges Pokemon '{0}'".format(pokem)
            return
        
        for pokemon in pkms:
            if not pkdao.valid_pk(pokemon):
                print "Ungueltiges Pokemon '{0}'".format(pokemon)
            else:
                printer(pokemon)
                
        
    #Ist das Pokemon ein int-Wert, wurde es im vorherigen Programmverlauf bereits auf Gueltigkeit geprueft.
    elif isinstance(pokem, int):
        printer(pokem)
  
#Gibt eine pokemonliste nach den uebergebenen argumenten gefiltert aus
def printa(arguments):
    arguments = arguments.split('-')
    arguments = arguments [1:]

    for arg in arguments:
        arg = arg.strip()
        if not pkdao.get_pk_is_known_arg(arg):
            print "Unbekannter Parameter '{0}'".format(arg)
            return

    list = pkdao.get_pk(arguments)
    
    if len(list) > 100:
        dispall = raw_input('Moechten Sie alle {0} Pokemon anzeigen lassen? Y/no > '.format(len(list)+1))
        if dispall == 'no' or dispall == 'n':
            return
            
    for pk in list:
        print_pokemon(pk)
        
# Macht die Ausgabe eines Pokemon. Wird nie direkt ueber das runmodul aufgerufen.
def printer(pokemon):
    #pkmns = pkdao.get_pk_by_name(pokemon)
    #for pk in pkmns:
    pkinfo, locs = pkdao.get_pkinfo(pokemon)
            
    catch = " ( ) "
    if pkinfo[2] != 0:
        catch = "gefangen!"
    
    info = ''
    if pkinfo[3] != None:
        info = "Info: '{0}'".format(pkinfo[3])
    
    print u"{0} {1},\t {2} \t {3}".format(pkinfo[0], pkinfo[1], catch, info)

    if len(locs) > 0:
        print "\t - - - - - - - - - - - - - -"
    for loc in locs:
        print u"\t Fangbar in {0}, {1}".format(loc[0], loc[1])
    if len(locs) > 0:
        print "\t - - - - - - - - - - - - - -"
  
# Ermoeglicht den Aufruf von add_location mit direkt angegebenen Parametern. Fehlt die direkte Angabe, wird abgefragt.   
def addloc(arguments):
    arguments = arguments.split(' ', 1)
    arguments = arguments [1:]
    if len(arguments) > 0:
        add_location(arguments[0])
    else:
        pokem = raw_input('Pokemonnr oder -name? > ')
        add_location(pokem)      
        
# Fuegt den angegebenen Pokemon eine Location, also einen Fundort, bestehend aus Edition und Fundort, hinzu
def add_location(pokem):
    edition = raw_input('Welche Edition? > ')
    location = raw_input('Welche Location? > ')
    
    pkms = create_list(pokem)
    invalidpk = 0
    for pokemon in pkms:
        if not pkdao.valid_pk(pokemon):
            print "Ungueltiges Pokemon '{0}'".format(pokemon)
            invalidpk += 1
        else:
            pkdao.add_loc(pokemon, edition, location)
            
            print_pokemon(pokemon)
    if invalidpk < len(pkms):        
        moreinput = raw_input("Moechten Sie mehr Daten einpflegen? yes/N > ")
        moreinput = moreinput.lower()
        
        while moreinput == 'yes' or moreinput == 'y':
            edition = raw_input('Welche Edition? > ')
            loc = raw_input('Welche Location? > ')
        
            for pokemon in pkms:
                if not pkdao.valid_pk(pokemon):
                    print "Ungueltiges Pokemon '{0}'".format(pokemon)
                else:
                    pkdao.add_loc(pokemon, edition, loc)
                    print_pokemon(pokemon)
            moreinput = raw_input("Moechten Sie mehr Daten einpflegen? yes/N > ")
            moreinput = moreinput.lower()
  

    
# Ermoeglicht den Aufruf von rm_location mit direkt angegebenen Parametern. Fehlt die direkte Angabe, wird abgefragt.   
def rmloc(arguments):
    arguments = arguments.split(' ', 1)
    arguments = arguments [1:]
    if len(arguments) > 0:
        rm_location(arguments[0])
    else:
        pokem = raw_input('Pokemonnr oder -name? > ')
        rm_location(pokem)      
 
# Loescht Locationeintraege. 
def rm_location(pokem):
    
    pkms = create_list(pokem)
    
    invalidpk = 0
    for pokemon in pkms:
        if not pkdao.valid_pk(pokemon):
            print "Ungueltiges Pokemon '{0}'".format(pokemon)
            invalidpk += 1
        else:
            if pkdao.have_locs(pokemon) == 0:
                print "Fuer Pokemon '{0}' existieren keine Locationangaben".format(pokemon)
                invalidpk += 1
            else:
                print_pokemon(pokemon)
    
    if invalidpk < len(pkms):
        rmall = raw_input('Sollen alle Eintraege geloescht werden? yes/N > ')
        rmall = rmall.lower()
        if rmall == 'yes' or rmall == 'y':
            for pokemon in pkms:
                pkdao.rm_all_loc(pokemon)
                print_pokemon(pokemon)
            
        else:
            print 'Spezifizieren Sie bitte den Eintrag der geloescht werden soll.'
            edition = raw_input('Loeschen: Welche Edition? > ')
            location = raw_input('Loeschen: Welche Location? > ')
            for pokemon in pkms:
                pkdao.rm_loc(pokemon, edition, location)
                print_pokemon(pokemon)
                          
            morerm = raw_input("Moechten Sie mehr Daten loeschen? yes/N > ")
            morerm = morerm.lower()
            
            while morerm == 'yes' or morerm == 'y':
                edition = raw_input('Loeschen: Welche Edition? > ')
                location = raw_input('Loeschen: Welche Location? > ')
                for pokemon in pkms:
                    pkdao.rm_loc(pokemon, edition, location)
                    print_pokemon(pokemon)
                morerm = raw_input("Moechten Sie mehr Daten loeschen? yes/N > ")
                morerm = morerm.lower()
            
# Ermoeglicht den Aufruf von add_info mit direkt angegebenen Parametern. Fehlt die direkte Angabe, wird abgefragt.   
def addinf(arguments):
    arguments = arguments.split(' ', 1)
    arguments = arguments [1:]
    if len(arguments) > 0:
        add_info(arguments[0])
    else:
        pokem = raw_input('Pokemonnr oder -name? > ')
        add_info(pokem) 

def add_info(pokem):
    info = raw_input('Info? > ')
    pkms = create_list(pokem)
    
    for pokemon in pkms:
        if not pkdao.valid_pk(pokemon):
            print "Ungueltiges Pokemon '{0}'".format(pokemon)
        else:
            pkdao.add_info(pokemon, unicode(info))
            print_pokemon(pokemon)
    
# Ermoeglicht den Aufruf von rm_info mit direkt angegebenen Parametern. Fehlt die direkte Angabe, wird abgefragt.   
def rminf(arguments):
    arguments = arguments.split(' ', 1)
    arguments = arguments [1:]
    if len(arguments) > 0:
        rm_info(arguments[0])
    else:
        pokem = raw_input('Von welchem Pokemon wollen Sie die Info loeschen? > ')
        rm_info(pokem) 
        
def rm_info(pokem):
    pkms = create_list(pokem)
    
    for pokemon in pkms:
        if not pkdao.valid_pk(pokemon):
            print "Ungueltiges Pokemon '{0}'".format(pokemon)
        else:
            pkdao.rm_info(pokemon)
            print_pokemon(pokemon)
  
# Ermoeglicht den Aufruf von set_c mit direkt angegebenen Parametern. Fehlt die direkte Angabe, wird abgefragt.   
def ct(arguments):
    arguments = arguments.split(' ', 1)
    arguments = arguments [1:]
    if len(arguments) > 0:
        set_c(arguments[0])
    else:
        pokem = raw_input('Pokemonnr oder -name? > ')
        set_c(pokem) 
  
def set_c(pokem):
    print 'Herzlichen Glueckwunsch zum Fangerfolg! :)'
    pkms = create_list(pokem)
    
    for pokemon in pkms:
        if not pkdao.valid_pk(pokemon):
            print "Ungueltiges Pokemon '{0}'".format(pokemon)
        else:
            pkdao.set_c(pokemon, 1)
            print_pokemon(pokemon)
           
            
# Ermoeglicht den Aufruf von uset_c mit direkt angegebenen Parametern. Fehlt die direkte Angabe, wird abgefragt.   
def uct(arguments):
    arguments = arguments.split(' ', 1)
    arguments = arguments [1:]
    if len(arguments) > 0:
        uset_c(arguments[0])
    else:
        pokem = raw_input('Pokemonnr oder -name? > ')
        uset_c(pokem)  
    
#Markiert uebergebene Pokemon als ungefangen
def uset_c(pokem):
    pkms = create_list(pokem)
    
    for pokemon in pkms:
        if not pkdao.valid_pk(pokemon):
            print "Ungueltiges Pokemon '{0}'".format(pokemon)
        else:
            pkdao.set_c(pokemon, 0)
            print_pokemon(pokemon)
 
def backup():
    filename = raw_input('Wie soll die Backupdatei heissen? > ')
    pkdao.create_backup(filename)
    
def export(): 
    info = raw_input('Moechten Sie die Infos mit exportieren? Y/no > ').lower()
    if info == 'no' or info == 'n':
        pkdao.export(False)
    else:
        pkdao.export(True)
    
            
def add_pk(nr, name):
    pkdao.add_pk(nr, name)
def credit():
    print '- - - Credits - - -'
    print 'Pokemonmanager V{0}'.format(ver)
    print 'Dient zur Unterstuetzung beim Komplettieren des eigenen Pokedex'
    print 'Dies ist kein Pokedex! Sondern ein Fundort/Info/Gefangen-nichtgefangen Manager'
    print 'Neuste unterstuetzte Pokemonversion: schwarz/weiss'
    print 'Geschrieben von Sam B. <sam(at)s-blu.de>'
    print 'Anfang Juli 2012 gestartetes Projekt in Python'
    print 'Ein sparkling Flausch an Tsurai fuers Testen <3'
    print '- - - - - - - - -'
    
def close():
    pkdao.close()
        
        
    
    
    
