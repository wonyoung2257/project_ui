# 찐 최종버전
import easygui
import cv2
import threading
import os
import sys
import numpy as np
import math
import re
import datetime
import json

from PyQt5 import QtCore, QtGui, QtWidgets

#############
number = 1
point_list = []
point_list_bool = False
mouse_mod = 0
count = 0

i = 0

location = [[], []]
perspect_map = None

point_temp = [[0, 0], [1024, 0]]
onepixel = 0

video_path = ""

img_original = None
img_result = None
img = None

rect_list = []
tracker = []
player_list = []

roi_i = 0
start_stop_check = 1

frame = 1
frame_check = 0

run_time = 0
start_check = 0
num = 255

slope_13 = None
slope_h2 = None
point_list_y_ratio = None

frame_num = 3
fps = 0
cap = None
out = cv2.VideoWriter()

tracker_x = 0
tracker_y = 0
tracker_w = 0
tracker_h = 0

mouse_callback_thead_mode = 0
click = False
stop_bool = False
####################

OPENCV_OBJECT_TRACKERS = {
    "csrt": cv2.TrackerCSRT_create,
    "kcf": cv2.TrackerKCF_create,
    "boosting": cv2.TrackerBoosting_create,
    "mil": cv2.TrackerMIL_create,
    "tld": cv2.TrackerTLD_create,
    "medianflow": cv2.TrackerMedianFlow_create,
    "mosse": cv2.TrackerMOSSE_create
}

player_create_count = 0  # 추적하고 있는 플레이어 수
# 플레이어 기록 키

# 플레이어 순서
player_ = [0, 0, 0, 0]


