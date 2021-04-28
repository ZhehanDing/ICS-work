import sys

import c as c
from button import *
import spacewar.spacewar as sp


class UI (QWidget) :
    def __init__ (self, parent=None, **kwargs) :
        super (UI, self).__init__ (parent)

        self.setFixedSize (577, 565)
        self.setWindowTitle ('GAME')

        palette = QPalette ()
        palette.setBrush (self.backgroundRole (), QBrush (QPixmap ('1.png')))
        self.setPalette (palette)

        self.b_button = PushButton (c.BUTTON.get ('a'), self)
        self.b_button.move (175, 100)
        self.b_button.show ()
        self.b_button.click_signal.connect (self.game)

        self.b_button1 = PushButton (c.BUTTON.get ('b'), self)
        self.b_button1.move (175, 175)
        self.b_button1.show ()

        self.b_button2 = PushButton (c.BUTTON.get ('b'), self)
        self.b_button2.move (175, 255)
        self.b_button2.show ()

    def game (self) :
        self.close ()
        self.gaming = sp.main ()
        self.gaming.show ()

    '''run'''


def main () :
    app = QApplication (sys.argv)
    handle = UI ()

    handle.show ()
    sys.exit (app.exec_ ())


