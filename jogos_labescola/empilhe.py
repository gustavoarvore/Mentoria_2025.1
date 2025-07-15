import pygame
import random
import time
import sys

# Inicialização
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Empilha Blocos Matemáticos")
FONT = pygame.font.SysFont('Arial', 36)
SMALL_FONT = pygame.font.SysFont('Arial', 24)

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
GRAY = (200, 200, 200)

# Configurações
BLOCK_WIDTH, BLOCK_HEIGHT = 100, 30
MAX_TIME = 90  # 1 minuto e 30 segundos

class Block:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
    
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, BLOCK_WIDTH, BLOCK_HEIGHT))
        pygame.draw.rect(screen, BLACK, (self.x, self.y, BLOCK_WIDTH, BLOCK_HEIGHT), 2)

def generate_question():
    operations = ['+', '-', '*', '/']
    operation = random.choice(operations)
    
    if operation == '+':
        a, b = random.randint(1, 20), random.randint(1, 20)
        return f"{a} + {b} = ?", a + b
    elif operation == '-':
        a, b = random.randint(1, 20), random.randint(1, 20)
        if a < b: a, b = b, a  # Evita resultados negativos
        return f"{a} - {b} = ?", a - b
    elif operation == '*':
        a, b = random.randint(1, 10), random.randint(1, 10)
        return f"{a} × {b} = ?", a * b
    elif operation == '/':
        b = random.randint(1, 10)
        answer = random.randint(1, 5)
        a = b * answer  # Garante divisão exata
        return f"{a} ÷ {b} = ?", answer

def main():
    blocks = []
    question, correct_answer = generate_question()
    user_input = ""
    correct = wrong = 0
    start_time = time.time()
    game_active = True

    while True:
        current_time = time.time()
        remaining_time = max(0, MAX_TIME - (current_time - start_time))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            if game_active and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_input.isdigit() and int(user_input) == correct_answer:
                        correct += 1
                        # Adiciona bloco
                        x = WIDTH//2 - BLOCK_WIDTH//2 if not blocks else blocks[-1].x + random.randint(-20, 20)
                        y = HEIGHT - 100 if not blocks else blocks[-1].y - BLOCK_HEIGHT
                        x = max(10, min(x, WIDTH - BLOCK_WIDTH - 10))  # Mantém na tela
                        blocks.append(Block(x, y, random.choice(COLORS)))
                    else:
                        wrong += 1
                        # Remove bloco se existir
                        if blocks:
                            blocks.pop()
                    question, correct_answer = generate_question()
                    user_input = ""
                
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.unicode.isdigit():
                    user_input += event.unicode
        
        # Renderização
        screen.fill(WHITE)
        
        # Desenha base
        pygame.draw.rect(screen, GRAY, (0, HEIGHT - 70, WIDTH, 70))
        
        # Desenha blocos
        for block in blocks:
            block.draw()
        
        # Mostra pergunta e input
        question_text = FONT.render(question, True, BLACK)
        input_text = FONT.render(f"Resposta: {user_input}", True, BLACK)
        screen.blit(question_text, (50, 50))
        screen.blit(input_text, (50, 100))
        
        # Mostra tempo
        time_text = FONT.render(f"Tempo: {int(remaining_time)}s", True, BLACK)
        screen.blit(time_text, (WIDTH - 200, 50))
        
        # Fim do jogo
        if remaining_time <= 0 and game_active:
            game_active = False
        
        if not game_active:
            # Fundo semi-transparente
            s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            s.fill((0, 0, 0, 180))
            screen.blit(s, (0, 0))
            
            # Resultados
            result_text = [
                "FIM DE JOGO!",
                f"Acertos: {correct}",
                f"Erros: {wrong}",
                f"Blocos empilhados: {len(blocks)}",
                "Pressione ESC para sair"
            ]
            
            for i, text in enumerate(result_text):
                text_surface = FONT.render(text, True, WHITE)
                text_rect = text_surface.get_rect(center=(WIDTH//2, 150 + i * 50))
                screen.blit(text_surface, text_rect)
            
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                pygame.quit()
                return

        pygame.display.flip()

if __name__ == "__main__":
    main()