class Ui_Form(object):
    running = False

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setEnabled(True)
        Form.resize(769, 450)
        Form.setMinimumSize(QtCore.QSize(769, 450))
        Form.setMaximumSize(QtCore.QSize(769, 450))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./image/icon_test2.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        Form.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.openVideo_pushButton = QtWidgets.QPushButton(Form)
        self.openVideo_pushButton.setEnabled(True)
        self.openVideo_pushButton.setGeometry(QtCore.QRect(20, 20, 100, 40))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.openVideo_pushButton.setFont(font)
        self.openVideo_pushButton.setStyleSheet("#openVideo_pushButton{    \n"
                                                "    border-style: solid;\n"
                                                "    border-width: 2px;\n"
                                                "    border-color: rgb(72, 72, 72);\n"
                                                "    border-radius: 5px;\n"
                                                "}\n"
                                                "\n"
                                                "#openVideo_pushButton:pressed\n"
                                                "{    \n"
                                                "    background-color: rgb(179, 179, 179);\n"
                                                "    border-style: solid;\n"
                                                "    border-width: 0px;\n"
                                                "    border-color: rgb(72, 72, 72);\n"
                                                "    border-radius: 5px;\n"
                                                "}\n"
                                                "#openVideo_pushButton:Disabled\n"
                                                "{        \n"
                                                "    color: rgb(0, 0, 0);\n"
                                                "    background-color: rgb(172, 172, 172);\n"
                                                "    border-style: solid;\n"
                                                "    border-width: 0px;\n"
                                                "    border-color: rgb(72, 72, 72);\n"
                                                "    border-radius: 5px;\n"
                                                "}\n"
                                                "\n"
                                                "\n"
                                                "\n"
                                                "")
        self.openVideo_pushButton.setObjectName("openVideo_pushButton")
        self.trans_pushButton = QtWidgets.QPushButton(Form)
        self.trans_pushButton.setGeometry(QtCore.QRect(10, 320, 100, 40))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.trans_pushButton.setFont(font)
        self.trans_pushButton.setStyleSheet("#trans_pushButton{    \n"
                                            "    border-style: solid;\n"
                                            "    border-width: 2px;\n"
                                            "    border-color: rgb(72, 72, 72);\n"
                                            "    border-radius: 5px;\n"
                                            "}\n"
                                            "\n"
                                            "#trans_pushButton:pressed\n"
                                            "{    \n"
                                            "    background-color: rgb(179, 179, 179);\n"
                                            "    border-style: solid;\n"
                                            "    border-width: 0px;\n"
                                            "    border-color: rgb(72, 72, 72);\n"
                                            "    border-radius: 5px;\n"
                                            "}\n"
                                            "#trans_pushButton:Disabled\n"
                                            "{        \n"
                                            "    color: rgb(0, 0, 0);\n"
                                            "    background-color: rgb(172, 172, 172);\n"
                                            "    border-style: solid;\n"
                                            "    border-width: 0px;\n"
                                            "    border-color: rgb(72, 72, 72);\n"
                                            "    border-radius: 5px;\n"
                                            "}\n"
                                            "\n"
                                            "\n"
                                            "\n"
                                            "")
        self.trans_pushButton.setObjectName("trans_pushButton")
        self.addTracker_pushButton = QtWidgets.QPushButton(Form)
        self.addTracker_pushButton.setGeometry(QtCore.QRect(140, 320, 100, 40))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.addTracker_pushButton.setFont(font)
        self.addTracker_pushButton.setStyleSheet("#addTracker_pushButton{    \n"
                                                 "    border-style: solid;\n"
                                                 "    border-width: 2px;\n"
                                                 "    border-color: rgb(72, 72, 72);\n"
                                                 "    border-radius: 5px;\n"
                                                 "}\n"
                                                 "\n"
                                                 "#addTracker_pushButton:pressed\n"
                                                 "{    \n"
                                                 "    background-color: rgb(179, 179, 179);\n"
                                                 "    border-style: solid;\n"
                                                 "    border-width: 0px;\n"
                                                 "    border-color: rgb(72, 72, 72);\n"
                                                 "    border-radius: 5px;\n"
                                                 "}\n"
                                                 "#addTracker_pushButton:Disabled\n"
                                                 "{        \n"
                                                 "    color: rgb(0, 0, 0);\n"
                                                 "    background-color: rgb(172, 172, 172);\n"
                                                 "    border-style: solid;\n"
                                                 "    border-width: 0px;\n"
                                                 "    border-color: rgb(72, 72, 72);\n"
                                                 "    border-radius: 5px;\n"
                                                 "}\n"
                                                 "\n"
                                                 "\n"
                                                 "\n"
                                                 "")
        self.addTracker_pushButton.setObjectName("addTracker_pushButton")
        self.routeDraw_pushButton = QtWidgets.QPushButton(Form)
        self.routeDraw_pushButton.setGeometry(QtCore.QRect(270, 320, 100, 40))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.routeDraw_pushButton.setFont(font)
        self.routeDraw_pushButton.setStyleSheet("#routeDraw_pushButton{    \n"
                                                "    border-style: solid;\n"
                                                "    border-width: 2px;\n"
                                                "    border-color: rgb(72, 72, 72);\n"
                                                "    border-radius: 5px;\n"
                                                "}\n"
                                                "\n"
                                                "#routeDraw_pushButton:pressed\n"
                                                "{    \n"
                                                "    background-color: rgb(179, 179, 179);\n"
                                                "    border-style: solid;\n"
                                                "    border-width: 0px;\n"
                                                "    border-color: rgb(72, 72, 72);\n"
                                                "    border-radius: 5px;\n"
                                                "}\n"
                                                "#routeDraw_pushButton:Disabled\n"
                                                "{        \n"
                                                "    color: rgb(0, 0, 0);\n"
                                                "    background-color: rgb(172, 172, 172);\n"
                                                "    border-style: solid;\n"
                                                "    border-width: 0px;\n"
                                                "    border-color: rgb(72, 72, 72);\n"
                                                "    border-radius: 5px;\n"
                                                "}\n"
                                                "\n"
                                                "\n"
                                                "\n"
                                                "")
        self.routeDraw_pushButton.setObjectName("routeDraw_pushButton")
        self.routeCancel_pushButton = QtWidgets.QPushButton(Form)
        self.routeCancel_pushButton.setGeometry(QtCore.QRect(270, 380, 100, 40))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.routeCancel_pushButton.setFont(font)
        self.routeCancel_pushButton.setStyleSheet("#routeCancel_pushButton{    \n"
                                                  "    border-style: solid;\n"
                                                  "    border-width: 2px;\n"
                                                  "    border-color: rgb(72, 72, 72);\n"
                                                  "    border-radius: 5px;\n"
                                                  "}\n"
                                                  "\n"
                                                  "#routeCancel_pushButton:pressed\n"
                                                  "{    \n"
                                                  "    background-color: rgb(179, 179, 179);\n"
                                                  "    border-style: solid;\n"
                                                  "    border-width: 0px;\n"
                                                  "    border-color: rgb(72, 72, 72);\n"
                                                  "    border-radius: 5px;\n"
                                                  "}\n"
                                                  "#routeCancel_pushButton:Disabled\n"
                                                  "{        \n"
                                                  "    color: rgb(0, 0, 0);\n"
                                                  "    background-color: rgb(172, 172, 172);\n"
                                                  "    border-style: solid;\n"
                                                  "    border-width: 0px;\n"
                                                  "    border-color: rgb(72, 72, 72);\n"
                                                  "    border-radius: 5px;\n"
                                                  "}\n"
                                                  "\n"
                                                  "\n"
                                                  "\n"
                                                  "")
        self.routeCancel_pushButton.setObjectName("routeCancel_pushButton")
        self.start_pushButton = QtWidgets.QPushButton(Form)
        self.start_pushButton.setGeometry(QtCore.QRect(20, 90, 100, 40))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.start_pushButton.setFont(font)
        self.start_pushButton.setStyleSheet("QPushButton{image:url(image/play.png);}\n"
                                            "#start_pushButton{    \n"
                                            "    border-style: solid;\n"
                                            "    border-width: 2px;\n"
                                            "    border-color: rgb(72, 72, 72);\n"
                                            "    border-radius: 5px;\n"
                                            "}\n"
                                            "\n"
                                            "#start_pushButton:pressed\n"
                                            "{    \n"
                                            "    background-color: rgb(179, 179, 179);\n"
                                            "    border-style: solid;\n"
                                            "    border-width: 0px;\n"
                                            "    border-color: rgb(72, 72, 72);\n"
                                            "    border-radius: 5px;\n"
                                            "}\n"
                                            "#start_pushButton:Disabled\n"
                                            "{        \n"
                                            "    color: rgb(0, 0, 0);\n"
                                            "    background-color: rgb(172, 172, 172);\n"
                                            "    border-style: solid;\n"
                                            "    border-width: 0px;\n"
                                            "    border-color: rgb(72, 72, 72);\n"
                                            "    border-radius: 5px;\n"
                                            "}\n"
                                            "\n"
                                            "\n"
                                            "\n"
                                            "")
        self.start_pushButton.setObjectName("start_pushButton")
        self.closeVideo_pushButton = QtWidgets.QPushButton(Form)
        self.closeVideo_pushButton.setGeometry(QtCore.QRect(140, 20, 100, 40))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.closeVideo_pushButton.setFont(font)
        self.closeVideo_pushButton.setStyleSheet("#closeVideo_pushButton{    \n"
                                                 "    border-style: solid;\n"
                                                 "    border-width: 2px;\n"
                                                 "    border-color: rgb(72, 72, 72);\n"
                                                 "    border-radius: 5px;\n"
                                                 "}\n"
                                                 "\n"
                                                 "#closeVideo_pushButton:pressed\n"
                                                 "{    \n"
                                                 "    background-color: rgb(179, 179, 179);\n"
                                                 "    border-style: solid;\n"
                                                 "    border-width: 0px;\n"
                                                 "    border-color: rgb(72, 72, 72);\n"
                                                 "    border-radius: 5px;\n"
                                                 "}\n"
                                                 "#closeVideo_pushButton:Disabled\n"
                                                 "{        \n"
                                                 "    color: rgb(0, 0, 0);\n"
                                                 "    background-color: rgb(172, 172, 172);\n"
                                                 "    border-style: solid;\n"
                                                 "    border-width: 0px;\n"
                                                 "    border-color: rgb(72, 72, 72);\n"
                                                 "    border-radius: 5px;\n"
                                                 "}\n"
                                                 "\n"
                                                 "\n"
                                                 "\n"
                                                 "")
        self.closeVideo_pushButton.setObjectName("closeVideo_pushButton")
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(390, 230, 371, 41))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.positions_second_label = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("HY헤드라인M")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.positions_second_label.setFont(font)
        self.positions_second_label.setStyleSheet("border-style: solid;\n"
                                                  "border-width: 5px;\n"
                                                  "border-color: rgb(94, 167, 255);\n"
                                                  "border-radius: 3px;")
        self.positions_second_label.setAlignment(QtCore.Qt.AlignCenter)
        self.positions_second_label.setObjectName("positions_second_label")
        self.gridLayout.addWidget(self.positions_second_label, 0, 0, 1, 1)
        self.positions_third_label = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("HY헤드라인M")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.positions_third_label.setFont(font)
        self.positions_third_label.setStyleSheet("border-style: solid;\n"
                                                 "border-width: 5px;\n"
                                                 "border-color: #FA8072;\n"
                                                 "border-radius: 3px;")
        self.positions_third_label.setAlignment(QtCore.Qt.AlignCenter)
        self.positions_third_label.setObjectName("positions_third_label")
        self.gridLayout.addWidget(self.positions_third_label, 0, 1, 1, 1)
        self.layoutWidget1 = QtWidgets.QWidget(Form)
        self.layoutWidget1.setGeometry(QtCore.QRect(390, 270, 371, 171))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout_2.setContentsMargins(5, 0, 5, 0)
        self.gridLayout_2.setHorizontalSpacing(10)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.layoutWidget1)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_27 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.label_27.setFont(font)
        self.label_27.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_27.setObjectName("label_27")
        self.gridLayout_4.addWidget(self.label_27, 0, 0, 1, 1)
        self.label_24 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.label_24.setFont(font)
        self.label_24.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_24.setObjectName("label_24")
        self.gridLayout_4.addWidget(self.label_24, 1, 0, 1, 1)
        self.second_speed_label = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.second_speed_label.setFont(font)
        self.second_speed_label.setText("")
        self.second_speed_label.setAlignment(QtCore.Qt.AlignCenter)
        self.second_speed_label.setObjectName("second_speed_label")
        self.gridLayout_4.addWidget(self.second_speed_label, 1, 1, 1, 1)
        self.label_30 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.label_30.setFont(font)
        self.label_30.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_30.setObjectName("label_30")
        self.gridLayout_4.addWidget(self.label_30, 2, 0, 1, 1)
        self.second_maxspeed_label = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.second_maxspeed_label.setFont(font)
        self.second_maxspeed_label.setText("")
        self.second_maxspeed_label.setAlignment(QtCore.Qt.AlignCenter)
        self.second_maxspeed_label.setObjectName("second_maxspeed_label")
        self.gridLayout_4.addWidget(self.second_maxspeed_label, 2, 1, 1, 1)
        self.label_22 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.label_22.setFont(font)
        self.label_22.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_22.setObjectName("label_22")
        self.gridLayout_4.addWidget(self.label_22, 3, 0, 1, 1)
        self.second_lead_label = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.second_lead_label.setFont(font)
        self.second_lead_label.setText("")
        self.second_lead_label.setAlignment(QtCore.Qt.AlignCenter)
        self.second_lead_label.setObjectName("second_lead_label")
        self.gridLayout_4.addWidget(self.second_lead_label, 3, 1, 1, 1)
        self.second_distance_label = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.second_distance_label.setFont(font)
        self.second_distance_label.setText("")
        self.second_distance_label.setAlignment(QtCore.Qt.AlignCenter)
        self.second_distance_label.setObjectName("second_distance_label")
        self.gridLayout_4.addWidget(self.second_distance_label, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox1 = QtWidgets.QGroupBox(self.layoutWidget1)
        self.groupBox1.setObjectName("groupBox1")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox1)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_38 = QtWidgets.QLabel(self.groupBox1)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.label_38.setFont(font)
        self.label_38.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_38.setObjectName("label_38")
        self.gridLayout_5.addWidget(self.label_38, 1, 0, 1, 1)
        self.label_40 = QtWidgets.QLabel(self.groupBox1)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.label_40.setFont(font)
        self.label_40.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_40.setObjectName("label_40")
        self.gridLayout_5.addWidget(self.label_40, 0, 0, 1, 1)
        self.label_31 = QtWidgets.QLabel(self.groupBox1)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.label_31.setFont(font)
        self.label_31.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_31.setObjectName("label_31")
        self.gridLayout_5.addWidget(self.label_31, 2, 0, 1, 1)
        self.third_maxspeed_label = QtWidgets.QLabel(self.groupBox1)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.third_maxspeed_label.setFont(font)
        self.third_maxspeed_label.setText("")
        self.third_maxspeed_label.setAlignment(QtCore.Qt.AlignCenter)
        self.third_maxspeed_label.setObjectName("third_maxspeed_label")
        self.gridLayout_5.addWidget(self.third_maxspeed_label, 2, 1, 1, 1)
        self.third_distance_label = QtWidgets.QLabel(self.groupBox1)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.third_distance_label.setFont(font)
        self.third_distance_label.setText("")
        self.third_distance_label.setAlignment(QtCore.Qt.AlignCenter)
        self.third_distance_label.setObjectName("third_distance_label")
        self.gridLayout_5.addWidget(self.third_distance_label, 0, 1, 1, 1)
        self.label_33 = QtWidgets.QLabel(self.groupBox1)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.label_33.setFont(font)
        self.label_33.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_33.setObjectName("label_33")
        self.gridLayout_5.addWidget(self.label_33, 3, 0, 1, 1)
        self.third_lead_label = QtWidgets.QLabel(self.groupBox1)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.third_lead_label.setFont(font)
        self.third_lead_label.setText("")
        self.third_lead_label.setAlignment(QtCore.Qt.AlignCenter)
        self.third_lead_label.setObjectName("third_lead_label")
        self.gridLayout_5.addWidget(self.third_lead_label, 3, 1, 1, 1)
        self.third_speed_label = QtWidgets.QLabel(self.groupBox1)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.third_speed_label.setFont(font)
        self.third_speed_label.setText("")
        self.third_speed_label.setAlignment(QtCore.Qt.AlignCenter)
        self.third_speed_label.setObjectName("third_speed_label")
        self.gridLayout_5.addWidget(self.third_speed_label, 1, 1, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox1, 0, 1, 1, 1)
        self.videoTime_label = QtWidgets.QLabel(Form)
        self.videoTime_label.setGeometry(QtCore.QRect(20, 210, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.videoTime_label.setFont(font)
        self.videoTime_label.setAlignment(QtCore.Qt.AlignCenter)
        self.videoTime_label.setObjectName("videoTime_label")
        self.videoTime_lineEdit = QtWidgets.QLineEdit(Form)
        self.videoTime_lineEdit.setGeometry(QtCore.QRect(140, 210, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.videoTime_lineEdit.setFont(font)
        self.videoTime_lineEdit.setStyleSheet("#videoTime_lineEdit{    \n"
                                              "    border-style: solid;\n"
                                              "    border-width: 2px;\n"
                                              "    border-color: rgb(72, 72, 72);\n"
                                              "    border-radius: 5px;\n"
                                              "}")
        self.videoTime_lineEdit.setInputMethodHints(QtCore.Qt.ImhTime)
        self.videoTime_lineEdit.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.videoTime_lineEdit.setObjectName("videoTime_lineEdit")
        self.videoTimeMove_pushButton = QtWidgets.QPushButton(Form)
        self.videoTimeMove_pushButton.setGeometry(QtCore.QRect(240, 210, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.videoTimeMove_pushButton.setFont(font)
        self.videoTimeMove_pushButton.setStyleSheet("#videoTimeMove_pushButton{    \n"
                                                    "    border-style: solid;\n"
                                                    "    border-width: 2px;\n"
                                                    "    border-color: rgb(72, 72, 72);\n"
                                                    "    border-radius: 5px;\n"
                                                    "}\n"
                                                    "\n"
                                                    "#videoTimeMove_pushButton:pressed\n"
                                                    "{    \n"
                                                    "    background-color: rgb(179, 179, 179);\n"
                                                    "    border-style: solid;\n"
                                                    "    border-width: 0px;\n"
                                                    "    border-color: rgb(72, 72, 72);\n"
                                                    "    border-radius: 5px;\n"
                                                    "}\n"
                                                    "#start_pushButton:Disabled\n"
                                                    "{        \n"
                                                    "    color: rgb(0, 0, 0);\n"
                                                    "    background-color: rgb(172, 172, 172);\n"
                                                    "    border-style: solid;\n"
                                                    "    border-width: 0px;\n"
                                                    "    border-color: rgb(72, 72, 72);\n"
                                                    "    border-radius: 5px;\n"
                                                    "}\n"
                                                    "\n"
                                                    "\n"
                                                    "\n"
                                                    "")
        self.videoTimeMove_pushButton.setObjectName("videoTimeMove_pushButton")
        self.gridLayoutWidget = QtWidgets.QWidget(Form)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(390, 50, 371, 172))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_6.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.groupBox2 = QtWidgets.QGroupBox(self.gridLayoutWidget)
        self.groupBox2.setStyleSheet("")
        self.groupBox2.setObjectName("groupBox2")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox2)
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtWidgets.QLabel(self.groupBox2)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.hitter_distance_label = QtWidgets.QLabel(self.groupBox2)
        self.hitter_distance_label.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.hitter_distance_label.setFont(font)
        self.hitter_distance_label.setStyleSheet("selection-color: rgb(0, 255, 136);")
        self.hitter_distance_label.setText("")
        self.hitter_distance_label.setAlignment(QtCore.Qt.AlignCenter)
        self.hitter_distance_label.setObjectName("hitter_distance_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.hitter_distance_label)
        self.label_3 = QtWidgets.QLabel(self.groupBox2)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.hitter_speed_label = QtWidgets.QLabel(self.groupBox2)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.hitter_speed_label.setFont(font)
        self.hitter_speed_label.setStyleSheet("")
        self.hitter_speed_label.setText("")
        self.hitter_speed_label.setAlignment(QtCore.Qt.AlignCenter)
        self.hitter_speed_label.setObjectName("hitter_speed_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.hitter_speed_label)
        self.label_4 = QtWidgets.QLabel(self.groupBox2)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.hitter_maxspeed_label = QtWidgets.QLabel(self.groupBox2)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.hitter_maxspeed_label.setFont(font)
        self.hitter_maxspeed_label.setText("")
        self.hitter_maxspeed_label.setAlignment(QtCore.Qt.AlignCenter)
        self.hitter_maxspeed_label.setObjectName("hitter_maxspeed_label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.hitter_maxspeed_label)
        self.gridLayout_6.addWidget(self.groupBox2, 0, 0, 1, 1)
        self.groupBox3 = QtWidgets.QGroupBox(self.gridLayoutWidget)
        self.groupBox3.setObjectName("groupBox3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.first_lead_label = QtWidgets.QLabel(self.groupBox3)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.first_lead_label.setFont(font)
        self.first_lead_label.setText("")
        self.first_lead_label.setAlignment(QtCore.Qt.AlignCenter)
        self.first_lead_label.setObjectName("first_lead_label")
        self.gridLayout_3.addWidget(self.first_lead_label, 3, 1, 1, 1)
        self.first_speed_label = QtWidgets.QLabel(self.groupBox3)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.first_speed_label.setFont(font)
        self.first_speed_label.setText("")
        self.first_speed_label.setAlignment(QtCore.Qt.AlignCenter)
        self.first_speed_label.setObjectName("first_speed_label")
        self.gridLayout_3.addWidget(self.first_speed_label, 1, 1, 1, 1)
        self.first_distance_label = QtWidgets.QLabel(self.groupBox3)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.first_distance_label.setFont(font)
        self.first_distance_label.setText("")
        self.first_distance_label.setAlignment(QtCore.Qt.AlignCenter)
        self.first_distance_label.setObjectName("first_distance_label")
        self.gridLayout_3.addWidget(self.first_distance_label, 0, 1, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.groupBox3)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_12.setObjectName("label_12")
        self.gridLayout_3.addWidget(self.label_12, 1, 0, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.groupBox3)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.label_17.setFont(font)
        self.label_17.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_17.setObjectName("label_17")
        self.gridLayout_3.addWidget(self.label_17, 0, 0, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.groupBox3)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.label_15.setFont(font)
        self.label_15.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_15.setObjectName("label_15")
        self.gridLayout_3.addWidget(self.label_15, 2, 0, 1, 1)
        self.first_maxspeed_label = QtWidgets.QLabel(self.groupBox3)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.first_maxspeed_label.setFont(font)
        self.first_maxspeed_label.setText("")
        self.first_maxspeed_label.setAlignment(QtCore.Qt.AlignCenter)
        self.first_maxspeed_label.setObjectName("first_maxspeed_label")
        self.gridLayout_3.addWidget(self.first_maxspeed_label, 2, 1, 1, 1)
        self.label_1 = QtWidgets.QLabel(self.groupBox3)
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(11)
        self.label_1.setFont(font)
        self.label_1.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_1.setObjectName("label_1")
        self.gridLayout_3.addWidget(self.label_1, 3, 0, 1, 1)
        self.gridLayout_6.addWidget(self.groupBox3, 0, 1, 1, 1)
        self.gridLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(390, 10, 371, 41))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.positions_hitter_label = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.positions_hitter_label.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("HY헤드라인M")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.positions_hitter_label.setFont(font)
        self.positions_hitter_label.setStyleSheet("color: rgb(0, 0, 0);\n"
                                                  "border-style: solid;\n"
                                                  "border-width: 5px;\n"
                                                  "border-color: rgb(255, 242, 99);\n"
                                                  "border-radius: 3px;")
        self.positions_hitter_label.setAlignment(QtCore.Qt.AlignCenter)
        self.positions_hitter_label.setObjectName("positions_hitter_label")
        self.gridLayout_7.addWidget(self.positions_hitter_label, 0, 0, 1, 1)
        self.positions_first_label = QtWidgets.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("HY헤드라인M")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.positions_first_label.setFont(font)
        self.positions_first_label.setStyleSheet("border-style: solid;\n"
                                                 "border-width: 5px;\n"
                                                 "border-color: rgb(117, 255, 110);\n"
                                                 "border-radius: 3px;")
        self.positions_first_label.setAlignment(QtCore.Qt.AlignCenter)
        self.positions_first_label.setObjectName("positions_first_label")
        self.gridLayout_7.addWidget(self.positions_first_label, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, 290, 81, 21))
        font = QtGui.QFont()
        font.setFamily("HY헤드라인M")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.label.setFont(font)
        self.label.setStyleSheet("")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(150, 290, 81, 21))
        font = QtGui.QFont()
        font.setFamily("HY헤드라인M")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(270, 290, 91, 20))
        font = QtGui.QFont()
        font.setFamily("HY헤드라인M")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(20, 180, 81, 21))
        font = QtGui.QFont()
        font.setFamily("HY헤드라인M")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("")
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(130, 180, 111, 21))
        font = QtGui.QFont()
        font.setFamily("HY헤드라인M")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("")
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(-20, 160, 401, 2))
        self.lineEdit.setTabletTracking(False)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(-20, 280, 401, 2))
        self.lineEdit_2.setTabletTracking(False)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(Form)
        self.lineEdit_3.setGeometry(QtCore.QRect(380, -10, 2, 500))
        self.lineEdit_3.setTabletTracking(False)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_2.raise_()
        self.lineEdit.raise_()
        self.openVideo_pushButton.raise_()
        self.trans_pushButton.raise_()
        self.addTracker_pushButton.raise_()
        self.routeDraw_pushButton.raise_()
        self.routeCancel_pushButton.raise_()
        self.start_pushButton.raise_()
        self.closeVideo_pushButton.raise_()
        self.layoutWidget.raise_()
        self.layoutWidget.raise_()
        self.videoTime_label.raise_()
        self.videoTime_lineEdit.raise_()
        self.videoTimeMove_pushButton.raise_()
        self.gridLayoutWidget.raise_()
        self.gridLayoutWidget_2.raise_()
        self.label.raise_()
        self.label_5.raise_()
        self.label_6.raise_()
        self.label_7.raise_()
        self.label_8.raise_()
        self.lineEdit_3.raise_()

        # 버튼 이벤트 처리 부분
        self.openVideo_pushButton.clicked.connect(self.openVideo)
        self.trans_pushButton.clicked.connect(self.transform)
        self.start_pushButton.clicked.connect(self.start_stop)

        self.addTracker_pushButton.clicked.connect(self.player_Roi)
        self.routeDraw_pushButton.clicked.connect(self.player_Draw)
        self.routeCancel_pushButton.clicked.connect(self.player_Cancel)
        self.videoTimeMove_pushButton.clicked.connect(self.setVideoTime)
        self.player_Roi_bool = [False, False, False, False]  # 선수의 박스를 그렸는지 판단
        self.player_Roi_draw = False
        self.player_Draw_bool = False
        self.player_Cancel_bool = False
        self.save_video_bool = False
        self.draw_ing = False

        self.closeVideo_pushButton.clicked.connect(self.closeVideo)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        ui.closeVideo_pushButton.setDisabled(True)
        ui.trans_pushButton.setDisabled(True)
        ui.addTracker_pushButton.setDisabled(True)
        ui.routeDraw_pushButton.setDisabled(True)
        ui.routeCancel_pushButton.setDisabled(True)
        ui.start_pushButton.setDisabled(True)
        ui.videoTimeMove_pushButton.setDisabled(True)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "야구 트랙킹 프로그램"))
        self.openVideo_pushButton.setText(_translate("Form", "영상 열기"))
        self.trans_pushButton.setText(_translate("Form", "변환"))
        self.addTracker_pushButton.setText(_translate("Form", "객체 선택"))
        self.routeDraw_pushButton.setText(_translate("Form", "추적 시작"))
        self.routeCancel_pushButton.setText(_translate("Form", "추적 종료"))
        self.closeVideo_pushButton.setText(_translate("Form", "영상 닫기"))
        self.positions_hitter_label.setText(_translate("Form", "타자"))
        self.positions_first_label.setText(_translate("Form", "1루 주자"))
        self.positions_second_label.setText(_translate("Form", "2루 주자"))
        self.positions_third_label.setText(_translate("Form", "3루 주자"))
        self.label_27.setText(_translate("Form", "이동거리"))
        self.label_24.setText(_translate("Form", "순간속도"))
        self.label_30.setText(_translate("Form", "최고속도"))
        self.label_22.setText(_translate("Form", "리드거리"))
        self.label_38.setText(_translate("Form", "순간속도"))
        self.label_40.setText(_translate("Form", "이동거리"))
        self.label_31.setText(_translate("Form", "최고속도"))
        self.label_33.setText(_translate("Form", "리드거리"))
        self.videoTime_label.setText(_translate("Form", "0:00:00"))
        self.videoTime_lineEdit.setText(_translate("Form", "0:00:00"))
        self.videoTimeMove_pushButton.setText(_translate("Form", "이동"))
        self.label_2.setText(_translate("Form", "이동거리"))
        self.label_3.setText(_translate("Form", "순간속도"))
        self.label_4.setText(_translate("Form", "최고속도"))
        self.label_12.setText(_translate("Form", "순간속도"))
        self.label_17.setText(_translate("Form", "이동거리"))
        self.label_15.setText(_translate("Form", "최고속도"))
        self.label_1.setText(_translate("Form", "리드거리"))
        self.positions_hitter_label.setText(_translate("Form", "타자"))
        self.positions_first_label.setText(_translate("Form", "1루 주자"))
        self.label.setText(_translate("Form", "- STEP 1 -"))
        self.label_5.setText(_translate("Form", "- STEP 2 -"))
        self.label_6.setText(_translate("Form", "- STEP 3 -"))
        self.label_7.setText(_translate("Form", "- 영상 총 시간 -"))
        self.label_8.setText(_translate("Form", "이동 시간 입력"))

    def openVideo(self):
        global video_path, labelm, img, img_original, fps, cap, out
        video_path = easygui.fileopenbox()
        cap = cv2.VideoCapture(video_path)


        fps = cap.get(cv2.CAP_PROP_FPS)

        if not cap.isOpened():
            print("영상 파일이 실행되지 않았습니다.")

        createFolder('perspect_map')
        createFolder("result")
        createFolder("result/%s_result"%video_path.split('.')[0].split('\\')[-1])
        createFolder("result/%s_result"%video_path.split('.')[0].split('\\')[-1]+ "/video")
        createFolder("result/%s_result" % video_path.split('.')[0].split('\\')[-1] + "/player")

        ret, img = cap.read()

        img_original = img
        # 영상 열기후 영상열기 비활, 영상 닫기, 변환, 재생, 이동 활성
        ui.openVideo_pushButton.setDisabled(True)
        ui.closeVideo_pushButton.setEnabled(True)
        ui.trans_pushButton.setEnabled(True)
        ui.start_pushButton.setEnabled(True)
        ui.videoTimeMove_pushButton.setEnabled(True)

        video_end_time = cap.get(cv2.CAP_PROP_FRAME_COUNT)/cap.get(cv2.CAP_PROP_FPS)

        self.videoTime_label.setText(str((datetime.timedelta(seconds=math.trunc(video_end_time)))))

        perspect_map_check()

        cv2.namedWindow('original')
        cv2.imshow("original", img)

    def transform(self):
        global mouse_mod
        if self.trans_pushButton.text() == "변환":
            cv2.setMouseCallback('original', mouse_callback)
        elif self.trans_pushButton.text() =="재 변환":
            mouse_mod = 0
            point_list_bool
            del point_list[0:4]  # 원래 포인트 리스트 삭제
            cv2.setMouseCallback('original', mouse_callback)

    def run(self):
        global running, img, frame, count, player_, player_create_count, frame_check, start_check, roi_i, out, fps, stop_bool

        while running:

            ret, img = cap.read()

            # self.videoTime_lineEdit.setText(_translate("Form", "0:00:00"))
            now_viedo_time = cap.get(cv2.CAP_PROP_POS_MSEC)*0.001
            self.videoTime_lineEdit.setText(str((datetime.timedelta(seconds=math.trunc(now_viedo_time)))))


            while stop_bool:
                if self.player_Roi_bool[0] == True:
                    ui.videoTimeMove_pushButton.setDisabled(True)

            if self.player_Roi_draw:
                global roi_i
                player_create()

                self.player_Roi_bool[roi_i] = True
                self.player_Roi_draw = False
                ui.routeDraw_pushButton.setEnabled(True)

                roi_i += 1


            if self.player_Draw_bool:

                for j in range(0, player_create_count):
                    player_list[j].start_time = round(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000, 2)
                frame_check = frame
                start_check = 1
                self.player_Draw_bool = False

            if self.player_Cancel_bool:
                frame_check = 0
                start_check = 0

                record_num = load_files_number("result/%s_result" % video_path.split('.')[0].split('\\')[-1] + "/player")
                for j in range(0, player_create_count):
                    save_record(player_list[0].player_position, player_list[0].player_distance, player_list[0].avg_speed,
                                player_list[0].max_speed, player_list[0].lead_distance, player_list[0].pointList, player_list[0].route_pointList, record_num)
                    player_delete(0)
                    self.player_Roi_bool[j] = False

                self.player_Cancel_bool = False

                player_create_count = 0

                roi_i = 0

            if self.player_Roi_bool[0]:
                player_tracking(1, frame_check, start_check)
            if self.player_Roi_bool[1]:
                player_tracking(2, frame_check, start_check)
            if self.player_Roi_bool[2]:
                player_tracking(3, frame_check, start_check)
            if self.player_Roi_bool[3]:
                player_tracking(4, frame_check, start_check)

            frame += 1
            count += 1

            if ret:
                if fps <= 30:
                    cv2.waitKey(int(fps))
                else:
                    cv2.waitKey(1)

            else:  # 마지막 프레임이 들어가도 걸리게 된다. 캠 화면을 들어오게 만들어서 계속진행되게 만들어짐
                # QtWidgets.QMessageBox.about(win, "Error", "Cannot read frame.")
                print("cannot read frame.")
                self.closeVideo()
                break

            if self.save_video_bool:
                out.write(img)
            else:
                out.release()

            cv2.imshow('original', img)

        cap.release()
        out.release()
        print("Thread end.")

    def start_stop(self):
        global running, start_stop_check, stop_bool

        if start_stop_check != 1:
            if stop_bool:
                stop_bool = False
                print("started..")
                self.start_pushButton.setStyleSheet("QPushButton{image:url(image/stop.png);}\n"
                                                    "#start_pushButton{    \n"
                                                    "    border-style: solid;\n"
                                                    "    border-width: 2px;\n"
                                                    "    border-color: rgb(72, 72, 72);\n"
                                                    "    border-radius: 5px;\n"
                                                    "}\n"
                                                    "\n"
                                                    "#start_pushButton:pressed\n"
                                                    "{    \n"
                                                    "    background-color: rgb(179, 179, 179);\n"
                                                    "    border-style: solid;\n"
                                                    "    border-width: 0px;\n"
                                                    "    border-color: rgb(72, 72, 72);\n"
                                                    "    border-radius: 5px;\n"
                                                    "}\n"
                                                    "#start_pushButton:Disabled\n"
                                                    "{        \n"
                                                    "    color: rgb(0, 0, 0);\n"
                                                    "    background-color: rgb(172, 172, 172);\n"
                                                    "    border-style: solid;\n"
                                                    "    border-width: 0px;\n"
                                                    "    border-color: rgb(72, 72, 72);\n"
                                                    "    border-radius: 5px;\n"
                                                    "}\n"
                                                    ""
                                                    )
                ui.closeVideo_pushButton.setDisabled(True)
                ui.videoTimeMove_pushButton.setDisabled(True)
                ui.trans_pushButton.setEnabled(False)
                if not point_list:  # 재 시작시 변환 좌표가 없으면 객체 선택버튼 비활성화
                    ui.addTracker_pushButton.setEnabled(False)
                else:
                    ui.addTracker_pushButton.setEnabled(True)
                if self.draw_ing == True:
                    ui.addTracker_pushButton.setEnabled(False)
                else:
                    ui.addTracker_pushButton.setEnabled(True)

                return 0

            stop_bool = True
            print("stoped..")

            self.start_pushButton.setStyleSheet("QPushButton{image:url(image/play.png);}\n"
                                                "#start_pushButton{    \n"
                                                "    border-style: solid;\n"
                                                "    border-width: 2px;\n"
                                                "    border-color: rgb(72, 72, 72);\n"
                                                "    border-radius: 5px;\n"
                                                "}\n"
                                                "\n"
                                                "#start_pushButton:pressed\n"
                                                "{    \n"
                                                "    background-color: rgb(179, 179, 179);\n"
                                                "    border-style: solid;\n"
                                                "    border-width: 0px;\n"
                                                "    border-color: rgb(72, 72, 72);\n"
                                                "    border-radius: 5px;\n"
                                                "}\n"
                                                "#start_pushButton:Disabled\n"
                                                "{        \n"
                                                "    color: rgb(0, 0, 0);\n"
                                                "    background-color: rgb(172, 172, 172);\n"
                                                "    border-style: solid;\n"
                                                "    border-width: 0px;\n"
                                                "    border-color: rgb(72, 72, 72);\n"
                                                "    border-radius: 5px;\n"
                                                "}\n"
                                                ""
                                                )
            if player_create_count > 0 :
                ui.closeVideo_pushButton.setEnabled(False)
                ui.trans_pushButton.setEnabled(False)
            else:
                ui.closeVideo_pushButton.setEnabled(True)
                ui.trans_pushButton.setEnabled(True)


            ui.videoTimeMove_pushButton.setEnabled(True)

            if self.draw_ing == True:
                ui.closeVideo_pushButton.setDisabled(True)
        # if not point_list:
            ui.addTracker_pushButton.setEnabled(False)
        # else:
        #     ui.addTracker_pushButton.setEnabled(True)



        # 최초 재생하여 쓰레드 만드는 부분
        if start_stop_check == 1:
            ui.trans_pushButton.setEnabled(False)
            ui.videoTimeMove_pushButton.setDisabled(True)
            running = True
            th = threading.Thread(target=self.run)
            th.start()
            print("started..")
            self.start_pushButton.setStyleSheet("QPushButton{image:url(image/stop.png);}\n"
                                                "#start_pushButton{    \n"
                                                "    border-style: solid;\n"
                                                "    border-width: 2px;\n"
                                                "    border-color: rgb(72, 72, 72);\n"
                                                "    border-radius: 5px;\n"
                                                "}\n"
                                                "\n"
                                                "#start_pushButton:pressed\n"
                                                "{    \n"
                                                "    background-color: rgb(179, 179, 179);\n"
                                                "    border-style: solid;\n"
                                                "    border-width: 0px;\n"
                                                "    border-color: rgb(72, 72, 72);\n"
                                                "    border-radius: 5px;\n"
                                                "}\n"
                                                "#start_pushButton:Disabled\n"
                                                "{        \n"
                                                "    color: rgb(0, 0, 0);\n"
                                                "    background-color: rgb(172, 172, 172);\n"
                                                "    border-style: solid;\n"
                                                "    border-width: 0px;\n"
                                                "    border-color: rgb(72, 72, 72);\n"
                                                "    border-radius: 5px;\n"
                                                "}\n"
                                                ""
                                                )
            ui.closeVideo_pushButton.setDisabled(True)
            # 변환되면 활성화
            if not point_list: # 최초 시작시 변환 좌표가 없으면 객체 선택버튼 비황
                ui.addTracker_pushButton.setEnabled(False)
            else:
                ui.addTracker_pushButton.setEnabled(True)

            start_stop_check += 1

    def player_Roi(self):
        self.player_Roi_draw = True
        ui.videoTimeMove_pushButton.setDisabled(True)
        ui.addTracker_pushButton.setEnabled(True)
        ui.start_pushButton.setDisabled(True)
        ui.routeDraw_pushButton.setDisabled(True)

    def player_Draw(self):
        save_video()
        self.save_video_bool = True
        self.player_Draw_bool = True
        self.draw_ing = True
        ui.closeVideo_pushButton.setDisabled(True)
        ui.addTracker_pushButton.setDisabled(True)
        ui.routeDraw_pushButton.setDisabled(True)
        ui.routeCancel_pushButton.setEnabled(True)

    def player_Cancel(self):
        self.save_video_bool = False
        self.player_Cancel_bool = True
        self.draw_ing = False
        ui.videoTimeMove_pushButton.setEnabled(True)
        if stop_bool == True:
            ui.closeVideo_pushButton.setEnabled(True)
        else:
            ui.videoTimeMove_pushButton.setDisabled(True)
        ui.addTracker_pushButton.setEnabled(True)
        ui.routeCancel_pushButton.setDisabled(True)

    def closeVideo(self):
        global running, start_stop_check, img, stop_bool, point_list, mouse_mod, point_list_bool
        point_list_bool = False
        stop_bool = False
        self.player_Roi_draw = False
        self.save_video_bool = False

        running = False
        start_stop_check = 1
        img = None
        del point_list[0:4]


        mouse_mod = 0

        cv2.destroyAllWindows()

        set_text(1, 0, 0, 0, 0)
        set_text(2, 0, 0, 0, 0)
        set_text(3, 0, 0, 0, 0)
        set_text(0, 0, 0, 0, 0)

        ui.trans_pushButton.setText("변환")
        ui.trans_pushButton.setEnabled(False)
        ui.openVideo_pushButton.setEnabled(True)
        ui.closeVideo_pushButton.setDisabled(True)
        ui.start_pushButton.setDisabled(True)
        ui.addTracker_pushButton.setDisabled(True)

    def setVideoTime(self):
        global cap, img
        second = 0
        second += int(self.videoTime_lineEdit.text()[0])*3600
        second += int(self.videoTime_lineEdit.text()[2])*600
        second += int(self.videoTime_lineEdit.text()[3])*60
        second += int(self.videoTime_lineEdit.text()[5])*10
        second += int(self.videoTime_lineEdit.text()[6])

        cap.set(cv2.CAP_PROP_POS_FRAMES, cap.get(cv2.CAP_PROP_FPS)*second)
        ret, img = cap.read()
        cv2.namedWindow('original')
        cv2.imshow("original", img)


