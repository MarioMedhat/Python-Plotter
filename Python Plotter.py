# BY : MARIO MEDHAT
# GITHUB REPOSITORY LINK : https://github.com/MarioMedhat/Python-Plotter

# first we have to import the libraries we are going to use
# or some classes from these libraries
import sys
from sympy import *
import numpy
from PySide2.QtWidgets import QApplication, QLabel, QLineEdit, QPushButton, QWidget, QGridLayout
from PySide2.QtGui import QFont
from math import inf
import pyqtgraph as pg


def plotter(equ, max_val, min_val, step):
    # the function that plots the input equation of the user

    # check first if the user has entered an input
    # or just blank input is found
    if (equ == '') or (max_val == '') or (min_val == '') or (step == ''):
        # if there is no input
        # then ends the function and print to user
        # informing him to enter an input
        return mainwin.errormsg.setText('please fill all the data')

    # clear the error msg
    mainwin.errormsg.setText('')

    # define the variable's symbol
    x = symbols('x')

    # we have to check if the user has entered a
    # valid input, some mistakes may occur from
    # the user, like entering a symbol instead of a number
    try:
        max_val = float(max_val)
        min_val = float(min_val)
        step = float(step)
    except:
        # if there is an error
        # then ends the function and print to user
        # informing him to enter a valid input
        return mainwin.errormsg.setText('max, min, step can only be numbers')

    # then we have to check for some logic errors that
    # may occur from the user
    # so we have to define first a counter for our loop
    counter = 0
    # then we have to define a variable
    # and assign to it the value of the
    # length of the equation
    length = len(equ)

    # the start of the loop
    # and the exit condition is
    # to reach the end of the input array
    while counter < length:
        # we check first that the user did not enter a number
        # next to the variable as this may cause some errors
        # so we have to check first if the current input is a number
        if (equ[counter] >= '0') and (equ[counter] <= '9'):
            # then be sure that this is not the last input of the array
            # as to be able to check for the next element
            # because if this is the last
            # element and we checked for the next element
            # we will have a runtime error of overflow of the array
            if counter + 1 < length:
                # then we have to check if the next element is a 'x'
                # which is the symbol of the input variable
                if equ[counter+1] == 'x':
                    # if true
                    # then ends the function and print to user
                    # informing him about the error
                    return mainwin.errormsg.setText('unable to write a number next to \'x\'')

        # then check if the user ended the equation with an operand
        # as this has no sense so it must be an error
        # to check for this we have to see if the current element an operand
        elif (equ[counter] == '+') or (equ[counter] == '-') or (equ[counter] == '/') \
                or (equ[counter] == '*') or (equ[counter] == '^'):
            # if yes then check if we reached the end of the array
            if counter + 1 >= length:
                # if true
                # then ends the function and print to user
                # informing him about the error
                return mainwin.errormsg.setText('unable to end the equation with an operand')

            # then check if the user has entered any operand and
            # after it entered '*' or '/' or '^'
            # as this have no meaning we have to inform him
            # to check this we have to see if
            # the current input is an operand
            # and this iis what is done before
            # then check if the next input is '*' or '/' or '^'
            elif equ[counter+1] == '*' or equ[counter+1] == '/' or equ[counter+1] == '^':
                # if true
                # then ends the function and print to user
                # informing him about the error
                return mainwin.errormsg.setText('unable to write \'' + equ[counter+1] + '\' '
                                                + 'next to \'' + equ[counter] + '\'')

        # increase the counter value by one to go
        # to the next element
        counter = counter + 1

    # then we have to check for other
    # logical errors related to numbers
    # first we have to check if the user
    # has entered a maximum value
    # is less than or equal the minimum value
    # as this has no meaning, it's only a point
    if min_val >= max_val:
        # if true
        # then ends the function and print to user
        # informing him about the error
        return mainwin.errormsg.setText('minimum value is greater or equal maximum value')

    # then we have to check if the step is equal to zero
    # as also this is meaningless
    if step <= 0:
        # if true
        # then ends the function and print to user
        # informing him about the error
        return mainwin.errormsg.setText('the step must be a positive value')

    # another logical error that could occur is to write
    # a false input step value
    # for example if the maximum is 5 and the minimum is 2
    # then the largest step value is 3 as we will have only 2 points
    # but what if the step value is 4 ?
    # then we will overflow the maximum value so
    # this is a very important logical error to care for
    if step+min_val > max_val:
        # if true
        # then ends the function and print to user
        # informing him about the error
        return mainwin.errormsg.setText('invalid step value')

    # then we have to calculate the x-axis array values
    # and this will be done in 2 steps

    # step 1:
    # first we have to know to size of the array
    # and this is done easily by the equation below
    size = (float(max_val) - float(min_val)) / float(step)
    # then we add one to the size as to
    # include the value on the interval
    # and the arrange function fills the
    # array from one to the size of the array
    # with step equals one
    a = numpy.arange(size + 1)
    # then we apply a simple cross multiplication
    # and the add the offset value which is
    # the minimum value and every thing is done
    a = (a * step) + float(min_val)

    # then here we continue the error checking
    # but why to use the if else while
    # we have the try except method?
    # first not all the errors are treated as errors
    # some of them is considered as warning only
    # like the division by zero in numpy library
    # also the output msg that we do get here
    # is not as specific like the ones
    # that we do catch from the if else method
    # so both methods complete each other
    # as not all the errors are that simple to be
    # predicted with if else method so in
    # some cases he is a must to use the try except method
    try:
        k = lambdify(x, equ, "numpy")
    except:
        # er is a defined variable to contain the
        # error msg printed from the system
        # and we have to cast it to string
        # to print it to the user
        er = sys.exc_info()[1]
        return mainwin.errormsg.setText(str(er))

    # and this try except is made to
    # print error that could happen during
    # calculation, but the division is not included here
    # as the numpy treats it as warning not error
    # so it will be handled manually with if else
    try:
        y = k(a)
    except:
        # er is a defined variable to contain the
        # error msg printed from the system
        # and we have to cast it to string
        # to print it to the user
        er = sys.exc_info()[1]
        return mainwin.errormsg.setText(str(er))

    # here we are going to start checking
    # for division by zero error
    # first we have to reset the counter as
    # we will make a loop for this check
    counter = 0

    # there is a special that we have to take care for
    # first we will discuss how to extract the error
    # and then we will know why this is a case to care for

    # to detect the error we will loop
    # for the array of the y-axis and check
    # if the value is 'inf' and this is the output
    # of a division by zero in numpy, that's why they
    # treat it as warning not an error
    # so we have to check for every iteration
    # if the value is equal to 'inf'
    # then the error occurred
    # but if the function is a number then the value of
    # the y-axis is an 'int' and it could
    # not be compared to 'inf'
    # but like that we are sure that
    # the error has not occurred
    if type(y) == int:
        # then first we must assure that
        # the loop will not be executed
        # so make the exit condition equal false
        # the condition is that the counter must be equal
        # or greater than the size so
        # as to exit the loop
        # then making counter = size,
        # make the condition false
        counter = size
        # then another thing that we have to care for
        # is that the plot function must be given 2 arrays
        # of equal size but here the y-axis
        # is only a single int
        # so we have to create an array with the same
        # size of the x-axis one and fill it the the int value
        y = numpy.arange(size + 1)
        y.fill(k(a))

    # start the loop
    while counter < size:
        # check if the value is 'inf'
        if y[counter] == inf:
            # if true
            # then ends the function and print to user
            # informing him about the error
            return mainwin.errormsg.setText('division by zero occurred')

        # increase the counter value by one to go
        # to the next element
        counter = counter + 1

    # plot the function
    mainwin.my_plot.plot(a, y)


