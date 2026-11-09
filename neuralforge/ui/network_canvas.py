"""Interactive painter-based network architecture canvas."""
from PySide6.QtCore import Qt, Signal, QRectF, QPointF
from PySide6.QtGui import QPainter, QPen, QBrush, QColor, QFont
from PySide6.QtWidgets import QWidget

class NetworkCanvas(QWidget):
    layer_selected = Signal(int)
    def __init__(self, parent=None):
        super().__init__(parent); self.layers=[]; self.selected=-1
        self.setMinimumHeight(280); self.setMinimumWidth(520)
    def set_layers(self, layers):
        self.layers=list(layers); self.update()
    def _rects(self):
        if not self.layers:return []
        margin=45; gap=max(1,self.width()-2*margin)/max(1,len(self.layers)-1)
        y=max(24,(self.height()-72)/2)
        return [QRectF(margin+i*gap-56,y,112,72) for i in range(len(self.layers))]
    def paintEvent(self,event):
        p=QPainter(self); p.setRenderHint(QPainter.Antialiasing)
        p.fillRect(self.rect(),QColor("#f7f3e9")); p.setPen(QPen(QColor("#e5dfd2"),1))
        for x in range(0,self.width(),24):p.drawLine(x,0,x,self.height())
        for y in range(0,self.height(),24):p.drawLine(0,y,self.width(),y)
        rects=self._rects()
        if not rects:
            p.setPen(QColor("#655e50")); p.drawText(self.rect(),Qt.AlignCenter,"Add layers to preview your network"); return
        p.setPen(QPen(QColor("#87917b"),2))
        for a,b in zip(rects,rects[1:]):p.drawLine(a.right(),a.center().y(),b.left(),b.center().y())
        for i,(r,layer) in enumerate(zip(rects,self.layers)):
            p.setPen(QPen(QColor("#68775d") if i==self.selected else QColor("#a99f8c"),2))
            p.setBrush(QBrush(QColor("#dce3d2") if i==self.selected else QColor("#eee8da")))
            p.drawRoundedRect(r,3,3); p.setPen(QColor("#302d27"))
            p.setFont(QFont("Tahoma",9,QFont.Bold)); p.drawText(QRectF(r.x()+4,r.y()+8,r.width()-8,22),Qt.AlignCenter,layer.kind)
            p.setFont(QFont("Tahoma",8)); p.drawText(QRectF(r.x()+4,r.y()+30,r.width()-8,34),Qt.AlignCenter,f"{layer.units} units\n{layer.activation}")
        p.end()
    def mousePressEvent(self,event):
        for i,r in enumerate(self._rects()):
            if r.contains(QPointF(event.position())):
                self.selected=i; self.layer_selected.emit(i); self.update(); return
