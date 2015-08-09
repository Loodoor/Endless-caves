#-*- coding:Utf-8 -*

from cx_Freeze import setup, Executable

# On appelle la fonction setup
setup(
    name = "Endless caves",
    version = "0.1",
    description = "Jouer a The real fake",
    executables = [Executable("main.py")],
)