def save_video():
    global out
    video_num = load_files_number("result/%s_result" % video_path.split('.')[0].split('\\')[-1] + "/video")
    video_name = "result/%s_result" % video_path.split('.')[0].split('\\')[-1] + "/video/video_" + str(video_num) + ".mp4"
    output_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))  # (width, height)
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    out = cv2.VideoWriter(video_name, fourcc, cap.get(cv2.CAP_PROP_FPS), output_size)


def save_record(player_position, player_distance, avg_speed, max_speed, lead_distance, pointList, route_pointList, record_num):
    # record_num = load_files_number("result/%s_result" % video_path.split('.')[0].split('\\')[-1] + "/player")
    player_data = {
        "1.Player_position": player_position,
        "2.Distance": player_distance,
        "3.Average_Speed": avg_speed,
        "4.Max_Speed": max_speed,
        "5.Lead_distance": lead_distance,
        "6.Point_Speed": [{"Point": pointList[0], "Speed": 0}]
    }

    for i in range(1, len(pointList)):
        player_data['6.Point_Speed'].append(
            {
                "Point": pointList[i], "Speed": route_pointList[i - 1]
            }
        )

    record_name = "result/%s_result" % video_path.split('.')[0].split('\\')[-1] + "/player/record_" + str(record_num) + ".json"
    with open(record_name, "w") as json_file:
	# with open(player_data, 'r', encoding="utf-8") as json_file:
	# json_data = json.load(json_file)
	# {"#": n, " ": , "": }
        json.dump(player_data, json_file, indent=4)

    if os.path.isfile(record_name):
        file_open = open(record_name, 'a') # 있으면 덮어쓰기
    else:
        file_open = open(record_name, 'w') # 없으면 만들기

    # file_open.write("■ 선수 포지션\n")
    # if player_position == 0:  # 3루
    #     file_open.write(" : 3루주자\n")
    #     file_open.write("■ 리드거리\n")
    #     file_open.write(" : %s M\n" % lead_distance)
    # if player_position == 1:  # 2루
    #     file_open.write(" : 2루주자\n")
    #     file_open.write("■ 리드거리\n")
    #     file_open.write(" : %s M\n" % lead_distance)
    # if player_position == 2:  # 1루
    #     file_open.write(" : 1루주자\n")
    #     file_open.write("■ 리드거리\n")
    #     file_open.write(" : %s M\n" % lead_distance)
    # if player_position == 3:  # 타자
    #     file_open.write(" : 타자\n")
    #
    # file_open.write("■ 이동 거리\n")
    # file_open.write(" : %s M\n" %player_distance)
    # file_open.write("■ 최고 속도\n")
    # file_open.write(" : %s km/h\n" %max_speed)
    #
    # file_open.write("■ 선수 경로 좌표\n")
    # file_open.write(str(pointList) + "\n")
    # file_open.write("----------------------------------\n")
    # file_open.closed


