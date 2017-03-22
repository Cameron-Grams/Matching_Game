from random import choice  #needed to choose an element from a list
import pyglet

window = pyglet.window.Window(width=400, height=450, caption="GraphicGame")

Im1 = pyglet.image.load("./images/apple.jpg")
Im2 = pyglet.image.load("./images/circle.jpeg")
Im3 = pyglet.image.load("./images/eagle.jpg")
Im4 = pyglet.image.load("./images/triangle.jpg")
Im5 = pyglet.image.load("./images/square.jpg")

def InitializeGrid(board):
    #Initializing the grid by inserting random value
    for i in range(8):
        for j in range(8):
            board[i][j] = choice(['Q','R','S','T','U'])
    return board


def Initialize(current_score):
    #Initialize the game
    #Initialing the grid
    InitializeGrid(board)

    #initializing score
    global score 
    score = 0

    global turn
    turn = 1


def ContinueGame(current_score, goal_score=100):
    #returns false if the game should end, true if game is not over
    
    if (current_score >= goal_score):
        return False
    else:
        return True


def DoRound(current_score):
    #Perform one round of the game
    #Display current board
    DrawBoard(board)
    #get move
    move = GetMove()
    #updae board
    Update(board, move)
    #update turn number
    global turn
    turn += 1

def SwapPieces(board, move):

    #swap objects in two positions
    temp = board[move[0]][move[1]]
    board[move[0]][move[1]] = board[move[2]][move[3]] 
    board[move[2]][move[3]]  = temp 
  
    return board



def RemovePieces(board):
    # remove any 3 in a row
    #create zero board to recgonize those that have to go
    remove = [[0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0]]

    #go through the ranks
    for i in range(8):
        for j in range(6):
            if (board[i][j] == board[i][j+1]) and (board[i][j] == board[i][j+2]):
                #indicates three in a row
                remove[i][j] = 1;
                remove[i][j+1] = 1;
                remove[i][j+2] = 1;

    for i in range(6):
        for j in range(8):
            if (board[i][j] == board[i+1][j]) and (board[i][j] == board[i+2][j]):
                remove[i][j] = 1;
                remove[i+1][j] = 1;
                remove[i+2][j] = 1;

    removed_any = False
    global score
    for i in range(8):
        for j in range(8):
            if remove[i][j] == 1:
                board[i][j] = 0
                score += 1
                removed_any = True
    return removed_any





def DropPieces(board):
    #fill in blanks with random pieces

    #this fills in by column, where is the matching by row? 


    for j in range(8):
        #make a list of the pieces in the column
        listofpieces = []
        for i in range(8):
            if board[i][j] != 0:
                listofpieces.append(board[i][j])

        #copy that list into column
        for i in range(len(listofpieces)):
            board[i][j] = listofpieces[i]

        #fill in remainder of column with 0s
        for i in range(len(listofpieces), 8):
            board[i][j] = 0




def FillBlanks(board):
    for i in range(8):
        for j in range(8):
            if board[i][j] == 0:
                board[i][j] = choice(['Q','R','S','T','U'])


def Update(board, move):
    #update the board according to move
    SwapPieces(board, move)
    pieces_eliminated = True
    while pieces_eliminated:
        pieces_eliminated = RemovePieces(board)
        DropPieces(board)
        FillBlanks(board)


@window.event
def on_draw():
    window.clear()
    for i in range(7, -1, -1):
        #Draw each row
        y = 50 + 50 * i
        for j in range(8):
            #draw each piece, first getting postion
            x = 50 * j
            if board[i][j] == 'Q':
                Im1.blit(x,y)
            elif board[i][j] == 'R':
                Im2.blit(x,y)
            elif board[i][j] == 'S':
                Im3.blit(x,y)
            elif board[i][j] == 'T':
                Im4.blit(x,y)
            elif board[i][j] == 'U':
                Im5.blit(x,y)
    label = pyglet.text.Label("Turn: " + str(turn) + "    Score: " + str(score),
                              font_name= "Arial",
                              font_size=18,
                              x=20, y=10)
    label.draw()


@window.event
def on_mouse_press(x, y, button, modifiers):
    #get the starting cell
    global startx
    global starty
    startx = x
    starty = y

@window.event
def on_mouse_release(x, y, button, modifiers):
    #get starting and ending cell and see if they are adjacent
    startcol = startx//50
    startrow = (starty - 50)//50
    endcol = x//50
    endrow = (y-50)//50
    #check to see if ending is adjacent to starting and if so move
    if ((startcol==endcol and startrow == endrow-1) or (startcol == endcol and startrow == endrow + 1) or (startrow == endrow and startcol == endcol - 1) or (startrow == endrow and startcol == endcol +1)):
        Update(board, [startrow, startcol, endrow, endcol])
    global turn
    turn += 1
    #see if game is over
    if not ContinueGame(score):
        print("You won in ", turn, " turns")
        exit()

#sate the main variables
score = 0
turn = 0
goalscore = 100
board = [[0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0]]

#Initialize the game
Initialize(board)
#Loop while the game is not over
# while ContinueGame(score):
    #Do a round of the game
#    DoRound(score)

pyglet.app.run()
