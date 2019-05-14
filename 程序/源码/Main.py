# -*- coding: utf-8 -*-
# @Time    : 2019/4/15 11:05 PM
# @Author  : LeeHW
# @File    : test_UI_NEW.py
# @Software: PyCharm
import warnings

warnings.filterwarnings("ignore")
import sys  # 导入sys模块
from PyQt5.QtWidgets import QSizePolicy  # 导入PyQt模块
from PyQt5 import QtCore, QtGui, QtWidgets
import UI_window
from load_data import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QMessageBox
from text_list import *
import baostock as bs
from roe import *

lg = bs.login(user_id="anonymous", password="123456")

class Figure_Canvas(FigureCanvas):
	def __init__(self, parent=None, width=5.78, height=4.27, dpi=100):
		# facecolor设置图表边框背景颜色
		self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor='white')
		FigureCanvas.__init__(self, self.fig)
		FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)
		self.setParent(parent)
		self.axes = self.fig.add_subplot(111)
		# 设置图表背景颜色
		self.axes.patch.set_facecolor("#1a1819")
		self.axes.grid(color='w', linestyle='--', linewidth=2, alpha=0.3)

	def test(self, x, y):
		# 清除figure
		self.figure.clf()
		# 重设axes
		self.axes = self.fig.add_subplot(111)
		self.axes.patch.set_facecolor("#1a1819")
		self.axes.plot(x, y, 'w')
		# 设置网格线
		self.axes.grid(color='w', linestyle='-', linewidth=2, alpha=0.3)
		self.draw()


class EmittingStream(QtCore.QObject):
	textWritten = QtCore.pyqtSignal(str)  # 定义一个发送str的信号

	def write(self, text):
		self.textWritten.emit(str(text))

#重写QMainWindow类
class MyWindow(QtWidgets.QMainWindow):
	def __init__(self, parent = None):
		QtWidgets.QMainWindow.__init__(self, parent)

	#重写关闭事件，在退出程序前将临时数据库删除
	def closeEvent(self, event):
		remove_db()
		# reply = QMessageBox.question(self, 'Message', 'Are you sure to quit?',
        #                                    QMessageBox.Yes, QMessageBox.No)
		# if reply == QMessageBox.Yes:
		# 	event.accept()
		# else:
		# 	event.ignore()

