import pygame
class Button():
    def __init__(self, color, x,y,width,height, text='', text_color=(0,0,0)):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.text_color = text_color
        
    def draw(self, win, outline=None, centered=True):
        #Call this method to draw the button on the screen
        if centered:
            draw_x = self.x - self.width // 2
            draw_y = self.y - self.height // 2

        else:
            draw_x = self.x 
            draw.y = self.y 

        if outline:
            pygame.draw.rect(win, outline, (draw_x-2, draw_y-2, self.width+4, self.height+4),0)
            
        pygame.draw.rect(win, self.color, (draw_x, draw_y, self.width, self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont(None, 30)
            text = font.render(self.text, 1, self.text_color)
            win.blit(text, (draw_x + (self.width/2 - text.get_width()/2),
                            draw_y + (self.height/2 - text.get_height()/2)))

        
    def isOver(self, pos, centered=True):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if centered:
            check_x = self.x - self.width // 2
            check_y = self.y - self.height // 2
        else:
            check_x = self.x
            check_y = self.y

        if pos[0] > check_x and pos[0] < check_x + self.width:
            if pos[1] > check_y and pos[1] < check_y + self.height:
                return True
            
        return False