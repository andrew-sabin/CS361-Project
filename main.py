from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtChart import QChart, QChartView, QPieSeries
from MainWindow import Ui_MainWindow
from IncomeEdit import Ui_IncomeEditWindow
from GroceriesWindow import Ui_GroceriesEditWindow
from EmergenciesWindow import Ui_EmergenciesWindow
from csv import reader
import sys

class window(QtWidgets.QMainWindow):
    def __init__(self):
        super(window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.load_income()
        self.load_expenses_list()
        # Menubar options that go to other windows
        self.ui.actionEdit.triggered.connect(lambda: self.open_incomeEdit())
        self.ui.actionGroceries_2.triggered.connect(lambda: self.open_Groceries())
        self.ui.actionView.triggered.connect(lambda: self.open_Emergencies())
        self.ui.actionExit.triggered.connect(lambda: self.QCoreApplication.quit())
        self.ui.actionExit.triggered.connect(lambda: self.QCoreApplication.quit())


    def open_incomeEdit(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_IncomeEditWindow()
        self.ui.setupUi(self.window)
        self.window.show()

    def open_Groceries(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_GroceriesEditWindow()
        self.ui.setupUi(self.window)
        self.window.show()

    def open_Emergencies(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_EmergenciesWindow()
        self.ui.setupUi(self.window)
        self.window.show()

    # def exit_Program(self):
    #

    def load_income(self):
        self.ui.incomeTable.setRowCount(0)
        self.ui.incomeTable.setColumnCount(2)

        self.ui.taxbrakTable.setRowCount(0)
        self.ui.taxbrakTable.setColumnCount(2)

        self.ui.incomeTable.setHorizontalHeaderLabels(('Source', 'Amount'))
        self.ui.taxbrakTable.setHorizontalHeaderLabels(('Percent', 'Bracket'))

        self.ui.incomeTable.setColumnWidth(0, 175)
        self.ui.incomeTable.setColumnWidth(1, 205)

        self.ui.taxbrakTable.setColumnWidth(0, 80)
        self.ui.taxbrakTable.setColumnWidth(1, 190)

        total = 0
        with open('Income Example.csv') as file:
            csv_read = reader(file)
            row = 0

            for source in csv_read:
                if source[1] != 'Amount':
                    self.ui.incomeTable.setRowCount(row + 1)
                    col = 0
                    self.ui.incomeTable.setItem(row,col,QTableWidgetItem(source[0]))
                    col += 1
                    inc_amt = float(source[1])
                    self.ui.incomeTable.setItem(row,col,QTableWidgetItem('$' + "{:.2f}".format(inc_amt)))
                    row += 1
                    total += float(source[1])
        with open('SingleTaxBracket.csv') as file:
            brak_read = reader(file)
            row = 0
            for bracket in brak_read:
                if bracket[1] != 'bracket':
                    self.ui.taxbrakTable.setRowCount(row + 1)
                    col = 0
                    self.ui.taxbrakTable.setItem(row,col,QTableWidgetItem(bracket[0]))
                    col += 1
                    self.ui.taxbrakTable.setItem(row, col, QTableWidgetItem(bracket[1]))
                    if bracket[3] != 'N/A':
                        if total > float(bracket[2])/12 and total < float(bracket[3])/12:
                            total = total - (total * (float(bracket[4])/12))
                    else:
                        if total > float(bracket[2])/12:
                            total = total - (total * (.37/12))
                    row += 1
            self.ui.fulltotalLabel.setText('$' + "{:.2f}".format(total))

    def load_expenses_list(self):
        # vbox = QVBoxLayout()

        # grab items from expenses csv file
        with open('Expenses Example.csv') as file:
            csv_loader = reader(file)
            total = 0
            list = []
            for expense in csv_loader:
                if expense[1] != 'Amount':
                    list.append(expense)
                    total += float(expense[1])
        # sort items
        for itr in range(1, len(list)):
            key_value = list[itr]

            jitr = itr - 1

            while jitr >= 0 and float(list[jitr][1]) < float(key_value[1]):
                list[jitr + 1] = list[jitr]
                jitr -= 1

            list[jitr + 1] = key_value
        # add items from list to listwidget
        new_item = 0
        series = QPieSeries()
        chart = QChart()
        for expense in list:
            self.ui.expensesList.addItem(expense[0] + ": $" "{:.2f}".format(float(expense[1])))
            series.append(expense[0],float(expense[1]))
        self.ui.labelExpTotal.setText("$" "{:.2f}".format(float(total)))
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        #TO DO: Fix QChartView to view chart created in function
        self.ui.piechartView = QChartView(chart)











def create_app():
    app = QtWidgets.QApplication(sys.argv)
    win = window()
    win.show()
    sys.exit(app.exec_())

create_app()

