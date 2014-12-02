#!/usr/bin/env python2
# -*- coding: utf-8 -*-

## Dependencies:    python-mechanize, python-keyring, curses
## Author:          Gijs Timmers
## Licence:         CC-BY-SA-4.0
##                  http://creativecommons.org/licenses/by-sa/4.0/

## This work is licensed under the Creative Commons
## Attribution-ShareAlike 4.0 International License. To view a copy of 
## this license, visit http://creativecommons.org/licenses/by-sa/4.0/ or
## send a letter to Creative Commons, PO Box 1866, Mountain View, 
## CA 94042, USA.

import re                               ## Basislib voor reguliere expressies
import time                             ## Voor timeout om venster te sluiten na login etc.
import keyring                          ## Voor ophalen wachtwoord
import argparse                         ## Parst argumenten
import mechanize                        ## Emuleert een browser
import getpass                          ## Voor invoer wachtwoord zonder feedback
import curses                           ## Voor tekenen op scherm.
import sys                              ## Basislib voor output en besturingssysteemintegratie
import os

import communicator
#from communicator import QuietCommunicator   ## Zorgt voor al dan niet afdrukken in de terminal.

class Credentials():
    def getset(self):
        if (keyring.get_password("kotnetcli", "gebruikersnaam") == None) or\
        (keyring.get_password("kotnetcli", "wachtwoord") == None):
            gebruikersnaam = raw_input("Voer uw s-nummer/r-nummer in... ")
            wachtwoord = getpass.getpass(prompt="Voer uw wachtwoord in... ")
            
            keyring.set_password("kotnetcli", "gebruikersnaam", gebruikersnaam)
            keyring.set_password("kotnetcli", "wachtwoord", wachtwoord)
        
        gebruikersnaam = keyring.get_password("kotnetcli", "gebruikersnaam")
        wachtwoord = keyring.get_password("kotnetcli", "wachtwoord")
        return gebruikersnaam, wachtwoord
    
    def forget(self):
        keyring.delete_password("kotnetcli", "gebruikersnaam")
        keyring.delete_password("kotnetcli", "wachtwoord")
        print "You have succesfully removed your kotnetcli credentials."
    
    def guest(self):
        gebruikersnaam = raw_input("Voer uw s-nummer/r-nummer in... ")
        wachtwoord = getpass.getpass(prompt="Voer uw wachtwoord in... ")
        return gebruikersnaam, wachtwoord

