from cli import Cli
from kontroller import Kontroller
from gui import start

def startGui():
    klient = Kontroller(brukere)
    start(klient)


def startCli():
    kontroller = Kontroller(brukere)
    Cli(brukere, kontroller)

if __name__ == "__main__":
    brukere = "Users.txt"
    startGui()
