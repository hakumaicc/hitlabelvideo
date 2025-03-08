# Copyright (c) 2025 Gongyue
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

import sys
import os
import json
import cv2
import numpy as np
from functools import partial
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel,
    QFileDialog, QSlider, QListWidget, QListWidgetItem, QGroupBox, QRadioButton,
    QButtonGroup, QTableWidget, QTableWidgetItem, QTabWidget, QMessageBox,
    QInputDialog, QDialog, QDialogButtonBox, QComboBox, QCheckBox, QStyle
)
from PyQt5.QtCore import Qt, QTimer, QRect, QPoint
from PyQt5.QtGui import QImage, QPixmap, QPainter, QColor
# 翻译字典
translations = {
    "简体中文": {
        "window_title": "视频标注器 v1.0.0309 哈尔滨工业大学（深圳）人机系统实验室",
        "label_management": "标签类别管理",
        "add": "添加",
        "modify": "修改",
        "delete": "删除",
        "frame_annotation": "帧标注",
        "segment_annotation": "段标注",
        "rect_mode": "矩形标注",
        "square_mode": "方形标注",
        "start_annotation": "开始标注",
        "finish_annotation": "完成标注",
        "set_start": "左区间定位",
        "set_end": "右区间定位",
        "annotated_data": "已标注数据",
        "open_video": "打开视频",
        "play": "播放",
        "pause": "暂停",
        "save": "保存",
        "exit_video": "退出视频",
        "scale": "缩放",
        "options": "选项(Options)",
        "choose_language": "选择语言(Language):",
        "error_no_annotation": "请先拖拽出标注框！",
        "error_no_label": "请至少选择一个标签！",
        "info_frame_annotation_added": "帧标注已添加（待保存）。",
        "info_segment_annotation_added": "段标注已添加（待保存）。",
        "info_data_saved": "数据已保存至 ",
        "error_no_video_path": "未设置视频路径，保存失败。",
        "table_action": "操作",
        "table_time": "时间/区间",
        "table_label": "标签"
    },
    "繁體中文": {
        "window_title": "HIT Video Annotation Tool (v1.0.0309), HIT (Shenzhen) Human-Machine Systems Lab",
        "label_management": "標籤類別管理",
        "add": "新增",
        "modify": "修改",
        "delete": "刪除",
        "frame_annotation": "幀標注",
        "segment_annotation": "段標注",
        "rect_mode": "矩形標注",
        "square_mode": "方形標注",
        "start_annotation": "開始標注",
        "finish_annotation": "完成標注",
        "set_start": "左區間定位",
        "set_end": "右區間定位",
        "annotated_data": "已標注資料",
        "open_video": "打開影片",
        "play": "播放",
        "pause": "暫停",
        "save": "保存",
        "exit_video": "退出影片",
        "scale": "縮放",
        "options": "選項(Options)",
        "choose_language": "選擇語言:",
        "error_no_annotation": "請先拖拽出標注框！",
        "error_no_label": "請至少選擇一個標籤！",
        "info_frame_annotation_added": "幀標注已添加（待保存）。",
        "info_segment_annotation_added": "段標注已添加（待保存）。",
        "info_data_saved": "數據已保存至 ",
        "error_no_video_path": "未設置影片路徑，保存失敗。",
        "table_action": "操作",
        "table_time": "時間/區間",
        "table_label": "標籤"
    },
    "English": {
        "window_title": "HIT Video Annotation Tool (v1.0.0309), HIT (Shenzhen) Human-Machine Systems Lab",
        "label_management": "Label Management",
        "add": "Add",
        "modify": "Modify",
        "delete": "Delete",
        "frame_annotation": "Frame Annotation",
        "segment_annotation": "Segment Annotation",
        "rect_mode": "Rectangle",
        "square_mode": "Square",
        "start_annotation": "Start Annotation",
        "finish_annotation": "Finish Annotation",
        "set_start": "Set Start",
        "set_end": "Set End",
        "annotated_data": "Annotated Data",
        "open_video": "Open Video",
        "play": "Play",
        "pause": "Pause",
        "save": "Save",
        "exit_video": "Exit Video",
        "scale": "Scale",
        "options": "Options",
        "choose_language": "Choose language:",
        "error_no_annotation": "Please draw an annotation box first!",
        "error_no_label": "Please select at least one label!",
        "info_frame_annotation_added": "Frame annotation added (pending save).",
        "info_segment_annotation_added": "Segment annotation added (pending save).",
        "info_data_saved": "Data saved to ",
        "error_no_video_path": "No video path set, save failed.",
        "table_action": "Action",
        "table_time": "Time/Interval",
        "table_label": "Label"
    },
    "Español": {
        "window_title": "HIT Video Annotation Tool (v1.0.0309), HIT (Shenzhen) Human-Machine Systems Lab",
        "label_management": "Gestión de Etiquetas",
        "add": "Añadir",
        "modify": "Modificar",
        "delete": "Eliminar",
        "frame_annotation": "Anotación de Fotograma",
        "segment_annotation": "Anotación de Segmento",
        "rect_mode": "Marcado Rectangular",
        "square_mode": "Marcado Cuadrado",
        "start_annotation": "Iniciar Anotación",
        "finish_annotation": "Finalizar Anotación",
        "set_start": "Establecer Inicio",
        "set_end": "Establecer Fin",
        "annotated_data": "Datos Anotados",
        "open_video": "Abrir Video",
        "play": "Reproducir",
        "pause": "Pausa",
        "save": "Guardar",
        "exit_video": "Salir del Video",
        "scale": "Escalar",
        "options": "Opciones(Options)",
        "choose_language": "Elija idioma:",
        "error_no_annotation": "¡Dibuja primero un recuadro de anotación!",
        "error_no_label": "¡Por favor, seleccione al menos una etiqueta!",
        "info_frame_annotation_added": "Anotación de fotograma agregada (pendiente de guardar).",
        "info_segment_annotation_added": "Anotación de segmento agregada (pendiente de guardar).",
        "info_data_saved": "Datos guardados en ",
        "error_no_video_path": "No se estableció la ruta del video, fallo al guardar.",
        "table_action": "Acción",
        "table_time": "Tiempo/Intervalo",
        "table_label": "Etiqueta"
    },
    "Français": {
        "window_title": "HIT Video Annotation Tool (v1.0.0309), HIT (Shenzhen) Human-Machine Systems Lab",
        "label_management": "Gestion des Étiquettes",
        "add": "Ajouter",
        "modify": "Modifier",
        "delete": "Supprimer",
        "frame_annotation": "Annotation d'Image",
        "segment_annotation": "Annotation de Segment",
        "rect_mode": "Annotation Rectangulaire",
        "square_mode": "Annotation Carrée",
        "start_annotation": "Démarrer l'Annotation",
        "finish_annotation": "Terminer l'Annotation",
        "set_start": "Définir le Début",
        "set_end": "Définir la Fin",
        "annotated_data": "Données Annotées",
        "open_video": "Ouvrir la Vidéo",
        "play": "Lecture",
        "pause": "Pause",
        "save": "Enregistrer",
        "exit_video": "Quitter la Vidéo",
        "scale": "Redimensionner",
        "options": "Options(Options)",
        "choose_language": "Choisissez la langue:",
        "error_no_annotation": "Veuillez d'abord tracer un cadre d'annotation !",
        "error_no_label": "Veuillez sélectionner au moins une étiquette !",
        "info_frame_annotation_added": "Annotation d'image ajoutée (en attente de sauvegarde).",
        "info_segment_annotation_added": "Annotation de segment ajoutée (en attente de sauvegarde).",
        "info_data_saved": "Données enregistrées dans ",
        "error_no_video_path": "Aucun chemin vidéo défini, échec de l'enregistrement.",
        "table_action": "Action",
        "table_time": "Temps/Intervalle",
        "table_label": "Étiquette"
    },
    "Deutsch": {
        "window_title": "HIT Video Annotation Tool (v1.0.0309), HIT (Shenzhen) Human-Machine Systems Lab",
        "label_management": "Etikettenverwaltung",
        "add": "Hinzufügen",
        "modify": "Bearbeiten",
        "delete": "Löschen",
        "frame_annotation": "Bildannotation",
        "segment_annotation": "Segmentannotation",
        "rect_mode": "Rechteck",
        "square_mode": "Quadrat",
        "start_annotation": "Annotation Starten",
        "finish_annotation": "Annotation Abschließen",
        "set_start": "Start festlegen",
        "set_end": "Ende festlegen",
        "annotated_data": "Annotierte Daten",
        "open_video": "Video öffnen",
        "play": "Abspielen",
        "pause": "Pause",
        "save": "Speichern",
        "exit_video": "Video beenden",
        "scale": "Skalieren",
        "options": "Optionen(Options)",
        "choose_language": "Sprache wählen:",
        "error_no_annotation": "Bitte zeichnen Sie zuerst ein Annotationsrechteck!",
        "error_no_label": "Bitte wählen Sie mindestens ein Etikett aus!",
        "info_frame_annotation_added": "Bildannotation hinzugefügt (noch nicht gespeichert).",
        "info_segment_annotation_added": "Segmentannotation hinzugefügt (noch nicht gespeichert).",
        "info_data_saved": "Daten gespeichert in ",
        "error_no_video_path": "Kein Videopfad gesetzt, Speicherung fehlgeschlagen.",
        "table_action": "Aktion",
        "table_time": "Zeit/Intervall",
        "table_label": "Etikett"
    },
    "Italiano": {
        "window_title": "HIT Video Annotation Tool (v1.0.0309), HIT (Shenzhen) Human-Machine Systems Lab",
        "label_management": "Gestione Etichette",
        "add": "Aggiungi",
        "modify": "Modifica",
        "delete": "Elimina",
        "frame_annotation": "Annotazione Fotogramma",
        "segment_annotation": "Annotazione Segmento",
        "rect_mode": "Annotazione Rettangolare",
        "square_mode": "Annotazione Quadrata",
        "start_annotation": "Inizia Annotazione",
        "finish_annotation": "Completa Annotazione",
        "set_start": "Imposta Inizio",
        "set_end": "Imposta Fine",
        "annotated_data": "Dati Annotati",
        "open_video": "Apri Video",
        "play": "Riproduci",
        "pause": "Pausa",
        "save": "Salva",
        "exit_video": "Esci dal Video",
        "scale": "Scala",
        "options": "Opzioni(Options)",
        "choose_language": "Scegli lingua:",
        "error_no_annotation": "Per favore, disegna prima un riquadro di annotazione!",
        "error_no_label": "Seleziona almeno un'etichetta!",
        "info_frame_annotation_added": "Annotazione fotogramma aggiunta (in attesa di salvataggio).",
        "info_segment_annotation_added": "Annotazione segmento aggiunta (in attesa di salvataggio).",
        "info_data_saved": "Dati salvati in ",
        "error_no_video_path": "Nessun percorso video impostato, salvataggio fallito.",
        "table_action": "Azione",
        "table_time": "Tempo/Intervallo",
        "table_label": "Etichetta"
    },
    "Русский": {
        "window_title": "HIT Video Annotation Tool (v1.0.0309), HIT (Shenzhen) Human-Machine Systems Lab",
        "label_management": "Управление метками",
        "add": "Добавить",
        "modify": "Изменить",
        "delete": "Удалить",
        "frame_annotation": "Аннотация кадра",
        "segment_annotation": "Аннотация сегмента",
        "rect_mode": "Прямоугольная",
        "square_mode": "Квадратная",
        "start_annotation": "Начать аннотацию",
        "finish_annotation": "Завершить аннотацию",
        "set_start": "Установить начало",
        "set_end": "Установить конец",
        "annotated_data": "Аннотированные данные",
        "open_video": "Открыть видео",
        "play": "Воспроизвести",
        "pause": "Пауза",
        "save": "Сохранить",
        "exit_video": "Выйти из видео",
        "scale": "Масштабировать",
        "options": "Опции(Options)",
        "choose_language": "Выберите язык:",
        "error_no_annotation": "Сначала нарисуйте рамку аннотации!",
        "error_no_label": "Пожалуйста, выберите хотя бы одну метку!",
        "info_frame_annotation_added": "Аннотация кадра добавлена (ожидает сохранения).",
        "info_segment_annotation_added": "Аннотация сегмента добавлена (ожидает сохранения).",
        "info_data_saved": "Данные сохранены в ",
        "error_no_video_path": "Видео не задано, сохранение не удалось.",
        "table_action": "Действие",
        "table_time": "Время/Интервал",
        "table_label": "Метка"
    },
    "日本語": {
        "window_title": "HIT Video Annotation Tool (v1.0.0309), HIT (Shenzhen) Human-Machine Systems Lab",
        "label_management": "ラベル管理",
        "add": "追加",
        "modify": "修正",
        "delete": "削除",
        "frame_annotation": "フレームアノテーション",
        "segment_annotation": "セグメントアノテーション",
        "rect_mode": "矩形モード",
        "square_mode": "正方形モード",
        "start_annotation": "アノテーション開始",
        "finish_annotation": "アノテーション完了",
        "set_start": "開始位置設定",
        "set_end": "終了位置設定",
        "annotated_data": "アノテーション済みデータ",
        "open_video": "動画を開く",
        "play": "再生",
        "pause": "一時停止",
        "save": "保存",
        "exit_video": "動画を終了",
        "scale": "拡大縮小",
        "options": "オプション(Options)",
        "choose_language": "言語を選択:",
        "error_no_annotation": "まずアノテーション枠を描いてください！",
        "error_no_label": "少なくとも1つのラベルを選択してください！",
        "info_frame_annotation_added": "フレームアノテーションが追加されました（保存待ち）。",
        "info_segment_annotation_added": "セグメントアノテーションが追加されました（保存待ち）。",
        "info_data_saved": "データが保存されました: ",
        "error_no_video_path": "動画パスが設定されていません、保存に失敗しました。",
        "table_action": "操作",
        "table_time": "時間/区間",
        "table_label": "ラベル"
    },
    "한국어": {
        "window_title": "HIT Video Annotation Tool (v1.0.0309), HIT (Shenzhen) Human-Machine Systems Lab",
        "label_management": "레이블 관리",
        "add": "추가",
        "modify": "수정",
        "delete": "삭제",
        "frame_annotation": "프레임 주석",
        "segment_annotation": "세그먼트 주석",
        "rect_mode": "사각형 모드",
        "square_mode": "정사각형 모드",
        "start_annotation": "주석 시작",
        "finish_annotation": "주석 완료",
        "set_start": "시작 위치 설정",
        "set_end": "종료 위치 설정",
        "annotated_data": "주석 데이터",
        "open_video": "비디오 열기",
        "play": "재생",
        "pause": "일시정지",
        "save": "저장",
        "exit_video": "비디오 종료",
        "scale": "크기 조절",
        "options": "옵션(Options)",
        "choose_language": "언어 선택:",
        "error_no_annotation": "먼저 주석 상자를 그려주세요!",
        "error_no_label": "최소 하나의 레이블을 선택해주세요!",
        "info_frame_annotation_added": "프레임 주석이 추가되었습니다 (저장 대기 중).",
        "info_segment_annotation_added": "세그먼트 주석이 추가되었습니다 (저장 대기 중).",
        "info_data_saved": "데이터가 저장되었습니다: ",
        "error_no_video_path": "비디오 경로가 설정되지 않았습니다. 저장 실패.",
        "table_action": "작업",
        "table_time": "시간/구간",
        "table_label": "레이블"
    }
}

