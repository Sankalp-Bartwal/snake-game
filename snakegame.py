import tkinter as tk
from tkmacosx import Button
import random

startX1, startY1, startX2, startY2, WIDTH, BORDER_WIDTH, status, SIDE_OF_FOOD = 150, 150, 180, 160, 10, 10, None, 10
velocity, initialVelocity, foodCoord, foodSizeInc, eaten = 0, 7, [], 10, False

CAN_HEIGHT, CAN_WIDTH = 300, 300

snake, snakeMeta, score = [], ['r'], 0

startMenu, endMenu, pauseMenu, difMenu = [], [], [], []

def init():

    global win

    win = tk.Tk()
    win.title('Snake Game')
    win.configure(background='black')


def createScreen():

    global screen

    screen = tk.Canvas(win, height=CAN_HEIGHT, width=CAN_WIDTH, background='grey')


def makeBorders():

    screen.create_rectangle(0, 0, 300, BORDER_WIDTH, fill='black', tag='border')
    screen.create_rectangle(0, BORDER_WIDTH, BORDER_WIDTH, 300, fill='black', tag='border')
    screen.create_rectangle(300-BORDER_WIDTH, BORDER_WIDTH, 300, 300, fill='black', tag='border')
    screen.create_rectangle(BORDER_WIDTH, 300-BORDER_WIDTH, 300-BORDER_WIDTH, 300, fill='black', tag='border')


def makeButton():

    global startButton, contButton, restartButton, difButton, helpButton, quitButton

    startButton = Button(text='Start Game', command=lambda: startGame(), bg='grey', activebackground='grey', bordercolor='grey')
    contButton = Button(text='Continue', command=lambda: contBut(), bg='grey', activebackground='grey', bordercolor='grey')
    restartButton = Button(text='Restart', command=restart, bg='grey', activebackground='grey', bordercolor='grey')
    difButton = Button(text='Difficulty', command=difficultyOs, bg='grey', activebackground='grey', bordercolor='grey')
    helpButton = Button(text='Help', command=None, bg='grey', activebackground='grey', bordercolor='grey')
    quitButton = Button(text='Quit', command=lambda: quitBut(), bg='grey', activebackground='grey', bordercolor='grey')


def startOs():

    l1 = tk.Label(text='Snake Game', font=('aerial bold', 30), background='grey')

    startMenu.append(screen.create_window(155, 100, window=l1))
    startMenu.append(screen.create_window(152, 135, window=startButton))
    startMenu.append(screen.create_window(152, 157, window=difButton))
    startMenu.append(screen.create_window(152, 179, window=helpButton))
    startMenu.append(screen.create_window(152, 201, window=quitButton))


def makeSnake(coord=(startX1, startY1, startX2, startY2)):

    s = screen.create_rectangle(coord, fill='black', tag='head')
    snake.append(s)


def startGame(event=None):

    global startMenu, status, velocity, initialVelocity

    for id in startMenu:
        screen.delete(id)
    startMenu = []
    status = True
    velocity = initialVelocity
    initialVelocity = 0

    makeSnake()
    makeFood()
    win.bind('<Escape>', pauseOs)
    motion()


def motion():

    global callMotion, eaten

    # for the node which eats

    tempCoord = screen.coords(snake[-1])

    if snakeMeta[-1] == 'u':
        tempCoord[1] -= velocity

    elif snakeMeta[-1] == 'd':
        tempCoord[3] += velocity

    elif snakeMeta[-1] == 'r':
        tempCoord[2] += velocity

    elif snakeMeta[-1] == 'l':
        tempCoord[0] -= velocity

    #print("Motion 1 is callled")
    screen.coords(snake[-1], tempCoord)
    snakeInteraction(tempCoord)

    # for the last node
    tempCoord = screen.coords(snake[0])

    if snakeMeta[0] == 'u':
        if not eaten:
            tempCoord[3] -= velocity
        else:
            tempCoord[3] = tempCoord[3] - velocity + foodSizeInc
            eaten = False

    elif snakeMeta[0] == 'd':
        if not eaten:
            tempCoord[1] += velocity
        else:
            tempCoord[1] = tempCoord[1] + velocity  - foodSizeInc
            eaten = False

    elif snakeMeta[0] == 'l':
        if not eaten:
            tempCoord[2] -= velocity
        else:
            tempCoord[2] = tempCoord[2] - velocity + foodSizeInc
            eaten = False

    elif snakeMeta[0] == 'r':
        if not eaten:
            tempCoord[0] += velocity
        else:
            tempCoord[0] = tempCoord[0] + velocity - foodSizeInc
            eaten = False

    screen.coords(snake[0], tempCoord)

    if tempCoord[0] >= tempCoord[2] or tempCoord[1] >= tempCoord[3]:
        screen.delete(snake[0])
        del(snake[0])
        del(snakeMeta[0])

    if status:
        screen.after(100, motion)


