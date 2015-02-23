#!/usr/bin/env python2
# -*- coding: utf-8 -*-

## Dependencies:    python-mechanize, python-keyring, curses
## Author:          Gijs Timmers: https://github.com/GijsTimmers
## Contributors:    Gijs Timmers: https://github.com/GijsTimmers
##                  Jo Van Bulck: https://github.com/jovanbulck

## Licence:         CC-BY-SA-4.0
##                  https://creativecommons.org/licenses/by-sa/4.0/

## This work is licensed under the Creative Commons
## Attribution-ShareAlike 4.0 International License. To view a copy of 
## this license, visit https://creativecommons.org/licenses/by-sa/4.0/ or
## send a letter to Creative Commons, PO Box 1866, Mountain View, 
## CA 94042, USA.

from worker import DummyLoginWorker, DummyLogoutWorker, SuperWorker, EXIT_SUCCESS, EXIT_FAILURE

from tools import log
import logging
logger = logging.getLogger(__name__)

class LoginTestsuiteWorker(SuperWorker):

    def go(self, co, creds):
        logger.info("running dummy login testsuite with communicator " + \
        "'%s'\n", co.__class__.__name__)
        self.run_dummy_login_tests(co, creds)
        logger.info("end of dummy login testsuite with communicator " + \
        "'%s'", co.__class__.__name__)
        exit(0)
    
    ## TODO assert for the correct fine grained exit code here (see corresponding issue)
    def run_dummy_login_tests(self, co, creds):
    
        logger.info("DEFAULT DUMMY LOGIN START")
        worker = DummyLoginWorker()
        try:
            worker.go(co, creds)
        except SystemExit, e:
            assert (e.code == EXIT_SUCCESS)
            logger.info("DEFAULT DUMMY LOGIN END\n")
        
        logger.info("LOW PERCENTAGES DUMMY LOGIN START")
        worker = DummyLoginWorker(True, False, 100, -5, 22.5)        
        try:
            worker.go(co, creds)
        except SystemExit, e:
            assert (e.code == EXIT_SUCCESS)
            logger.info("LOW PERCENTAGES DUMMY LOGIN END\n")
        
        logger.info("KOTNET OFFLINE DUMMY LOGIN START")
        worker = DummyLoginWorker(False)        
        try:
            worker.go(co, creds)
        except SystemExit, e:
            assert (e.code == EXIT_FAILURE)
            logger.info("KOTNET OFFLINE DUMMY LOGIN END\n")
        
        logger.info("NETLOGIN OFFLINE DUMMY LOGIN START")
        worker = DummyLoginWorker(True, True)        
        try:
            worker.go(co, creds)
        except SystemExit, e:
            assert (e.code == EXIT_FAILURE)
            logger.info("NETLOGIN OFFLINE DUMMY LOGIN END\n")
        
        logger.info("INVALID USERNAME DUMMY LOGIN START")
        worker = DummyLoginWorker(True, False, 201)        
        try:
            worker.go(co, creds)
        except SystemExit, e:
            assert (e.code == EXIT_FAILURE)
            logger.info("INVALID USERNAME DUMMY LOGIN END\n")
        
        logger.info("INVALID PASSWORD DUMMY LOGIN START")
        worker = DummyLoginWorker(True, False, 202)        
        try:
            worker.go(co, creds)
        except SystemExit, e:
            assert (e.code == EXIT_FAILURE)
            logger.info("INVALID PASSWORD DUMMY LOGIN END\n")
        
        logger.info("MAX IP DUMMY LOGIN START")
        worker = DummyLoginWorker(True, False, 206)        
        try:
            worker.go(co, creds)
        except SystemExit, e:
            assert (e.code == EXIT_FAILURE)
            logger.info("MAX IP DUMMY LOGIN END\n")

        logger.info("UNKNOWN RC (DEBUG ON) DUMMY LOGIN START")
        worker = DummyLoginWorker(True, False, 300)
        worker_logger = logging.getLogger("worker")
        worker_logger.setLevel(logging.DEBUG)
        try:
            worker.go(co, creds)
        except SystemExit, e:
            assert (e.code == EXIT_FAILURE)
            logger.info("UNKNOWN RC (DEBUG ON) DUMMY LOGIN END\n")        
        
        logger.info("UNKNOWN RC (DEBUG OFF) DUMMY LOGIN START")
        worker_logger.setLevel(logging.WARNING)
        try:
            worker.go(co, creds)
        except SystemExit, e:
            assert (e.code == EXIT_FAILURE)
            logger.info("UNKNOWN RC (DEBUG OFF) DUMMY LOGIN END\n")
        
## end class LoginTestsuiteWorker