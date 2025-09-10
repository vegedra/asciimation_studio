from bearlibterminal import terminal as blt
from itertools import cycle
import sys
import os
import random

"""---------------------------------------------
Funções importantes que são usadas no programa:
---------------------------------------------"""

def clear_input_queue():
    # Clear the input queue
    while blt.has_input():
        blt.read()
        
def ascii_art(filename, x, y, ansi):
    # Construct the full file path using path_manager
    file_path = os.path.join('assets')

    try:
        # Tenta ler o arquivo .txt como UTF-8
        with open(file_path, 'r', encoding="utf-8") as file:
            content = file.read()
            blt.printf(x, y, content)
            if ansi == True:
                blt.printf(x, y, " ")
    except UnicodeDecodeError:
        try:
            # se nao for UTF-8 tenta com ANSI
            with open(file_path, 'r', encoding="ansi") as file:
                content = file.read()
                blt.printf(x, y, content)
                blt.printf(x, y, " ")
        except UnicodeDecodeError:
            print("Error: Unable to decode the file. Make sure it is saved in either UTF-8 or ANSI encoding.")
            
def transition(delay=100):
    blt.bkcolor('white') 
    blt.clear()  
    blt.refresh()  
    blt.delay(delay)

    blt.bkcolor('gray') 
    blt.clear()  
    blt.refresh()  
    blt.delay(delay+50)  

    blt.bkcolor('#171717') 
    blt.clear()  
    blt.refresh()  
    blt.delay(delay)

    blt.bkcolor('black')
    blt.clear()  
    blt.refresh()
    blt.delay(delay)  

    blt.clear()  
    blt.refresh()
    
def loading_bar(total, current, x, y, delay):
    # Animação da barra de loading com o logo da Relicorp em um .txt
    while current <= total:
        #blt.clear()
            
        # Preenche a barra de carregamento
        for i in range(current):
            blt.print(x+i, y, "█")
        blt.refresh()

        current += 1
        blt.delay(delay)
        
def auto_text(text, x, y, tempo):
    # Posição do texto
    cursor_x = x
    cursor_y = y
    
    # Loop que faz as letras aparecerem a cada x milisegundos
    for c in text:
        blt.print(cursor_x, cursor_y, c)
        cursor_x += 1
        blt.refresh()
        blt.delay(tempo)