class ScaleDialog(QDialog):
    def __init__(self, parent=None, initial_scale=1.0):
        super().__init__(parent)
        if parent is not None and hasattr(parent, "language"):
            self.current_language = parent.language
        else:
            self.current_language = "简体中文"
        # 定义 t，用于从翻译字典中取对应字符串
        t = translations[self.current_language]
        self.setWindowTitle(t["scale"])
        self.resize(500, 100)
        layout = QVBoxLayout(self)
        # 显示当前比例标签
        self.scale_label = QLabel(f"{initial_scale:.2f}x")
        layout.addWidget(self.scale_label)
        # 创建一个水平滑块，范围 10 ~ 300，初始值对应 initial_scale*100
        self.scale_slider = QSlider(Qt.Horizontal)
        self.scale_slider.setMinimum(10)
        self.scale_slider.setMaximum(300)
        self.scale_slider.setValue(int(initial_scale * 100))
        self.scale_slider.setTickPosition(QSlider.TicksBelow)
        self.scale_slider.setTickInterval(10)
        layout.addWidget(self.scale_slider)
        # 关闭按钮
        self.current_scale = initial_scale
        # 实时更新：当滑块变化时更新标签和调用父窗口的缩放函数
        self.scale_slider.valueChanged.connect(self.on_value_changed)

    def on_value_changed(self, value):
        self.current_scale = value / 100.0
        self.scale_label.setText(f" {self.current_scale:.2f}x")
        # 实时调用父窗口的设置缩放函数
        if self.parent():
            self.parent().set_scale(self.current_scale)

    def get_scale(self):
        return self.current_scale


