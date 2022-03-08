from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor
import time


class BookMarkToolBar(QtWidgets.QToolBar):
    bookmarkClicked = QtCore.pyqtSignal(QtCore.QUrl, str)

    def __init__(self, parent=None):
        super(BookMarkToolBar, self).__init__(parent)
        self.actionTriggered.connect(self.onActionTriggered)
        self.bookmark_list = []

    def setBoorkMarks(self, bookmarks):
        for bookmark in bookmarks:
            self.addBookMarkAction(bookmark["title"], bookmark["url"])

    def addBookMarkAction(self, title, url):
        bookmark = {"title": title, "url": url}
        fm = QtGui.QFontMetrics(self.font())
        if bookmark not in self.bookmark_list:
            text = fm.elidedText(title, QtCore.Qt.ElideRight, 150)
            action = self.addAction(text)
            action.setData(bookmark)
            self.bookmark_list.append(bookmark)

    @QtCore.pyqtSlot(QtWidgets.QAction)
    def onActionTriggered(self, action):
        bookmark = action.data()
        self.bookmarkClicked.emit(bookmark["url"], bookmark["title"])


class QCustomTabWidget (QtWidgets.QTabWidget):
    def __init__(self, parent=None):
        super(QCustomTabWidget, self).__init__(parent)
        self.setTabsClosable(True)
        # connect to method to close
        self.tabCloseRequested.connect(self.closeTab)
        #for i in range(1, 10):  # add tabs here
        #self.addTab(QtWidgets.QWidget(), 'Tab %d' % i)

    def closeTab(self, currentIndex):
        currentQWidget = self.widget(currentIndex)
        currentQWidget.deleteLater()
        self.removeTab(currentIndex)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.defaultUrl = QtCore.QUrl()

        #self.tabs = QtWidgets.QTabWidget()
        self.tabs = QCustomTabWidget()

        self.tabs.setStyleSheet(
            "color: rgb(255,20,147); background-color: rgb(31,31,31)")

        #self.tabs.setTabsClosable(True)
        #self.tabs.tabCloseRequested.connect(self.tabs.removeTab)

        self.setCentralWidget(self.tabs)

        self.urlLe = QtWidgets.QLineEdit()
        self.urlLe.returnPressed.connect(self.onReturnPressed)
        self.favoriteButton = QtWidgets.QToolButton()
        self.favoriteButton.setIcon(QtGui.QIcon("images/star.png"))
        self.favoriteButton.clicked.connect(self.addFavoriteClicked)

        self.newTab = QtWidgets.QToolButton()

        self.newTab.setText('New Tab')

        self.newTab.clicked.connect(
            lambda: self.add_new_tab(self.defaultUrl, 'Home'))

        self.reload_btn = QAction('Reload', self)

        self.toolbar = self.addToolBar("")
        self.toolbar.setStyleSheet(
            "color: rgb(255,20,147); background-color: rgb(31,31,31)")
        self.toolbar.addAction(self.reload_btn)
        self.toolbar.addWidget(self.urlLe)
        self.toolbar.addWidget(self.favoriteButton)
        self.toolbar.addWidget(self.newTab)

        self.addToolBarBreak()
        self.bookmarkToolbar = BookMarkToolBar()
        self.bookmarkToolbar.setStyleSheet(
            "color: rgb(255,20,147); background-color: rgb(31,31,31)")
        self.bookmarkToolbar.bookmarkClicked.connect(self.add_new_tab)
        self.addToolBar(self.bookmarkToolbar)
        self.readSettings()

    def onReturnPressed(self):
        self.tabs.currentWidget().setUrl(QtCore.QUrl.fromUserInput(self.urlLe.text()))

    def addFavoriteClicked(self):
        loop = QtCore.QEventLoop()

        def callback(resp):
            setattr(self, "title", resp)
            loop.quit()

        web_browser = self.tabs.currentWidget()
        web_browser.loadFinished.connect(self.loadFinishedHandler)
        web_browser.page().runJavaScript(
            "(function() { return document.title;})();", callback)
        url = web_browser.url()
        loop.exec_()
        self.bookmarkToolbar.addBookMarkAction(getattr(self, "title"), url)

    @QtCore.pyqtSlot()
    def loadFinishedHandler(self):
        index = self.tabs.currentIndex()

        loop = QtCore.QEventLoop()

        def callback(resp):
            setattr(self, "title", resp)
            loop.quit()

        web_browser = self.tabs.currentWidget()
        web_browser.loadFinished.connect(self.loadFinishedHandler)
        web_browser.page().runJavaScript(
            "(function() { return document.title;})();", callback)
        loop.exec_()

        self.tabs.setTabText(index, getattr(self, "title"))
        self.tabs.tabBar().setTabTextColor(index, QColor("red"))

    def add_new_tab(self, qurl=QtCore.QUrl(), label='Blank'):
        self.web_browser = QtWebEngineWidgets.QWebEngineView()

        if qurl is False:
            qurl = QtCore.QUrl('http://www.google.com')
        else:
            self.web_browser.setUrl(qurl)

        self.web_browser.adjustSize()
        self.web_browser.loadFinished.connect(self.loadFinishedHandler)
        self.web_browser.urlChanged.connect(self.updateUlrLe)

        self.index = self.tabs.addTab(self.web_browser, label)
        self.tabs.setCurrentIndex(self.index)

        self.urlLe.setText(qurl.toString())

        self.reload_btn.triggered.connect(self.web_browser.reload)

    def updateUlrLe(self, url):
        self.urlLe.setText(url.toDisplayString())

    def readSettings(self):
        setting = QtCore.QSettings()
        self.defaultUrl = setting.value(
            "defaultUrl", QtCore.QUrl('http://www.google.com'))
        self.add_new_tab(self.defaultUrl, 'Home Page')
        self.bookmarkToolbar.setBoorkMarks(setting.value("bookmarks", []))

    def saveSettins(self):
        settings = QtCore.QSettings()
        settings.setValue("defaultUrl", self.defaultUrl)
        settings.setValue("bookmarks", self.bookmarkToolbar.bookmark_list)

    def closeEvent(self, event):
        self.saveSettins()
        super(MainWindow, self).closeEvent(event)


if __name__ == '__main__':
    import sys

    QtCore.QCoreApplication.setOrganizationName("Shalora")
    QtCore.QCoreApplication.setOrganizationDomain("www.Shalora.com")
    QtCore.QCoreApplication.setApplicationName("Test Browser")
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
