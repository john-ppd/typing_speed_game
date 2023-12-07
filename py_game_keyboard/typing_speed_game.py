import time
from datetime import date
import pygame
import pygame.freetype
from essential_generators import DocumentGenerator

# Initialize a new instance of the DocumentGenerator class.
# This will be used to generate random sentences for our game.
gen = DocumentGenerator()

# make gui with dimensions (900, 600)
screen = pygame.display.set_mode((900, 600))
# store rgb of green color
GREEN = (0, 255, 0)
# create a variable to store the length of the game time (5 minutes) in seconds
timer = 60 * 5
# get current date
today = date.today()
# store the current date in yy/mm/dd format
d3 = today.strftime("%y_%m_%d_")
# keeps track of wrong moves each game
wrong_moves = 0
# keeps track of correct moves each game
correct_moves = 0
# keeps track of how many backspaces the user has to press before they can type more
needs_backspace = 0
# keeps track of what game mode the user selects
game_mode = 0
# will be used to keep track of the time we start our play through
time_start = 0
# game active flag, when false we display menu and wait for key press
game_active = False
# a dictionary with all keys we can press and their corresponding x,y locations on the gui
all_keys = {
    'a': (236, 296),
    'b': (419, 334),
    'c': (335, 331),
    'd': (318, 293),
    'e': (305, 257),
    'f': (361, 294),
    'g': (400, 294),
    'h': (442, 295),
    'i': (510, 258),
    'j': (484, 294),
    'k': (525, 294),
    'l': (567, 294),
    'm': (500, 330),
    'n': (459, 331),
    'o': (551, 258),
    'p': (592, 258),
    'q': (222, 259),
    'r': (346, 257),
    's': (275, 297),
    't': (389, 257),
    'u': (471, 256),
    'v': (375, 332),
    'w': (263, 257),
    'x': (291, 330),
    'y': (429, 257),
    'z': (250, 331),
    '.': (578, 332),
    ',': (542, 331),
    ' ': (439, 370),
    '(': (534, 220),
    ')': (575, 220),
    '!': (211, 221),
    '@': (252, 222),
    '#': (299, 222),
    '$': (336, 222),
    '%': (375, 223),
    '^': (417, 223),
    '&': (457, 222),
    '*': (497, 222),
    '0': (581, 222),
    '1': (211, 221),
    '2': (252, 222),
    '3': (299, 222),
    '4': (336, 222),
    '5': (375, 223),
    '6': (417, 223),
    '7': (457, 222),
    '8': (497, 222),
    '9': (540, 222),
    '\'': (496 + 155, 97 + 198),
    '\"': (496 + 155, 97 + 198),
    '-': (469 + 155, 24 + 198),
    '_': (469 + 155, 24 + 198),
    ';': (453 + 155, 94 + 198),
    ':': (453 + 155, 94 + 198),
    '/': (471 + 155, 132 + 198),
    '?': (471 + 155, 132 + 198),
    '[': (484 + 155, 59 + 198),
    '{': (484 + 155, 59 + 198),
    ']': (524 + 155, 60 + 198),
    '}': (524 + 155, 60 + 198)

}


# a function that draws a green circle around the key were supposed to press, displayed on the gui
def paint_key(key_pressed):
    try:
        pygame.draw.circle(screen, GREEN, all_keys[key_pressed], 15, 4)
    except:
        # print('must not have labeled that key in gui yet')
        return


# a function that will return a randomly generated sentence with length of 3 to 9 words
def get_new_sentence():
    # create flag for loop
    is_safe = False
    while not is_safe:
        # generate a random sentence with between 3 and 9 words
        current = gen.gen_sentence(3, 9)
        # set loop exit flag to True
        is_safe = True
        # increment search through each char in our sentence
        for i in current:
            # check if current char is a string
            if type(i) == str:
                # set char to lower case and check if the char is in our accepted all_keys list
                # if not we break and generate a new sentence and try again
                if i.lower() not in all_keys:
                    print(f'not: {i}')
                    is_safe = False
                    break
            # if number or special char is not in our all_keys dict we break and generate a new sentence
            elif i not in all_keys:
                print(f'not: 2: {i}')
                is_safe = False
                break
    # return the randomly generated sentence for gui display
    return current


