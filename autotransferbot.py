#!/usr/bin/env python
# -*- Coding: UTF-8 -*-
"""
Auto Transfer Bot for T80S Telescope:
This module containg the class that perform the automatic data Transfer
process every day in a given time.
"""
import time
from datetime import datetime, timedelta
import sched
import os
# from subprocess import check_call, CalledProcessError
import copy
import logging


__AUTHOR = "E. S. Pereira"
__DATE = "14/06/2017"
__EMAIL = "pereira.somoza@gmail.com"


class Autotransferbot(object):
    """
    Auto Transfer Bot: Used to perform the automatic data Transfer.
    Attr:
        user: A name of user or a alternative name for bot
        useremail: e-mail address that the bot will send info
        about the reduction process
    Optional Attr:
        client_ip: IP of the machine that the bot is running
        delta_time_hours: Time range between reductions
        work_dir: The location where the bot will save temp data and log files
    """

    def __init__(self,
                 user,
                 useremail,
                 **kwargs):

        client_ip = "localhost"
        self._delta_time_hours = 24,
        self._work_dir = "./"

        allowed_keys = set(['client_ip',
                            'delta_time_hours',
                            'work_dir'])

        self._scheduler = sched.scheduler(timefunc=time.time,
                                          delayfunc=time.sleep)

        self._next_transfer = datetime.now()
        self.useremail = useremail

        if kwargs is not None:
            for key, value in kwargs.items():
                if key in allowed_keys:
                    if key == 'client_ip':
                        client_ip = value
                    else:
                        setattr(self, '_' + key, value)

        self._extra = {'clientip': client_ip, 'user': user}

        if self._work_dir[-1] == "/":
            self._work_dir += "autotransferWDir/"
        else:
            self._work_dir += "/autotransferWDir/"

        if os.path.isdir(self._work_dir) is False:
            os.makedirs(self._work_dir)

        if os.path.isdir(self._work_dir + "botLoggin") is False:
            os.makedirs(self._work_dir + "botLoggin")

        self._logger = logging.getLogger()

        _format = "%(asctime)-15s %(clientip)s %(user)-8s %(message)s"

        loggin_name = "reduction_{}.log".format(
            datetime.now().strftime("%Y%m%dT%H:%M:%S"))

        logging.basicConfig(filename=self._work_dir + "/botLoggin/"
                            + loggin_name,
                            level=logging.DEBUG,
                            format=_format)

        self._logger.info("The Transfer Bot is Starting.", extra=self._extra)

    def get_next_transfer(self):
        """
        Return a date object representing the next Transfer date time.
        """
        return copy.copy(self._next_transfer)

    def has_newData(self):
        """
        Verify if there are new reduced data.
        """
        return True

    def _start_transfer(self):
        pass

    def _rescheduler(self):
        self._next_transfer = datetime.now() + \
            timedelta(hours=self._delta_time_hours)

        if self.has_newData() is True:
            self._start_transfer()

        info = "Next Transfer will be started at: {}".format(
            self._next_transfer)

        self._logger.info(info, extra=self._extra)

        self._scheduler.enterabs(time.mktime(self._next_transfer.timetuple()),
                                 priority=0,
                                 action=self._rescheduler,
                                 argument=())

    def _set_time(self, hours, minutes):
        """
        Set the start time of the Transfer process.
        """
        current_time = datetime.now()
        set_time = current_time.replace(hour=hours, minute=minutes)
        delta_time = set_time - current_time
        if delta_time.total_seconds() < 0:
            next_time = current_time + timedelta(hours=12)
            next_time = next_time.replace(hour=hours, minute=minutes)
        else:
            next_time = set_time

        self._next_transfer = next_time
        info = "Next Transfer will be started at: {}".format(
            self._next_transfer)

        self._logger.info(info, extra=self._extra)

        self._scheduler.enterabs(time.mktime(next_time.timetuple()),
                                 priority=0,
                                 action=self._rescheduler,
                                 argument=())

    def run(self, hours, minutes):
        """
        Start the scheduler to run the Transfer in autonomous mode.
        input:
            hours: the hour of firts Transfer start
            minutes: the minutes of firts Transfer start
        """
        self._set_time(hours, minutes)
        try:
            self._scheduler.run()
        except KeyboardInterrupt:
            self._logger.info("Stopping the Bot.", extra=self._extra)


if __name__ == "__main__":
    import argparse
    DESCRIPTION = '''Autonomos Transfer Bot.
    The Bot Search for reduced data in current day and start the
    data Transfer process.
    '''
    PARSER = argparse.ArgumentParser(
        description=DESCRIPTION)

    PARSER.add_argument("-u",
                        help="User Name",
                        type=str,
                        default="jype")

    PARSER.add_argument("-e",
                        help="User email",
                        type=str,
                        default='')

    TINFO = "Time interval, in hours, for the next data Transfer"

    PARSER.add_argument("-t",
                        help=TINFO,
                        type=int,
                        default=24)

    PARSER.add_argument("-s",
                        help="The hour that the bot start the Transfer",
                        type=int,
                        default=7)

    PARSER.add_argument("-m",
                        help="The minutes that the bot start the Transfer",
                        type=int,
                        default=0)

    ARGS = PARSER.parse_args()

    BOT = Autotransferbot(user=ARGS.u,
                          useremail=ARGS.e,
                          delta_time_hours=ARGS.t)
    BOT.run(ARGS.s, ARGS.m)
