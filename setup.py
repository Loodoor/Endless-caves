#-*- coding:Utf-8 -*

from cx_Freeze import setup, Executable

setup(
    name = "Endless caves",
    version = "0.2.2",
    description = "Jouer a Endless caves",
    executables = [Executable("main.py")],
)