class Kotnetlogin():
    def __init__(self, co, gebruikersnaam, wachtwoord):
        
        self.browser = mechanize.Browser()
        self.browser.addheaders = [('User-agent', 'Firefox')]
        
        self.gebruikersnaam = gebruikersnaam
        self.wachtwoord = wachtwoord
        
        self.co = co
        
        self.co.kprint(0, 0, "Netlogin openen.......")
        self.co.kprint(0, 22, "[    ]", self.co.tekstOpmaakVet)
        #self.co.kprint(0, 23, "WAIT", co.tekstOpmaakVet | co.tekstKleurGeel)
        self.co.kprint(0, 23, "WAIT", self.co.tekstKleurGeelOpmaakVet)
        self.co.kprint(1, 0, "KU Leuven kiezen......")
        self.co.kprint(1, 22, "[    ]", self.co.tekstOpmaakVet)
        self.co.kprint(2, 0, "Gegevens invoeren.....")
        self.co.kprint(2, 22, "[    ]", self.co.tekstOpmaakVet)
        self.co.kprint(3, 0, "Gegevens opsturen.....")
        self.co.kprint(3, 22, "[    ]", self.co.tekstOpmaakVet)
        self.co.kprint(4, 0, "Download:")
        self.co.kprint(4, 10, "[          ][    ]", self.co.tekstOpmaakVet)
        self.co.kprint(5, 0, "Upload:")
        self.co.kprint(5, 10, "[          ][    ]", self.co.tekstOpmaakVet)
    
    def netlogin(self):
        try:
            respons = self.browser.open("https://netlogin.kuleuven.be", timeout=1.8)
            html = respons.read()
            self.co.kprint(0, 23, " OK ", self.co.tekstKleurGroenOpmaakVet)
            self.co.kprint(1, 23, "WAIT", self.co.tekstKleurGeelOpmaakVet)
            
            #self.scherm.addstr(0, 23, " OK ", curses.color_pair(2) | curses.A_BOLD)
            #self.scherm.addstr(1, 23, "WAIT", curses.color_pair(3) | curses.A_BOLD)
            #self.scherm.refresh()
        except:
            self.co.kprint(0, 23, "FAIL", self.co.tekstKleurRoodOpmaakVet)
            #self.scherm.addstr(0, 23, "FAIL", curses.color_pair(1) | curses.A_BOLD)
            #self.scherm.refresh()
            sys.exit()
        
    def kuleuven(self):
        try:
            self.browser.select_form(nr=1)
            self.browser.submit()
            self.co.kprint(1, 23, " OK ", self.co.tekstKleurGroenOpmaakVet)
            self.co.kprint(2, 23, "WAIT", self.co.tekstKleurGeelOpmaakVet)
            #self.scherm.addstr(1, 23, " OK ", curses.color_pair(2) | curses.A_BOLD)
            #self.scherm.addstr(2, 23, "WAIT", curses.color_pair(3) | curses.A_BOLD)
            #self.scherm.refresh()
        except:
            self.co.kprint(1, 23, "FAIL", self.co.tekstKleurRoodOpmaakVet)
            #self.scherm.addstr(1, 23, "FAIL", curses.color_pair(1) | curses.A_BOLD)
            #self.scherm.refresh()
            sys.exit()
        

    def gegevensinvoeren(self):
        try:
            self.browser.select_form(nr=1)
            self.browser.form["uid"] = self.gebruikersnaam
            wachtwoordvaknaam = self.browser.form.find_control(type="password").name
            self.browser.form[wachtwoordvaknaam] = self.wachtwoord
            self.co.kprint(2, 23, " OK ", self.co.tekstKleurGroenOpmaakVet)
            self.co.kprint(3, 23, "WAIT", self.co.tekstKleurGeelOpmaakVet) 
            self.co.kprint(4, 14, "WAIT", self.co.tekstKleurGeelOpmaakVet)
            self.co.kprint(4, 23, "WAIT", self.co.tekstKleurGeelOpmaakVet) 
            self.co.kprint(5, 14, "WAIT", self.co.tekstKleurGeelOpmaakVet)
            self.co.kprint(5, 23, "WAIT", self.co.tekstKleurGeelOpmaakVet) 
            #self.scherm.refresh()
        except:
            self.co.kprint(2, 23, "FAIL", self.co.tekstKleurRoodOpmaakVet)
            #self.scherm.addstr(2, 23, "FAIL", curses.color_pair(1) | curses.A_BOLD)
            #self.scherm.refresh()
            sys.exit()
        
        
    def gegevensopsturen(self):
        try:
            self.browser.submit()
            self.co.kprint(3, 23, " OK ", self.co.tekstKleurGroenOpmaakVet)
            #self.scherm.refresh()
        except:
            self.co.kprint(3, 23, "FAIL", self.co.tekstKleurGeelOpmaakVet) 
            #self.scherm.refresh()
            sys.exit()
        
        
    def tegoeden(self):
        ## Tegoeden parsen
        html = self.browser.response().read()
        #print html
        zoekresultaten = (re.findall("<br>\(\d*%\)</TD>", html))
        #print zoekresultaten
        ## zoek naar: <br>(40%)</TD>
        self.downloadpercentage = int(zoekresultaten[0].strip("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ%()<>br/"))
        self.uploadpercentage   = int(zoekresultaten[1].strip("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ%()<>br/"))


        self.balkgetal_download = int(round(float(self.downloadpercentage) / 10.0))
        self.balkgetal_upload = int(round(float(self.uploadpercentage) / 10.0))
        
        ## Balken tekenen in de terminal
        
        if self.downloadpercentage <= 10:
            self.voorwaardelijke_kleur_download = self.co.tekstKleurRoodOpmaakVet
        elif 10 < self.downloadpercentage < 60:
            self.voorwaardelijke_kleur_download = self.co.tekstKleurGeelOpmaakVet
        else:
            self.voorwaardelijke_kleur_download = self.co.tekstKleurGroenOpmaakVet
        
        if self.uploadpercentage <= 10:
            self.voorwaardelijke_kleur_upload = self.co.tekstKleurRoodOpmaakVet
        elif 10 < self.uploadpercentage < 60:
            self.voorwaardelijke_kleur_upload = self.co.tekstKleurGeelOpmaakVet
        else:
            self.voorwaardelijke_kleur_upload = self.co.tekstKleurGroenOpmaakVet
        
        
        
        self.co.kprint(4, 23, " " * (3 - len(str(self.downloadpercentage))) + str(self.downloadpercentage) + "%", self.voorwaardelijke_kleur_download)
        self.co.kprint(5, 23, " " * (3 - len(str(self.uploadpercentage))) + str(self.uploadpercentage) + "%", self.voorwaardelijke_kleur_upload)
    
        self.co.kprint(4, 11, "=" * self.balkgetal_download + " " * (10-self.balkgetal_download), self.voorwaardelijke_kleur_download)
        self.co.kprint(5, 11, "=" * self.balkgetal_upload + " " * (10-self.balkgetal_upload), self.voorwaardelijke_kleur_upload)
        self.co.kprint(5, 28, "")
        
        
        #self.scherm.refresh()
        #time.sleep(10000)
        time.sleep(2)
        self.co.beeindig_sessie()
        #self.scherm.getch()
        
