#Sorting CLASS!
from PyQt5 import QtWidgets

class personalizedTableWidgetItem(QtWidgets.QTableWidgetItem):
    def __init__(self, text, sortKey):
        QtWidgets.QTableWidgetItem.__init__(self, text, QtWidgets.QTableWidgetItem.UserType)
        self.sortKey = sortKey

    def __lt__(self, other):
        return self.sortKey < other.sortKey
