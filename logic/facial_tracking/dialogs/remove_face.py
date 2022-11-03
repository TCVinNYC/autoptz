import os
import shutil

from threading import Thread
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog

from logic.facial_tracking.dialogs.train_face import Trainer
from ui.shared.message_prompts import show_info_messagebox


class RemoveFaceUI(object):
    def __init__(self):
        self.path = None
        self.name_list = None
        self.horizontalLayout = None
        self.cancel_btn = None
        self.remove_face_btn = None
        self.remove_face_title_label = None
        self.verticalLayout = None
        self.window = None
        self.count = 0

    def setupUi(self, remove_face):
        self.window = remove_face
        remove_face.setObjectName("remove_face")
        remove_face.resize(180, 60)
        self.verticalLayout = QtWidgets.QVBoxLayout(remove_face)
        self.verticalLayout.setObjectName("verticalLayout")
        self.remove_face_title_label = QtWidgets.QLabel(remove_face)
        self.remove_face_title_label.setText("remove_face_title")
        self.verticalLayout.addWidget(self.remove_face_title_label)

        self.name_list = QtWidgets.QListWidget(remove_face)
        self.name_list.setObjectName("name_list")

        # Path for face image database
        self.path = '../logic/facial_tracking/images/'
        for folder in os.listdir(self.path):
            self.name_list.addItem(folder)

        self.verticalLayout.addWidget(self.name_list)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.remove_face_btn = QtWidgets.QPushButton(remove_face)
        self.remove_face_btn.setObjectName("remove_face_btn")
        self.remove_face_btn.clicked.connect(self.remove_face_prompt)
        self.horizontalLayout.addWidget(self.remove_face_btn)

        self.cancel_btn = QtWidgets.QPushButton(remove_face)
        self.cancel_btn.setObjectName("cancel_btn")
        self.cancel_btn.clicked.connect(self.window.close)
        self.horizontalLayout.addWidget(self.cancel_btn)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.translate_ui(remove_face)
        QtCore.QMetaObject.connectSlotsByName(remove_face)

    def remove_face_prompt(self):
        selected_face = self.path + self.name_list.currentItem().text()
        shutil.rmtree(selected_face)
        show_info_messagebox("Face Removed. \nRetraining model,  please wait...")
        trainer_thread = Thread(target=Trainer().train_face(True))
        trainer_thread.daemon = True
        trainer_thread.start()
        trainer_thread.join()
        self.window.close()

    def translate_ui(self, remove_face):
        _translate = QtCore.QCoreApplication.translate
        remove_face.setWindowTitle(_translate("remove_face", "Remove Face"))
        self.remove_face_title_label.setText(_translate("remove_face_title", "Select Name:"))
        self.remove_face_btn.setText(_translate("remove_face_btn", "Remove"))
        self.cancel_btn.setText(_translate("cancel_btn", "Cancel"))


class RemoveFaceDlg(QDialog):
    """Setup Add Face Dialog"""

    def __init__(self, parent=None):
        super().__init__(parent)
        # Create an instance of the GUI
        self.ui = RemoveFaceUI()
        # Run the .setupUi() method to show the GUI
        self.ui.setupUi(self)