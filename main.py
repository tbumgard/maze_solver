from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height, title):
        self.__root = Tk(className=title)
        self.__new_canvas = Canvas(self.__root, width=width, height=height, )
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
    def __init__(self, x1, x2, y1, y2, win, has_left_wall = True, has_right_wall = True, has_top_wall = True, has_bottom_wall = True):
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        self.__x1 = x1
        self.__x2 = x2
        self.__y1 = y1
        self.__y2 = y2
        self.__win = win

    def get_x1(self):
        return self.__x1
    
    def get_x2(self):
        return self.__x2
    
    def get_y1(self):
        return self.__y1
    
    def get_y2(self):
        return self.__y2
    
    def draw(self):
        if self.has_left_wall:
            self.__win.draw_line(Line(Point(self.__x1, self.__y1), Point(self.__x1, self.__y2)), "black")

        if self.has_right_wall:
            self.__win.draw_line(Line(Point(self.__x2, self.__y1), Point(self.__x2, self.__y2)), "black")

        if self.has_top_wall:
            self.__win.draw_line(Line(Point(self.__x1, self.__y1), Point(self.__x2, self.__y1)), "black")
            
        if self.has_bottom_wall:
            self.__win.draw_line(Line(Point(self.__x1, self.__y2), Point(self.__x2, self.__y2)), "black")

    def draw_move(self, to_cell, undo=False):
        if undo:
            color = "gray"
        else:
            color = "red"

        self.__win.draw_line(Line(Point((self.__x1 + self.__x2) / 2,
                                        (self.__y1 + self.__y2) / 2),
                                        Point((to_cell.get_x1() + to_cell.get_x2()) / 2,
                                              (to_cell.get_y1() + to_cell.get_y2()) / 2)), color)

def main():

    win = Window(800, 600, "Test Window")
    point1 = Point(50, 50)
    point2 = Point(100, 100)
    line1 = Line(point1, point2)
    ##win.draw_line(line1, "black")

    cell1 = Cell(10, 20, 10, 20, win)
    cell2 = Cell(20, 30, 10, 20, win)
    
    cell1.draw()
    cell2.draw()
    
    cell1.draw_move(cell2)

    win.wait_for_close()


main()