def load_files_number(folderName):
    # print(folderName)
    numbers = []
    for i in os.listdir(folderName):
        str1 = i.split(".")[0]

        num = (re.findall("\d+", str1))
        numbers.append(int(num[0]))
        # print("number: ", numbers)
    if not numbers:
        return 0
    else:
        return max(numbers)+1

def mouse_callback(event, x, y, flags, param):
    global point_list, mouse_mod

    # 마우스 왼쪽 버튼 누를 때마다 좌표를 리스트에 저장
    if len(point_list) < 4:
        if event == cv2.EVENT_LBUTTONDOWN:
            point_list.append((x, y))
            print(point_list)
            cv2.circle(img, (x, y), 3, (0, 0, 255), -1)
            cv2.imshow("original", img)
            print(len(point_list))

    if len(point_list) == 4 and mouse_mod == 0 and ui.trans_pushButton.text() == "재 변환":
        calculator_point_list_y_ratio()
        mouse_mod += 1

    elif len(point_list) == 4 and mouse_mod == 0 :
        print("재변환 아님")
        calculator_point_list_y_ratio()
        mouse_mod += 1



def calculator_point_list_y_ratio():
    global slope_13, slope_h2, point_list_y_ratio, img_result, perspect_map, onepixel

    pts1 = np.float32([list(point_list[0]), list(point_list[1]), list(point_list[2]), list(point_list[3])])
    # 목적 좌표
    pts2 = np.float32([[0, 0], [1024, 0], [1024, 1024], [0, 1024]])

    if not point_list_bool:
        save_pointList()
    elif ui.trans_pushButton.text() == "재 변환":
        resave_poiintList(perspect_map_check())

    # 원근 변환 행렬
    perspect_map = cv2.getPerspectiveTransform(pts1, pts2)

    img_result = cv2.warpPerspective(img_original, perspect_map, (1024, 1024))

    arg_length = math.sqrt(pow(point_temp[0][0] - point_temp[1][0], 2) + pow(point_temp[0][1] - point_temp[1][1], 2))
    # real_length = float(input("거리를 입력하세요: "))
    real_length = 27.432

    onepixel = real_length / arg_length

    # 홈과 2루 비율
    slope_13 = (point_list[0][1] - point_list[2][1]) / (point_list[0][0] - point_list[2][0])
    constant_13 = point_list[0][1] - slope_13 * point_list[0][0]
    slope_h2 = (point_list[1][1] - point_list[3][1]) / (point_list[1][0] - point_list[3][0])
    constant_h2 = point_list[1][1] - slope_h2 * point_list[1][0]
    constant_ip = (constant_h2 - constant_13) / (slope_13 - slope_h2)
    intersect_point = [int(constant_ip), int(slope_13 * constant_ip + constant_13)]

    point_list_y_ratio = math.sqrt((pow(intersect_point[0] - point_list[3][0], 2)) + (pow(intersect_point[1] - point_list[3][1], 2))) / \
                         math.sqrt((pow(intersect_point[0] - point_list[1][0], 2)) + (pow(intersect_point[1] - point_list[1][1], 2)))

    # ui.trans_pushButton.setDisabled(True)  # 버튼 비활성화


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("만들기 에러" + directory)


