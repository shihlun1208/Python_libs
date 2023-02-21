if not __package__:
    import os
    import sys
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), os.pardir)
    sys.path.insert(0, path)


# from Library_Foxconn.File.pandas_csv import value
import numpy as np
import traceback
import enum
import copy

from PyQt5 import  QtWidgets
from PyQt5.QtWidgets import QSizePolicy, QVBoxLayout
#---------------------------------------------
import matplotlib
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
# from matplotlib import markers
#---------------------------------------------
from Library_Foxconn.Chart.Line_Chart.Ui_chart import Ui_ChartForm


class PayloadLineChart(enum.Enum):
    NAME = "name"
    Y_AXES_DATA = "y_axes_data"
    X_AXES_DATA = "x_axes_data"
    Y_LABEL = "y_label"
    COLOR = "color"
    MARKER = "marker"
    MARKER_FACECOLOR = "marker_facecolor"
    MARKER_SIZE = "marker_size"

    TEXT = "text"
    TEXT_X = "text_x"
    TEXT_Y = "text_y"
    TEXT_COLOR = "text_color"
    TEXT_SIZE = "text_size"
    TEXT_HORIZONTAL = "text_horizontal"
    TEXT_VERTICAL = "text_vertical"

    LEGEND_LOC = "legend_loc"
    LEGEND_X_SCALE = "legend_x_scale"
    LEGEND_Y_SCALE = "legend_y_scale"

class LegendLocate(enum.Enum):
    BEST = "best"
    UPPER_RIGHT = "upper right"
    UPPER_LEFT = "upper left"
    LOWER_LEFT = "lower left"
    LOWER_RIGHT = "lower right"
    RIGHT = "right"
    CENTER_LEFT = "center left"
    CENTER_RIGTH = "center right"
    LOWER_CENTER = "lower center"
    UPPER_CENTER = "upper center"
    CENTER = "center"



class COLOR(enum.Enum):
    BLUE = "blue"
    CYAN = "cyan"
    GREEN = "green"
    BLACK = "black"
    MAGENTA = "magenta"
    RED = "red"
    WHITE = "white"
    YELLOW = "yellow"

class HorizontalLoc(enum.Enum):
    CENTER = "center"
    RIGHT = "right"
    LEFT = "left"

class VerticalLoc(enum.Enum):
    CENTER = "center"
    TOP = "top"
    BOTTOM = "bottom"



