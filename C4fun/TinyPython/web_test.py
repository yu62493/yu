import sys 
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import * 
from PyQt5.QtWebEngineWidgets import QWebEngineView 
################################################ #######创建主窗口 ################################################ 
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('My Browser')
        self.showMaximized()
        self.tabWidget = QTabWidget()
        self.tabWidget.setTabShape(QTabWidget.Triangular)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.close_Tab)
        self.setCentralWidget(self.tabWidget)
        
        self.webview = WebEngineView()
        self.webview.load(QUrl("http://www.baidu.com"))
        self.create_tab(self.webview)
    #创建tab
    def create_tab(self,webview):
        self.tab = QWidget()
        self.tabWidget.addTab(self.tab, "新标签页")
        self.tabWidget.setCurrentWidget(self.tab)
        #####
        self.Layout = QHBoxLayout(self.tab)
        self.Layout.setContentsMargins(0, 0, 0, 0)
        self.Layout.addWidget(webview)
        
    #关闭tab
    def close_Tab(self,index):
        if self.tabWidget.count()>1:
            self.tabWidget.removeTab(index)
            
class WebEngineView(QWebEngineView): 
    # 重写createwindow()
    def createWindow(self, QWebEnginePage_WebWindowType):
        new_webview = WebEngineView()
        the_mainwindow.create_tab(new_webview)
        return new_webview

if __name__ == "__main__":
    app = QApplication(sys.argv)
    the_mainwindow = MainWindow()
    the_mainwindow.show()
    sys.exit(app.exec_())
