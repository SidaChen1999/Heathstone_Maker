import pyautogui as pg
img_start = 'pics/start.jpg'
img_loss = 'pics/loss.jpg'
img_win = 'pics/win.jpg'
img_confirm = 'pics/confirm.jpg'
img_end_turn = 'pics/end_turn.jpg'
img_enemy_turn = 'pics/enemy_turn.jpg'
img_my_turn = 'pics/my_turn.jpg'
img_traditional_game = 'pics/traditional_game.jpg'
img_play = 'pics/play.jpg'
img_battlenet = 'pics/battlenet.jpg'
img_hearthstone = 'pics/hearthstone.jpg'
img_click = 'pics/click.jpg'
img_close = 'pics/close.jpg'
hwnd_name = '炉石传说'
pid_name = 'Hearthstone.exe'

green = (213, 255, 139)
yellow = (255, 255, 30)
green2 = (208, 233, 97)
red = (255, 255, 126)
confi = 0.85
timeout = 120 # seconds
epsilon = 15
screensize = (int(pg.size()[0]/2), int(pg.size()[1]/2))
game_window = (screensize[0]-960-8, screensize[1]-540-30, screensize[0]+960+8, screensize[1]+540+8)
priority = {'enemy_hero': 1, 'enemy_minions': 2, 'minions': 3, 'hero': 4}

class param():
    def __init__(self):
        self.img_start = 'pics/start.jpg'
        self.img_loss = 'pics/loss.jpg'
        self.img_win = 'pics/win.jpg'
        self.img_confirm = 'pics/confirm.jpg'
        self.img_end_turn = 'pics/end_turn.jpg'
        self.img_enemy_turn = 'pics/enemy_turn.jpg'
        self.img_my_turn = 'pics/my_turn.jpg'
        self.img_traditional_game = 'pics/traditional_game.jpg'
        self.img_play = 'pics/play.jpg'
        self.img_battlenet = 'pics/battlenet.jpg'
        self.img_click = 'pics/click.jpg'
        self.log_path = 'G:\Hearthstone\Logs\Power.log'

        self.green = (213, 255, 139)
        self.yellow = (255, 255, 30)
        self.green2 = (208, 233, 97)
        self.red = (255, 255, 126)
        self.confi = 0.8
        self.timeout = 120 # seconds
        self.epsilon = 20
        screensize = (int(pg.size()[0]/2), int(pg.size()[1]/2))
        self.game_window = (screensize[0]-960-8, screensize[1]-540-30, screensize[0]+960+8, screensize[1]+540+8)
        self.update(self.game_window)
    
    def update(self, game_window):
        self.game_window = game_window
        self.cards = (game_window[0]+650, game_window[1]+980, 600, 40)
        self.minions = (game_window[0]+380, game_window[1]+530, 1050, 30)
        self.enemy_minions = (game_window[0]+420, game_window[1]+345, 1020, 30)
        self.hero = (game_window[0]+780, game_window[1]+800, 460, 30)
        self.enemy_hero = (game_window[0]+933, game_window[1]+143)
        self.waiting_pos = ((game_window[0]+game_window[2])/2, game_window[1]+870)