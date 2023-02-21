if not __package__:
    import os
    import sys
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), os.pardir)
    sys.path.insert(0, path)


import traceback

from PyQt5 import  QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QSizePolicy, QVBoxLayout
#---------------------------------------------
from matplotlib import font_manager as fm
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
#---------------------------------------------
from Library_Foxconn.Chart.Pie_Chart.Ui_chart import Ui_ChartForm
# from Pie_Chart.Ui_chart import Ui_ChartForm


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        #------------------------------------------
        # Setup the show of chinese word
        plt.rcParams['font.family'] = ['SimHei']            # Show chinese lable 
        plt.rcParams['axes.unicode_minus'] = False          # Show negative 
        #------------------------------------------
        self.fig = Figure(figsize=(width, height), dpi=dpi) # Create a drawing object
        #------------------------------------------
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        #------------------------------------------
        '''定义FigureCanvas的尺寸策略，这部分的意思是设置FigureCanvas，使之尽可能的向外填充空间。'''
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        #------------------------------------------
        self.chart_title = ""
        self.legend_title = ""
        self.pcts = []
        self.items = []
        self.sizes = []
        self.colors = []
        self.font_size = 9
        self.pct_size = 9
        #------------------------------------------
        self.fig.clear()

    def clear(self):
        self.fig.clear()
        self.draw()


    def set_pct_size(self, value):
        try:
            self.pct_size = value
            return True
        except:
            traceback.print_exc()
            return False


    def set_font_size(self, value):
        try:
            self.font_size = value
            return True
        except:
            traceback.print_exc()
            return False

    def set_colors(self, value):
        try:
            self.colors = value
            return True
        except:
            traceback.print_exc()
            return False

    def set_percentages(self, value):
        try:
            self.pcts = value
            return True
        except:
            traceback.print_exc()
            return False

    def set_items(self, value):
        try:
            self.items = value
            return True
        except:
            traceback.print_exc()
            return False



    # def ini_chart_data(self, num=0):
    #     try:
    #         self.listAxesData.clear()
    #         for i in range(num):
    #             self.listAxesData.append([])
    #             self.listAxesData[i].append("")
    #             self.listAxesData[i].append([])
    #     except:
    #         traceback.print_exc()
    #         return False

    # def enable_legend(self):
    #     self.bolLabel = True
    # def disable_legend(self):
    #     self.bolLabel = False

    def set_chart_grid(self, value=True):
        self.bolGrid = value

    def set_chart_subtitle(self, title=""):
        self.chart_title = title
        self.fig.suptitle(title)

        # self.strTitle = strTitle

    def show_chart(self):
        try:
            #--------------------------------------------------------
            # proptease
            proptease_font = fm.FontProperties()
            proptease_font.set_size(self.font_size)

            proptease_pcts = fm.FontProperties()
            proptease_pcts.set_size(self.pct_size)


            # labels = ["Fail","Pass"]
            # size = [10,90]
            # colors = ["red","green"]

            axes = self.fig.add_subplot(111)
            #--------------------------------------------------------
            wedges, texts, autotexts = axes.pie(self.pcts, 
                                                labels=self.items,
                                                autopct="%1.1f%%",
                                                colors=self.colors)
            #--------------------------------------------------------
            if self.legend_title != "":
                # axes.axis("off")
                axes.legend(title=self.legend_title,loc='left')
                # plt.tight_layout()

            plt.setp(autotexts, fontproperties=proptease_pcts)
            plt.setp(texts, fontproperties=proptease_font)

            self.draw()
        except Exception:
            traceback.print_exc()


class CtrlPiChart(QtWidgets.QWidget, Ui_ChartForm):
    def __init__(self, toolbar=False): 
        super().__init__()
        self.setupUi(self)

        # self.layout = QVBoxLayout(self)
        self.mpl = MplCanvas(self, width=5, height=4, dpi=100)
        self.gridLayout.addWidget(self.mpl)
        if toolbar:
            self.mpl_ntb = NavigationToolbar(self.mpl, self)  # 添加完整的 toolbar
            self.gridLayout.addWidget(self.mpl_ntb)
        
        self.gridLayout.setContentsMargins(0,0,0,0)



if __name__ == "__main__":
    from PyQt5.QtWidgets import QMainWindow, QApplication
    strCurrPath = os.getcwd()
    app = QApplication(sys.argv)
    MyWin = CtrlPiChart()

    #---------------------------------------------------------------
    # MyWin.mpl.set_chart_subtitle("Chart")
    MyWin.mpl.set_colors(["red","green"])
    MyWin.mpl.set_percentages([10,90])
    MyWin.mpl.set_items(["FAIL","PASS"])
    MyWin.mpl.set_font_size(18)
    MyWin.mpl.set_pct_size(10)
    MyWin.mpl.legend_title = "Test Result"
    MyWin.mpl.show_chart()

    MyWin.mpl.clear()

    #---------------------------------------------------------------
    MyWin.show()
    sys.exit(app.exec_())
    print()


 
# if __name__ == "__main__":
#     from PyQt5.QtWidgets import QMainWindow, QApplication
#     strCurrPath = os.getcwd()
#     app = QApplication(sys.argv)
#     MyWin = CtrlChart()
#     #---------------------------------------------------------------
#     listData = []
#     listLine1st = []
#     listLine2nd = []
#     listLineX = [0,1,2,3,4]
#     listLineY = [2,100,4,2,2]
#     listLineY2 = [2,50,4,2,2]


#     listLine1st.append("Line1")
#     listLine1st.append(listLineY)

#     listLine2nd.append("Line2")
#     listLine2nd.append(listLineY2)
    
#     listData.append(listLine1st)
#     listData.append(listLine2nd)

#     #---------------------------------------------------------------
#     MyWin.mpl.ini_chart_data(2)
#     MyWin.mpl.set_chart_subtitle("Chart")
#     MyWin.mpl.set_axes_data(value=listData, axes_x=listLineX)
#     MyWin.mpl.set_chart_grid(True)
#     MyWin.mpl.set_axes_x_name("Frequency")
#     MyWin.mpl.set_axes_y_name("Amplitude")
#     MyWin.mpl.enable_legend()
#     MyWin.mpl.show_chart()
#     #---------------------------------------------------------------
#     MyWin.show()
#     sys.exit(app.exec_())