class MainWindow (QWidget):
    # this is the class that contains the GUI form

    # define the initialization function
    def __init__(self):
        # define the super to have single inheritance
        # it makes a class derives (or inherits)
        # attributes and behaviors
        # from another class without needing
        # to implement them again.
        super().__init__()

        # then we have to create our gui

        # define the title of the form
        self.setWindowTitle("Function Plotter")
        # define the opening size and axis
        self.setGeometry(250, 250, 1200, 570)
        # define the maximum size of the form
        # and this is very important so as if the
        # form is maximized the widgets will have bad look
        # and bad organization due to expansion property
        self.setMaximumSize(1200, 570)

        # then we have to define the label that
        # prints the user some rules to follow
        ReqMsg = QLabel('<h1>please fill all the data '
                        ',do not type a x next to a number '
                        ',do not enter any other variable that \'x\'</h1>', parent=self)
        # this function helps to organize the
        # label text in multi-line instead of
        # being in one single line because this
        # will cause the msg to not appear
        ReqMsg.setWordWrap(True)
        # set the font policy and size
        ReqMsg.setFont(QFont("Sanserif", 6))
        # set some other preferences in the style like:
        # the boarder, the background, the line color
        ReqMsg.setStyleSheet("border : 1px solid black; background-color: white; color : green")

        # then we have to define the label that
        # prints the user the errors done
        # either during calculation
        # or due to false entered inputs
        self.errormsg = QLabel()
        # multi-line organization
        self.errormsg.setWordWrap(True)
        # set the font policy and size
        self.errormsg.setFont(QFont("Sanserif", 10))
        # set some other preferences in the style like:
        # the boarder, the background, the line color
        self.errormsg.setStyleSheet("border: 1px solid black; background-color: white; color: red")

        # each widget in the form must be followed by a
        # label that explains what is the widget

        # the error msg label
        errormsgname = QLabel('<h1>ERROR MSG</h1>', parent=self)
        # multi-line organization
        errormsgname.setWordWrap(True)
        # set the font policy and size
        errormsgname.setFont(QFont("Sanserif", 3))

        # the function input label
        funcmsg = QLabel('<h1>FUNCTION</h1>', parent=self)
        # multi-line organization
        funcmsg.setWordWrap(True)
        # set the font policy and size
        funcmsg.setFont(QFont("Sanserif", 4))

        # the maximum input label
        maxmsg = QLabel('<h1>MAX</h1>', parent=self)
        # multi-line organization
        maxmsg.setWordWrap(True)
        # set the font policy and size
        maxmsg.setFont(QFont("Sanserif", 4))

        # the minimum input label
        minmsg = QLabel('<h1>MMIN</h1>', parent=self)
        # multi-line organization
        minmsg.setWordWrap(True)
        # set the font policy and size
        minmsg.setFont(QFont("Sanserif", 4))

        # the step input label
        stepmsg = QLabel('<h1>STEP</h1>', parent=self)
        # multi-line organization
        stepmsg.setWordWrap(True)
        # set the font policy and size
        stepmsg.setFont(QFont("Sanserif", 4))

        # then we have to define the text-box for each input
        self.func_user_input = QLineEdit()
        self.min_user_input = QLineEdit()
        self.max_user_input = QLineEdit()
        self.step_user_input = QLineEdit()

        # then we have to define the action buttons
        self.calc_btn = QPushButton('ADD PLOT', self)
        self.clear_btn = QPushButton('CLEAR', self)

        # then we have to define the plot widget box
        self.my_plot = pg.PlotWidget()
        # set the background color, 'w' == white
        self.my_plot.setBackground('w')
        # set a boarder for the plot-box
        self.my_plot.setStyleSheet("border : 1px solid black;")

        # then we have to define a very important parameter
        # in our form organization, which is the layout
        # and here we choose the Grid layout as
        # we have many widgets in many rows and columns
        layout = QGridLayout()

        # then we will start organizing our form layout

        # first add i the first row the requirements msg
        # and this widget will take the place of 5 units in the column part
        # as it must be a little bit tall
        layout.addWidget(ReqMsg, 0, 0, 5, 1)

        # then in the next row we will add the
        # 4 labels of the inputs
        # one in a column
        layout.addWidget(funcmsg, 0, 1)
        layout.addWidget(maxmsg, 1, 1)
        layout.addWidget(minmsg, 2, 1)
        layout.addWidget(stepmsg, 3, 1)

        # then in the next row we will add all
        # the input text-boxes
        # one in a column
        layout.addWidget(self.func_user_input, 0, 2)
        layout.addWidget(self.max_user_input, 1, 2)
        layout.addWidget(self.min_user_input, 2, 2)
        layout.addWidget(self.step_user_input, 3, 2)
        # then we will add in the same row at the bottom
        # the calculation button
        layout.addWidget(self.calc_btn, 6, 2)
        # then next to it we will add the clear button
        layout.addWidget(self.clear_btn, 6, 3)

        # then in the fourth row we will add
        # the plot widget in the place of 5 row units
        # and 4 column units
        layout.addWidget(self.my_plot, 0, 4, 5, 4)

        # then bellow the plot widget and next to the buttons
        # we will add the error label msg
        layout.addWidget(errormsgname, 5, 4)
        # and the error msg itself in the place of 4 column units
        layout.addWidget(self.errormsg, 6, 4, 1, 4)

        # then we have to make the buttons click events

        # first we will start with the plot one
        # when it is clicked a function is called and
        # in it's order it calls the plot function
        # and passes to it the input parameters
        self.calc_btn.clicked.connect(self.go_to_plot)

        # then the clear one
        # and it only calls the plot widget instance and clears
        # the printed or plotted data
        self.clear_btn.clicked.connect(self.my_plot.clear)

        # then we have to assure to the window that
        # the layout we designed is the one we want to be shown
        self.setLayout(layout)
        # and finally show the form
        self.show()

    def go_to_plot(self):

        # and this is the function to relate
        # the plot button with the plot function
        # it calls the plot function and passes to it the data in the text-boxes
        plotter(self.func_user_input.text(), self.max_user_input.text(),
                self.min_user_input.text(), self.step_user_input.text())


if __name__ == "__main__":

    app = QApplication(sys.argv)
    mainwin = MainWindow()
    mainwin.show()

    status = app.exec_()
    sys.exit(status)



