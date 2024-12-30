from PySide6.QtWidgets import QLabel,QGraphicsOpacityEffect
from PySide6.QtCore import QPropertyAnimation,QAbstractAnimation

"""
Script dedicated to designing animation effects for the GUI
"""

class OpacityEffect(QLabel):
    """
    Designing a fading effect for the Values Copied prompt
    """
    def __init__(self,*args,**kwargs):
        QLabel.__init__(self,*args,**kwargs)

        self.opacityEffect = QGraphicsOpacityEffect(self)
        self.opacityEffect.setOpacity(1.0)
        self.setGraphicsEffect(self.opacityEffect)
        self.opacityAnim = QPropertyAnimation(self.opacityEffect,b'opacity')
        self.opacityAnim.setDuration(2500)
        self.opacityAnim.finished.connect(self.animation_finished)
    
    def showEvent(self,event):
        self.opacityAnim.setDirection(QAbstractAnimation.Forward)
        if self.opacityAnim.state() == self.opacityAnim.State.Stopped:
            self.opacityAnim.setStartValue(1)
            self.opacityAnim.setEndValue(0)
            self.opacityAnim.start()
        QLabel.showEvent(self,event)
    
    def animation_finished(self):
        self.hide()