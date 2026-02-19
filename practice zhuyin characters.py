import pygame
import random
import sys

pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zhuyin Typing Trainer")

font = pygame.font.SysFont("Microsoft JhengHei", 100)
small_font = pygame.font.SysFont("Microsoft JhengHei", 40)
Xsmall_font = pygame.font.SysFont("Microsoft JhengHei", 20)

# Full Zhuyin to keyboard mapping
mapping = {
    'ㄅ B': '1', 'ㄆ P': 'q', 'ㄇ M': 'a', 'ㄈ F': 'z',
    'ㄉ D': '2', 'ㄊ T': 'w', 'ㄋ N': 's', 'ㄌ L': 'x',
    'ㄍ G': 'e', 'ㄎ K': 'd', 'ㄏ H': 'c',
    'ㄐ J': 'r', 'ㄑ Q': 'f', 'ㄒ X': 'v',
    'ㄓ Zh': '5', 'ㄔ Ch': 't', 'ㄕ Sh': 'g', 'ㄖ R': 'b',
    'ㄗ Z': 'y', 'ㄘ C': 'h', 'ㄙ S': 'n',
    'ㄧ Yi': 'u', 'ㄨ W': 'j', 'ㄩ Yu': 'm',
    'ㄚ A': '8', 'ㄛ O': 'i', 'ㄜ E': 'k', 'ㄝ Eh': ',',
    'ㄞ Ai': '9', 'ㄟ Ei': 'o', 'ㄠ Ao': 'l', 'ㄡ Ou': '.',
    'ㄢ An': '0', 'ㄣ En': 'p', 'ㄤ Ang': ';', 'ㄥ Eng': '/',
    'ㄦ Er': '-', 
    'Tone_up': '6', 'ˇ': '3', '`': '4', '˙': '7'
}

# Levels (all keys must match mapping keys exactly)
levels_normal = [
    ['ㄅ B','ㄆ P','ㄇ M','ㄈ F'],  # Level 1
    ['ㄉ D','ㄊ T','ㄋ N','ㄌ L'],  # Level 2
    ['ˇ','ㄍ G','ㄎ K','ㄏ H'],           # Level 3
    ['`','ㄐ J','ㄑ Q','ㄒ X'],           # Level 4
    ['ㄓ Zh','ㄔ Ch','ㄕ Sh','ㄖ R'], # Level 5
    ['Tone_up','ㄗ Z','ㄘ C','ㄙ S'],           # Level 6
    ['˙','ㄧ Yi', 'ㄨ W', 'ㄩ Yu'],           # Level 7
    ['ㄚ A','ㄛ O','ㄜ E','ㄝ Eh'],   # Level 8
    ['ㄞ Ai','ㄟ Ei','ㄠ Ao','ㄡ Ou'],  # Level 9
    ['ㄢ An','ㄣ En','ㄤ Ang','ㄥ Eng', 'ㄦ Er'] # Level 10
]

# start from lvl 10 to lvl 1
levels_mirror = levels_normal[::-1].copy()


# if want to train on rows rather than columns, change this into levels and vice versa (change score to change level to 30, next_unlock always 30 and += 30)
transposed = [
    ['ㄅ B','ㄉ D','ˇ','`','ㄓ Zh','Tone_up','˙','ㄚ A','ㄞ Ai','ㄢ An','ㄦ Er'], # Level 1
    ['ㄆ P','ㄊ T','ㄍ G','ㄐ J','ㄔ Ch','ㄗ Z','ㄧ Yi','ㄛ O','ㄟ Ei','ㄣ En'], # Level 2
    ['ㄇ M','ㄋ N','ㄎ K','ㄑ Q','ㄕ Sh','ㄘ C','ㄨ W','ㄜ E','ㄠ Ao','ㄤ Ang'], # Level 3
    ['ㄈ F','ㄌ L','ㄏ H','ㄒ X','ㄖ R','ㄙ S','ㄩ Yu','ㄝ Eh','ㄡ Ou','ㄥ Eng'] # Level 4
]

levels = levels_normal


