import time
import random
from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height, title):
        self.__root = Tk(className=title)
        self.__new_canvas = Canvas(self.__root, width=width, height=height, background="white",)
        self.__new_canvas.pack()
        self.__running = True
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
        

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
    
    def close(self):
        self.__running = False
    
    def draw_line(self, line, fill_color):
        line.draw(self.__new_canvas, fill_color)

class Point:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def get_x(self):
        return self.__x
    
    def get_y(self):
        return self.__y
    
    def set_x(self, x):
        self.__x = x

    def set_y(self, y):
        self.__y = y

class Line:
    def __init__(self, point1, point2):
        self.__point1 = point1
        self.__point2 = point2

    def draw(self, canvas, fill_color):
        canvas.create_line(self.__point1.get_x(), self.__point1.get_y(), self.__point2.get_x(), self.__point2.get_y(), fill = fill_color, width = 2)

class Cell:
    def __init__(self, x1, x2, y1, y2, win=None, has_left_wall=True, has_right_wall=True, has_top_wall=True, has_bottom_wall=True):
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        self.__x1 = x1
        self.__x2 = x2
        self.__y1 = y1
        self.__y2 = y2
        self.__win = win
        self.visited = False

    def get_x1(self):
        return self.__x1
    
    def get_x2(self):
        return self.__x2
    
    def get_y1(self):
        return self.__y1
    
    def get_y2(self):
        return self.__y2
    
    def wall_color(self, has_wall):
        if has_wall:
            return "black"
        return "white"
    
    def draw(self, x_offset=0, y_offset=0):
        
        self.__win.draw_line(Line(Point(self.__x1 + x_offset, self.__y1 + y_offset), Point(self.__x1 + x_offset, self.__y2 + y_offset)), self.wall_color(self.has_left_wall))
        self.__win.draw_line(Line(Point(self.__x2 + x_offset, self.__y1 + y_offset), Point(self.__x2 + x_offset, self.__y2 + y_offset)), self.wall_color(self.has_right_wall))
        self.__win.draw_line(Line(Point(self.__x1 + x_offset, self.__y1 + y_offset), Point(self.__x2 + x_offset, self.__y1 + y_offset)), self.wall_color(self.has_top_wall))
        self.__win.draw_line(Line(Point(self.__x1 + x_offset, self.__y2 + y_offset), Point(self.__x2 + x_offset, self.__y2 + y_offset)), self.wall_color(self.has_bottom_wall))

    def draw_move(self, to_cell, undo=False, x_offset=0, y_offset=0):
        if undo:
            color = "gray"
        else:
            color = "red"

        self.__win.draw_line(Line(Point(((self.__x1 + self.__x2) / 2  + x_offset),
                                        ((self.__y1 + self.__y2) / 2) + y_offset),
                                        Point(((to_cell.get_x1() + to_cell.get_x2()) / 2 + x_offset),
                                              ((to_cell.get_y1() + to_cell.get_y2()) / 2 + y_offset))), color)
    def __repr__(self):
        return (f"x1: {self.__x1}, x2: {self.__x2}, y1: {self.__y1}, y2: {self.__y2}, visited: {self.visited}")

class Maze:
    def __init__(
            self,
            x1,
            y1,
            num_rows,
            num_cols,
            cell_size_x,
            cell_size_y,
            win=None,
            seed=None
    ):
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        self._cells = []
        self._create_cells()
        if seed:
            random.seed(seed)
    
    def _create_cells(self):
        
        width = self.__cell_size_x / 2
        height = self.__cell_size_y / 2

        for i in range(self.__num_cols):
            new_column = []
            for j in range(self.__num_rows):
                new_column.append(Cell(i + (i * width), i + (i * width) + width, j + (j * height), j + (j * height) + height, self.__win))
            self._cells.append(new_column)
               
        for i in range(self.__num_cols):
            for j in range(self.__num_rows):
                self._draw_cell(i, j)
                
    def _draw_cell(self, i, j):
        self._cells[i][j].draw(self.__x1 + self.__cell_size_x, self.__y1 + self.__cell_size_y)
        self._animate()

    def _animate(self):
        self.__win.redraw()
        time.sleep(0.05)

    def __repr__(self):
        output = ""
        output = f"\nMaze Properties\nX: {self.__x1}\nY: {self.__y1}\nNum_Rows: {self.__num_rows}\nNum_Cols: {self.__num_cols}\nCell Width: {self.__cell_size_x}\nCell Height: {self.__cell_size_y}\n\n"

        for i in range(self.__num_cols):
            for j in range(self.__num_rows):
                output += (f"Cell[{i}][{j}]: {self._cells[i][j]}\n")

        return output
    
    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._cells[self.__num_cols-1][self.__num_rows-1].has_bottom_wall = False
        self._draw_cell(0, 0)
        self._draw_cell(self.__num_cols - 1, self.__num_rows - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True

        
        while True:
            possible_cells = []

            ## Add left cell if exists and not visited 
            if i > 0:
                if not self._cells[i-1][j].visited:
                    possible_cells.append(list((i - 1, j)))
            ## Add bottom cell if exists and not visited
            if j < self.__num_rows - 1:
                if not self._cells[i][j+1].visited:
                    possible_cells.append(list((i, j + 1)))
            
            ## Add right cell if exists and not visited
            if i < self.__num_cols - 1:
                if not self._cells[i+1][j].visited:
                    possible_cells.append(list((i + 1, j)))
            
            ## Add top cell if exists and not visited
            if j > 0:
                if not self._cells[i][j-1].visited:
                    possible_cells.append(list((i, j - 1)))
            
            ## If the possible cells list is empty break out of the loop
            if possible_cells == []:
                self._draw_cell(i,j)
                return
        
            ## Choose a random cell from the possible cells list
            chosen_cell = possible_cells[random.randrange(len(possible_cells))]

            ## Check if chosen cell shares left or right
            if chosen_cell[1] == j:
                ## Then check if it is either left or right
                
                ## Chosen cell is left
                if chosen_cell[0] + 1 == i:
                    self._cells[i][j].has_left_wall = False
                    self._cells[i - 1][j].has_right_wall = False
                    self._break_walls_r(i - 1, j)
                else:
                ## Chosen cell is right               
                    self._cells[i][j].has_right_wall = False
                    self._cells[i + 1][j].has_left_wall = False
                    self._break_walls_r(i + 1, j)

            ## Check if chosen cell shares top or bottom
            if chosen_cell[0] == i:
                ## Then check if it is either top or bottom
            
                ## Chosen cell is top
                if chosen_cell[1] + 1 == j:
                    self._cells[i][j].has_top_wall = False
                    self._cells[i][j - 1].has_bottom_wall = False
                    self._break_walls_r(i, j - 1)
                else:
                ## Chosen cell is bottom
                    self._cells[i][j].has_bottom_wall = False
                    self._cells[i][j + 1].has_top_wall = False
                    self._break_walls_r(i, j + 1)

    def _reset_cells_visited(self):
        
        for col in self._cells:
            for row in col:
                row.visited = False

def main():

    ## Create a window
    win = Window(800, 600, "Maze Solver")
   
    num_cols = 5
    num_rows = 5
    m1 = Maze(0, 0, num_rows, num_cols, 40, 40, win, seed=0)
    m1._break_entrance_and_exit()
    m1._break_walls_r(0, 0)
    m1._reset_cells_visited()

    for col in m1._cells:
        for row in col:
            print(row)


    win.wait_for_close()


main()
