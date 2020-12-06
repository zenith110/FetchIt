from PySide2 import QtWidgets, QtCore, QtGui
import json
import formatter
import os
import shutil
class algo():
    def __init__(self):
        self.choice = ""
        
algodata = algo()
class tool(formatter.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self):
        super(tool, self).__init__()
        self.setupUi(self)
        self.save.clicked.connect(self.save_data)
        self.comboBox.currentTextChanged.connect(self.algo_switch)
    def algo_switch(self, index):
        algodata.choice = index
    def save_data(self):
        problemName = self.problemName.text()
        termDate = self.termDate.text()
        Statement = self.Statement.text()
        Code = self.Code.text()
        Solution = self.Solution.text()
        Statement = Statement.replace(".", ".\n").replace("\r", "")
        fileName = str.lower(termDate).replace(" ", "-")
        data = {'Problem_Name': problemName, 'Seen_On': termDate, 'Problem_Statement': Statement, 'Problem_Code': Code, 'Solution': Solution}
        file = open(fileName + ".json", "w")
        # Dumps the data to the file
        json.dump(data, file, indent = 1)
        print("Dumping data now...")
        file.close()
        shutil.move(fileName + ".json", "../src/" + algodata.choice)
        
if __name__ == "__main__":
    app = QtWidgets.QApplication()
    qt_app = tool()
    qt_app.show()
    app.exec_()