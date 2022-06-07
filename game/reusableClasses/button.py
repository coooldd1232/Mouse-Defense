from reusableClasses.Collision import Collision


class Button:
    def __init__(self, bgColor, bgColorOnHover, text, textColor, font, pos, width, height):
        self.bgColor = bgColor
        self.bgColorOffHover = bgColor
        self.bgColorOnHover = bgColorOnHover
        self.font = font

        self.text = self.font.render(text, True, textColor)
        self.textRect = self.text.get_rect()
        self.textRect.center = pos.x + width/2, pos.y + height/2

        self.pos = pos
        self.width = width
        self.height = height

    def GetRect(self):
        return self.pos.x, self.pos.y, self.width, self.height

    def Update(self, mousePos):
        if Collision.PointOnRect(mousePos, self.pos, self.width, self.height):
            self.bgColor = self.bgColorOnHover
        else:
            self.bgColor = self.bgColorOffHover
