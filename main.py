from cli import Cli
from kontroller import Kontroller
from gui import start

if __name__ == "__main__":
    filnavn = "Passord.txt"
    brukere = "Users.txt"
    klient = Kontroller(filnavn, brukere)
    start(filnavn, brukere, klient)