# 自定义视频显示标签，支持框选绘制及显示当前帧数/总帧数
class VideoLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.drawing_mode = False
        self.moving_mode = False
        self.square_mode = False
        self.start_point = None
        self.end_point = None
        self.annotation_rect = None
        self.frame_info = ""
        self.move_offset = QPoint(0, 0)
        self.annotation_labels = ""  # 添加此行初始化属性

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            if self.annotation_rect is not None:
                self.annotation_rect = None
                self.drawing_mode = False
                self.moving_mode = False
                self.update()
            return
        elif event.button() == Qt.LeftButton:
            if self.annotation_rect is not None:
                if self.annotation_rect.contains(event.pos()):
                    self.moving_mode = True
                    self.move_offset = event.pos() - self.annotation_rect.topLeft()
                else:
                    self.annotation_rect = None
                    self.drawing_mode = True
                    self.start_point = event.pos()
                    self.end_point = self.start_point
            else:
                self.drawing_mode = True
                self.start_point = event.pos()
                self.end_point = self.start_point
            self.update()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            if self.moving_mode and self.annotation_rect is not None:
                new_top_left = event.pos() - self.move_offset
                self.annotation_rect = QRect(new_top_left, self.annotation_rect.size())
                self.update()
            elif self.drawing_mode:
                current_point = event.pos()
                if self.square_mode:
                    dx = current_point.x() - self.start_point.x()
                    dy = current_point.y() - self.start_point.y()
                    side = min(abs(dx), abs(dy))
                    new_x = self.start_point.x() + (side if dx >= 0 else -side)
                    new_y = self.start_point.y() + (side if dy >= 0 else -side)
                    self.end_point = QPoint(new_x, new_y)
                else:
                    self.end_point = current_point
                self.annotation_rect = QRect(self.start_point, self.end_point).normalized()
                self.update()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.moving_mode:
                self.moving_mode = False
            elif self.drawing_mode:
                self.drawing_mode = False
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        # 绘制当前帧信息
        if self.frame_info:
            painter.setPen(Qt.white)
            painter.drawText(10, 20, self.frame_info)
        # 绘制标注框
        if self.annotation_rect:
            painter.setPen(Qt.red)
            painter.drawRect(self.annotation_rect)
            # 如果有标签，则在框上边显示标签：绘制红底白字
            if self.annotation_labels:
                # 设置字体
                font = painter.font()
                font.setPointSize(7)
                painter.setFont(font)
                # 计算文本尺寸
                metrics = painter.fontMetrics()
                text = self.annotation_labels
                text_width = metrics.horizontalAdvance(text)
                text_height = metrics.height()
                # 定位：让文本区域的底边与框的顶部对齐，并居左于框左边（可以调整偏移）
                x = self.annotation_rect.left()
                y = self.annotation_rect.top() - text_height  # 2像素间隙
                # 如果 y 小于 0，可调整为 0
                if y < 0:
                    y = 0
                text_rect = QRect(x, y-2, text_width + 4, text_height+2)  # 多加4像素宽度用于内边距
                # 绘制红色背景（填充与标注框边框一致的红色）
                painter.fillRect(text_rect, Qt.red)
                # 绘制边框（可选，如需与标注框一致）
                painter.setPen(Qt.red)
                painter.drawRect(text_rect)
                # 绘制白色文本，内部稍微偏右
                painter.setPen(Qt.white)
                painter.drawText(text_rect.adjusted(2, 0, 0, 0), Qt.AlignLeft | Qt.AlignVCenter, text)
        painter.end()



