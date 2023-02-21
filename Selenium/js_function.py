from selenium.common.exceptions import WebDriverException

class selenium_js_func():
    
    @staticmethod
    def wheel_element(webdriver, element, deltaY = 120, offsetX = 0, offsetY = 0):
        error = webdriver.execute_script("""
        var element = arguments[0];
        var deltaY = arguments[1];
        var box = element.getBoundingClientRect();
        var clientX = box.left + (arguments[2] || box.width / 2);
        var clientY = box.top + (arguments[3] || box.height / 2);
        var target = element.ownerDocument.elementFromPoint(clientX, clientY);

        for (var e = target; e; e = e.parentElement) {
            if (e === element) {
                target.dispatchEvent(new MouseEvent('mouseover', {view: window, bubbles: true, cancelable: true, clientX: clientX, clientY: clientY}));
                target.dispatchEvent(new MouseEvent('mousemove', {view: window, bubbles: true, cancelable: true, clientX: clientX, clientY: clientY}));
                target.dispatchEvent(new WheelEvent('wheel',     {view: window, bubbles: true, cancelable: true, clientX: clientX, clientY: clientY, deltaY: deltaY}));
                return;
            }
        }    
        return "Element is not interactable";
        """, element, deltaY, offsetX, offsetY)
        if error:
            raise WebDriverException(error)