def gameStop():

    if status:
        pause()

    l1 = tk.Label(text='Game Over', font=('aerial bold', 40), background='grey')
    l2 = tk.Label(text=f'Score : {score}', font=('aerial bold', 27), background='grey')

    endMenu.append(screen.create_window(155, 84, window=l1))
    endMenu.append(screen.create_window(155, 119, window=l2))
    endMenu.append(screen.create_window(152, 152, window=restartButton))
    endMenu.append(screen.create_window(152, 173, window=difButton))
    endMenu.append(screen.create_window(152, 194, window=helpButton))
    endMenu.append(screen.create_window(152, 215, window=quitButton))


def pause():

    global initialVelocity, velocity, status

    initialVelocity = velocity
    velocity = 0
    status = False


def pauseOs(event=None):

    if status:
        pause()
    global pauseMenu

    l1 = tk.Label(text=f'Score : {score}', font=('aerial bold', 27), background='grey')

    pauseMenu.append(screen.create_window(155, 90, window=l1))
    pauseMenu.append(screen.create_window(152, 131, window=contButton))
    pauseMenu.append(screen.create_window(152, 152, window=restartButton))
    pauseMenu.append(screen.create_window(152, 173, window=difButton))
    pauseMenu.append(screen.create_window(152, 194, window=helpButton))
    pauseMenu.append(screen.create_window(152, 215, window=quitButton))

    win.bind("<Escape>", contBut)

def cont():

    global initialVelocity, velocity, status

    velocity = initialVelocity
    initialVelocity = 0
    status = True
    motion()


def contBut(event=None):

    global pauseMenu

    for id in pauseMenu:
        screen.delete(id)
    pauseMenu=[]

    if not status:
        cont()
    win.bind("<Escape>", pauseOs)


def restart():

    global snake, snakeMeta, status, score, endMenu, pauseMenu

    for node in snake:
        screen.delete(node)

    for id in endMenu:
        screen.delete(id)

    for id in pauseMenu:
        screen.delete(id)

    screen.delete(food)

    snake, snakeMeta, score, endMenu, pauseMenu = [], ['r'], 0, [], []

    makeSnake()
    makeFood()

    cont()


def makeFood():

    global food, foodCoord

    x1 = random.randint(10, 300-BORDER_WIDTH-SIDE_OF_FOOD)
    y1 = random.randint(10, 300-BORDER_WIDTH-SIDE_OF_FOOD)
    x2 = x1 + SIDE_OF_FOOD
    y2 = y1 + SIDE_OF_FOOD

    food = screen.create_oval(x1, y1, x2, y2, fill='white', tag='food')
    foodCoord = [x1, y1, x2, y2]


def snakeInteraction(coords):

    global eaten, score

    if snakeMeta[-1] == 'l':
        ids = screen.find_overlapping(coords[0], coords[1]+2, coords[0], coords[3]-2)

    elif snakeMeta[-1] == 'r':
        ids = screen.find_overlapping(coords[2], coords[1]+2, coords[2], coords[3]-2)

    elif snakeMeta[-1] == 'u':
        ids = screen.find_overlapping(coords[0]+2, coords[1], coords[2]-2, coords[1])

    elif snakeMeta[-1] == 'd':
        ids = screen.find_overlapping(coords[0]+2, coords[3], coords[2]-2, coords[3])


    if len(ids) >=2:
        for id in ids:
            for tag in screen.gettags(id):
                if tag == 'food':
                    screen.delete(food)
                    makeFood()
                    eaten = True
                    score+=100
                    return

                elif tag == 'border' or tag == 'body':
                    gameStop()
                    return


