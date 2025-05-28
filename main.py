import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog, QMessageBox

from main_window import Ui_MainWindow
from shop_window import Ui_Shop_window
from connection import DatabaseManager
from add_product import Ui_Dialog
from PyQt6.QtGui import QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon("icon.png"))
        self.db = DatabaseManager()

        self.load_products()

        self.ui.open_shop.clicked.connect(self.open_shop_window)
        self.ui.delete_btn.clicked.connect(self.delete_products)
        self.ui.add_btn.clicked.connect(self.open_add_products)

    def load_products(self):
        data = self.db.load_all_products()
        self.ui.tableWidget.setColumnCount(8)
        self.ui.tableWidget.setRowCount(len(data))
        self.ui.tableWidget.setHorizontalHeaderLabels(["ID", "Название", "Тип", "Артикул", "Мин. цена", "Материал", "Цех", "Время(мин)"])

        for row, item in enumerate(data):
            for col, value in enumerate(item):
                self.ui.tableWidget.setItem(row, col, QTableWidgetItem(str(value)))


    def open_shop_window(self):
        self.dialog = ShopWindow()
        self.dialog.exec()

    def delete_products(self):
        select_row = self.ui.tableWidget.currentRow()
        product_id = self.ui.tableWidget.item(select_row, 0).text()
        self.db.delete_product_id(product_id)
        self.load_products()

    def open_add_products(self):
        self.dialog = AddProduct()
        self.dialog.exec()  # Ожидание закрытия диалога
        self.load_products()  # Обновление данных после закрытия



class ShopWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Shop_window()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon("icon.png"))
        self.db = DatabaseManager()

        self.load_shop()

    def load_shop(self):
        data = self.db.load_all_shop()
        self.ui.tableWidget.setColumnCount(3)
        self.ui.tableWidget.setRowCount(len(data))
        self.ui.tableWidget.setHorizontalHeaderLabels(["ID", "Наименование", "Кол-во людей"])

        for row, item in enumerate(data):
            for col, value in enumerate(item):
                self.ui.tableWidget.setItem(row, col, QTableWidgetItem(str(value)))

class AddProduct(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.db = DatabaseManager()

        self.load_data_combobox()
        self.ui.save_btn.clicked.connect(self.save_products)

    def load_data_combobox(self):
        type_products = self.db.load_data_from_table("type_products", "name_type_products")
        for type_products_id, type_products_column in type_products:
            self.ui.box_type.addItem(type_products_column, userData=type_products_id)

        materials = self.db.load_data_from_table("materials", "name_material")
        for materials_id, materials_column in materials:
            self.ui.box_material.addItem(materials_column, userData=materials_id)

        shop = self.db.load_data_from_table("shop", "name_shop")
        for shop_id, shop_column in shop:
            self.ui.box_shop.addItem(shop_column, userData=shop_id)

    def save_products(self):
        name_products = self.ui.line_name.text()
        id_type_products = self.ui.box_type.currentData()
        article = self.ui.line_article.text()
        min_price = self.ui.line_price.text()
        id_materials = self.ui.box_material.currentData()
        id_shop = self.ui.box_shop.currentData()
        time_ready = self.ui.line_time.text()

        self.db.add_products_table(name_products, id_type_products, article, min_price, id_materials, id_shop, time_ready)
        self.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    sys.exit(app.exec())