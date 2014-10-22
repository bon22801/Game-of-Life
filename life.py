" CS108 p3 "
" Yu-Jer Lin "
" Narrative: The first thing I do is to create the 4 buttons: reset, go, and save."
" My first apporoch was to put 4 rectangle under the grid. But then I found it"
" is more difficult to declear the hitbox of the buttons. So I did what Prof."
" Campball suggest, divid the bottom area into 4 parts and that way we only"
" need to determine what x is when we click outside of the grid."
" Then it was easy to get the bottons done just by create 4 rectangle and texts."

" After understood the click was determined in the while true loop"
" and realized the click outside of grid is just y >= cells:, I divided the"
" area into 4 sections, where x = 0~10 is botton reset, 10~20 is Go, 20~30 is save"
" and above 30 is read."
" To implement Reset and Go is really easy. For Reset we just need to close the"
" current win and open a new one by calling life. Just win.close() and life() work."
" For Go we just need to call nextGeneration()."

" Save takes much more work. First I went online to find out how to write into a"
" file. I think both open() and json() would work. But for simple data it might be"
" easier to use open(). Then I learned how to use open and realized it can't cast"
" interger into string so we have to do s = str(i) + str(j) first. However, the result"
" wasn't a list of lists but a list and everything else is a list of object like, which"
" isn't what I wanted. So I for every marked cells, I used list.append() to take input"
" into the list. To test it I simply mark some cell and save it. it gave me something like"
" [[0, 0], [1, 1], [1, 3], [3, 3]], which is what I wanted. After that I"
" just need to fix the graph and botton"

" Read gave me the most trouble. Because I used myFile = open(input.getText() + '.txt', 'r')"
" I couldn't convert myFile into a list. Then I decided to create a new list and extend what"
" myFile.readline() return. and to scan the [x,y], I search in the list that extend the myFile."
" and if it is a digit, I append it it into a string. So after that I would get a string like"
" 00111333 for [[0, 0], [1, 1], [1, 3], [3, 3]]. Then all I have to do is mark the every 2"
" digit from the string like mark(int(x[j]),int(x[k]))"
" I tested the read it can mark the cells correctly, However, it doesn't unmark whatever was"
" on the grid. so to do that, I unmark all whenever we call the read."




# John Conway's Game of Life
#
# A rather naive version written using the Zelle graphics Package.
#
# Bill Campbell

# So, our 2-D grid of cells is cells * cells in size, but actually
# we maintain a border of empty cells around this grid
# (making the counting of neighbors simpler; the border cells are
# always unpopulated). So the grid is actually (cells+2) * (cells+2).

# In this version we represent our 2-D grids as lists of lists;  
# each row is represented as a nested list.
#
# For example, the 2-D
#   1 2 3
#   4 5 6
#   7 8 9
# would be represented as a list [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
#
# Of course, since we are representing our cells by 0's and 1's,
# 0 for unpopulated, 1 for populated, a completely populated
# grid
#   1 1 1
#   1 1 1
#   1 1 1
# would be represented as [[1, 1, 1], [1, 1, 1], [1, 1, 1]].
#
# Or, because we wrap a border of unpopulated cells around the grid
# (so that every cell on the grid proper has 8 neighbors) we have
# the grid
#   0 0 0 0 0
#   0 1 1 1 0
#   0 1 1 1 0
#   0 1 1 1 0
#   0 0 0 0 0
# represented as
# [[0,0,0,0,0],[0,1,1,1,0],[0,1,1,1,0],[0,1,1,1,0],[0,0,0,0,0]].
#
# (In this example, cells = 3. It is more in our simulation, eg 40.)


from graphics import *

cellSize = 10 # pixels

cells = 40    # along one side

gridSize = cellSize * cells # along one side (in pixels)

nextGen = []  # the next generation is always computed
lastGen = []  # from the last generation

win = None    # The main window

def isMarked(x,y):
    """Is the cell (x,y) populated in the last generation?"""
    return lastGen[x+1][y+1] == 1

def isNextGenMarked(x,y):
    """Is the cell (x,y) populated in the last generation?"""
    return nextGen[x+1][y+1] == 1


def mark(x,y):
    """Populate cell(x,y) in the next generation"""
    rec = Rectangle(Point(x*cellSize,y*cellSize),
              Point((x+1)*cellSize,(y+1)*cellSize))
    rec.setFill("black")
    rec.draw(win)
    nextGen[x+1][y+1] = 1

def unmark(x,y):
    """Unpopulate cell (x,y) in the next generation."""
    rec = Rectangle(Point(x*cellSize,y*cellSize),
              Point((x+1)*cellSize,(y+1)*cellSize))
    rec.setFill("white")
    rec.draw(win)
    nextGen[x+1][y+1] = 0

def neighbors(x,y):
    """The number of populated neighbors for cell (x,y)
        in the last generation.
    
    """
    def nbr(x,y):
        """Return 1 if cell (x,y) is populated in the
           last generation and 0 if not.

        """
        return lastGen[x+1][y+1]
    
    return  nbr(x-1,y-1) + nbr(x,y-1) + nbr(x+1,y-1) + nbr(x-1,y) + \
                nbr(x+1,y) + nbr(x-1,y+1) + nbr(x,y+1) + nbr(x+1,y+1)
    
def getCellClicked():
    """ The (x,y) for the grid cell that was clicked on,
        where x is in the range 0..39 and y is in the range 0..39.

        Notice that we translate the actual pixel positions to
        cell positions by dividing both x and y by cellSize,
        which is the width (or height) of each cell in pixels.

        Also notice that if y >= 40, then we are clicking below the grid.

    """
    p = win.getMouse()
    x = p.getX() // cellSize 
    y = p.getY() // cellSize
    print("("+str(x)+","+str(y)+")")
    return (x,y)


