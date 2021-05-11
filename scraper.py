from PyQt5 import QtCore, QtGui, QtWidgets
import os
import requests
from PyQt5.QtWidgets import QApplication
from bs4 import BeautifulSoup


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(808, 576)
        MainWindow.setWindowOpacity(1.0)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setAutoFillBackground(False)

        qss_file = open('Diffnes.qss').read()
        MainWindow.setStyleSheet(qss_file)
        MainWindow.setWindowIcon(QtGui.QIcon('invader.ico'))

        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label1 = QtWidgets.QLabel(self.centralwidget)
        self.label1.setGeometry(QtCore.QRect(10, 10, 271, 41))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(26)
        font.setUnderline(True)
        self.label1.setFont(font)
        self.label1.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.label1.setAlignment(QtCore.Qt.AlignCenter)
        self.label1.setObjectName("label1")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 100, 791, 41))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.btn_run = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_run.setFont(font)
        self.btn_run.setObjectName("btn_run")
        self.gridLayout.addWidget(self.btn_run, 0, 0, 1, 1)
        self.btn_clear = QtWidgets.QPushButton(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_clear.setFont(font)
        self.btn_clear.setObjectName("btn_clear")
        self.gridLayout.addWidget(self.btn_clear, 0, 1, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 150, 791, 371))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.textBrowser.setFont(font)
        self.textBrowser.setObjectName("textBrowser")
        self.field_txt_enter_site = QtWidgets.QLineEdit(self.centralwidget)
        self.field_txt_enter_site.setGeometry(QtCore.QRect(290, 17, 501, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.field_txt_enter_site.setFont(font)
        self.field_txt_enter_site.setStatusTip("")
        self.field_txt_enter_site.setText("")
        self.field_txt_enter_site.setObjectName("field_txt_enter_site")
        self.field_txt_num_pages = QtWidgets.QLineEdit(self.centralwidget)
        self.field_txt_num_pages.setGeometry(QtCore.QRect(290, 57, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.field_txt_num_pages.setFont(font)
        self.field_txt_num_pages.setStatusTip("")
        self.field_txt_num_pages.setText("")
        self.field_txt_num_pages.setObjectName("field_txt_num_pages")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 808, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Web Scraper", "Web Scraper"))
        self.label1.setText(_translate("MainWindow", "Web Scraper"))
        self.btn_run.setText(_translate("MainWindow", "Run"))
        self.btn_clear.setText(_translate("MainWindow", "Clear"))
        self.field_txt_enter_site.setWhatsThis(_translate("MainWindow", "enter site"))
        self.field_txt_enter_site.setPlaceholderText(_translate("MainWindow", "Enter topic"))
        self.field_txt_num_pages.setWhatsThis(_translate("MainWindow", "enter site"))
        self.field_txt_num_pages.setPlaceholderText(_translate("MainWindow", "Enter number of pages"))

    def insert_text_console(self, text):
        self.textBrowser.append(text)
        QApplication.processEvents()
        self.textBrowser.ensureCursorVisible()

    def clear_text(self):
        self.textBrowser.clear()


headers = {'Accept-Language': 'en-US,en;q=0.5'}


def format_file_name(name):
    return name.replace(" ", '_').translate(str.maketrans('', '', "!\"#$%&'()*+,-./:;<=>?@[\\]^`{|}~")).strip()


def write_to_file(article_name_, article_soup_):
    article_file = open(f"{format_file_name(article_name_)}.txt", "wb")
    article_file.write(bytes(
        article_soup_.find('div', {"class": ["article-item__body", "article__body"]}).text.strip().encode("utf-8")))
    article_file.close()


def change_page(page_count_):
    params = {"page": str(page_count_)}
    return requests.get("https://www.nature.com/nature/articles", headers=headers, params=params)


def run_logic(ui):
    page_num = int(ui.field_txt_num_pages.text())
    topic = ui.field_txt_enter_site.text()
    req = requests.get("https://www.nature.com/nature/articles", headers=headers)
    soup = BeautifulSoup(req.content, "html.parser")

    page_count = 1
    total_num_articles_site = 0

    for p in range(1, page_num + 1):
        article_count_page = 0
        new_page_dir_name = "Page_" + str(page_count)

        if not os.path.exists(new_page_dir_name):
            os.mkdir(new_page_dir_name)
        os.chdir(new_page_dir_name)
        if not os.path.exists(topic):
            os.mkdir(topic)
        os.chdir(topic)

        articles = soup.find_all('article')

        ui.insert_text_console("------------------------------------")
        ui.insert_text_console(f"Checking Page {page_count}")
        ui.insert_text_console(req.url)

        for i in range(0, 20):

            if articles[i].find('span', {'data-test': 'article.type'}).text.lower().strip() == topic.lower():
                ui.insert_text_console(
                    "-> Getting article: " + "https://www.nature.com" + articles[i].find('a').get('href'))

                req_article = requests.get("https://www.nature.com" + articles[i].find('a').get('href'),
                                           headers={'Accept-Language': 'en-US,en;q=0.5'})
                article_soup = BeautifulSoup(req_article.content, "html.parser")

                article_name = format_file_name(articles[i].find('a').text)
                ui.insert_text_console(f"--Writing {article_name} into file...")

                if article_soup.find('div', {"class": ["article-item__body", "article__body"]}):
                    write_to_file(article_name, article_soup)

                article_count_page += 1

        ui.insert_text_console(f"Total num of articles found on page {page_count}: {article_count_page}")

        page_count += 1
        total_num_articles_site += article_count_page

        req = change_page(page_count)
        soup = BeautifulSoup(req.content, "html.parser")

        os.chdir("../../")

    ui.insert_text_console("\nAll articles have been saved! :)")
    ui.insert_text_console(f"Total num of articles: {total_num_articles_site}")


# Client code
def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    ui.btn_run.clicked.connect(lambda: run_logic(ui))
    ui.btn_clear.clicked.connect(lambda: ui.clear_text())

    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
