# Line Chart

### display

![alt tag](https://imgur.com/eEuaH88.jpg)


### How to use

### set_axes_data([value], [axes_x])

```python
value = [
    ["Label_1",[1,4,5,6,6....]],
    ["Label_2",[1,4,5,6,6....]],
    ...
]

```

### Python Code

```python

MyWin = CtrlChart()
MyWin.mpl.ini_chart_data(2)             # set y axis number
MyWin.mpl.set_chart_subtitle("Chart")      # set chart title
MyWin.mpl.set_axes_data(value=listData, axes_x=listLineX)
MyWin.mpl.set_chart_grid(True)
MyWin.mpl.set_axes_x_name("Frequency")
MyWin.mpl.set_axes_y_name("Amplitude")
MyWin.mpl.enable_legend()
MyWin.mpl.set_xlime([1,10])    
MyWin.mpl.set_ylime([1,50])    
MyWin.mpl.set_chart_show()


```