class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        #------------------------------------------
        # Setup the show of chinese word
        # plt.rcParams['font.family'] = ['SimHei']            # Show chinese lable 
        # plt.rcParams['axes.unicode_minus'] = False          # Show negative 
        # plt.margins(x=10)
        matplotlib.rcParams['font.sans-serif'] = "Console"
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
        # matplotlib.

        self.strAxesNameX = ""
        self.strAxesNameY = ""
        self.strTitle = ""
        self.listAxesX = []
        self.listAxesData = []
        self.bolGrid = False
        self.bolLegend = False

        self.y_lim = []
        self.x_lim = []
        self.x_stick = []
        self.y_stick = []
        #--------------------------------------------------
        self.__ini_Payloads()
        self.__ini_text()
        self.__ini_legend()


    def __ini_legend(self):
        try:
            self.payload_legend = {
                PayloadLineChart.LEGEND_LOC.value : None,
                PayloadLineChart.LEGEND_X_SCALE.value: None,
                PayloadLineChart.LEGEND_Y_SCALE.value: None
            }
        except:
            traceback.print_exc()


    def __ini_text(self):
        try:
            self.payload_text = {
                    PayloadLineChart.TEXT.value : None,
                    PayloadLineChart.TEXT_X.value : None,
                    PayloadLineChart.TEXT_Y.value : None,
                    PayloadLineChart.TEXT_COLOR.value : None,
                    PayloadLineChart.TEXT_SIZE.value : None,
                    PayloadLineChart.TEXT_HORIZONTAL.value: None,
                    PayloadLineChart.TEXT_VERTICAL.value: None
            }
        except:
            traceback.print_exc()


    def __ini_Payloads(self):
        self.payloads = {
            PayloadLineChart.Y_AXES_DATA.value: None,
            PayloadLineChart.X_AXES_DATA.value: None,
            PayloadLineChart.Y_LABEL.value: None,
            PayloadLineChart.COLOR.value: None,
            PayloadLineChart.NAME.value: None
        }

    #---------------------------------------------------------------
    def add_new_line(self, name=""):
        try:
            temp_payload = copy.deepcopy(self.payloads)
            temp_payload.update({PayloadLineChart.NAME.value: name})
            self.listAxesData.append(temp_payload)
        except:
            traceback.print_exc()
            return False        


    def adjust_bottom_size(self, value=0):
        try:
            self.fig.subplots_adjust(bottom=value)
        except:
            traceback.print_exc()


    def set_legend(self, loc=LegendLocate.BEST.value):
        try:
            self.payload_legendx.update({loc})
        except:
            traceback.print_exc()


    def set_text(self, 
                        text=None,
                        coord_x=None,
                        coord_y=None,
                        color=COLOR.BLACK.value,
                        size=15,
                        horizontal=HorizontalLoc.CENTER.value,
                        vertical=VerticalLoc.CENTER.value                        
                        ):
        try:
            self.payload_text.update({
                            PayloadLineChart.TEXT.value : text,
                            PayloadLineChart.TEXT_X.value : coord_x,
                            PayloadLineChart.TEXT_Y.value : coord_y,
                            PayloadLineChart.TEXT_COLOR.value : color,
                            PayloadLineChart.TEXT_SIZE.value : size,
                            PayloadLineChart.TEXT_HORIZONTAL.value : horizontal,
                            PayloadLineChart.TEXT_VERTICAL.value : vertical                        
            })
        except:
            traceback.print_exc()
            pass


    def set_axes_data(self, index=0, 
                            y_data=None, 
                            x_data=None, 
                            y_label=None,
                            color=None,
                            marker=None,
                            markerfacecolor=None,
                            markersize=None
                            ):
        try:
            if y_data != None:
                self.listAxesData[index].update({
                        PayloadLineChart.Y_AXES_DATA.value: y_data
                })
            if x_data != None:
                self.listAxesData[index].update({
                        PayloadLineChart.X_AXES_DATA.value: x_data
                })
            if y_label != None:
                self.listAxesData[index].update({
                        PayloadLineChart.Y_LABEL.value: y_label
                })
            if color != None:
                self.listAxesData[index].update({
                        PayloadLineChart.COLOR.value: color
                })
            if marker != None:
                self.listAxesData[index].update({
                        PayloadLineChart.MARKER.value: marker
                })                
            if markerfacecolor != None:
                self.listAxesData[index].update({
                        PayloadLineChart.MARKER_FACECOLOR.value: markerfacecolor
                })                
            if markersize != None:
                self.listAxesData[index].update({
                        PayloadLineChart.MARKER_SIZE.value: markersize
                })                
        except:
            traceback.print_exc()
            return False        


    def enable_grid(self):
        self.bolGrid = True
    def disable_grid(self):
        self.bolGrid = False


    def __get_list_y_label(self):
        try:
            list_y_label = []
            for i in range(len(self.listAxesData)):
                temp_axes_data = self.listAxesData[i]
                y_label = temp_axes_data.get(PayloadLineChart.Y_LABEL.value)
                list_y_label.append(y_label)
            return list_y_label
        except:
            traceback.print_exc()
            return None


    def set_chart_show(self):
        try:
            perm_x_data = None
            perm_axes = None
            #-------------------------------------------------
            self.fig.clear()
            self.fig.suptitle(self.strTitle)
            axes = self.fig.add_subplot(111)                   # Disable Warning 将标题与刻度放在绘制图画之后

            # axes.annotate('local maximum')
            #-------------------------------------------------
            # text
            text = self.payload_text.get(PayloadLineChart.TEXT.value)
            if text != None:
                coord_x = self.payload_text.get(PayloadLineChart.TEXT_X.value)
                coord_y = self.payload_text.get(PayloadLineChart.TEXT_Y.value)
                text_horizontal = self.payload_text.get(PayloadLineChart.TEXT_HORIZONTAL.value)
                text_vertical = self.payload_text.get(PayloadLineChart.TEXT_VERTICAL.value)
                text_color = self.payload_text.get(PayloadLineChart.TEXT_COLOR.value)
                text_size = self.payload_text.get(PayloadLineChart.TEXT_SIZE.value)

                axes.text(coord_x, coord_y, text,
                            verticalalignment=text_vertical, 
                            horizontalalignment=text_horizontal,
                            transform=axes.transAxes,
                            color=text_color, 
                            fontsize=text_size)
                
            #-------------------------------------------------
            for i in range(len(self.listAxesData)):
                temp_axes_data = self.listAxesData[i]
                x_data = temp_axes_data.get(PayloadLineChart.X_AXES_DATA.value)
                if i == 0:
                    perm_x_data = x_data
                elif (i != 0 and x_data == None):
                    x_data = perm_x_data
                y_data = temp_axes_data.get(PayloadLineChart.Y_AXES_DATA.value)
                color = temp_axes_data.get(PayloadLineChart.COLOR.value)
                y_label = temp_axes_data.get(PayloadLineChart.Y_LABEL.value)
                marker = temp_axes_data.get(PayloadLineChart.MARKER.value)
                markerfacecolor = temp_axes_data.get(PayloadLineChart.MARKER_FACECOLOR.value)
                markersize = temp_axes_data.get(PayloadLineChart.MARKER_SIZE.value)
                #----------------------------------------------------------------------
                if y_data != None:
                    axes.plot(x_data, y_data, 
                                label=y_label,
                                color=color,
                                marker=marker,
                                markerfacecolor=markerfacecolor,
                                markersize=markersize
                                )
                    
                if i == 0:
                    perm_axes = axes

            if len(self.listAxesData):
                temp_axes_data = self.listAxesData[0]
                perm_axes.set_xlabel(self.strAxesNameX)
                perm_axes.set_ylabel(self.strAxesNameY)
                self.__set_x_lim(perm_axes)
                self.__set_y_lim(perm_axes)
                self.__set_x_stick(perm_axes)
                self.__set_y_stick(perm_axes)
                # perm_axes.set_yticks(np.arange(0, 60, 5))
                perm_axes.grid(self.bolGrid)
                if self.bolLegend:
                    legend_loc = self.payload_legend.get(PayloadLineChart.LEGEND_LOC.value)
                    legend_x_scale = self.payload_legend.get(PayloadLineChart.LEGEND_X_SCALE.value)
                    legend_y_scale = self.payload_legend.get(PayloadLineChart.LEGEND_Y_SCALE.value)
                    list_y_label = self.__get_list_y_label()
                    if legend_x_scale != None and legend_y_scale != None:
                        perm_axes.legend(list_y_label,bbox_to_anchor=(legend_x_scale, legend_y_scale))
                    else:
                        perm_axes.legend(list_y_label,loc=legend_loc)
            self.draw()
        except Exception:
            traceback.print_exc()


    def savefig(self,path=""):
        try:
            perm_x_data = None
            perm_axes = None
            #-------------------------------------------------
            self.fig.clear()
            self.fig.suptitle(self.strTitle)
            axes = self.fig.add_subplot(111) 
            # axes = None
            #-------------------------------------------------
            # text
            text = self.payload_text.get(PayloadLineChart.TEXT.value)
            if text != None:
                coord_x = self.payload_text.get(PayloadLineChart.TEXT_X.value)
                coord_y = self.payload_text.get(PayloadLineChart.TEXT_Y.value)
                text_horizontal = self.payload_text.get(PayloadLineChart.TEXT_HORIZONTAL.value)
                text_vertical = self.payload_text.get(PayloadLineChart.TEXT_VERTICAL.value)
                text_color = self.payload_text.get(PayloadLineChart.TEXT_COLOR.value)
                text_size = self.payload_text.get(PayloadLineChart.TEXT_SIZE.value)

                axes.text(coord_x, coord_y, text,
                            verticalalignment=text_vertical, 
                            horizontalalignment=text_horizontal,
                            transform=axes.transAxes,
                            color=text_color, 
                            fontsize=text_size)
            #-------------------------------------------------
            for i in range(len(self.listAxesData)):
                # if i == 0:
                #     axes = self.fig.add_subplot(111)
                    
                temp_axes_data = self.listAxesData[i]
                x_data = temp_axes_data.get(PayloadLineChart.X_AXES_DATA.value)
                if i == 0:
                    perm_x_data = x_data
                elif (i != 0 and x_data == None):
                    x_data = perm_x_data
                y_data = temp_axes_data.get(PayloadLineChart.Y_AXES_DATA.value)
                color = temp_axes_data.get(PayloadLineChart.COLOR.value)
                y_label = temp_axes_data.get(PayloadLineChart.Y_LABEL.value)
                marker = temp_axes_data.get(PayloadLineChart.MARKER.value)
                markerfacecolor = temp_axes_data.get(PayloadLineChart.MARKER_FACECOLOR.value)
                markersize = temp_axes_data.get(PayloadLineChart.MARKER_SIZE.value)
                #----------------------------------------------------------------------
                if y_data != None:
                    axes.plot(x_data, y_data, 
                                label=y_label,
                                color=color,
                                marker=marker,
                                markerfacecolor=markerfacecolor,
                                markersize=markersize                            
                                )

                if i == 0:
                    perm_axes = axes

            if len(self.listAxesData):
                temp_axes_data = self.listAxesData[0]
                perm_axes.set_xlabel(self.strAxesNameX)
                perm_axes.set_ylabel(self.strAxesNameY)                
                self.__set_x_lim(perm_axes)
                self.__set_y_lim(perm_axes)
                self.__set_x_stick(perm_axes)
                self.__set_y_stick(perm_axes)
                perm_axes.grid(self.bolGrid)
                if self.bolLegend:
                    legend_loc = self.payload_legend.get(PayloadLineChart.LEGEND_LOC.value)
                    legend_x_scale = self.payload_legend.get(PayloadLineChart.LEGEND_X_SCALE.value)
                    legend_y_scale = self.payload_legend.get(PayloadLineChart.LEGEND_Y_SCALE.value)
                    list_y_label = self.__get_list_y_label()
                    if legend_x_scale != None and legend_y_scale != None:
                        perm_axes.legend(list_y_label,bbox_to_anchor=(legend_x_scale, legend_y_scale))
                    else:
                        perm_axes.legend(list_y_label,loc=legend_loc)

            self.fig.savefig(path, bbox_inches='tight')
            return True
        except:
            traceback.print_exc()
            return False




    def __set_x_lim(self, axes):
        try:
            if len(self.x_lim):
                axes.set_xlim(self.x_lim)
            return True
        except:
            traceback.print_exc()
            return False


    def __set_y_lim(self, axes):
        try:
            if len(self.y_lim):
                axes.set_ylim(self.y_lim)
            return True
        except:
            traceback.print_exc()
            return False

    def __set_y_stick(self, axes):
        try:
            if len(self.y_stick):
                axes.set_yticks(self.y_stick)
            return True
        except:
            traceback.print_exc()
            return False

    def __set_x_stick(self, axes):
        try:
            if len(self.x_stick):
                axes.set_xticks(self.x_stick)
            return True
        except:
            traceback.print_exc()
            return False

    #---------------------------------------------------------------


    def ini_chart_data(self, num=0):
        try:
            self.listAxesData.clear()
            for i in range(num):
                self.listAxesData.append([])
                self.listAxesData[i].append("")
                self.listAxesData[i].append([])
        except:
            traceback.print_exc()
            return False


    def set_xlime(self, axes_range=[]):
        try:
            self.x_lim = axes_range
            return True
        except:
            traceback.print_exc()
            return False

    def set_ylime(self, axes_range=[]):
        try:
            self.y_lim = axes_range
            return True
        except:
            traceback.print_exc()
            return True

    def set_y_stick(self, min, max, step):
        try:
            self.y_stick = np.arange(min, max, step)
            return True
        except:
            traceback.print_exc()
            return True

    def set_x_stick(self, min, max, step):
        try:
            self.x_stick = np.arange(min, max, step)
            return True
        except:
            traceback.print_exc()
            return True


    def enable_legend(self):
        self.bolLegend = True
    def disable_legend(self):
        self.bolLegend = False

    def set_chart_grid(self, value=True):
        self.bolGrid = value

    # def set_text(self, text=""):
    #     try:
    #         self.fig.text(15, -0.01, "Correlation Graph between Citation & Favorite Count")
    #         pass
    #     except:
    #         traceback.print_exc()

    def set_chart_subtitle(self, strTitle=""):
        self.strTitle = strTitle

    def set_axes_x_name(self, strAxesX="X Axes"):
        self.strAxesNameX = strAxesX

    def set_axes_y_name(self, strAxesY="Y Axes"):
        self.strAxesNameY = strAxesY

    def set_line_name(self, index=0, name=""):
        try:
            # if len(self.listAxesData[index]) > 0:
            self.listAxesData[index][0] = name
            return True
            # else:
            #     self.listAxesData[index][0].append(name)
            # return None
        except:
            traceback.print_exc()
            return False

    def set_axes_x_value(self, value):
        try:
            self.listAxesX = value
            return True
        except:
            traceback.print_exc()
            return False




