from bearlibterminal import terminal
import time

# Configurações da animação (mesmo padrão do main)
COLUMNS, ROWS = 80, 45
FPS = 10
TOTAL_FRAMES = 80

def play_animation():
    """Executa a animação da cena (ex: @ andando) no terminal."""
    for x in range(TOTAL_FRAMES):
        start = time.time()
        terminal.clear()
        terminal.printf(x % COLUMNS, ROWS // 2, "@")  # animação simples
        terminal.refresh()
        elapsed = time.time() - start
        if elapsed < 1 / FPS:
            time.sleep(1 / FPS)
