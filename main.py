from bearlibterminal import terminal
import os
import time
import importlib
import mss, mss.tools
import cv2

# ===========================
# CONFIGURAÇÃO DO TERMINAL
# ===========================
COLUMNS, ROWS = 80, 45
CELL_W, CELL_H = 16, 16
TITLE = "ASCIIMATION Studio"
FPS = 10
TOTAL_FRAMES = 80

# abre o terminal
terminal.open()
terminal.set(f"window: size={COLUMNS}x{ROWS}, cellsize={CELL_W}x{CELL_H}, title='{TITLE}'")

# ===========================
# DETECTA CENAS
# ===========================
# retorna uma lista de nomes de módulos Python na pasta 'scenes'
def get_scenes():
    scenes_folder = "scenes"
    scene_files = [f[:-3] for f in os.listdir(scenes_folder)
                   if f.endswith(".py") and f != "__init__.py"]
    return scene_files

# ===========================
# FUNÇÃO DO MENU GENÉRICO
# ===========================
def menu(options, title="MENU"):
    # menu genérico para escolher opções no terminal
    selected = 0
    while True:
        terminal.clear()
        terminal.printf(27, 1, f"=== {title} ===")
        for i, option in enumerate(options):
            prefix = "-> " if i == selected else "   "
            terminal.printf(25, 3 + i, f"{prefix}{option}")
        terminal.refresh()

        key = terminal.read()
        if key == terminal.TK_UP:
            selected = (selected - 1) % len(options)
        elif key == terminal.TK_DOWN:
            selected = (selected + 1) % len(options)
        elif key == terminal.TK_ENTER:
            return selected
        elif key in (terminal.TK_CLOSE, terminal.TK_ESCAPE):
            return None

# ===========================
# FUNÇÃO PARA EXPORTAR ANIMAÇÃO
# ===========================
def export_animation(scene_module, scene_number=1):
    # exporta a animação da cena selecionada para MASTER/scn_XX.mp4
    print(f"Iniciando exportação da cena '{scene_module.__name__}'...")

    # cria pastas MASTER e frames da cena
    master_folder = "MASTER"
    os.makedirs(master_folder, exist_ok=True)
    frames_folder = f"frames/{scene_module.__name__}"
    os.makedirs(frames_folder, exist_ok=True)
    print(f"Pasta '{frames_folder}' criada ou já existente.")

    sct = mss.mss()
    frames = []

    for i in range(TOTAL_FRAMES):
        start = time.time()

        # roda frame da animação no terminal
        scene_module.play_animation()

        # captura tela inteira
        filename = os.path.join(frames_folder, f"frame_{i:03}.png")
        screenshot = sct.grab(sct.monitors[1])
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=filename)
        frames.append(filename)

        print(f"Capturado frame {i + 1}/{TOTAL_FRAMES}")
        elapsed = time.time() - start
        if elapsed < 1 / FPS:
            time.sleep(1 / FPS)

    # cria vídeo
    screen_width = sct.monitors[1]["width"]
    screen_height = sct.monitors[1]["height"]
    output_file = os.path.join(master_folder, f"scn_{scene_number:02}.mp4")
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video = cv2.VideoWriter(output_file, fourcc, FPS, (screen_width, screen_height))

    print(f"Criando vídeo {output_file}...")
    for frame in frames:
        img = cv2.imread(frame)
        img_resized = cv2.resize(img, (screen_width, screen_height), interpolation=cv2.INTER_NEAREST)
        video.write(img_resized)

    video.release()
    print(f"Vídeo exportado com sucesso: {output_file}")

# ===========================
# LOOP PRINCIPAL
# ===========================
while True:
    # obtém lista de cenas
    scenes = get_scenes()
    if not scenes:
        print("Nenhuma cena encontrada na pasta 'scenes'.")
        break

    # menu de escolha de cena
    selected_index = menu(scenes + ["Sair"], title="Escolha a cena")
    if selected_index is None or selected_index == len(scenes):
        break

    # importa módulo da cena selecionada
    scene_name = scenes[selected_index]
    scene_module = importlib.import_module(f"scenes.{scene_name}")

    # menu de ação
    action_index = menu(["Tocar animação", "Tocar e exportar animação", "Voltar"], title=f"Cena: {scene_name}")
    if action_index == 0:
        print(f"Tocando cena '{scene_name}'...")
        scene_module.play_animation()
    elif action_index == 1:
        export_animation(scene_module, scene_number=selected_index + 1)
    else:
        continue

terminal.close()
print("Programa encerrado.")