class CtrlChart(QtWidgets.QWidget, Ui_ChartForm):
    def __init__(self, toolbar=False, width=5, height=5): 
        super().__init__()
        self.setupUi(self)
        self.mpl = MplCanvas(self, width=width, height=height, dpi=100)
        self.gridLayout.addWidget(self.mpl)
        if toolbar:
            self.mpl_ntb = NavigationToolbar(self.mpl, self)  # 添加完整的 toolbar
            self.gridLayout.addWidget(self.mpl_ntb)

        self.gridLayout.setContentsMargins(0,0,0,0,)

        # self.test()


    # def test(self):
    #     try:
    #         self.mpl.add_new_line("a")
    #         self.mpl.add_new_line("b")

    #         self.mpl.set_axes_data(index=0,y_data=[2,50,4,10,15],x_data=[0,1,2,3,4],color=COLOR.RED.value,y_label="a")
    #         self.mpl.set_axes_data(index=1,y_data=[1,5,np.nan,2,2],x_data=None,color=COLOR.BLUE.value,y_label="b")

    #         self.mpl.set_chart_grid(True)
    #         self.mpl.set_axes_x_name("FREQ")
    #         self.mpl.set_axes_y_name("dBm")
    #         self.mpl.enable_legend()            
    #         self.show()

    #     except:
    #         traceback.print_exc()




    def set_ylim(self, range=[]):
        try:
            pass
        except:
            traceback.print_exc()
            return False


    def set_xlim(self, range=[]):
        try:
            pass
        except:
            traceback.print_exc()
            return False



