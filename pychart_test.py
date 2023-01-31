from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from PyQt5.QtChart import QChart, QChartView, QPieSeries
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
from csv import reader

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt PieChart")
        self.setGeometry(100,100,680,500)

        self.create_piechart()

        self.show()

    def create_piechart(self):
        series = QPieSeries()
        with open('Expenses Example.csv') as file:
            csv_read = reader(file)
            row = 0
            for expense in csv_read:
                if expense[1] != 'Amount':
                    series.append(expense[0],float(expense[1]))

        chart = QChart()
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle("Current Expenses With Percentages")

        chartview = QChartView(chart)
        chartview.setRenderHint(QPainter.Antialiasing)

        self.setCentralWidget(chartview)


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec_())

