from graphics import Window, Line, Point
from cell import Cell


def main():
    win = Window(800, 600)
    point_one = Point(2,3)
    point_two = Point(100,100)
    #line = Line(point_one,point_two)
    cell = Cell(100,200,100,200, win)
    cell.draw()
    cell_two = Cell(200,300,200,300, win)
    cell_two.draw()
    cell.draw_move(cell_two, True)
    win.wait_for_close()


main()