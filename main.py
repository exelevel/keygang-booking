import sys
import os
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QThread, pyqtSignal

# 1. 실제 매크로 로직이 돌아갈 별도의 쓰레드 (중요!)
class MacroWorker(QThread):
    status_signal = pyqtSignal(str)  # UI에 상태 메시지를 전달하기 위한 신호

    def run(self):
        # 여기에 나중에 Selenium 로직이 들어갑니다.
        self.status_signal.emit("매크로를 시작합니다...")
        # (예시) 작업 수행 중...
        self.status_signal.emit("브라우저 실행 중...")

# 2. 메인 윈도우 클래스
class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Qt Designer에서 만든 ui 파일을 로드합니다.
        uipath = os.path.join(os.getcwd(), "src", "gui", "keygang_booking.ui")
        uic.loadUi("ticketing_main.ui", self) 

        # UI에 있는 버튼 이름이 'start_btn'이라고 가정합니다.
        self.start_btn.clicked.connect(self.start_macro)
        
        # 로그를 보여줄 QTextEdit 이름이 'log_text'라고 가정합니다.
        self.worker = MacroWorker()
        self.worker.status_signal.connect(self.update_log)

    def start_macro(self):
        # 버튼을 누르면 쓰레드 시작
        self.update_log("버튼 클릭됨: 준비 중...")
        self.worker.start()

    def update_log(self, text):
        # 쓰레드에서 받은 메시지를 UI에 출력
        self.log_text.append(text)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())