class myMainWindow(UI_window.Ui_MainWindow):

	def __init__(self, mainwindow):
		super().setupUi(mainwindow)  # 调用父类的setupUI函数
		# self.scrollArea.hide()
		self.search.clicked.connect(self.on_click)
		self.lineEdit.returnPressed.connect(self.on_click)
		sys.stdout = EmittingStream(textWritten=self.outputWritten)
		sys.stderr = EmittingStream(textWritten=self.outputWritten)
		self.Profitability_canvas = Figure_Canvas(self.groupBox_2)  # 实例化一个获利能力分析的FigureCanvas
		self.Solvency_canvas = Figure_Canvas(self.groupBox_3)  # 实例化一个偿债能力分析的FigureCanvas
		self.Economic_efficiency_canvas = Figure_Canvas(self.groupBox_4)  # 实例化一个经济效益分析的FigureCanvas
		self.Financial_Structure_canvas = Figure_Canvas(self.groupBox_5)  # 实例化一个财务结构分析的FigureCanvas

	def on_click(self):
		self.textEdit.clear()
		self.lineEdit.text_list.hide()
		self.stock_id = self.lineEdit.text()
		if find_code(self.stock_id, self.lineEdit.stock_lib, self.lineEdit.comp_lib):
			self.pushButton_4.clicked.connect(self.show_yymll)
			self.pushButton_5.clicked.connect(self.show_yyjll)
			self.pushButton_6.clicked.connect(self.show_syzqybcl)
			self.pushButton_9.clicked.connect(self.show_zcbcl)

			self.pushButton_7.clicked.connect(self.show_ldbl)
			self.pushButton_8.clicked.connect(self.show_lxbzbs)

			self.pushButton_10.clicked.connect(self.show_chzzl)
			self.pushButton_11.clicked.connect(self.show_yszkzzl)
			self.pushButton_12.clicked.connect(self.show_zzczzl)

			self.pushButton_13.clicked.connect(self.show_syzqybl)
			self.pushButton_14.clicked.connect(self.show_fzbl)


			download_data(self.stock_id)
			create_data(self.stock_id)

			# 初始化获利能力分析
			self.show_yymll()
			# 初始化偿债能力分析
			self.show_ldbl()
			# 初始化经济效益分析
			self.show_chzzl()
			# 初始化财务结构分析
			self.show_syzqybl()
			# 展示roe
			self.show_roe(self.stock_id)
		else:
			print("请输入正确的公司代码")

	# 展示roe
	def show_roe(self, stock_id):
		roe = str(round(roeAvg(stock_id)*100,2)) + '%'
		self.textEdit_2.setText('上一年度ROE综合评价指数：' + roe)
		# self.textEdit_2.show()

	# 展示获利能力分析图表
	def show_yymll(self):
		yymll, yyjll, syzqybcl, zcbcl, time_list = Profitability_Analysis(self.stock_id)
		self.Profitability_canvas.test(time_list, yymll)  # 初始显示营业毛利率
		self.Profitability_canvas.show()

	def show_yyjll(self):
		yymll, yyjll, syzqybcl, zcbcl, time_list = Profitability_Analysis(self.stock_id)
		self.Profitability_canvas.test(time_list, yyjll)  # 初始显示营业净利率
		self.Profitability_canvas.show()

	def show_syzqybcl(self):
		yymll, yyjll, syzqybcl, zcbcl, time_list = Profitability_Analysis(self.stock_id)
		self.Profitability_canvas.test(time_list, syzqybcl)  # 初始显示所有者权益报酬率
		self.Profitability_canvas.show()

	def show_zcbcl(self):
		yymll, yyjll, syzqybcl, zcbcl, time_list = Profitability_Analysis(self.stock_id)
		self.Profitability_canvas.test(time_list, zcbcl)  # 初始显示资产报酬率
		self.Profitability_canvas.show()

	# 展示偿债能力分析图表
	def show_ldbl(self):
		ldbl, lxbzbs, time_list = Solvency_analysis(self.stock_id)
		self.Solvency_canvas.test(time_list, ldbl)  # 初始显示流动比率
		self.Solvency_canvas.show()

	def show_lxbzbs(self):
		ldbl, lxbzbs, time_list = Solvency_analysis(self.stock_id)
		self.Solvency_canvas.test(time_list, lxbzbs)  # 初始显示利息保障倍数
		self.Solvency_canvas.show()

	# 展示经济效益分析图表
	def show_chzzl(self):
		chzzl, yszkzzl, zzczzl, time_list = Economic_efficiency_analysis(self.stock_id)
		self.Economic_efficiency_canvas.test(time_list, chzzl)  # 初始显示存货周转率
		self.Economic_efficiency_canvas.show()

	def show_yszkzzl(self):
		chzzl, yszkzzl, zzczzl, time_list = Economic_efficiency_analysis(self.stock_id)
		self.Economic_efficiency_canvas.test(time_list, yszkzzl)  # 初始显示应收账款周转率
		self.Economic_efficiency_canvas.show()

	def show_zzczzl(self):
		chzzl, yszkzzl, zzczzl, time_list = Economic_efficiency_analysis(self.stock_id)
		self.Economic_efficiency_canvas.test(time_list, zzczzl)  # 初始显示总资产周转率
		self.Economic_efficiency_canvas.show()

	# 展示财务结构分析
	def show_syzqybl(self):
		syzqybl, fzbl, time_list = Financial_Structure_Analysis(self.stock_id)
		self.Financial_Structure_canvas.test(time_list, syzqybl)  # 初始显示所有者权益比率

	def show_fzbl(self):
		syzqybl, fzbl, time_list = Financial_Structure_Analysis(self.stock_id)
		self.Financial_Structure_canvas.test(time_list, fzbl)  # 初始显示负债比率

	def outputWritten(self, text):
		cursor = self.textEdit.textCursor()
		cursor.movePosition(QtGui.QTextCursor.End)
		cursor.insertText(text)
		self.textEdit.setTextCursor(cursor)
		self.textEdit.ensureCursorVisible()
		QApplication.processEvents()  # 刷新界面


if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = MyWindow()
	ui = myMainWindow(MainWindow)
	# 居中显示
	screen = QDesktopWidget().screenGeometry()
	size = MainWindow.geometry()
	MainWindow.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)
	ui.lineEdit.setFocus()
	# 获取数据
	stock_id, comp_lib = load_code()
	ui.lineEdit.fill_data(stock_id, comp_lib)
	# 获取样式
	with open('qss.qss', 'r') as f:
		MainWindow.setStyleSheet(f.read())
	MainWindow.show()
	sys.exit(app.exec_())