class AnnotationSlider(QSlider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frame_marks = []          # 帧标注位置列表（整数值）
        self.segment_intervals = []    # 段标注区间列表，每个元素为 (start, end)
        self._mousePressPos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._mousePressPos = event.pos()  # 记录按下位置
            # 调用默认行为以便拖拽正常
            super().mousePressEvent(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            # 判断如果鼠标移动距离很小，则认为是单击
            if self._mousePressPos is not None and (event.pos() - self._mousePressPos).manhattanLength() < 5:
                new_val = QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), event.x(), self.width())
                self.setValue(new_val)
                self.sliderMoved.emit(new_val)
                event.accept()
            super().mouseReleaseEvent(event)
        else:
            super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        total = self.maximum()

        # 绘制段标注区间：用浅蓝色圆角矩形（细一些）
        painter.setBrush(QColor(173, 216, 100, 150))  # 浅蓝色，透明度150
        painter.setPen(Qt.NoPen)
        segment_height = 4  # 高度为4像素
        y = (self.height() - segment_height) // 2  # 垂直居中
        for (start, end) in self.segment_intervals:
            if total > 0:
                fraction_start = start / total
                fraction_end = end / total
            else:
                fraction_start = 0
                fraction_end = 0
            x = int(fraction_start * self.width())
            w = int((fraction_end - fraction_start) * self.width())
            # 绘制圆角矩形，圆角半径设为2
            painter.drawRoundedRect(x, y, w, segment_height, 2, 2)

            # 绘制帧标注标记（红色圆角矩形），更美观
        marker_height = 6  # 标记高度
        y = (self.height() - marker_height) // 2  # 垂直居中
        painter.setBrush(QColor(255, 150, 50, 255))  # 浅蓝色，透明度150
        painter.setPen(Qt.NoPen)
        for mark in self.frame_marks:
            fraction = mark / total if total > 0 else 0
            x = int(fraction * self.width())
            # 绘制宽度为2，高度为marker_height的圆角矩形，圆角半径为1
            rect = QRect(x - 1, y, 2, marker_height)
            painter.drawRoundedRect(rect, 1, 1)
        painter.end()



# 选项对话框
class OptionsDialog(QDialog):
    def __init__(self, parent=None, current_language="简体中文", auto_scale=True):
        super().__init__(parent)
        self.current_language = current_language
        self.auto_scale = auto_scale
        self.initUI()

    def initUI(self):
        t = translations[self.current_language]
        self.setWindowTitle(t["options"])
        self.resize(300, 150)
        layout = QVBoxLayout()
        lang_group = QGroupBox(t["choose_language"])
        lang_group.setObjectName("langGroup")
        lang_layout = QHBoxLayout()
        lang_layout.addWidget(QLabel(t["choose_language"]))
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["简体中文", "繁體中文", "English", "Español", "Français", "Deutsch", "Italiano", "Русский", "日本語", "한국어"])
        index = self.lang_combo.findText(self.current_language)
        if index >= 0:
            self.lang_combo.setCurrentIndex(index)
        lang_layout.addWidget(self.lang_combo)
        lang_group.setLayout(lang_layout)
        layout.addWidget(lang_group)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def get_settings(self):
        return {
            "language": self.lang_combo.currentText()
        }

