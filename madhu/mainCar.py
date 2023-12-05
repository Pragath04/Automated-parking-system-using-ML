import mysql.connector
import datetime
import sys
import re
from PyQt5 import QtCore, QtWidgets, uic

# Constants
MAX_SLOTS = 16

class ParkingSystem:
    def __init__(self):
        self.slots = [False for _ in range(MAX_SLOTS)]
        self.connect_to_database()

    def connect_to_database(self):
        try:
            self.mydb = mysql.connector.connect(
                host="localhost", user="smoke", passwd="hellomoto", database="car", autocommit=True
            )
            self.mycursor = self.mydb.cursor()
            # Additional database setup code goes here
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def check_duplicate_car(self, car_number):
        self.mycursor.execute("SELECT carNumber FROM slot")
        return any(car_number in s for s in self.mycursor.fetchall())

    def insert_entry(self, car_number, entry_time):
        slot_number = self.slots.index(False) + 1
        self.slots[slot_number - 1] = True

        self.mycursor.execute("INSERT INTO slot (carNumber, slot) VALUES(%s, %s)", (car_number, slot_number))
        self.mycursor.execute("INSERT INTO entry (carNumber, entry) VALUES(%s, %s)", (car_number, entry_time))
        self.mycursor.execute("INSERT INTO exits (carNumber) VALUES(%s)", (car_number,))
        self.mycursor.execute("INSERT INTO duration (carNumber) VALUES(%s)", (car_number,))
        self.mycursor.execute("INSERT INTO cost (carNumber) VALUES(%s)", (car_number,))

        return slot_number

    def update_exit(self, car_number, exit_time):
        self.mycursor.execute("UPDATE exits SET exit1 = %s WHERE carNumber = %s", (exit_time, car_number))

        self.mycursor.execute("SELECT slot FROM slot WHERE carNumber = %s", (car_number,))
        slot_number = int(re.sub("[^0-9]", "", str(self.mycursor.fetchone())))
        self.slots[slot_number - 1] = False

        # Other updates and calculations go here
        return slot_number


class Ui(QtWidgets.QMainWindow):
    def __init__(self, parking_system):
        super(Ui, self).__init__()
        uic.loadUi("front.ui", self)
        self.parking_system = parking_system
        self.ENTRYBUTTON.released.connect(self.handle_entry)
        self.EXITBUTTON.released.connect(self.handle_exit)

    def handle_entry(self):
        car_number = self.lineEdit.text()
        if self.parking_system.check_duplicate_car(car_number):
            self.label_2.setText("Duplicate")
        else:
            entry_time = datetime.datetime.now()
            slot_number = self.parking_system.insert_entry(car_number, entry_time)
            self.label_2.setText(f"Slot: {slot_number}")

    def handle_exit(self):
        car_number = self.lineEdit.text()
        exit_time = datetime.datetime.now()
        slot_number = self.parking_system.update_exit(car_number, exit_time)
        self.label_2.setText(f"Slot {slot_number} exited")


def main():
    app = QtWidgets.QApplication(sys.argv)

    parking_system = ParkingSystem()
    window = Ui(parking_system)
    window.show()

    app.exec_()

if __name__ == "__main__":
    main()