def nextGeneration():
    """ Compute the next generation of grid cells from the last
        generation, following the rules of life (and death).

        As we compute the values (0 or 1) for each of the cells
        on the (next generation grid), mark() and unmark() paint
        the states, populated or unpopulated respectively,
        on to the drawn grid. Notice only changes are drawn;
        this mimimizes painting on the window's canvas.

    """
    global lastGen # so as not to be confused as defining a local var.
    # lastgen is a copy of nextgen (but has its own identity).
    lastGen = [row[:] for row in nextGen]
    for i in range(0,cells):
        for j in range(0,cells):
            n = neighbors(i,j)
            if isMarked(i,j):
                if n <= 1:
                    unmark(i,j) # from isolation
                elif n >= 4:
                    unmark(i,j) # from overcrowding
            else: # unmarked in previous generation
                if n == 3:
                    mark(i,j)



    
def life():
    """ Run a simlulation for John Conway's game of life.

        In this version, we paint the grid onto the window's
        canvas. Clicking on an unpopulated cell populates it;
        clicking on a populated cell unpopulates it. Once we one
        is satisfied with the initial configulation, clicking
        in the space below the grid on the window starts the game;
        successive clicks in this same region advance the game 
        to successive generations.

        The only way to end (currently) is to close the window,
        which raises an error exception because the game is
        waiting on a mouse click on the window's canvas.

    """


    










    
    # Create window and draw the grid.
    global win
    global lastGen
    global nextGen # So that these are not confused as local variables.
    win = GraphWin("John Conway's Game of Life", gridSize, gridSize+100 )
    Line(Point(1,1),Point(win.getWidth(),1)).draw(win)
    Line(Point(1,0),Point(1,win.getHeight())).draw(win)
    Line(Point(win.getWidth(),0), \
         Point(win.getWidth(), win.getHeight())).draw(win)
    Line(Point(0,win.getHeight()), \
         Point(win.getWidth(),win.getHeight())).draw(win)

    # Create and draw the 4 bottons: reset, go, .
    Rectangle(Point(0,400), Point(100,600)).draw(win)
    button = Text(Point(50 ,450),"Reset")
    button.draw(win)
    Rectangle(Point(100,400), Point(200,600)).draw(win)
    button = Text(Point(150 ,450),"Go")
    button.draw(win)
    Rectangle(Point(200,400), Point(300,600)).draw(win)
    button = Text(Point(250 ,450),"Save")
    button.draw(win)
    Rectangle(Point(300,400), Point(400,600)).draw(win)
    button = Text(Point(350 ,450),"Read")
    button.draw(win)
  



    for i in range (0, cells+1):
        Line(Point(0, i*cellSize), Point(gridSize, i*cellSize)).draw(win)
        Line(Point(i*cellSize, 0), Point(i*cellSize, gridSize)).draw(win)

    # Initialize the cells (all unpopulated).
    # Notice here and only here, these are the same lists.
    lastGen = nextGen = [[0] * (cells+2) for i in range(cells+2)]





    # TESTING:
    #testSave()

    # User clicks on cells to populate them.
    while True:
        x,y = getCellClicked()
        if y >= cells:
            if x <= 10:
                win.close()
                life()
            elif x <= 20:
                nextGeneration()
            elif x <= 30:
                save()
            else:
                read()
        elif isMarked(x,y):
            unmark(x,y)
        else:
            mark(x,y)

    # Now, compute and show successive generations.
    for i in range(0,100):
        getCellClicked() 
        # time.sleep(1.0) # replace line above with this for animation.
        nextGeneration()


def save():
    win2 = GraphWin("Save", 300, 300 )
    Text(Point(100,30), "Insert a file name:").draw(win2)
    input = Entry(Point(100,60), 15)
    input.setText("file_name")
    input.draw(win2)
    Rectangle(Point(10,80), Point(300,300)).draw(win2)
    button = Text(Point(150 ,200),"Save")
    button.draw(win2)
    win2.getMouse()
    myFile = open(input.getText() + '.txt', 'w')
    list1 = list()
    for i in range(0,cells):
        for j in range(0,cells):
            if isNextGenMarked(i,j):              
  #             s = "[" + str(i) + "," + str(j) + "]"                
                list1.append([i,j])
    myFile.write(str(list1))
    win2.close()


def read():
    
    for i in range(0,cells):
        for j in range(0,cells):
            unmark(i,j)
            
    win3 = GraphWin("Read", 300, 300 )
    Text(Point(70,30), "Insert a file name:").draw(win3)
    input = Entry(Point(100,60), 15)
    input.setText("file_name")
    input.draw(win3)
    Rectangle(Point(10,80), Point(300,300)).draw(win3)
    button = Text(Point(150 ,200),"Read")
    button.draw(win3)
    win3.getMouse()
    myFile = open(input.getText() + '.txt', 'r')

    list2 = list()
    list2.extend(myFile.readline())
    x = str()
    for i in list2:
        if (i.isdigit()):
            x = x + i
    j = 0
    k = 1
    while k < len(x):
        mark(int(x[j]),int(x[k]))
        j = j+2
        k = k+2    
    win3.close()

#test save by mark some cells and call save to see the save.txt file get
#the result
def testSave():   
    mark(1,1)
    mark(1,2)
    mark(1,3)
    mark(5,5)
    mark(10,10)
    save()
    nextGeneration()
    save()




life()
           