# Game state
score = 0
level = 1
next_unlock = 10  # first unlock at 10 points
feedback_color = (255, 255, 255)  # default white
feedback_time = 0  # when feedback started
feedback_level_color = (255, 255, 255)  # default white
feedback_level_time = 0  # when feedback started
mistakes = 0

# Game loop
clock = pygame.time.Clock()

start_ticks = pygame.time.get_ticks()  # store start time

unlocked = levels[0].copy()  # start with level 1 set
target = random.choice(unlocked)

def new_target():
    return random.choice(unlocked)

def unlock_next_level():
    global level, unlocked
    if level < len(levels):
        level += 1
        unlocked.extend(levels[level-1])  # do next group
        return True
    return False

# Game loop
while True:
    screen.fill((30, 30, 30))
    # Suppose target = 'ㄅ B'
    # Split Zhuyin and phonetic
    if ' ' in target:
        zhuyin_char, phonetic = target.split(' ', 1)
    else:
        zhuyin_char, phonetic = target, ''

    # Show current zhuyin character
    text = font.render(zhuyin_char, True, feedback_color)
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//3))

    # Render phonetic hint smaller, top-right corner
    if phonetic:
        phonetic_text = font.render(phonetic, True, (150, 150, 150))
        screen.blit(phonetic_text, (WIDTH - phonetic_text.get_width() - 20, 20))
    # Show score and level
    score_text = small_font.render(f"Score: {score}", True, (200, 200, 200))
    screen.blit(score_text, (10, 10))
    level_text = small_font.render(f"Level: {level}", True, feedback_level_color)
    screen.blit(level_text, (10, 50))

    # Show howlong you been playin
    elapsed_seconds = (pygame.time.get_ticks() - start_ticks) / 1000
    timer_text = Xsmall_font.render(f"Time: {int(elapsed_seconds)}s", True, (200,200,200))
    screen.blit(timer_text, (WIDTH - timer_text.get_width() - 20, HEIGHT - 30))

    mistake_text = Xsmall_font.render(f"Amount of mistakes: {mistakes}", True, (200, 200, 200))
    screen.blit(mistake_text, (10, HEIGHT - 30))

    # Define button rectangle
    button_width, button_height = 75, 25
    button_x = 5 
    button_y = HEIGHT//2 # below the Zhuyin character
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    # Render button
    pygame.draw.rect(screen, (50, 150, 50), button_rect)  # green button
    button_text = Xsmall_font.render("Restart", True, (255, 255, 255))
    screen.blit(button_text, (10,
                            button_y + (button_height - button_text.get_height())//2))

    pygame.display.flip()

    # Reset feedback color after 300 ms
    if feedback_time and pygame.time.get_ticks() - feedback_time > 500:
        feedback_color = (255, 255, 255)
        feedback_time = 0
        # Reset feedback color after 300 ms
    if feedback_level_time and pygame.time.get_ticks() - feedback_level_time > 1500:
        feedback_level_color = (255, 255, 255)
        feedback_level_time = 0

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.unicode == mapping[target]:
                score += 1
                feedback_color = (0, 255, 0)  # green
                feedback_time = pygame.time.get_ticks()
                # Unlock next level every 10 points
                if score >= next_unlock:
                    if unlock_next_level():
                        next_unlock += 10  
                        feedback_level_color = (0, 255, 0)  # green
                        feedback_level_time = pygame.time.get_ticks()
                        print(f"Unlocked Level {level}!")
                new_target_test = new_target()  
                while new_target_test == target:
                    new_target_test = new_target()                      
                target = new_target_test
            else:
                score = max(0, score - 1)  # small penalty
                feedback_color = (255, 0, 0)  # red
                mistakes += 1
                feedback_time = pygame.time.get_ticks()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                # Reset game state
                score = 0
                level = 1
                next_unlock = 10
                unlocked = levels[0].copy()
                target = random.choice(unlocked)
                start_ticks = pygame.time.get_ticks()  # reset timer
                feedback_color = (255, 255, 255)
                feedback_time = 0     
                feedback_level_color = (255, 255, 255)
                feedback_level_time = 0     
                mistakes = 0           
    clock.tick(60)