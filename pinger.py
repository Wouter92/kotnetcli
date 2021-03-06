#!/usr/bin/env python2
# -*- coding: utf-8 -*-

## Dependencies:    python-mechanize, python-keyring, curses
## Author:          Gijs Timmers: https://github.com/GijsTimmers
## Contributors:    Gijs Timmers: https://github.com/GijsTimmers
##                  Jo Van Bulck: https://github.com/jovanbulck
##
## Licence:         GPLv3
##
## kotnetcli is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## kotnetcli is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with kotnetcli.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import subprocess

def ping(co):    
    if os.name == "posix":
        with open(os.devnull, 'w') as dev_null:
            if subprocess.call(["ping", "-c", "1", "-w", "1", "netlogin.kuleuven.be"], \
            stdout=dev_null, stderr=dev_null) == 0:
                ## 0 staat voor een exit code van True van het ping-commando.
                if subprocess.call(["ping", "-c", "1", "-w", "1", "toledo.kuleuven.be"], \
                stdout=dev_null, stderr=dev_null) == 0:
                    ## we zijn al online
                    co.eventPingAlreadyOnline()
                    co.beeindig_sessie()
                    sys.exit(1)
                else:
                    ## we moeten nog inloggen
                    co.eventPingSuccess()
            else:
                ## geen netwerkverbinding
                co.eventPingFailure()
                co.beeindig_sessie()
                sys.exit(1)
    
    elif os.name == "nt":
        with open("NUL", 'w') as dev_null:
            if subprocess.call(["ping", "-n", "1", "-w", "1", "netlogin.kuleuven.be"], \
            stdout=dev_null, stderr=dev_null) == 0:
                ## 0 staat voor een exit code van True van het ping-commando.
                if subprocess.call(["ping", "-c", "1", "-w", "1", "toledo.kuleuven.be"], \
                stdout=dev_null, stderr=dev_null) == 0:
                    ## we zijn al online
                    co.eventPingAlreadyOnline()
                    co.beeindig_sessie()
                    sys.exit(1)
                else:
                    ## we moeten nog inloggen
                    co.eventPingSuccess()
            else:
                ## geen netwerkverbinding
                co.eventPingFailure()
                co.beeindig_sessie()
                sys.exit(1)