def main(co, gebruikersnaam, wachtwoord):
    kl = Kotnetlogin(co, gebruikersnaam, wachtwoord) ## Vervang door jouw gegevens!        
    kl.netlogin()
    kl.kuleuven()
    kl.gegevensinvoeren()
    kl.gegevensopsturen()
    kl.tegoeden()

def argumentenParser():
    parser = argparse.ArgumentParser(description="Script om in- of uit \
    te loggen op KotNet")

    parser.add_argument("-i", "--login",\
    help="Logs you in on KotNet (default)",\
    action="store_true")

    parser.add_argument("-o", "--logout",\
    help="Logs you out off KotNet",\
    action="store_true")

    parser.add_argument("-f", "--forget",\
    help="Makes kotnetcli forget your credentials",\
    action="store_true")

    parser.add_argument("-q", "--quiet",\
    help="Hides all output",\
    action="store_true")

    parser.add_argument("-g", "--guest-mode",\
    help="Logs you in as a different user without forgetting your \
    default credentials",\
    action="store_true")


    argumenten = parser.parse_args()
    return argumenten

def aanstuurderObvArgumenten(argumenten, cr):
    argumententuple_omgekeerd = [not i for i in vars(argumenten).values()]
    if argumenten.forget:
        print "ik wil vergeten"
        cr.forget()
    
    if argumenten.guest_mode:
        ## werkt alleen met login op het moment
        print "ik wil me anders voordoen dan ik ben"
        gebruikersnaam, wachtwoord = cr.guest()
        co = communicator.CursesCommunicator()
        main(co, gebruikersnaam, wachtwoord)
        #curses.wrapper(main, gebruikersnaam, wachtwoord)
        
    if argumenten.quiet:
        print "ik wil zwijgen"
        gebruikersnaam, wachtwoord = cr.getset()
        co = communicator.QuietCommunicator()
        main(co, gebruikersnaam, wachtwoord)
        return()
        ## needs to be removed, but if I do that, it will log in as normal
        ## login mode
        
    if argumenten.logout:
        print "ik wil uitloggen"
        print "(Nog niet geïmplementeerd)"
        return()
    
    #if argumenten.login or all(argumententuple_omgekeerd):
    if argumenten.login:    
        print "ik wil inloggen"
        gebruikersnaam, wachtwoord = cr.getset()
        co = communicator.CursesCommunicator()
        main(co, gebruikersnaam, wachtwoord)
        #curses.wrapper(main, gebruikersnaam, wachtwoord) 
        ## wrapper: Zorgt er voor dat curses netjes opstart en afsluit.
    
    
    print "ik wil inloggen"
    gebruikersnaam, wachtwoord = cr.getset()
    co = communicator.CursesCommunicator()
    main(co, gebruikersnaam, wachtwoord)
    ## wrapper: Zorgt er voor dat curses netjes opstart en afsluit.
    
    ## .login op 't einde, zonder return, zodat er altijd wordt
    ## ingelogd, zowel met --login als zonder argumenten. Als er moet
    ## worden uitgelogd, is de .logout True en zal de .login() niet worden
    ## gestart; daardoor is het te combineren met de andere vlaggen.

cr = Credentials()
aanstuurderObvArgumenten(argumentenParser(), cr)
