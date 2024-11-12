import pygame
import sys
import os

# Initialize pygame
pygame.init()

# Set up display with increased window size
WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 800
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Advanced Image Augmentation Tool")

# Load an image
img_path = "img/1.jpg"  # Replace with the path to your image
if not os.path.exists(img_path):
    raise FileNotFoundError("Image file not found!")

# Load and scale image to fit window while maintaining aspect ratio
original_image = pygame.image.load(img_path)
original_width, original_height = original_image.get_size()
scale_ratio = min(WINDOW_WIDTH / original_width, (WINDOW_HEIGHT - 160) / original_height)  # Leave room for toolbar
image = pygame.transform.scale(original_image, (int(original_width * scale_ratio), int(original_height * scale_ratio)))
image_rect = image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))

# Define transformation options
rotation_angle = 0
scale_factor = 1
flip_x, flip_y = False, False

# Set up fonts and colors
font = pygame.font.SysFont(None, 28)
button_color = (70, 70, 70)
button_hover_color = (100, 100, 100)
button_text_color = (255, 255, 255)

# Ensure output folder exists
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

# Define the draw_text function to display text on the screen
def draw_text(text, pos, color=(255, 255, 255)):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, pos)

# Button class
class Button:
    def __init__(self, text, pos, action=None, width=140, height=50):
        self.text = text
        self.pos = pos
        self.action = action
        self.width = width
        self.height = height
        self.rect = pygame.Rect(pos[0], pos[1], width, height)

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        color = button_hover_color if self.rect.collidepoint(mouse_pos) else button_color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        
        text_surface = font.render(self.text, True, button_text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if self.action:
                self.action()

# Define button actions
def rotate_left():
    global rotation_angle
    rotation_angle -= 15

def rotate_right():
    global rotation_angle
    rotation_angle += 15

def scale_up():
    global scale_factor
    scale_factor += 0.1 if scale_factor < 3 else 0

def scale_down():
    global scale_factor
    scale_factor -= 0.1 if scale_factor > 0.3 else 0

def flip_horizontal():
    global flip_x
    flip_x = not flip_x

def flip_vertical():
    global flip_y
    flip_y = not flip_y

def reset_image():
    global rotation_angle, scale_factor, flip_x, flip_y
    rotation_angle = 0
    scale_factor = 1
    flip_x, flip_y = False, False

def save_image():
    transformed_image = pygame.transform.rotozoom(original_image, rotation_angle, scale_factor * scale_ratio)
    if flip_x or flip_y:
        transformed_image = pygame.transform.flip(transformed_image, flip_x, flip_y)
    
    output_path = os.path.join(output_folder, "edited_image.jpg")
    pygame.image.save(transformed_image, output_path)
    print(f"Image saved to {output_path}")

# Create buttons with updated positions, sizes, and clear spacing
buttons = [
    Button("Rotate Left", (40, 700), rotate_left),
    Button("Rotate Right", (200, 700), rotate_right),
    Button("Scale Up", (360, 700), scale_up),
    Button("Scale Down", (520, 700), scale_down),
    Button("Flip Horizontal", (680, 700), flip_horizontal),
    Button("Flip Vertical", (840, 700), flip_vertical),
    Button("Reset", (40, 760), reset_image, 180, 50),
    Button("Save", (360, 760), save_image, 180, 50),
    Button("Quit", (680, 760), sys.exit, 180, 50)
]

# Main loop
running = True
while running:
    screen.fill((50, 50, 50))  # Darker background for better contrast

    # Display title
    draw_text("Image Augmentation Tool", (20, 20), (200, 200, 200))

    # Transform image
    transformed_image = pygame.transform.rotozoom(image, rotation_angle, scale_factor)
    if flip_x or flip_y:
        transformed_image = pygame.transform.flip(transformed_image, flip_x, flip_y)
    
    # Draw image
    transformed_rect = transformed_image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
    screen.blit(transformed_image, transformed_rect)

    # Draw buttons
    for button in buttons:
        button.draw()

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for button in buttons:
                button.check_click(event)

    pygame.display.flip()  # Update the screen

pygame.quit()
sys.exit()
