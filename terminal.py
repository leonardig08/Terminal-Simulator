import os
import sys
import time

from rich.console import Console
from rich.live import Live

from commands import Commands
from computer import Computer


class Terminal:
    def __init__(self):
        self.running = True
        self.pc = Computer(200, 16, 200)
        self.console = Console()
        self.running = True
        self.dir = "virtualenv"
        self.umask = "022"
        self.commands = Commands(self.console, self.umask)
        self.commandSyn = {"mkdir": ["mkdir", "md"], "rmdir": ["rmdir", "rm"], "remove": ["rm"], "ls": ["ls", "list"],
                           "echo": ["echo"], "clear": ["clear"], "shutdown": ["shutdown"], "reboot": ["reboot"],
                           "pwd": ["pwd"], "cat": ["cat"], "cd": ["cd", "chdir"] }

    @staticmethod
    def countram(chars, mem):
        time.sleep(0.02)
        char3 = chars
        # - / | \

        pri = ("ARCHLinux 3.2\n"
               "MAXARCHITECTURE v9\n"
               "MSI 756468\n\n"
               ) + "\nCounting RAM " + char3 + " " + str(mem) + "KB"
        return pri

    def turnon(self):
        self.running = False
        self.commands.clear()
        prog = 0
        pri = "ARCHLinux 3.2\n\n" + "\nCounting RAM"
        laps = 0
        i = 0
        past = ""
        with Live(pri, refresh_per_second=60) as live:
            while i < 200:
                match prog:
                    case 5:
                        char3 = "-"
                    case 10:
                        char3 = "\\"
                    case 15:
                        char3 = "|"
                    case 20:
                        char3 = "/"
                    case 25:
                        char3 = "-"
                        prog = 0
                    case _:
                        char3 = past
                laps += 1
                i += 1
                live.update(self.countram(char3, i))
                prog += 1
                past = char3
        time.sleep(0.5)
        self.console.print("CPU --- " + str(self.pc.mhz) + "MHZ")
        time.sleep(0.5)
        self.console.print("DISK -- " + str(self.pc.disk) + "MB")
        time.sleep(0.2)
        self.console.print("\n")
        with self.console.status(

                "Loading Shell", spinner="dots"

        ):
            time.sleep(5)
        self.console.print("Shell Loaded")
        self.running = True
        self.update()

    def update(self):
        while self.running:
            command = input("\n" + self.dir.replace("virtualenv", "@") + " >>")
            lest = command.split(" ")
            comd = lest[0]
            if comd in self.commandSyn.get("cat"):
                self.commands.cat(lest, self.dir)
            elif comd in self.commandSyn.get("rmdir"):
                self.commands.rmdir(lest, self.dir)
            elif comd in self.commandSyn.get("mkdir"):
                self.commands.mkdir(lest, self.dir)
            elif comd in self.commandSyn.get("cd"):
                self.console.print(self.commands.cd(lest, self.dir))
                self.dir = self.commands.cd(lest, self.dir)
            elif comd in self.commandSyn.get("ls"):
                self.commands.ls(self.dir)
            elif comd in self.commandSyn.get("clear"):
                self.commands.clear()
            elif comd in self.commandSyn.get("echo"):
                self.commands.echo(lest, self.dir)
            elif comd in self.commandSyn.get("shutdown"):
                self.running = False
                sys.exit(0)
            elif comd in self.commandSyn.get("reboot"):
                self.console.print("Rebooting...")
                time.sleep(1)
                os.system("py terminal.py")
            elif comd in self.commandSyn.get("pwd"):
                self.commands.pwd(self.dir)
            else:
                self.console.print("Command " + lest[0] + " not found")


terminal = Terminal()
terminal.turnon()