def save_pointList() : # 베이스 좌표 저장하는 함수
    global point_list_bool
    point_list_bool = True
    fileNum = 0

    for i in os.listdir('perspect_map'):
        str1 = i.split(".")[0]
        fileNum = int(str1)  # perspect_map안에 저장된 파일의 목록을 가져옴
        print("파일이름:",fileNum)
    fileNum += 1

    fileName = open('perspect_map/' + str(fileNum) + ".txt", 'w')
    fileName.write(video_path + "\n")
    fileName.write(str(point_list))

    print("변환 좌표가 저장되었습니다.")
    ui.trans_pushButton.setText("재 변환")
    ui.trans_pushButton.setEnabled(True)  # 버튼 활성화

    fileName.close()

def resave_poiintList(fileName):
    str1 = fileName.split(".")[0]

    fileNum = int(str1)

    fileName = open('perspect_map/' + str(fileNum) + ".txt", 'w+')
    fileName.write(video_path + "\n")
    fileName.write(str(point_list))

    print("재 변환 좌표가 저장되었습니다.")
    fileName.close()


def perspect_map_check():
    global point_list, point_list_bool

    if ui.trans_pushButton.text() == "재 변환":
        for name in os.listdir('perspect_map'):
            file = open('perspect_map\\' + name, 'r')
            file_str = file.readline()
            remove_str = file_str.rstrip('\n')

            if remove_str == video_path:
                return name
    else:
        for name in os.listdir('perspect_map'):
            file = open('perspect_map\\' + name, 'r')
            file_str = file.readline()
            remove_str = file_str.rstrip('\n')

            if remove_str == video_path:  # 변환 좌표가 있을 때
                file_str = file.readline()  # 두번째 줄 읽어와 저장

                change_list(file_str)

                point_list_bool = True
                calculator_point_list_y_ratio()

                ui.trans_pushButton.setText("재 변환")
                ui.trans_pushButton.setEnabled(True)  # 버튼 활성화

                file.close()
                break
            else:
                print("변환좌표 없음")


