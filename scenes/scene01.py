from bearlibterminal import terminal as blt
import utils as utils
import time

# Configurações da animação (mesmo padrão do main)
COLUMNS, ROWS = 80, 45
FPS = 12
TOTAL_FRAMES = 80

def play_animation():
    # Executa a animação da cena (ex: @ andando) no terminal
    for x in range(TOTAL_FRAMES):
        start = time.time()
        blt.clear()
        blt.printf(x % COLUMNS, ROWS // 2, "@")  # animação simples
        blt.refresh()
        elapsed = time.time() - start
        if elapsed < 1 / FPS:
            time.sleep(1 / FPS)
        utils.clear_input_queue()