# 主窗口
class VideoPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.video_path = None
        self.cap = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_frame)
        self.playing = False

        self.scale_factor = 1.0
        self.video_width = None
        self.video_height = None
        self.auto_scale = True

        self.language = "简体中文"

        self.segment_start_time = None
        self.segment_end_time = None

        self.annotations_data = {
            "video_name": "",
            "tags": [],
            "frame_annotations": {},
            "segment_annotations": []
        }

        self.initUI()
        self.update_ui_texts()

    def set_scale(self, scale):
        self.scale_factor = scale
        # 记住当前帧位置
        #pos = self.slider.value()
        self.update_video_display_size()
        #self.set_position(pos)

    def table_cell_double_clicked(self, row, column):
        if column != 1:
            return
        item = self.annotation_table.item(row, column)
        if not item:
            return
        data = item.data(Qt.UserRole)
        if not data:
            return
        # 修改为解包三个值：annotation_type, key, index
        annotation_type, key, index = data
        if annotation_type == "frame":
            frame_value = int(key)
            self.set_position(frame_value)
            self.slider.setValue(frame_value)
            ann_list = self.annotations_data["frame_annotations"].get(str(frame_value), [])
            if ann_list and 0 <= index - 1 < len(ann_list):
                ann = ann_list[index - 1]
                top_left = ann.get("top_left")
                bottom_right = ann.get("bottom_right")
                if top_left and bottom_right:
                    factor = self.scale_factor if self.scale_factor != 0 else 1
                    x1 = int(top_left[0] * factor)
                    y1 = int(top_left[1] * factor)
                    x2 = int(bottom_right[0] * factor)
                    y2 = int(bottom_right[1] * factor)
                    self.video_label.annotation_rect = QRect(QPoint(x1, y1), QPoint(x2, y2))
            if ann_list and 0 <= index - 1 < len(ann_list):
                ann = ann_list[index - 1]
                top_left = ann.get("top_left")
                bottom_right = ann.get("bottom_right")
                # 保存当前标注的标签文本到 video_label 的属性中
                self.video_label.annotation_labels = ", ".join(ann.get("labels", []))
                if top_left and bottom_right:
                    factor = self.scale_factor if self.scale_factor != 0 else 1
                    x1 = int(top_left[0] * factor)
                    y1 = int(top_left[1] * factor)
                    x2 = int(bottom_right[0] * factor)
                    y2 = int(bottom_right[1] * factor)
                    self.video_label.annotation_rect = QRect(QPoint(x1, y1), QPoint(x2, y2))
            self.video_label.update()
        elif annotation_type == "segment":
            start_frame = int(key)
            self.set_position(start_frame)
            self.slider.setValue(start_frame)
            self.video_label.annotation_rect = None
            self.video_label.update()
        



    def initUI(self):
        self.setWindowTitle("视频标注器")
        self.resize(1500, 800)
        self.setStyleSheet("background-color: #2E3440; color: white;")
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # =================== 左侧面板 ===================
        left_panel = QVBoxLayout()
        left_panel.setSpacing(5)
        left_panel.setContentsMargins(5, 5, 5, 5)

        # (1) 标签类别管理（上部，可拉伸）
        label_group = QGroupBox()
        label_group.setObjectName("labelGroup")
        label_layout = QVBoxLayout(label_group)
        label_layout.setContentsMargins(5,5,5,5)
        # 标签管理按钮
        btn_style = """
            QPushButton {
                background-color: #4C566A;
                color: white;
                border: none;
                padding: 6px;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #5E81AC;
            }
        """
        self.add_label_btn = QPushButton()
        self.modify_label_btn = QPushButton()
        self.delete_label_btn = QPushButton()
        self.add_label_btn.setStyleSheet(btn_style)
        self.modify_label_btn.setStyleSheet(btn_style)
        self.delete_label_btn.setStyleSheet(btn_style)
        label_btn_layout = QHBoxLayout()
        label_btn_layout.addWidget(self.add_label_btn)
        label_btn_layout.addWidget(self.modify_label_btn)
        label_btn_layout.addWidget(self.delete_label_btn)
        label_layout.addLayout(label_btn_layout)
        self.label_list = QListWidget()
        self.label_list.setDragDropMode(QListWidget.InternalMove)
        label_layout.addWidget(self.label_list)
        left_panel.addWidget(label_group, stretch=1)

        # (2) 标注操作区（中部，固定高度）
        self.tab_widget = QTabWidget()
        self.tab_widget.setFixedHeight(150)
        self.tab_widget.setStyleSheet("""
            QTabBar::tab {
                background: #808080;
                color: white;
                padding: 8px;
                margin: 2px;
            }
            QTabBar::tab:selected {
                background: #5E81AC;
                color: white;
            }
            QTabWidget::pane {
                border: 1px solid #808080;
            }
        """)
        self.frame_tab = QWidget()
        frame_layout = QVBoxLayout(self.frame_tab)
        mode_layout = QHBoxLayout()
        self.rect_radio = QRadioButton()
        self.square_radio = QRadioButton()
        self.rect_radio.setChecked(True)
        mode_layout.addWidget(self.rect_radio)
        mode_layout.addWidget(self.square_radio)
        self.frame_mode_group = QButtonGroup()
        self.frame_mode_group.addButton(self.rect_radio)
        self.frame_mode_group.addButton(self.square_radio)
        frame_layout.addLayout(mode_layout)
        btn_layout = QHBoxLayout()
        self.frame_start_btn = QPushButton()
        self.frame_finish_btn = QPushButton()
        self.frame_start_btn.setStyleSheet(btn_style)
        self.frame_finish_btn.setStyleSheet(btn_style)
        btn_layout.addWidget(self.frame_start_btn)
        btn_layout.addWidget(self.frame_finish_btn)
        frame_layout.addLayout(btn_layout)
        self.tab_widget.addTab(self.frame_tab, "")
        self.segment_tab = QWidget()
        segment_layout = QVBoxLayout(self.segment_tab)
        btn_layout2 = QHBoxLayout()
        self.segment_start_btn = QPushButton()
        self.segment_left_btn = QPushButton()
        self.segment_right_btn = QPushButton()
        self.segment_finish_btn = QPushButton()
        self.segment_start_btn.setStyleSheet(btn_style)
        self.segment_left_btn.setStyleSheet(btn_style)
        self.segment_right_btn.setStyleSheet(btn_style)
        self.segment_finish_btn.setStyleSheet(btn_style)
        btn_layout2.addWidget(self.segment_start_btn)
        btn_layout2.addWidget(self.segment_left_btn)
        btn_layout2.addWidget(self.segment_right_btn)
        btn_layout2.addWidget(self.segment_finish_btn)
        segment_layout.addLayout(btn_layout2)
        self.tab_widget.addTab(self.segment_tab, "")
        left_panel.addWidget(self.tab_widget, stretch=0)  # 固定高度区域

        # (3) 已标注数据区域（下部，可拉伸）
        data_group = QGroupBox()
        data_group.setObjectName("dataGroup")
        data_layout = QVBoxLayout(data_group)
        data_layout.setContentsMargins(5,5,5,5)
        self.annotation_table = QTableWidget()
        self.annotation_table.setColumnCount(3)
        self.annotation_table.setHorizontalHeaderLabels([translations[self.language]["table_action"],
                                                        translations[self.language]["table_time"],
                                                        translations[self.language]["table_label"]])
        self.annotation_table.setStyleSheet("""
            QTableWidget {
                background-color: #3B4252;
                color: white;
                gridline-color: #5E81AC;
            }
            QHeaderView::section {
                background-color: #3B4252;
                color: white;
                padding: 4px;
                border: 1px solid #5E81AC;
            }
            QTableCornerButton::section {
                background-color: #3B4252;  /* 与表格背景相同 */
                border: 1px solid #5E81AC;  /* 同表格边框一致 */
            }
        """)
        data_layout.addWidget(self.annotation_table)
        left_panel.addWidget(data_group, stretch=1)

        left_panel.addStretch()
        main_layout.addLayout(left_panel, 1)

        self.annotation_table.cellDoubleClicked.connect(self.table_cell_double_clicked)

        # =================== 右侧面板 ===================
        # 右侧面板采用 QVBoxLayout，并去掉任何多余的边距和间距
        right_panel = QVBoxLayout()
        right_panel.setContentsMargins(0, 0, 0, 0)
        right_panel.setSpacing(0)

        # 按钮区域（顶部，固定高度）
        top_btn_widget = QWidget()
        top_btn_layout = QHBoxLayout(top_btn_widget)
        top_btn_layout.setContentsMargins(5, 5, 5, 5)  # 可以留一点边距让按钮看起来更美观
        top_btn_layout.setSpacing(5)

        self.open_btn = QPushButton()
        self.play_pause_btn = QPushButton()
        self.save_btn = QPushButton()
        self.close_btn = QPushButton()
        self.scale_btn = QPushButton()

        self.options_btn = QPushButton()

        for btn in [self.open_btn, self.play_pause_btn, self.save_btn, self.close_btn, self.scale_btn, self.options_btn]:
            btn.setStyleSheet(btn_style)
            top_btn_layout.addWidget(btn)
        
        self.scale_btn.setEnabled(False)
        self.scale_btn.setStyleSheet(
            "QPushButton { background-color: #4C566A; color: white; border: none; padding: 6px; font-size: 14px; border-radius: 4px; }"
            "QPushButton:disabled { background-color: #4C566A; color: grey; }"
        )

        right_panel.addWidget(top_btn_widget, 0)  # 固定在顶部

        # 视频显示区域（中间，自动拉伸）
        video_container = QWidget()
        video_container_layout = QVBoxLayout(video_container)
        video_container_layout.setContentsMargins(0, 0, 0, 0)
        video_container_layout.setSpacing(0)

        self.video_label = VideoLabel(self)
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet("border: 2px solid #81A1C1; background-color: #3B4252; margin:0; padding:0;")
        # 把 video_label 放入一个可拉伸的布局中
        video_container_layout.addWidget(self.video_label, 1)

        right_panel.addWidget(video_container, 1)

        # 时间轴（底部，固定高度）
        self.slider = AnnotationSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal { background: #4C566A; height: 6px; border-radius: 4px; }
            QSlider::handle:horizontal { background: #88C0D0; border-radius: 3px; width: 6px; margin: 0 0 0 -4px; }
        """)
        self.slider.sliderMoved.connect(self.set_position)
        right_panel.addWidget(self.slider, 0)

        # 把右侧面板加到 main_layout 中
        main_layout.addLayout(right_panel, 3)


        # 连接按钮信号
        self.open_btn.clicked.connect(self.open_video)
        self.play_pause_btn.clicked.connect(self.toggle_play_pause)
        self.close_btn.clicked.connect(self.close_video)
        self.scale_btn.clicked.connect(self.scale_video)
        self.options_btn.clicked.connect(self.open_options)
        self.add_label_btn.clicked.connect(self.add_label)
        self.modify_label_btn.clicked.connect(self.modify_label)
        self.delete_label_btn.clicked.connect(self.delete_label)
        self.frame_start_btn.clicked.connect(self.start_frame_annotation)
        self.frame_finish_btn.clicked.connect(self.finish_frame_annotation)
        self.segment_start_btn.clicked.connect(self.start_segment_annotation)
        self.segment_left_btn.clicked.connect(self.set_segment_left)
        self.segment_right_btn.clicked.connect(self.set_segment_right)
        self.segment_finish_btn.clicked.connect(self.finish_segment_annotation)
        self.save_btn.clicked.connect(self.save_all)


    def update_ui_texts(self):
        t = translations[self.language]
        self.setWindowTitle(t["window_title"])
        self.findChild(QGroupBox, "labelGroup").setTitle(t["label_management"])
        self.findChild(QGroupBox, "dataGroup").setTitle(t["annotated_data"])
        self.tab_widget.setTabText(0, t["frame_annotation"])
        self.tab_widget.setTabText(1, t["segment_annotation"])
        self.add_label_btn.setText(t["add"])
        self.modify_label_btn.setText(t["modify"])
        self.delete_label_btn.setText(t["delete"])
        self.rect_radio.setText(t["rect_mode"])
        self.square_radio.setText(t["square_mode"])
        self.frame_start_btn.setText(t["start_annotation"])
        self.frame_finish_btn.setText(t["finish_annotation"])
        self.segment_start_btn.setText(t["start_annotation"])
        self.segment_left_btn.setText(t["set_start"])
        self.segment_right_btn.setText(t["set_end"])
        self.segment_finish_btn.setText(t["finish_annotation"])
        self.open_btn.setText(t["open_video"])
        # 根据当前播放状态设置播放/暂停按钮文本
        if self.playing:
            self.play_pause_btn.setText(t["pause"])
        else:
            self.play_pause_btn.setText(t["play"])
        self.save_btn.setText(t["save"])
        self.close_btn.setText(t["exit_video"])
        self.scale_btn.setText(t["scale"])
        self.options_btn.setText(t["options"])
        self.update_annotation_table()



    def get_annotation_file_path(self):
        if self.video_path:
            base = os.path.splitext(os.path.basename(self.video_path))[0]
            return os.path.join(os.path.dirname(self.video_path), base + "_annotations.json")
        return None

    def load_annotations(self):
        ann_file = self.get_annotation_file_path()
        if ann_file and os.path.exists(ann_file):
            with open(ann_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"video_name": os.path.basename(self.video_path) if self.video_path else "unknown",
                "tags": [],
                "frame_annotations": {},
                "segment_annotations": []}

    def update_annotation_table(self):
        rows = []
        # 遍历帧标注：每个帧可能有多个标注
        for ts, ann_list in self.annotations_data.get("frame_annotations", {}).items():
            if not isinstance(ann_list, list):
                if isinstance(ann_list, dict):
                    ann_list = [ann_list]
                    self.annotations_data["frame_annotations"][ts] = ann_list
                else:
                    continue
            for idx, annotation in enumerate(ann_list, 1):
                time_str = f"{ts} ({idx})"  # 例如 "314 (1)"
                labels = ", ".join(annotation.get("labels", []))
                rows.append(("frame", int(ts), idx, time_str, labels))
        # 遍历段标注：这里 key 为段的起始帧，index 为列表中的索引
        for idx, ann in enumerate(self.annotations_data.get("segment_annotations", [])):
            start_frame = int(ann.get("start"))
            time_str = f"{ann.get('start')} - {ann.get('end')}"
            labels = ", ".join(ann.get("labels", []))
            rows.append(("segment", start_frame, idx, time_str, labels))
        t = translations[self.language]
        self.annotation_table.setColumnCount(3)
        self.annotation_table.setHorizontalHeaderLabels([t["table_action"], t["table_time"], t["table_label"]])
        self.annotation_table.setColumnWidth(0, 70)
        self.annotation_table.setRowCount(len(rows))
        for i, (atype, key, index, time_str, labels) in enumerate(rows):
            btn = QPushButton(t["delete"])
            btn.setStyleSheet("background-color: #BF616A; color: white; padding: 2px 5px; font-size: 13px;")
            btn.setFixedWidth(70)
            btn.clicked.connect(partial(self.delete_annotation, atype, key, index))
            self.annotation_table.setCellWidget(i, 0, btn)
            time_item = QTableWidgetItem(time_str)
            # 存储 (atype, key, index) 以便双击跳转
            time_item.setData(Qt.UserRole, (atype, key, index))
            time_item.setFlags(time_item.flags() & ~Qt.ItemIsEditable)
            self.annotation_table.setItem(i, 1, time_item)
            label_item = QTableWidgetItem(labels)
            label_item.setFlags(label_item.flags() & ~Qt.ItemIsEditable)
            self.annotation_table.setItem(i, 2, label_item)
        self.annotation_table.verticalHeader().setDefaultSectionSize(30)
        
        # 更新 AnnotationSlider 的标记数据（保持原来的逻辑）
        frame_marks = []
        for ts, ann in self.annotations_data.get("frame_annotations", {}).items():
            if not isinstance(ann, list):
                ann = [ann]
            frame_marks.extend([int(ts)] * len(ann))
        segment_intervals = []
        for ann in self.annotations_data.get("segment_annotations", []):
            start = int(ann.get("start"))
            end = int(ann.get("end"))
            segment_intervals.append((start, end))
        self.slider.frame_marks = frame_marks
        self.slider.segment_intervals = segment_intervals
        self.slider.update()

        
        # 更新 AnnotationSlider 的标记数据
        frame_marks = []
        for ts, ann in self.annotations_data.get("frame_annotations", {}).items():
            if not isinstance(ann, list):
                ann = [ann]
            frame_marks.extend([int(ts)] * len(ann))
        self.slider.frame_marks = frame_marks
        self.slider.segment_intervals = segment_intervals
        self.slider.update()



    def delete_annotation(self, annotation_type, key, index):
        if annotation_type == "frame":
            ts_key = str(key)
            if ts_key in self.annotations_data.get("frame_annotations", {}):
                ann_list = self.annotations_data["frame_annotations"][ts_key]
                if 0 <= index - 1 < len(ann_list):
                    del ann_list[index - 1]
                    if not ann_list:
                        del self.annotations_data["frame_annotations"][ts_key]
        elif annotation_type == "segment":
            # 对于段标注，key 这里为起始帧，但我们用 index 来删除列表中的对应项
            try:
                del self.annotations_data["segment_annotations"][index]
            except IndexError:
                pass
        self.update_annotation_table()



    def add_label(self):
        new_item = QListWidgetItem("新标签")
        new_item.setData(Qt.UserRole, new_item.text())
        new_item.setFlags(new_item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEditable)
        new_item.setCheckState(Qt.Unchecked)
        self.label_list.addItem(new_item)
        self.label_list.setCurrentItem(new_item)
        self.label_list.editItem(new_item)

    def modify_label(self):
        current_item = self.label_list.currentItem()
        if current_item:
            current_item.setFlags(current_item.flags() | Qt.ItemIsEditable)
            self.label_list.editItem(current_item)

    def delete_label(self):
        current_item = self.label_list.currentItem()
        if current_item:
            row = self.label_list.row(current_item)
            self.label_list.takeItem(row)

    def start_frame_annotation(self):
        self.pause_video()
        self.video_label.drawing_mode = True
        self.video_label.square_mode = self.square_radio.isChecked()
        self.video_label.annotation_rect = None
        self.video_label.update()
        print("启动帧标注，视频已暂停。")

    def finish_frame_annotation(self):
        self.video_label.drawing_mode = False
        if not self.video_label.annotation_rect:
            QMessageBox.warning(self, translations[self.language]["window_title"],
                                translations[self.language]["error_no_annotation"])
            return
        selected_labels = []
        for i in range(self.label_list.count()):
            item = self.label_list.item(i)
            if item.checkState() == Qt.Checked:
                selected_labels.append(item.text())
        if not selected_labels:
            QMessageBox.warning(self, translations[self.language]["window_title"],
                                translations[self.language]["error_no_label"])
            return
        timestamp = self.slider.value()
        rect = self.video_label.annotation_rect
        factor = self.scale_factor if self.scale_factor != 0 else 1
        x1 = int(rect.left() / factor)
        y1 = int(rect.top() / factor)
        x2 = int(rect.right() / factor)
        y2 = int(rect.bottom() / factor)
        annotation = {
            "timestamp": timestamp,
            "top_left": [x1, y1],
            "bottom_right": [x2, y2],
            "labels": selected_labels
        }
        # 改为：如果该帧已有标注，则追加，否则新建列表
        ts_key = str(timestamp)
        if ts_key in self.annotations_data["frame_annotations"]:
            self.annotations_data["frame_annotations"][ts_key].append(annotation)
        else:
            self.annotations_data["frame_annotations"][ts_key] = [annotation]
        QMessageBox.information(self, translations[self.language]["window_title"],
                                translations[self.language]["info_frame_annotation_added"])
        print("帧标注完成：", annotation)
        self.video_label.annotation_rect = None
        self.video_label.update()
        self.update_annotation_table()


    def start_segment_annotation(self):
        self.segment_start_time = None
        self.segment_end_time = None
        QMessageBox.information(self, translations[self.language]["window_title"],
                                "已清空段标注记录，请定位左区间和右区间。")

    def set_segment_left(self):
        self.segment_start_time = self.slider.value()
        if self.segment_end_time is not None and self.segment_end_time < self.segment_start_time:
            self.segment_start_time = self.segment_end_time - 1
        QMessageBox.information(self, translations[self.language]["window_title"],
                                f"左区间定位：{self.segment_start_time}")

    def set_segment_right(self):
        self.segment_end_time = self.slider.value()
        if self.segment_start_time is not None and self.segment_end_time < self.segment_start_time:
            self.segment_end_time = self.segment_start_time + 1
        QMessageBox.information(self, translations[self.language]["window_title"],
                                f"右区间定位：{self.segment_end_time}")

    def finish_segment_annotation(self):
        if self.segment_start_time is None or self.segment_end_time is None:
            QMessageBox.warning(self, translations[self.language]["window_title"],
                                "请先定位左右区间！")
            return
        selected_labels = []
        for i in range(self.label_list.count()):
            item = self.label_list.item(i)
            if item.checkState() == Qt.Checked:
                selected_labels.append(item.text())
        if not selected_labels:
            QMessageBox.warning(self, translations[self.language]["window_title"],
                                translations[self.language]["error_no_label"])
            return
        annotation = {
            "start": self.segment_start_time,
            "end": self.segment_end_time,
            "labels": selected_labels
        }
        self.annotations_data.setdefault("segment_annotations", []).append(annotation)
        QMessageBox.information(self, translations[self.language]["window_title"],
                                translations[self.language]["info_segment_annotation_added"])
        print("段标注完成：", annotation)
        self.update_annotation_table()

    def save_all(self):
        # 遍历标签列表构造旧→新映射
        mapping = {}
        new_tags = []
        for i in range(self.label_list.count()):
            item = self.label_list.item(i)
            new_tag = item.text().strip()
            new_tags.append(new_tag)
            old_tag = item.data(Qt.UserRole)
            if old_tag is None:
                old_tag = new_tag
            mapping[old_tag.strip()] = new_tag
            item.setData(Qt.UserRole, new_tag)
        data = self.annotations_data  # 使用内存中的数据

        # 更新帧标注中的标签
        for ts, ann_list in data.get("frame_annotations", {}).items():
            # 如果ann_list不是列表，但如果是字典，则包装成列表，否则跳过
            if not isinstance(ann_list, list):
                if isinstance(ann_list, dict):
                    ann_list = [ann_list]
                    data["frame_annotations"][ts] = ann_list
                else:
                    continue
            for annotation in ann_list:
                if not isinstance(annotation, dict):
                    continue  # 如果不是字典则跳过
                updated = []
                for tag in annotation.get("labels", []):
                    if isinstance(tag, str):
                        tag_clean = tag.strip()
                        updated.append(mapping.get(tag_clean, tag))
                    else:
                        updated.append(tag)
                annotation["labels"] = updated

        # 更新段标注中的标签
        for annotation in data.get("segment_annotations", []):
            if not isinstance(annotation, dict):
                continue
            updated = []
            for tag in annotation.get("labels", []):
                if isinstance(tag, str):
                    tag_clean = tag.strip()
                    updated.append(mapping.get(tag_clean, tag))
                else:
                    updated.append(tag)
            annotation["labels"] = updated

        data["tags"] = new_tags
        if self.video_path:
            data["video_name"] = os.path.basename(self.video_path)
        ann_file = self.get_annotation_file_path()
        if ann_file:
            with open(ann_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            QMessageBox.information(self, translations[self.language]["window_title"],
                                    translations[self.language]["info_data_saved"] + ann_file)
            print("保存成功，数据：", data)
        else:
            QMessageBox.warning(self, translations[self.language]["window_title"],
                                translations[self.language]["error_no_video_path"])
        self.update_annotation_table()

    def open_video(self):
        file_path, _ = QFileDialog.getOpenFileName(self, translations[self.language]["open_video"], "", "视频文件 (*.mp4 *.avi *.mov)")
        if file_path:
            self.video_path = file_path
            self.cap = cv2.VideoCapture(file_path)
            total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.slider.setRange(0, total_frames)
            self.video_width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            self.video_height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            if self.auto_scale:
                self.update_scale_factor()
            # 根据视频原始尺寸和 scale_factor 计算实际显示尺寸
            displayed_width = int(self.video_width * self.scale_factor)
            displayed_height = int(self.video_height * self.scale_factor)
            # 将 video_label 尺寸调整为视频实际显示尺寸
            self.video_label.setFixedSize(displayed_width, displayed_height)
            self.set_position(0)
            self.slider.setValue(0)
            self.play_video()
            data = self.load_annotations()
            self.annotations_data = data
            self.label_list.clear()
            for tag in data.get("tags", []):
                item = QListWidgetItem(tag)
                item.setData(Qt.UserRole, tag)
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable | Qt.ItemIsEditable)
                item.setCheckState(Qt.Unchecked)
                self.label_list.addItem(item)
            self.update_annotation_table()
            self.scale_btn.setEnabled(True)
            QTimer.singleShot(1, lambda: self.resize(self.layout().sizeHint()))


    def toggle_play_pause(self):
        if self.playing:
            self.pause_video()
        else:
            self.play_video()

    def play_video(self):
        if self.cap and not self.playing:
            self.timer.start(30)
            self.playing = True
            self.update_ui_texts()  # 这样会把按钮文本更新为“暂停”
            
    def pause_video(self):
        if self.playing:
            self.timer.stop()
            self.playing = False
            self.update_ui_texts()  # 更新为“播放”


    def close_video(self):
        if self.cap:
            self.timer.stop()
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.playing = False
            self.slider.setValue(0)
            self.video_label.clear()
            self.play_pause_btn.setText(translations[self.language]["play"])
            self.scale_btn.setEnabled(False)

    def scale_video(self):
        # 弹出缩放对话框，初始比例为当前 scale_factor
        dlg = ScaleDialog(self, initial_scale=self.scale_factor)
        if dlg.exec_() == QDialog.Accepted:
            self.scale_factor = dlg.get_scale()
        else:
            pass

    def update_scale_factor(self):
        available_width = self.width() - 300
        available_height = self.height() - 120
        if self.video_width and self.video_height:
            self.scale_factor = min(available_width / self.video_width, available_height / self.video_height)

    def set_position(self, position):
        if self.cap:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, position)
            if not self.playing:
                ret, frame = self.cap.read()
                if ret:
                    frame = cv2.resize(frame, (0, 0), fx=self.scale_factor, fy=self.scale_factor)
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    height, width, channel = frame.shape
                    bytes_per_line = 3 * width
                    qimg = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
                    self.video_label.setPixmap(QPixmap.fromImage(qimg))
            total = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            current = position
            self.video_label.frame_info = f"{current}/{total}"
            # 如果帧发生改变（单击或拖动），清除展示的标注框
            self.video_label.annotation_rect = None
            self.video_label.update()


    def next_frame(self):
        if self.cap:
            ret, frame = self.cap.read()
            if ret:
                current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
                total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
                self.video_label.frame_info = f"{current_frame}/{total_frames}"
                frame = cv2.resize(frame, (0, 0), fx=self.scale_factor, fy=self.scale_factor)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                height, width, channel = frame.shape
                bytes_per_line = 3 * width
                qimg = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
                self.video_label.setPixmap(QPixmap.fromImage(qimg))
                self.slider.setValue(current_frame)
                # 每次刷新帧时清除已展示的标注框
                self.video_label.annotation_rect = None
                self.video_label.update()
            else:
                self.timer.stop()
                self.playing = False
                self.play_pause_btn.setText(translations[self.language]["play"])

    def update_video_display_size(self):
        if self.video_width and self.video_height:
            pos = self.slider.value()
            displayed_width = int(self.video_width * self.scale_factor)
            displayed_height = int(self.video_height * self.scale_factor)
            self.video_label.setFixedSize(displayed_width, displayed_height)
        QTimer.singleShot(1, lambda: self.resize(self.layout().sizeHint()))
        self.set_position(pos)


    def resizeEvent(self, event):
        if self.cap and self.video_width and self.video_height:
            displayed_width = int(self.video_width * self.scale_factor)
            displayed_height = int(self.video_height * self.scale_factor)
            self.video_label.setFixedSize(displayed_width, displayed_height)
        super().resizeEvent(event)



    def open_options(self):
        dialog = OptionsDialog(self, current_language=self.language, auto_scale=self.auto_scale)
        if dialog.exec_() == QDialog.Accepted:
            settings = dialog.get_settings()
            self.language = settings["language"]
            print("更新设置:", settings)
            self.update_ui_texts()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec_())
