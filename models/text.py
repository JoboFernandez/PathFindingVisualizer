import pygame


class Text:

    def __init__(self, name="", text="", align="left", font="calibri", fontsize=12, pos=(0, 0), dim=(0, 0),
                 fg=(0, 0, 0), bg=(255, 255, 255), bg_on=False, bold=False, italic=False, underline=False, wrap=False,
                 visible=True, enabled=True):
        self.name = name
        self.text = text
        self.font = font
        self.font_size = fontsize
        self.pos = pos
        self.left, self.top = pos
        self.dim = dim
        self.width, self.height = dim
        self.align = align
        self.fg = fg
        self.bg = bg
        self.bg_on = bg_on
        self.bold = bold
        self.italic = italic
        self.underline = underline
        self.wrap = wrap
        self.visible = visible
        self.enabled = enabled

    def draw(self, window: pygame.display.set_mode):
        if self.visible:
            object_font = pygame.font.SysFont(self.font, self.font_size, self.bold, self.italic)
            object_font.set_underline(self.underline)
            text_wrappings = self.get_text_wrapping(object_font=object_font)
            self.draw_text_wrapping(window=window, text_wrappings=text_wrappings, object_font=object_font)

    def get_text_wrapping(self, object_font: pygame.font.SysFont) -> list:
        object_font_w, object_font_h = object_font.size(self.text)

        # if wrapping is True, split text into multi-lines
        if self.wrap:
            line = ""
            sentence = self.text
            object_texts = []
            for letter in sentence:
                temp = line + letter
                if object_font.size(temp)[0] > self.width:
                    object_texts.append(line)
                    line = letter
                else:
                    line += letter
            else:
                object_texts.append(line)

        # if wrapping is False, text is one-liner
        else:
            object_texts = [self.text]
            if self.width < object_font_w:
                self.width = object_font_w
            if self.height < object_font_h:
                self.height = object_font_h

        # return text wrapping
        return object_texts

    def draw_text_wrapping(self, window: pygame.display.set_mode, text_wrappings: list, object_font: pygame.font.SysFont):
        object_font_w, object_font_h = object_font.size(self.text)

        for i in range(len(text_wrappings)):
            line = text_wrappings[i]
            line_w, line_h = object_font.size(line)
            indent = round(line_h * 1.2) * i
            location = {
                "left": (self.pos[0], self.pos[1] + indent),
                "center": (self.pos[0] + round((self.width - object_font_w) // 2), self.pos[1] + indent),
                "right": (self.pos[0] + self.width - object_font_w, self.pos[1] + indent)
            }

            if self.bg_on:
                window.blit(object_font.render(line, True, self.fg, self.bg), location[self.align])
            else:
                window.blit(object_font.render(line, True, self.fg), location[self.align])
