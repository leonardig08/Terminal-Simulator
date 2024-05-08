import os
import re
import time
from pathlib import Path
import json


class Commands:
    def __init__(self, console, umask):
        self.console = console
        self.umask = umask


    def cat(self, lest, direc):
        for i in lest[1:]:
            stringcat = ""
            if os.path.isfile(f"{direc}/{i}"):
                stringcat += i
            else:
                self.console.print(f"{i} not found or not enough permission")

    def rmdir(self, lest, direc):
        content = lest[1:]
        for i in content:
            try:
                os.rmdir(f"{direc}/{i}")
                os.remove(f"prop/{direc}/{i}.prop")
            except FileExistsError or FileNotFoundError:
                self.console.print("Error: File not found")

    def mkdir(self, lest, direc):
        content = lest[1:]
        for i in content:
            try:
                os.mkdir(f"{direc}/{i}")
            except FileExistsError or FileNotFoundError:
                self.console.print("Error: File already exists")
            info = Path(f"prop/{direc}/{i}.prop")
            properties = 777
            properties -= int(self.umask)
            write = json.dumps(properties)
            info.write_text(write)

    @staticmethod
    def cd(lest, direc):
        i = lest[1]
        if i == ".":
            lul = direc.split("/")
            if os.path.isdir(lul.pop(len(lul) - 1)):
                print("no dir" + lul)
                direc = "/".join(lul)
            else:
                pass
        elif os.path.isdir(direc + "/" + i):
            direc += "/" + i
        return direc

    def ls(self, direc):
        stringprint = ""
        for i in os.listdir(direc):
            binperm = Path("prop/" + direc + f"/{i}.prop")
            perms = binperm.read_text()
            permstring = ""
            if os.path.isdir(direc + f"/{i}"):
                permstring += "d"
            for j in perms:
                j = str(bin(int(j)))[2:]
                if j[0] == "1":
                    permstring += "r"
                else:
                    permstring += "-"
                if j[1] == "1":
                    permstring += "w"
                else:
                    permstring += "-"
                if j[2] == "1":
                    permstring += "x"
                else:
                    permstring += "-"
            stringprint += f"\n{permstring}\t{i}"
        self.console.print(stringprint)

    def echo(self, lest, direc):
        check = 0
        print(lest)
        cont = " ".join(lest)
        stringer = str(re.findall("(\".+\")", cont)[0])
        stringer = stringer.replace('"', "")
        stringer = stringer.encode().decode("unicode_escape")
        for i in lest[1:]:
            if i == ">" and len(lest) >= 3:
                try:
                    num = lest.index(">")
                except ValueError:
                    self.console.print("Error: Syntax Error")
                    break
                title = lest[num + 1]
                file = Path(f"{direc}/{title}")
                file.write_text(stringer)
                properties = 666
                properties -= int(self.umask)
                info = Path(f"prop/{direc}/{title}.prop")
                write = json.dumps(properties)
                info.write_text(write)
                check = 1
            elif i == ">>" and len(lest) >= 3:
                try:
                    num = lest.index(">>")
                except ValueError:
                    self.console.print("Error: Syntax Error")
                    break
                title = lest[num + 1]
                file = Path(f"{direc}/{title}")
                try:
                    past = file.read_text()
                    file.write_text(past + "\n" + stringer)
                except FileNotFoundError:
                    file.write_text(stringer)
                    properties = 666
                    properties -= int(self.umask)
                    info = Path(f"prop/{direc}/{title}.prop")
                    write = json.dumps(properties)
                    info.write_text(write)
                check = 1
        if check == 0:
            self.console.print(stringer)

    def pwd(self, direc):
        direc = direc.replace("virtualenv", "@")
        self.console.print("\n"+direc)

    def id(self, utype):
        usertypes = ["guest", "root"]
        user = usertypes[utype]
        self.console.print("\n"+user)
    def reload(self):
        self.console.print("Reloading")
        time.sleep(0.8)
        text = json.dumps(1)
        file = Path("status/reload.stat")
        file.write_text(text)
        os.system("py terminal.py")


    @staticmethod
    def clear():
        os.system("cls")
