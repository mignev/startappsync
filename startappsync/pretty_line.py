from termcolor import colored, cprint
from pyfiglet import figlet_format

class CLElement():
    def __init__(self, **kwargs):
        self.width = kwargs.get('width', 80)
        self.content = ''
        self.padding_left = 0

    def text(self,text):
        self.content = text
        self.content_width = len(text)
        return self

    @property
    def text_align(self):
        return self

    @property
    def text_decoration(self):
        return self

    @property
    def left(self):
        text = self.content
        self.output = text
        return self

    @property
    def right(self):
        text = self.content
        container_width = self.width
        text_width = self.content_width
        paddng_left = " " * (container_width - text_width)
        self.output = "{0}{1}".format(paddng_left, text)

        return self

    @property
    def center(self):
        text = self.content
        container_width = self.width
        text_width = self.content_width
        paddng_left = " " * int((container_width - text_width)/2)

        self.output = "{0}{1}".format(paddng_left, text)

        return self

    def color(self, color):
        self._color = color
        self.content = colored(self.content, self._color)
        return self

    def padding_left(self,amount):
        self.padding_left = amount

    @property
    def underline(self):
        self.content = colored(self.content, self._color, attrs=['underline'])
        return self

    def render(self):
        print(self.output)

    def __str__(self):
        return self.output

    @property
    def result(self):
        return self.output

class CLDocument():
    def __init__(self, **kwargs):
        self.width = kwargs.get('width', 80)
        self.el = CLElement(width=self.width)

    def br(self):
        print("")

    def hr(self):
        el = self.el
        el.text("-" * self.width)
        el.color('grey')
        el.text_align.left
        el.render()

    def heading(self, text, font, color):
        cprint(figlet_format(text, font=font), color)

    def create_element(self):
        return self.el
