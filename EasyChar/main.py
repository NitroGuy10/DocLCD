# http://thepythongamebook.com/en:pygame:start
# https://coderslegacy.com/python/python-pygame-tutorial/
import pygame
# import serial_dummy as serial
import serial

print("Hello, EasyChar!")


ArduinoCmd = {
    "NULL": chr(0),  # null separator after an integer to terminate it (i.e., keep Serial.parseInt() from waiting for more)
    "CLEAR": chr(1),  # clear() screen and go home()
    "CURSOR_X": chr(2),  # send this command and then the desired (integer) cursor position
    "CURSOR_Y": chr(3)  # send this command and then the desired (integer) cursor position
}

ser = serial.Serial("/dev/ttyAMA0")
ser.baudrate = 115200


class Cursor:
    # LCD dimensions
    MAX_X = 20 - 1
    MAX_Y = 4 - 1

    x = 0
    y = 0

    # ROW_ORDER = [0, 2, 1, 3]
    ROW_ORDER = [0, 1, 2, 3]

    def __init__(self, serial):
        self.ser = serial

    def right(self):
        if self.x == self.MAX_X:
            self.x = 0
            self.down()
            return True
        else:
            self.x += 1
            return False

    def left(self):
        if self.x == 0:
            self.x = self.MAX_X
            self.up()
            return True
        else:
            self.x -= 1
            return False

    def up(self):
        self.y = self.ROW_ORDER[(self.ROW_ORDER.index(self.y) - 1) % 4]

    def down(self):
        self.y = self.ROW_ORDER[(self.ROW_ORDER.index(self.y) + 1) % 4]

    """
    def __serial_x(self):  # depricated
        return bytes(ArduinoCmd["CURSOR_X"] + str(self.x), "ascii")

    def __serial_y(self):  # depricated
        return bytes(ArduinoCmd["CURSOR_Y"] + str(self.y), "ascii")
    """

    def serial_xy(self):
        self.ser.write(bytes(ArduinoCmd["CURSOR_X"] + str(self.x) +
                             ArduinoCmd["CURSOR_Y"] + str(self.y) +
                             ArduinoCmd["NULL"], "ascii"))

    def serial_write(self, string):
        self.ser.write(bytes(string, "ascii"))
        if self.right():
            self.serial_xy()

    def serial_clear(self):
        self.ser.write(bytes(ArduinoCmd["CLEAR"], "ascii"))
        x = 0
        y = 0


def main():
    cursor = Cursor(ser)
    cursor.serial_clear()

    pygame.init()
    pygame.display.set_caption("EasyChar")

    clock = pygame.time.Clock()
    framerate = 15

    screen = pygame.display.set_mode((200, 200))
    background = pygame.Surface(screen.get_size())
    background.fill((200, 200, 200))
    background = background.convert()

    """
    drawables = []
    player = player_class.Player((5, 5))
    drawables.append(player)
    """

    running = True
    print("Ready!")

    # Game Loop
    while running:
        clock.tick(framerate)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.unicode != "" and 31 < ord(event.unicode) < 127:
                    try:
                        print(event.unicode + " -- " + str(bytes(event.unicode, "ascii")))
                        cursor.serial_write(event.unicode)
                    except UnicodeEncodeError:
                        print("Unencodable character typed: \'" + str(event.unicode) + "\'")
                elif event.key == pygame.K_LEFT:
                    cursor.left()
                    cursor.serial_xy()
                    print("Left!")

                elif event.key == pygame.K_RIGHT:
                    cursor.right()
                    cursor.serial_xy()
                    print("Right!")

                elif event.key == pygame.K_UP:
                    cursor.up()
                    cursor.serial_xy()
                    print("Up!")

                elif event.key == pygame.K_DOWN:
                    cursor.down()
                    cursor.serial_xy()
                    print("Down!")

                elif event.key == pygame.K_ESCAPE:
                    cursor.x = 0
                    cursor.y = 0
                    cursor.serial_clear()
                    print("Clear Screen!")

                elif event.key == pygame.K_BACKSPACE:
                    if not (cursor.x == 0 and cursor.y == 0):
                        cursor.left()
                        cursor.serial_xy()
                        cursor.serial_write(" ")
                        cursor.left()
                        cursor.serial_xy()
                    print("Backspace!")

                elif event.key == pygame.K_DELETE:
                    # Type a space at the cursor position but do not move the cursor
                    cursor.serial_write(" ")
                    cursor.left()
                    cursor.serial_xy()
                    print("Delete!")

                elif event.key == pygame.K_TAB:
                    # Clear line and move cursor to start of line
                    cursor.x = 0
                    cursor.serial_xy()
                    for r in range(cursor.MAX_X + 1):
                        cursor.serial_write(" ")
                    cursor.up()
                    cursor.serial_xy()
                    print("Clear Line!")

                elif event.key == pygame.K_RETURN:
                    # Move cursor to start of next line
                    cursor.x = 0
                    cursor.down()
                    cursor.serial_xy()
                    print("Return!")

        screen.blit(background, (0, 0))
        """
        for drawable in drawables:
            screen.blit(drawable.surface, drawable.get_draw_pos())
        """

        pygame.display.flip()

    pygame.quit()
    print("All done!")


main()
