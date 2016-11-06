# coding=utf-8

"""
FeedService launches IQConnect.exe if necessary.

On Windows it does this by simply calling the Windows API function
ShellExecute, which with the right parameters launches IQConnect.exe
only if an instance is not already running.

On Linux and OSX it tries to connect to the Administrative Port of
IQConnect.exe. If it can connect it assumes that IQConnect.exe is
running and returns. Otherwise it launches IQConnect.exe and tries
connecting repeatedly until it connects and returns or times out
and throws.

If you are running under Wine, the wine executable must be in your
path.

This class assumes that you have not changed the default ports on
which IQConnect.exe listens. If you have, you will need to change the
port numbers in class FeedConn in file conn.py.

DO NOT plan to create a new FeedService and launch to start IQFeed.exe
from each of multiple instances of some trading app. There just doesn't
seem to be a way of making that actually robust.  Instead write
something which runs from cron, which starts IQFeed.exe and stays
connected to it because once the last app disconnects, IQFeed.exe exits.

"""


import os
import sys
import time
import socket
import select
import subprocess


def _is_iqfeed_running():
    """Return True if a socket can connect to the IQFeed Admin Port."""
    iqfeed_host = "127.0.0.1"
    iqfeed_ports = [5009, 9100, 9200, 9300, 9400]

    try:
        for port in iqfeed_ports:
            s = socket.create_connection((iqfeed_host, port), 5)
            rl = select.select([s], [], [], 0.5)
            while rl[0]:
                # Read startup messages otherwise you get a zombie socket
                s.recv(16384)
                rl = select.select([s], [], [], 0.5)
            s.shutdown(socket.SHUT_RDWR)
            s.close()
        return True
    except ConnectionRefusedError:
        return False


class FeedService:
    """
    FeedService launches IQConnect.exe if necessary.

    Initialize the FeedService by passing your IQFeed login parameters to
    __init__  and then call launch to actually launch IQConnect.exe.
    Launch checks if IQConnect.exe is running and only starts a new instance
    if it isn't already running.

    """

    def __init__(self,
                 product: str,
                 version: str,
                 login: str,
                 password: str):
        """
        Initialize the FeedService class.

        :param product: The Product ID given to you by DTN
        :param version: The version of YOUR APP. Not the version of IQFeed.
        :param login: Your IQFeed Service Login
        :param password: Your IQFeed Service Password

        """
        self.product = product
        self.version = version
        self.login = login
        self.password = password

    def launch(self,
               timeout: int=20,
               check_conn: bool = True,
               headless: bool = False,
               launch_log: str = "~/nohup_launch_iqfeed.log") -> None:
        """
        Launch IQConnect.exe if necessary

        :param timeout: Throw if IQConnect is not listening in timeout secs.
        :param check_conn: Try opening connections to IQFeed before returning.
        :param headless: Set to true if running in headless mode on X windows.
        :param launch_log: Logs errors while launching IQFeed. This is NOT the
            IQFeed log file.
        :return: True if IQConnect is now listening for connections.

        """
        # noinspection PyPep8
        iqfeed_args = ("-product %s -version %s -login %s -password %s -autoconnect -savelogininfo" %
                       (self.product, self.version, self.login, self.password))

        if not _is_iqfeed_running():
            if sys.platform == 'win32':
                # noinspection PyPep8Naming
                ShellExecute = __import__('win32api').ShellExecute
                # noinspection PyPep8Naming
                SW_SHOWNORMAL = __import__('win32con').SW_SHOWNORMAL
                ShellExecute(0, "open", "IQConnect.exe", iqfeed_args, "",
                             SW_SHOWNORMAL)
            elif sys.platform == 'darwin' or sys.platform == 'linux':
                if launch_log is None:
                        raise RuntimeError(
                            "Must set a log file for logging launch errors.")
                base_iqfeed_call = "wine iqconnect.exe %s" % iqfeed_args
                if headless:
                    iqfeed_call = ("nohup xvfb-run -s -noreset -a %s > %s" %
                                   (base_iqfeed_call, launch_log))
                else:
                    iqfeed_call = ("nohup %s > %s" %
                                   (base_iqfeed_call, launch_log))

                print("Running %s" % iqfeed_call)
                subprocess.Popen(iqfeed_call,
                                 shell=True,
                                 stdin=subprocess.DEVNULL,
                                 stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL,
                                 preexec_fn=os.setpgrp)
                time.sleep(1)
            if check_conn:
                start_time = time.time()
                while not _is_iqfeed_running():
                    time.sleep(1)
                    if time.time() - start_time > timeout:
                        raise RuntimeError("Launching IQFeed timed out.")

    def admin_variables(self):
        """Return a dict of admin variables used to launch"""
        return {"product": self.product,
                "login": self.login,
                "password": self.password}