# a function to convert seconds into minutes and seconds format of (mm:ss)
def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# a function that returns the file save number of the most recent game save you have
def get_text_file_save_number():
    if game_mode == 1:
        # location of game mode 1 file saves
        with open(r"C:\Users\john\PycharmProjects\pythonAPIRequests\py_game\game_images\\typing_pics/count.txt",
                  'r') as f:
            lines = f.readlines()
    elif game_mode == 2:
        # location of game mode 2 file saves
        with open(r"C:\Users\john\PycharmProjects\pythonAPIRequests\py_game\game_images\\typing_pics_backspace/count"
                  r".txt", 'r') as f:
            lines = f.readlines()
    # return the int in our count file
    return int(lines[0])


# function that increments the count txt file text by 1
def write_to_file(numba):
    if game_mode == 1:
        with open(r"C:\Users\john\PycharmProjects\pythonAPIRequests\py_game\game_images\\typing_pics/count.txt",
                  'w') as f:
            numba += 1
            print(f'numba {numba} type {type(numba)}')
            f.write(str(numba))
    elif game_mode == 2:
        with open(
                r"C:\Users\john\PycharmProjects\pythonAPIRequests\py_game\game_images\\typing_pics_backspace/count.txt",
                'w') as f:
            numba += 1
            print(f'numba {numba} type {type(numba)}')
            f.write(str(numba))

# function that saves a screenshot of your score at the end of the game
def save_screenshot(numba):
    # the box section of the screen that has our game stats, (x0,y0,w,h)
    rect = pygame.Rect(0, 0, 40, 60)
    # create a new image of that region
    sub = screen.subsurface(rect)
    # save our score image as a .jpg file
    if game_mode == 1:
        pygame.image.save(sub,
                          r"C:\Users\john\PycharmProjects\pythonAPIRequests\py_game\game_images\\typing_pics/" + f'{d3}' + 'Capture' + f'{numba}' + '.JPG')
    elif game_mode == 2:
        pygame.image.save(sub,
                          r"C:\Users\john\PycharmProjects\pythonAPIRequests\py_game\game_images\\typing_pics_backspace/" + f'{d3}' + 'Capture' + f'{numba}' + '.JPG')


# a function that is called at game over that does the image save and .txt file modifications
def read_write_save():
    number_in_file = get_text_file_save_number()
    save_screenshot(number_in_file)
    write_to_file(number_in_file)

# a function that draws our game selection menu
def draw_homepage():
    global game_active, game_mode
    # Load our menu image and convert it for better performance.
    imp = pygame.image.load("game_images/keys_2.jpg").convert()

    # Scale the loaded image to a size of 900x600 pixels
    # and blit (draw) it onto the screen starting at coordinates (0, 0).
    screen.blit(pygame.transform.scale(imp, (900, 600)), (0, 0))

    # Update the display to show any changes made in the window.
    pygame.display.flip()

    # Get all the events from the event queue (e.g., key presses, mouse actions).
    events = pygame.event.get()

    # Loop through each event obtained from the event queue.
    for e in events:
        # Check if the event is a key press event.
        if e.type == pygame.KEYDOWN:
            # Print the Unicode character associated with the key press.
            print(e.unicode)

            # Check if the pressed key is '1'.
            if e.unicode == str(1):
                # Print and set the game mode to 1 if the '1' key is pressed.
                print('game mode 1 selected')
                game_mode = 1
                game_active = True
            # Check if the pressed key is '2'.
            elif e.unicode == str(2):
                # Print and set the game mode to 2 if the '2' key is pressed.
                print('game mode 2 with backspaces selected')
                game_mode = 2
                game_active = True

        # Check if the event is a quit event (like closing the window).
        if e.type == pygame.QUIT:
            # Quit Pygame and exit the program.
            pygame.quit()
            quit()


