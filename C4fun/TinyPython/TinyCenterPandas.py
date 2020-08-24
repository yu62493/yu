import sys
from PyQt5.QtWidgets import QApplication,  QMainWindow,  QMessageBox, QFileDialog
from qt_ui.ControlCenter2 import  *
from YUSCO.Core.DB_RDB import RDBConn
from pyodbc import connect as pyodbc_connect

from subprocess import call as subprocess_call
from pandas import read_sql_query as pd_read_sql_query
import socket
import csv
from PandasModel import PandasModel

class TinyControlCenter(QMainWindow,  Ui_TinyControlCenter):
    def __init__(self,  parent=None):
        super(TinyControlCenter,  self).__init__(parent)
        self.setupUi(self)
        self.LANButton.clicked.connect(self.LANConnect)
        self.WLANButton.clicked.connect(self.WLANConnect)
        self.btn_LoadData.clicked.connect(self.Load_Data)
        self.btn_SaveCSV.clicked.connect(self.SaveCSV)

    def LANConnect(self):
        subprocess_call('D:\TinyCMD\origin_setting.bat')

    def WLANConnect(self):
        subprocess_call('D:\TinyCMD\wifi_setting.bat')

    def Load_Data(self):

        if check_ip():
            s_sql = self.lineEdit.text().strip()
            db_name = str(self.comboBox.currentText())
            if s_sql :
                conn = pyodbc_connect(RDBConn(db_name))
                df = pd_read_sql_query(s_sql,con=conn)
                self.model = PandasModel(df)
                self.tableView.setModel(self.model)                    
                conn.close()
            else:
                QMessageBox.about(self, "Warning:", "請勿輸入空白")
        else:
            QMessageBox.about(self,"Warning:", "請先切換回內網")

    def SaveCSV(self):
        path = QFileDialog.getSaveFileName(
                self, 'Save File', '', 'CSV(*.csv)')
        if path[0] != '':
            print(path[0])
            self.model._df.to_csv(path[0], encoding='big5')

def check_ip():
    myname = socket.getfqdn(socket.gethostname())
    myaddr = socket.gethostbyname(myname)
    if myaddr[:3] == '172':
        return True
    else:
        return False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = TinyControlCenter()
    myWin.show()
    sys.exit(app.exec_())
   
