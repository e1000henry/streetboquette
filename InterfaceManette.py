import pygame

# --- CONFIGURATION DE VOTRE MANETTE ---
# MODIFIÉ SELON VOS SPÉCIFICATIONS : X=0, A=1, B=2, Y=3

# Dictionnaire qui associe un NUMÉRO de bouton à un NOM d'action.
BUTTON_MAP = {
    0: "action_x",    # Votre bouton X
    1: "action_a",    # Votre bouton A
    2: "action_b",    # Votre bouton B
    3: "action_y",    # Votre bouton Y
    
    # ATTENTION : VÉRIFIEZ LES NUMÉROS POUR CES BOUTONS AVEC LE SCRIPT DE DIAGNOSTIC
    4: "action_l",    # Gâchette Gauche (Left)
    5: "action_r",    # Gâchette Droite (Right)
    8: "select",      # Bouton Select
    9: "start",       # Bouton Start
}

# Configuration de la croix directionnelle (D-Pad)
# La plupart des manettes modernes utilisent deux axes pour le D-Pad.
# Si votre diagnostic a montré un "Chapeau (HAT)", mettez USE_HAT_FOR_DPAD à True.
USE_HAT_FOR_DPAD = False 
DPAD_AXIS_HORIZONTAL = 0  # Numéro de l'axe pour Gauche/Droite
DPAD_AXIS_VERTICAL = 1    # Numéro de l'axe pour Haut/Bas

# --- FIN DE LA CONFIGURATION ---


def get_actions_from_joystick(joystick):
    """
    Lit l'état de la manette et retourne un dictionnaire d'actions claires.
    C'est le "traducteur" universel.
    """
    actions = {
        "haut": 0, "bas": 0, "gauche": 0, "droite": 0,
        "action_a": 0, "action_b": 0, "action_x": 0, "action_y": 0,
        "action_l": 0, "action_r": 0, "select": 0, "start": 0
    }

    # 1. Traduire les boutons (A, B, X, Y, Start, etc.)
    for btn_index in range(joystick.get_numbuttons()):
        if joystick.get_button(btn_index):
            if btn_index in BUTTON_MAP:
                action_name = BUTTON_MAP[btn_index]
                actions[action_name] = 1

    # 2. Traduire la croix directionnelle (D-Pad)
    if USE_HAT_FOR_DPAD:
        if joystick.get_numhats() > 0:
            hat_x, hat_y = joystick.get_hat(0)
            if hat_x == -1: actions["gauche"] = 1
            if hat_x == 1: actions["droite"] = 1
            if hat_y == 1: actions["haut"] = 1
            if hat_y == -1: actions["bas"] = 1
    else:
        if joystick.get_numaxes() >= 2:
            axis_x = joystick.get_axis(DPAD_AXIS_HORIZONTAL)
            axis_y = joystick.get_axis(DPAD_AXIS_VERTICAL)
            if axis_x < -0.5: actions["gauche"] = 1
            if axis_x > 0.5: actions["droite"] = 1
            if axis_y < -0.5: actions["haut"] = 1
            if axis_y > 0.5: actions["bas"] = 1
            
    return actions

# --- Programme principal pour tester le traducteur ---
pygame.init()
screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("Testeur de Mappage Manette")
font = pygame.font.Font(None, 24)
clock = pygame.time.Clock()

try:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Manette prête : {joystick.get_name()}")
except pygame.error:
    print("ERREUR : Aucune manette détectée.")
    exit()

# Boucle principale
running = True
last_actions_str = ""
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # On récupère toutes les actions dans un format simple !
    current_actions = get_actions_from_joystick(joystick)

    # On prépare l'affichage
    active_actions = [name for name, active in current_actions.items() if active]
    actions_str = "Actions actives : " + ", ".join(active_actions)
    
    if actions_str != last_actions_str:
        print(actions_str)
        last_actions_str = actions_str

    # Affichage à l'écran
    screen.fill((20, 20, 40))
    text_surface = font.render(actions_str, True, (255, 255, 255))
    screen.blit(text_surface, (10, 10))
    pygame.display.flip()

    # Quitter le test en appuyant sur START
    if current_actions["start"] == 1:
        running = False
        
    clock.tick(30)

pygame.quit()