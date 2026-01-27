from PyQt5 import QtCore, QtWidgets, QtMultimedia

BlackIdx = 1, 3, -1, 6, 8, 10
WhiteIdx = 0, 2, 4, 5, 7, 9, 11
KeyNames = 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'


class KeyButton(QtWidgets.QPushButton):
    triggered = QtCore.pyqtSignal(int, bool)

    def __init__(self, key, isBlack=False):
        super().__init__()
        self.key = key
        self.setProperty('isBlack', isBlack)

        octave, keyIdx = divmod(key, 12)

        self.setMinimumWidth(25)
        self.setMinimumSize(25, 80 if isBlack else 120)

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred,
            QtWidgets.QSizePolicy.Expanding
        )
        self.pressed.connect(lambda: self.triggered.emit(key, True))
        self.released.connect(lambda: self.triggered.emit(key, False))


class Keyboard(QtWidgets.QWidget):
    def __init__(self, octaves=2, octaveStart=3):
        super().__init__()

        self.load_mp3()

        layout = QtWidgets.QGridLayout(self)
        layout.setRowStretch(0, 2)
        layout.setRowStretch(1, 1)
        layout.setSpacing(0)

        blackKeys = []
        for octave in range(octaves):
            for k in range(12):
                isBlack = k in BlackIdx
                keyButton = KeyButton(k + (octaveStart + octave) * 12, isBlack)
                keyButton.triggered.connect(self.keyTriggered)
                if isBlack:
                    keyPos = BlackIdx.index(k)
                    col = keyPos * 3 + 2
                    vSpan = 1
                    hSpan = 2
                    blackKeys.append(keyButton)
                else:
                    keyPos = WhiteIdx.index(k)
                    col = keyPos * 3
                    vSpan = 2
                    hSpan = 3
                col += octave * 21
                layout.addWidget(keyButton, 0, col, vSpan, hSpan)

            efSpacer = QtWidgets.QWidget()
            efSpacer.setMinimumWidth(25)
            layout.addWidget(efSpacer, 0, octave * 21 + 8, 1, 2)
            efSpacer.lower()
            baSpacer = QtWidgets.QWidget()
            baSpacer.setMinimumWidth(25)
            layout.addWidget(baSpacer, 0, octave * 21 + 20, 1, 2)
            baSpacer.lower()

        octave += 1
        lastButton = KeyButton((octaveStart + octave) * 12)
        lastButton.setMinimumWidth(32)
        lastButton.triggered.connect(self.keyTriggered)
        layout.addWidget(lastButton, 0, octave * 21, 2, 3)

        for keyButton in blackKeys:
            keyButton.raise_()

        for col in range(layout.columnCount()):
            if col % 3 == 1:
                layout.setColumnStretch(col, 4)
            else:
                layout.setColumnStretch(col, 3)

        self.setStyleSheet('''
            KeyButton {
                border: 1px outset palette(dark);
                border-radius: 2px;
                background: white;
            }
            KeyButton:pressed {
                border-style: inset;
            }
            KeyButton[isBlack=true] {
                color: palette(light);
                background: black;
            }
            KeyButton[isBlack=true]:pressed {
                background: rgb(50, 50, 50);
            }
        ''')

    def keyTriggered(self, key, pressed):
        octave, keyIdx = divmod(key, 12)
        keyName = '{}{}'.format(KeyNames[keyIdx], octave)
        state = 'pressed' if pressed else 'released'
        print('Key {} ({}) {}'.format(key, keyName, state))

        if state == 'pressed':
            if keyName == 'C4' or keyName == 'C3' or keyName == 'C5' or keyName == 'G#3':
                self.si.play()
            elif keyName == 'D4' or keyName == 'D3' or keyName == 'C#3' or keyName == 'D#4':
                self.fa.play()
            elif keyName == 'E4' or keyName == 'E3' or keyName == 'F#3' or keyName == 'G#4':
                self.lja.play()
            elif keyName == 'F4' or keyName == 'F3' or keyName == 'D#3' or keyName == 'A#4':
                self.mi.play()
            elif keyName == 'G4' or keyName == 'G3' or keyName == 'A#3':
                self.do.play()
            elif keyName == 'A4' or keyName == 'A3' or keyName == 'F#4':
                self.re.play()
            elif keyName == 'B4' or keyName == 'B3' or keyName == 'C#4':
                self.sol.play()

    def load_mp3(self):
        fa = QtCore.QUrl.fromLocalFile('sounds/fa.mp3')
        self.fa = QtMultimedia.QMediaPlayer()
        self.fa.setMedia(QtMultimedia.QMediaContent(fa))
        self.fa.setVolume(50)

        lja = QtCore.QUrl.fromLocalFile('sounds/lja.mp3')
        self.lja = QtMultimedia.QMediaPlayer()
        self.lja.setMedia(QtMultimedia.QMediaContent(lja))
        self.lja.setVolume(50)

        mi = QtCore.QUrl.fromLocalFile('sounds/mi.mp3')
        self.mi = QtMultimedia.QMediaPlayer()
        self.mi.setMedia(QtMultimedia.QMediaContent(mi))
        self.mi.setVolume(50)

        do = QtCore.QUrl.fromLocalFile('sounds/noty-do.mp3')
        self.do = QtMultimedia.QMediaPlayer()
        self.do.setMedia(QtMultimedia.QMediaContent(do))
        self.do.setVolume(50)

        re = QtCore.QUrl.fromLocalFile('sounds/re.mp3')
        self.re = QtMultimedia.QMediaPlayer()
        self.re.setMedia(QtMultimedia.QMediaContent(re))
        self.re.setVolume(50)

        si = QtCore.QUrl.fromLocalFile('sounds/si.mp3')
        self.si = QtMultimedia.QMediaPlayer()
        self.si.setMedia(QtMultimedia.QMediaContent(si))
        self.si.setVolume(50)

        sol = QtCore.QUrl.fromLocalFile('sounds/sol.mp3')
        self.sol = QtMultimedia.QMediaPlayer()
        self.sol.setMedia(QtMultimedia.QMediaContent(sol))
        self.sol.setVolume(50)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    keyboard = Keyboard()
    keyboard.show()
    sys.exit(app.exec_())