def main():
    # Global variables initialization
    global correct_moves, wrong_moves, timer, time_run, time_start, accuracy, needs_backspace, game_active

    # Initialize Pygame module
    pygame.init()

    # Game loop: Runs until 'game_active' becomes True
    while not game_active:
        # Draw the homepage or initial screen
        draw_homepage()

    # Obtain a new sentence for the game
    current = get_new_sentence()
    print(f'current {current}')

    # Initialize variables for text rendering
    current_idx = 0  # Pointer to the current char

    # Initialize font properties
    font = pygame.freetype.Font(None, 42)
    font.origin = True  # Set font origin mode

    # Metric for horizontal advance of each character in the font
    M_ADV_X = 4

    # Calculate the bounding rectangle for the text surface
    text_surf_rect = font.get_rect(current)
    text_surf_rect[2] += 10  # Increase text width by 10 pixels

    # Ensure the generated sentence fits within the display window
    while text_surf_rect[2] > 890:
        # If the sentence is too long, regenerate a new one within acceptable bounds
        current = get_new_sentence()
        text_surf_rect = font.get_rect(current)
        text_surf_rect[2] += 10  # Increase text width by 10 pixels
        current_idx = 0  # Reset current letter pointer
        M_ADV_X = 4  # Reset horizontal advance metric
        font.origin = True  # Reset font origin mode

    # Determine the  y coordinate baseline for text display
    baseline = text_surf_rect.y

    # Create a surface to render the text and center it on the screen
    text_surf = pygame.Surface(text_surf_rect.size)
    text_surf_rect.center = (screen.get_rect().center[0], 120)
    print(text_surf_rect.center)

    # Obtain metrics for each letter in the text
    metrics = font.get_metrics(current)
    print('metrics', metrics)

    first_run = True  # Flag to indicate if it's the first run of the game
    while True:  # Game loop runs indefinitely
        events = pygame.event.get()  # Retrieve all events in the event queue
        for e in events:  # Iterate through each event
            if e.type == pygame.QUIT:  # Check if the event is quitting the game
                return  # Exit the program

            if e.type == pygame.KEYDOWN:  # If a key is pressed
                if first_run:  # If it's the first run of the game
                    # Initialize time tracking variables
                    time_start = time.time()
                    time_run = time.time() - time_start
                    first_run = False  # Set first_run flag to False after initialization

                if game_mode == 1:  # If game mode is 1
                    needs_backspace = 0  # Reset the needs_backspace counter

                if e.key == pygame.K_BACKSPACE:  # If Backspace key is pressed
                    if needs_backspace > 0:  # If backspace is needed
                        needs_backspace -= 1  # Decrement the backspace counter
                        print(f'needs backspace {needs_backspace}')

                # Check if the typed key matches the current letter or move right
                if e.unicode == current[current_idx].lower() or e.key == pygame.K_RIGHT:
                    if needs_backspace == 0 or game_mode == 1:  # If backspace not needed or in game mode 1
                        correct_moves += 1  # Increment correct moves counter
                        current_idx += 1  # Move to the next letter

                        if current_idx >= len(current):  # If the sentence is complete
                            current_idx = 0  # Reset to the start
                            current = get_new_sentence()  # Get a new sentence
                            text_surf_rect = font.get_rect(current)  # Calculate the text size
                            text_surf_rect[2] += 10  # Adjust text width

                            while text_surf_rect[2] > 890:  # Ensure the text fits within the screen width
                                current = get_new_sentence()
                                text_surf_rect = font.get_rect(current)
                                text_surf_rect[2] += 10
                                current_idx = 0  # Reset current letter pointer
                                M_ADV_X = 4  # Reset horizontal advance metric
                                font.origin = True  # Reset font origin mode

                            text_surf_rect = font.get_rect(current)  # Get the bounding rectangle for the current text
                            baseline = text_surf_rect.y  # Get the y-coordinate of the baseline of the text

                            # Create a surface for rendering the text using its bounding rectangle size
                            text_surf = pygame.Surface(text_surf_rect.size)

                            # Center the text surface at the horizontal center and 100 pixels from the top of the screen
                            text_surf_rect.center = (screen.get_rect().center[0], 100)

                            # Retrieve metrics for each character in the current text
                            metrics = font.get_metrics(current)


                else:  # If a wrong key is pressed
                    if e.key != pygame.K_BACKSPACE and e.key != pygame.K_LSHIFT and e.key != pygame.K_RSHIFT or game_mode == 1:
                        print('increasing wrong moves')
                        wrong_moves += 1
                        needs_backspace += 1

        # Set the background color for the screen
        background_color = ("#697c96")
        screen.fill(background_color)  # Fill the screen with the background color

        text_surf.fill(background_color)  # Fill the text surface with the same background color

        # Calculate accuracy based on correct and wrong moves
        VA = wrong_moves + correct_moves
        VO = wrong_moves
        if VA > 0:
            accuracy = round((VA - VO) / VA * 100, 1)
        else:
            accuracy = 100

        # Define font sizes and render text labels
        myFont = pygame.font.SysFont('arial', 18)
        myFont_small = pygame.font.SysFont('arial', 12)
        label = myFont.render(str(correct_moves), 1, (0, 255, 0))
        label2 = myFont_small.render(str(wrong_moves), 1, (255, 0, 0))
        label9 = myFont_small.render(str(accuracy) + '%', 1, (173, 216, 255))

        time_runs = (time_start + timer) - time.time()  # Calculate remaining time for the game

        # Handle game over conditions when time runs out
        if time_runs <= 0 and not first_run:
            # Display scores and accuracy
            label = myFont.render(str(correct_moves), 1, (0, 255, 0))
            label2 = myFont_small.render(str(wrong_moves), 1, (255, 0, 0))
            label9 = myFont_small.render(str(accuracy) + '%', 1, (155, 208, 225))
            screen.blit(label, (5, 5))
            screen.blit(label2, (5, 30))
            screen.blit(label9, (5, 43))
            pygame.display.flip()  # Update the display
            read_write_save()  # Perform read/write operations

            # Reset game variables for a new game
            while time_runs <= 0 and not first_run:
                game_active = False
                while not game_active:
                    draw_homepage()
                wrong_moves = 0
                correct_moves = 0
                time_run = 0
                first_run = True
                main()

        # Update and display the timer based on game status
        if not first_run:
            time_runs = convert(time_runs)
            label3 = myFont.render(str(time_runs), 1, (0, 255, 255))
            screen.blit(label3, (800, 10))
        else:
            time_runs = convert(timer)
            label3 = myFont.render(str(time_runs), 1, (0, 255, 255))
            screen.blit(label3, (800, 10))

        # Display scores and accuracy on the screen
        screen.blit(label, (5, 5))
        screen.blit(label2, (5, 27))
        screen.blit(label9, (5, 43))

        x = 0  # Initialize x-coordinate for rendering letters

        # Render each letter of the current sentence one by one
        for (idx, (letter, metric)) in enumerate(zip(current, metrics)):
            if idx == current_idx:  # Check if the letter is the current one being typed
                if needs_backspace > 0 and game_mode == 2:  # Handle backspace functionality
                    color = 'red'
                    if letter == ' ':
                        filled = 0
                        pygame.draw.rect(text_surf, [255, 0, 0], [x + 2, 3, 9, 30], filled)
                else:
                    color = '#a1e7ff'  # Default color for the current letter

            elif idx < current_idx:  # Letters already typed
                color = '#c1c1c1'  # Color for previously typed letters

            else:  # Letters yet to be typed
                color = 'white'  # Color for upcoming letters

                # Handle error indication by painting letters red that need backspaces
                if current_idx < idx < (current_idx + needs_backspace) and game_mode == 2:
                    color = 'red'
                    if letter == ' ':
                        filled = 0
                        pygame.draw.rect(text_surf, [255, 0, 0], [x + 2, 3, 9, 30], filled)

            # Render the letter at its position with the selected color
            font.render_to(text_surf, (x, baseline), letter, color)

            # Move the x-coordinate for the next letter based on its metric
            try:
                x += metric[M_ADV_X]
            except:
                x = 1

        # Display an image of a keyboard on the screen
        pygame.display.set_caption('image')
        imp = pygame.image.load("game_images/keyboard_img.JPG").convert()
        screen.blit(imp, (150, 200))

        # Highlight the current key being typed on the keyboard image
        paint_key(current[current_idx].lower())

        # Display the text surface containing the sentence being typed
        screen.blit(text_surf, text_surf_rect)

        pygame.display.flip()  # Update the display

if __name__ == '__main__':
    main()  # Start the main function of the game