def attachWidgets():

    screen.grid(row=0, column=0, rowspan=3, columnspan=3)


def upDown(event):
    global snakeVelocityY, snakeVelocityX

    if status:
        coords = screen.coords(snake[-1])
        if (snakeMeta[-1] == 'l' or snakeMeta[-1] == 'r') and (abs(coords[0]-coords[2]) >= 2*WIDTH):

            newSnakeCoords = []

            if snakeMeta[-1] == 'l':
                newSnakeCoords.append(coords[0])
                newSnakeCoords.append(coords[1])
                newSnakeCoords.append(coords[0]+WIDTH)
                newSnakeCoords.append(coords[3])

                coords[0]+=WIDTH

            else:
                newSnakeCoords.append(coords[2]-WIDTH)
                newSnakeCoords.append(coords[1])
                newSnakeCoords.append(coords[2])
                newSnakeCoords.append(coords[3])

                coords[2]-=WIDTH

            screen.coords(snake[-1], coords)

            screen.dtag(snake[-1], 'head')
            screen.addtag_withtag('body', snake[-1])
            newSnake = screen.create_rectangle(newSnakeCoords, fill='white', tag='head')
            snake.append(newSnake)

            snakeVelocityX = 0
            if event.keysym == 'Up':
                snakeVelocityY = -2
                snakeMeta.append('u')
            else :
                snakeVelocityY = 2
                snakeMeta.append('d')


def leftRight(event):
    global snakeVelocityY, snakeVelocityX

    if status:
        coords = screen.coords(snake[-1])

        if (snakeMeta[-1] == 'u' or snakeMeta[-1] == 'd') and (abs(coords[1]-coords[3]) >= 2*WIDTH):

            newSnakeCoords = []

            if snakeMeta[-1] == 'u':
                newSnakeCoords.append(coords[0])
                newSnakeCoords.append(coords[1])
                newSnakeCoords.append(coords[2])
                newSnakeCoords.append(coords[1]+WIDTH)

                coords[1] += WIDTH

            else:
                newSnakeCoords.append(coords[0])
                newSnakeCoords.append(coords[3]-WIDTH)
                newSnakeCoords.append(coords[2])
                newSnakeCoords.append(coords[3])

                coords[3] -= WIDTH

            screen.coords(snake[-1], coords)

            screen.dtag(snake[-1], 'head')
            screen.addtag_withtag('body', snake[-1])
            newSnake = screen.create_rectangle(newSnakeCoords, fill='orange', tag='head')
            snake.append(newSnake)

            snakeVelocityY = 0
            if event.keysym == 'Left':
                snakeVelocityX = -2
                snakeMeta.append('l')
            else :
                snakeVelocityX = 2
                snakeMeta.append('r')


def quitBut():

    win.destroy()
    quit()


def difficultyOs():

    global startMenu, endMenu, pauseMenu, t1, difMenu

    remember = ''
    for id in endMenu:
        screen.delete(id)
        remember = 'e'

    for id in pauseMenu:
        screen.delete(id)
        remember = 'p'

    for id in startMenu:
        screen.delete(id)
        remember = 's'

    l1 = tk.Label(text='Snake Velocity', font=('Aerial Bold', 15), bg='grey')
    t1 = tk.Text(background='grey', width=3, height=1)
    b1 = Button(text='Apply', bg='grey', activebackground='grey', bordercolor='grey', command=lambda:difficulty(remember))

    difMenu.append(screen.create_window(120, 120, window=l1))
    difMenu.append(screen.create_window(220, 120, window=t1))
    difMenu.append(screen.create_window(150, 200, window=b1))

    endMenu, pauseMenu, startMenu = [], [], []


def difficulty(x):

    global difMenu, initialVelocity

    for id in difMenu:
        screen.delete(id)
    difMenu = []

    newVelocity = int(t1.get('1.0', 'end'))
    initialVelocity = newVelocity

    if x == 's':
        startOs()
    elif x == 'e':
        gameStop()
    elif x == 'p':
        pauseOs()


def main():

    init()
    createScreen()
    makeBorders()

    win.bind('<Up>', upDown)
    win.bind('<Down>', upDown)
    win.bind('<Left>', leftRight)
    win.bind('<Right>', leftRight)

    makeButton()
    startOs()
    attachWidgets()

    win.mainloop()


main()