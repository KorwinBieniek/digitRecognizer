from utils import *
import tensorflow as tf
import keras.models
from tkinter import *
from tkinter import messagebox


def load_model():
    return keras.models.load_model("model/digit_recognition_model")


class Pixel(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (255, 255, 255)
        self.neighbors = []

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.x + self.width, self.y + self.height))

    def get_neighbors(self, grid):
        # Get the neighbours of each pixel in the grid, this is used for drawing thicker lines
        j = self.x // 20  # the var i is responsible for denoting the current col value in the grid
        i = self.y // 20  # the var j is responsible for denoting thr current row value in the grid
        rows = 28
        cols = 28

        # Horizontal and vertical neighbors
        if i < cols - 1:  # Right
            self.neighbors.append(grid.pixels[i + 1][j])
        if i > 0:  # Left
            self.neighbors.append(grid.pixels[i - 1][j])
        if j < rows - 1:  # Up
            self.neighbors.append(grid.pixels[i][j + 1])
        if j > 0:  # Down
            self.neighbors.append(grid.pixels[i][j - 1])

        # Diagonal neighbors
        if j > 0 and i > 0:  # Top Left
            self.neighbors.append(grid.pixels[i - 1][j - 1])

        if j + 1 < rows and i > -1 and i > 1:  # Bottom Left
            self.neighbors.append(grid.pixels[i - 1][j + 1])

        if j - 1 < rows and i < cols - 1 and j > 1:  # Top Right
            self.neighbors.append(grid.pixels[i + 1][j - 1])

        if j < rows - 1 and i < cols - 1:  # Bottom Right
            self.neighbors.append(grid.pixels[i + 1][j + 1])


class Grid(object):
    pixels = []

    def __init__(self, row, col):
        self.rows = row
        self.cols = col
        self.len = row * col
        self.width = WIDTH
        self.height = HEIGHT
        self.generate_pixels()

    def draw(self, surface):
        for row in self.pixels:
            for col in row:
                col.draw(surface)
        for wind_button in buttons:
            wind_button.draw(win)

    def generate_pixels(self):
        x_gap = self.width // self.cols
        y_gap = (self.height - 40) // self.rows
        self.pixels = []
        for r in range(self.rows):
            self.pixels.append([])
            for c in range(self.cols):
                self.pixels[r].append(Pixel(x_gap * c, y_gap * r, x_gap, y_gap))

        for r in range(self.rows):
            for c in range(self.cols):
                self.pixels[r][c].get_neighbors(self)

    def clicked(self, position):  # Return the position in the grid that user clicked on
        t = position[0]
        w = position[1]
        g1 = int(t) // self.pixels[0][0].width
        g2 = int(w) // self.pixels[0][0].height

        return self.pixels[g2][g1]

    def convert_binary(self):
        li = self.pixels

        new_matrix = [[] for _ in range(len(li))]

        for i in range(len(li)):
            for j in range(len(li[i])):
                if li[i][j].color == (255, 255, 255):
                    new_matrix[i].append(0)
                else:
                    new_matrix[i].append(1)

        mnist = tf.keras.datasets.mnist
        (_, _), (x_test, y_test) = mnist.load_data()
        x_test = tf.keras.utils.normalize(x_test, axis=1)
        for row in range(28):
            for x in range(28):
                x_test[0][row][x] = new_matrix[row][x]

        return x_test[:1]


def guess_num(li):
    model = load_model()

    predictions = model.predict(li)
    predicted_number = (np.argmax(predictions[0]))
    window = Tk()
    window.withdraw()
    messagebox.showinfo("Number Prediction", "This number is a " + str(predicted_number))
    window.destroy()


button_y = HEIGHT - TOOLBAR_HEIGHT / 2 - 25
buttons = [
    MyButton(0, button_y, 90, 50, WHITE, "Clear", BLACK),
    MyButton(90, button_y, 470, 50, RED, "Predict", BLACK),
]


def main():
    global pos
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                try:
                    pos = pygame.mouse.get_pos()
                    _, y = pos
                    if y >= HEIGHT - TOOLBAR_HEIGHT:
                        raise IndexError
                    clicked = g.clicked(pos)
                    clicked.color = (0, 0, 0)
                    for n in clicked.neighbors:
                        n.color = (0, 0, 0)

                except IndexError:
                    for wind_button in buttons:

                        if not wind_button.clicked(pos):
                            continue

                        if wind_button.text == "Clear":
                            g.generate_pixels()
                        if wind_button.text == "Predict":
                            li = g.convert_binary()
                            guess_num(li)

        g.draw(win)
        pygame.display.update()

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Digit Recognizer")
g = Grid(28, 28)
main()

pygame.quit()
quit()