if __name__ == "__main__":
    # import matplotlib
    # print(matplotlib.__version__)

    from PyQt5.QtWidgets import QMainWindow, QApplication
    strCurrPath = os.getcwd()
    app = QApplication(sys.argv)
    MyWin = CtrlChart()
    MyWin.mpl.add_new_line("a")
    MyWin.mpl.add_new_line("b")

    MyWin.mpl.set_chart_subtitle("subtitle")
    MyWin.mpl.adjust_bottom_size(0.25)
    # MyWin.mpl.set_text()

    # MyWin.mpl.set_axes_data(index=0,y_data=[2,50,4,10,15],x_data=[0,1,2,3,4],color=COLOR.RED.value,y_label="a",marker="o",markerfacecolor=COLOR.BLUE.value,markersize=12)
    MyWin.mpl.set_axes_data(index=0,y_data=[2,50,4,10,15],x_data=[0,1,2,3,4],color=COLOR.RED.value,y_label="a")
    MyWin.mpl.set_axes_data(index=1,y_data=[np.nan,50,np.nan,np.nan,np.nan],x_data=[0,1,2,3,4],color=COLOR.RED.value,y_label="b",marker="o",markerfacecolor=COLOR.BLUE.value,markersize=12)
    # MyWin.mpl.set_axes_data(index=2,y_data=[np.nan,50,np.nan,np.nan,np.nan],x_data=[0,1,2,3,4],color=COLOR.RED.value,y_label="b",marker="o",markerfacecolor=COLOR.BLUE.value,markersize=12)
    # MyWin.mpl.set_axes_data(index=1,y_data=[1,5,np.nan,2,2],x_data=None,color=COLOR.BLUE.value,y_label="b")

    MyWin.mpl.set_chart_grid(True)
    # MyWin.mpl.set_xlime([1,10]) 
    MyWin.mpl.set_ylime([0,60])
    MyWin.mpl.set_y_stick(0,60,5)

    # MyWin.mpl.enable_legend()
    MyWin.mpl.set_axes_x_name("FREQ")
    MyWin.mpl.set_axes_y_name("dBm")
    MyWin.mpl.enable_legend()
    # text = """[Atten] 10 dB   [Ext Gain] -12.00 dB   [TYPE] M    [RBW] -6dB   [VBW] 3.0 MHz   [Sweep] 1001 pts\n"""
    text_1 = "[Ext Gain]{:10}[Atten ]{:10}[VBM ]{:10}".format("","","")
    text_2 = "[Ext        ]{:10}[Points]{:10}[TYPE]{:10}".format("","","")
    text = text_1 + "\n" +text_2
    # MyWin.mpl.set_text(text=text,coord_x=0.25,coord_y=-0.3,horizontal=HorizontalLoc.LEFT.value,vertical=VerticalLoc.BOTTOM.value,size=10)
    MyWin.mpl.set_text(text=text,coord_x=0,coord_y=-0.3,horizontal=HorizontalLoc.LEFT.value,vertical=VerticalLoc.BOTTOM.value,size=10)
    # MyWin.mpl.set_text(text=text_2,coord_x=0,coord_y=-0.3,horizontal=HorizontalLoc.LEFT.value,vertical=VerticalLoc.BOTTOM.value,size=10, color=COLOR.RED.value)

    MyWin.mpl.set_chart_show()

    # MyWin.mpl.

    # MyWin.mpl.savefig("D:\\abc.png")
    MyWin.show()
    sys.exit(app.exec_())


 
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
#     listLineY = [2,100,np.nan,2,2]
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
#     # MyWin.mpl.savefig("test2.png")

#     # MyWin.mpl.set_xlime([1,10])    
#     # MyWin.mpl.set_ylime([1,50])    
#     MyWin.mpl.set_chart_show()
#     #---------------------------------------------------------------
#     MyWin.show()
#     sys.exit(app.exec_())