def change_list(file_str):
    global point_list

    str_replace = file_str.replace('[', "").replace(']', "").replace('(', "").replace(')', "")
    str_split = str_replace.split(', ')

    num = 0
    for i in range(0, int(len(str_split) / 2)):
        tmep = []
        tmep.append(int(str_split[num]))
        tmep.append(int(str_split[num + 1]))
        point_list.append(tmep)
        num += 2


def perstpective(perspect_map, pointList, onepixel):  # 이동경로 변환하는 함수
    trans_list = list()
    trans_point = np.ones((1, 3))
    num = 0
    for temp_list in pointList:
        for i in perspect_map[0:3]:  # x                      y
            trans_point[0][num] = (i[0] * temp_list[0]) + (i[1] * temp_list[1]) + i[2]
            num += 1
        trans_point /= trans_point[0][2]  # z값 나누기
        num = 0
        trans_list.append(trans_point[0:2])
        trans_point = np.ones((1, 3))

    temp = []
    trans_length = 0.0
    for temp_list2 in trans_list:
        if len(temp):
            trans_length += (math.sqrt(pow(temp[0][0] - temp_list2[0][0], 2) + pow(temp[0][1] - temp_list2[0][1], 2)))
        temp = temp_list2

    return trans_length * onepixel


def player_create():
    global player_create_count
    # global player_create_count, tracker_x, tracker_y, tracker_w, tracker_h
    # 선수의 수만큼 tracker와 추적 ROI를 만듬
    tracker.append(OPENCV_OBJECT_TRACKERS['csrt']())
    cv2.destroyWindow('original')
    box = cv2.selectROI('original', img, False)
    rect_list.append(box)
    # rect_list.append(cv2.selectROI('original', img, fromCenter=False, showCrosshair=True))

    tracker[player_create_count].init(img, rect_list[player_create_count])

    player_list.append(Player())
    player_list[player_create_count].box(box)
    player_list[player_create_count].mean_avg_list_init()

    player_create_count += 1

    ui.start_pushButton.setEnabled(True)
    ui.routeDraw_pushButton.setEnabled(True)


def player_tracking(player_order, frame_key, start):
    success, box = tracker[player_order - 1].update(img)
    # success_list.append(success)
    # box_list.append(box)
    player_list[player_order - 1].box(box)

    if frame_key + 1 == frame:
        player_list[player_order - 1].fir_top = player_list[player_order - 1].top
    player_list[player_order - 1].constant(slope_13, slope_h2, point_list_y_ratio)
    player_list[player_order - 1].positional_correction()

    if count % frame_num == 0:
        player_list[player_order - 1].mean_avg(start)
        player_list[player_order - 1].route_color(frame, frame_key, perspect_map, onepixel)
        player_list[player_order - 1].calculation_between_base()

    player_list[player_order - 1].draw_route()

    rect_list[player_order - 1] = player_list[player_order - 1].draw_box(player_list[player_order - 1].player_position)
    cv2.line(img, (player_list[player_order - 1].adj_center_x, player_list[player_order - 1].adj_center_y),
             (player_list[player_order - 1].adj_center_x, player_list[player_order - 1].adj_center_y), (255, 0, 255), 3)

    player_list[player_order - 1].player_data_box()


def player_delete(player_create_count):
    del tracker[player_create_count]
    del rect_list[player_create_count]
    del player_list[player_create_count]


