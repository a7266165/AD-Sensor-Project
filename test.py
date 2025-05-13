from PyQt6 import QtWidgets
import sys
app = QtWidgets.QApplication(sys.argv)

Form = QtWidgets.QWidget()
Form.setWindowTitle('oxxo.studio')
Form.resize(300, 200)

label = QtWidgets.QLabel(Form)
label.setGeometry(10,10,200,30)


box = QtWidgets.QComboBox(Form)
box.addItems(['請選擇性別', '男', '女', '其他'])
box.setGeometry(10,50,200,30)
box.setCurrentIndex(0)
box.setStyleSheet("color: black; font-size: 20px; font-family: 微軟正黑體; border: 1px solid black; border-radius: 5px; background-color: rgb(255, 255, 255); font-weight:bold")

Form.show()
sys.exit(app.exec())