def set_text(player_position, distance, speed, maxspeed, lead=0):
    if player_position == 0: # 3루
        ui.third_distance_label.setText(str(distance) + " M")
        ui.third_speed_label.setText(str(speed) + " km/h")
        ui.third_maxspeed_label.setText(str(maxspeed) + " km/h")
        ui.third_lead_label.setText(str(lead) + " M")

    if player_position == 1: # 2루
        ui.second_distance_label.setText(str(distance) + " M")
        ui.second_speed_label.setText(str(speed) + " km/h")
        ui.second_maxspeed_label.setText(str(maxspeed) + " km/h")
        ui.second_lead_label.setText(str(lead) + " M")

    if player_position == 2: # 1루

        ui.first_distance_label.setText(str(distance) + " M")
        ui.first_speed_label.setText(str(speed) + " km/h")
        ui.first_maxspeed_label.setText(str(maxspeed) + " km/h")
        ui.first_lead_label.setText(str(lead) + " M")

    if player_position == 3: # 홈
        ui.hitter_distance_label.setText(str(distance) + " M")
        ui.hitter_speed_label.setText(str(speed) + " km/h")
        ui.hitter_maxspeed_label.setText(str(maxspeed) + " km/h")


class Player():
    def __init__(self):
        self.fir_top = 0
        self.cur_time = 0  # 현재시간
        self.pre_time = 0
        self.start_time = 0  # 각 선수의 출발 시간 현재 개발 과정에서는 run_time 전역 변수로 통일되어 있음
        self.pre_top = 0
        self.right = 0
        self.bottom = 0
        self.center_x = 0
        self.left = 0
        self.top = 0
        self.w = 0
        self.h = 0
        self.f_t_h_cal = 0
        self.t_p_h_cal = 0
        self.adj_center_x = 0
        self.adj_center_y = 0
        self.route_pers_distance = 0
        self.pre_route_pers_distance = 0
        self.nowPoint = [0, 0]
        self.point_sum = [0, 0]
        self.point_mean = [0, 0]
        self.pointList = []
        self.route_pointList = []
        self.mean_avg_list = []
        self.line_count = 1

        self.length = 0.0
        self.pix_num_move = 0.0
        self.pre_route_pointList_index = 0

        self.player_distance = 0
        self.now_speed = 0
        self.max_speed = 0
        self.avg_speed = 0
        self.now_base = []
        self.next_base = []
        self.lead_distance = 0.0

        self.player_position = 0  # 1번: 2루, 2번: 1루, 3번: 홈, 0번: 3루 플레이어의 초기 베이스 위치
        self.player_position_check = 0
        self.impormation = {
            "베이스": [],
            "시간": [],
            "최고속도": [],
            "속도": [],
            "거리": []
        }

    # 경로를 그리기 위한 변수들

    # 이동평균 리스트 크기

    def mean_avg_list_init(self):  # 이동평균 초기화
        self.mean_avg_list_size = 6 #int(fps / 2)
        for i in range(self.mean_avg_list_size):  # 개수만큼 만듬
            self.mean_avg_list.append([0, 0])

    def box(self, box):
        self.left, self.top, self.w, self.h = [int(v) for v in box]

        if self.fir_top == 0:
            self.fir_top = self.top
        self.right = self.left + self.w
        self.bottom = self.top + self.h
        self.center_x = int(self.left + self.w / 2)
        self.center_y = int(self.top + self.h)

    def draw_box(self, number):
        pt1 = (int(self.left), int(self.top))
        pt2 = (int(self.right), int(self.bottom))

        if number == 0:
            return cv2.rectangle(img, pt1, pt2, (0, 0, 255), 3)
        elif number == 1:
            return cv2.rectangle(img, pt1, pt2, (255, 0, 0), 3)
        elif number == 2:
            return cv2.rectangle(img, pt1, pt2, (0, 255, 0), 3)
        elif number == 3:
            return cv2.rectangle(img, pt1, pt2, (0, 255, 255), 3)

    def constant(self, slope_13, slope_h2, point_list_y_ratio):
        constant_b1 = self.center_y - slope_13 * self.center_x  # 1, 3루
        constant_b2 = self.center_y - slope_h2 * self.center_x  # h, 2루

        # 오른쪽방향에서 촬영될 때를 기준
        if point_list[1][0] > point_list[3][0]:
            if (constant_b1 > 0 and constant_b2 < 0) or (constant_b1 < 0 and constant_b2 > 0) or (constant_b1 == 0 and constant_b2 >= 0):  # 2,4면이랑 각 선에 있을때
                self.f_t_h_cal = (self.h * (abs(self.fir_top - self.top) / int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))) * point_list_y_ratio)  # 초기위치 - 현재위치
            if (constant_b1 > 0 and constant_b2 > 0) or (constant_b1 < 0 and constant_b2 < 0):  # 1,3면에 있을때
                self.f_t_h_cal = (self.h * (abs(self.fir_top - self.top) / int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

        # 왼쪽방향에서 촬영될 때를 기준
        if point_list[1][0] < point_list[3][0]:
            if (constant_b1 > 0 and constant_b2 > 0) or (constant_b1 < 0 and constant_b2 < 0) or (constant_b1 == 0 and constant_b2 <= 0):  # 1,3면이랑 각 선에 있을때
                self.f_t_h_cal = (self.h * (abs(self.fir_top - self.top) / int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))) * point_list_y_ratio)  # 초기위치 - 현재위치
            if (constant_b1 > 0 and constant_b2 < 0) or (constant_b1 < 0 and constant_b2 > 0):  # 2,4면에 있을때
                self.f_t_h_cal = (self.h * (abs(self.fir_top - self.top) / int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))  # 초기위치 - 현재위치

        # 정면방향에서 촬영될 때를 기준
        if point_list[1][0] == point_list[3][0]:
            if (constant_b1 == 0 and constant_b2 == 0):  # 2,4면이랑 각 선에 있을때
                self.f_t_h_cal = (self.h * (abs(self.fir_top - self.top) / int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))  # 초기위치 - 현재위치


    def positional_correction(self):  # 위치에 따른 점의 보정을 위한 함수
        self.t_p_h_cal = (self.h * (abs(self.top - self.pre_top) / int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
        self.adj_center_x = int(self.left + self.w / 2)

        if self.fir_top > self.top:  # 초기위치보다 멀때
            if self.top < self.pre_top:  # 위쪽움직임
                self.adj_center_y = int(self.top + self.h - self.f_t_h_cal - self.t_p_h_cal)
            if self.top > self.pre_top:  # 아래쪽움직임
                self.adj_center_y = int(self.top + self.h - self.f_t_h_cal + self.t_p_h_cal)
            if self.top == self.pre_top:
                self.adj_center_y = int(self.top + self.h - self.f_t_h_cal)

        if self.fir_top < self.top:  # 초기위치보다 가까워질때
            if self.top < self.pre_top:
                self.adj_center_y = int(self.top + self.h + self.f_t_h_cal - self.t_p_h_cal)
            if self.top > self.pre_top:
                self.adj_center_y = int(self.top + self.h + self.f_t_h_cal + self.t_p_h_cal)
            if self.top == self.pre_top:
                self.adj_center_y = int(self.top + self.h + self.f_t_h_cal)

        if self.fir_top == self.top:
            if self.top < self.pre_top:
                self.adj_center_y = int(self.top + self.h - self.t_p_h_cal)
            if self.top > self.pre_top:
                self.adj_center_y = int(self.top + self.h + self.t_p_h_cal)
            if self.top == self.pre_top:
                self.adj_center_y = int(self.top + self.h)
        self.pre_top = self.top

    # 이동평균 계산하여 경로 그리기 보정 & 속도별 칼라추가 작업
    def mean_avg(self, start):
        self.nowPoint[0] = self.adj_center_x
        self.nowPoint[1] = self.adj_center_y
        if start == 1:
            self.point_sum[0] -= self.mean_avg_list[0][0]
            self.point_sum[1] -= self.mean_avg_list[0][1]

            self.mean_avg_list.pop(0)

            self.point_sum[0] += self.nowPoint[0]
            self.point_sum[1] += self.nowPoint[1]

            self.mean_avg_list.append(self.nowPoint[0:2])

            if self.mean_avg_list.count([0, 0]) < self.mean_avg_list_size:
                self.point_mean[0] = int(self.point_sum[0] / (self.mean_avg_list_size - self.mean_avg_list.count([0, 0])))
                self.point_mean[1] = int(self.point_sum[1] / (self.mean_avg_list_size - self.mean_avg_list.count([0, 0])))

                self.pointList.append(self.point_mean[0:2])
                print(len(self.pointList), "좌표값")

        cv2.line(img, (self.adj_center_x, self.adj_center_y), (self.adj_center_x, self.adj_center_y), (255, 0, 255), 3)

    def route_color(self, frame, frame_key, perspect_map, onepixel):  # 이동경로를 색상으로 표현하기 위하여 구간별 속도 계산
        if frame_key + 1 == frame:
            self.pre_route_pers_distance = self.route_pers_distance
            self.pre_time = self.cur_time

        self.cur_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
        route_run_time = round(self.cur_time - self.pre_time, 2)  # 현재시간과 직전시간을 뺀 시간 시간 간격 확인
        # print("시간 ", route_run_time)
        self.pre_time = self.cur_time
        # 총 달린거리
        self.route_pers_distance = round(perstpective(perspect_map, self.pointList, onepixel), 2)
        # print("거리", self.route_pers_distance)
        # 단위거리 = 총달린거리 - 직전달린거리
        if route_run_time != 0:
            route_v = round(abs(self.route_pers_distance - self.pre_route_pers_distance) / route_run_time * 3.6, 2)

            if route_v != 0.0:
                self.route_pointList.append(route_v)
                print(len(self.route_pointList), "속도")
            elif len(self.route_pointList) > 0:
                self.route_pointList.append(route_v)
                print(len(self.route_pointList), "속도")
        # print("속도 ", route_v)
        self.pre_route_pers_distance = self.route_pers_distance
        # 속도 변화 값??

    def draw_route(self):
        speed = 18
        temp_x = 0
        temp_y = 0
        route_pointList_i = 0
        if len(self.route_pointList) > 0:
            for [x, y] in self.pointList:
                # print("x: ",x,y)
                if temp_x != 0 and temp_y != 0:
                    route_pointList_index = self.route_pointList[route_pointList_i]
                    if self.line_count == 1:
                        self.pre_route_pointList_index = route_pointList_index
                        self.line_count += 1

                    route_pointList_index_div = abs(route_pointList_index - self.pre_route_pointList_index) / 2
                    self.pre_route_pointList_index = route_pointList_index

                    color_cal1 = 0
                    if route_pointList_index >= self.pre_route_pointList_index:
                        color_cal1 = abs(self.pre_route_pointList_index + route_pointList_index_div - speed) * 10
                    if route_pointList_index < self.pre_route_pointList_index:
                        color_cal1 = abs(self.pre_route_pointList_index - route_pointList_index_div - speed) * 10
                    color_cal2 = abs(route_pointList_index - speed) * 10

                    if route_pointList_index - speed >= 0:
                        large_color1_255 = 127 - color_cal1
                        if large_color1_255 <= 0:
                            large_color1_255 = 0
                        large_color2_255 = 127 - color_cal2
                        if large_color2_255 <= 0:
                            large_color2_255 = 0
                        cv2.line(img, (x, y), (int((temp_x + x) / 2), int((temp_y + y) / 2)), (0, large_color1_255, 255), 4)
                        cv2.line(img, (int((temp_x + x) / 2), int((temp_y + y) / 2)), (temp_x, temp_y),
                                 (0, large_color2_255, 255), 4)
                    if route_pointList_index - speed < 0:
                        little_color1_255 = 127 + color_cal1
                        if little_color1_255 >= 255:
                            little_color1_255 = 255
                        little_color2_255 = 127 + color_cal2
                        if little_color2_255 >= 255:
                            little_color2_255 = 255
                        cv2.line(img, (x, y), (int((temp_x + x) / 2), int((temp_y + y) / 2)), (0, little_color1_255, 255),
                                 4)
                        cv2.line(img, (int((temp_x + x) / 2), int((temp_y + y) / 2)), (temp_x, temp_y),
                                 (0, little_color2_255, 255), 4)

                    route_pointList_i += 1
                temp_x = x
                temp_y = y

            # cv2.line(img, (self.adj_center_x, self.adj_center_y), (self.adj_center_x, self.adj_center_y), (255, 0, 255), 3)

    # 베이스의 위치를 반환한다.
    def dase_check(self, now_base):
        if point_list.index(now_base) == 0:
            return 3
        elif point_list.index(now_base) == 1:
            return 2
        elif point_list.index(now_base) == 2:
            return 1
        elif point_list.index(now_base) == 3:
            return 0

    # 통과 후 정보 측정하기
    def measure(self):
        running_time = round(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000, 2) - self.start_time  # 달린시간 = 현재시간 - 출발시간
        # self.impormation["경로"].append(self.pointList)
        running_route = round(perstpective(perspect_map, self.pointList, onepixel), 2)
        if not self.impormation["베이스"]:  # 베이스를 첫번쨰 밟을 때
            self.impormation["베이스"].append(self.now_base)
            self.impormation["시간"].append(running_time)
            self.impormation["거리"].append(running_route)
            self.impormation["속도"].append(round(running_route / running_time * 3.6, 2))
            print("구간 시간: " + str(self.impormation["시간"][-1]))
            print("구간 거리: " + str(self.impormation["거리"][-1]))
            print("구간 속도: " + str(self.impormation["속도"][-1]))
            print("----------")
        else:  # 베이스를 두번째 부터 밟을 때
            self.impormation["베이스"].append(self.now_base)
            self.impormation["시간"].append(running_time - sum(self.impormation["시간"]))
            self.impormation["거리"].append(running_route - sum(self.impormation["거리"]))
            self.impormation["속도"].append(round(self.impormation["거리"][-1] / self.impormation["시간"][-1] * 3.6, 2))
            print("구간 시간: " + str(self.impormation["시간"][-1]))
            print("구간 거리: " + str(self.impormation["거리"][-1]))
            print("구간 속도: " + str(self.impormation["속도"][-1]))
            print("----------")

        # self.impormation["속도"]
        # self.impormation["최고속도"]

    # 베이스와 거리를 계산하여 베이스의 반지름보다 작으면 베이스를 밟은 것으로 인식하고 다음 베이스를 설정한다.
    def calculation_between_base(self):
        if not self.now_base:
            self.set_base()
            self.set_next_base()

        if (math.sqrt(pow(self.next_base[0] - self.nowPoint[0], 2) + pow(self.next_base[1] - self.nowPoint[1], 2))) < 13.0:
            self.set_next_base()  # 현재 베이스와 다음 베이스를 설정
            self.measure()  # 베이스 설정 후 현재 베이스까지의 정보를 측정하여 저장

    # 현재 선수의 위치에서 가장 가까운 베이스를 now_base 에 설정한다.
    def set_base(self):
        base_length = {
            "거리": [],
            "베이스": [],
        }

        for i in point_list:
            base_length["거리"].append(math.sqrt(pow(i[0] - self.nowPoint[0], 2) + pow(i[1] - self.nowPoint[1], 2)))
            base_length["베이스"].append(i)

        # lead_List = [[self.now_base[0], self.now_base[1]], [self.nowPoint[0], self.nowPoint[1]]]
        lead_List = []

        self.now_base = base_length["베이스"][base_length["거리"].index(min(base_length["거리"]))]

        lead_List.append(self.now_base[0:2])
        lead_List.append(self.nowPoint[0:2])
        if self.lead_distance == 0.0 and self.fir_top != 0:
            self.lead_distance = round(perstpective(perspect_map, lead_List, onepixel), 2)

        if self.player_position_check == 0:
            self.player_position = point_list.index((self.now_base))
            self.player_position_check = 1

    # now_base의 다음 베이스 좌표 세팅
    def set_next_base(self):
        self.set_base()
        self.next_base = point_list[point_list.index(self.now_base) - 1]

    def player_data_box(self):
        if self.route_pointList != []:
            self.now_speed = self.route_pointList[-1]
            self.max_speed = max(self.route_pointList)
            self.avg_speed = round(sum(self.route_pointList) / len(self.route_pointList), 2)
            self.player_distance = round(perstpective(perspect_map, self.pointList, onepixel), 2)

            start_width_point = 0
            end_width_point = 0

            # if self.player_position == 3:
            #     start_rect_point_num = 0
            #     end_rect_point_num = 1
            #     start_width_point = int(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) * start_rect_point_num / 8)
            #     end_width_point = int(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) * end_rect_point_num / 8)
            #     cv2.rectangle(img, (start_width_point, 0), (end_width_point + 2, 92), (0, 0, 255), 2)
            # elif self.player_position == 2:
            #     start_rect_point_num = 2
            #     end_rect_point_num = 3
            #     start_width_point = int(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) * start_rect_point_num / 8)
            #     end_width_point = int(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) * end_rect_point_num / 8)
            #     cv2.rectangle(img, (start_width_point, 0), (end_width_point + 2, 92), (255, 0, 0), 2)
            # elif self.player_position == 1:
            #     start_rect_point_num = 4
            #     end_rect_point_num = 5
            #     start_width_point = int(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) * start_rect_point_num / 8)
            #     end_width_point = int(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) * end_rect_point_num / 8)
            #     cv2.rectangle(img, (start_width_point, 0), (end_width_point + 2, 92), (0, 255, 0), 2)
            # elif self.player_position == 0:
            #     start_rect_point_num = 6
            #     end_rect_point_num = 7
            #     start_width_point = int(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) * start_rect_point_num / 8)
            #     end_width_point = int(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) * end_rect_point_num / 8)
            #     cv2.rectangle(img, (start_width_point, 0), (end_width_point + 2, 92), (0, 255, 255), 2)
            #
            # cv2.rectangle(img, (start_width_point, 0), (end_width_point, 90), (255, 255, 255), -1)
            #
            # cv2.putText(img, 'Player : ' + str(self.player_position), (start_width_point + 3, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)
            # cv2.putText(img, 'now_V : ' + str(self.now_speed), (start_width_point + 3, 40), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)
            # cv2.putText(img, 'max_V : ' + str(self.max_speed), (start_width_point + 3, 60), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)
            # cv2.putText(img, 'avg_V : ' + str(self.avg_speed), (start_width_point + 3, 80), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)

            set_text(self.player_position, self.player_distance, self.now_speed, self.max_speed, self.lead_distance)

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())