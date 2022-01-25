img_start = 'pics/start.jpg'
img_loss = 'pics/loss.jpg'
img_win = 'pics/win.jpg'
img_confirm = 'pics/confirm.jpg'
img_end_turn = 'pics/end_turn.jpg'
img_enemy_turn = 'pics/enemy_turn.jpg'
img_my_turn = 'pics/my_turn.jpg'
img_my_turn1 = 'pics/my_turn1.jpg'
img_traditional_game = 'pics/traditional_game.jpg'
img_play = 'pics/play.jpg'
img_battlenet = 'pics/battlenet.jpg'
img_click = 'pics/click.jpg'
log_path = 'G:\Hearthstone\Logs\Power.log'

green = (213, 255, 139)
yellow = (255, 255, 12)
green2 = (208, 233, 97)
red = (255, 255, 126)
confi = 0.8
timeout = 120 # seconds
epsilon = 15

default_game_window = (0, 0, 1936, 1118)

priority = {'enemy_hero': 1, 'enemy_minions': 2, 'minions': 3, 'hero': 4}

class parameters():
    def __init__(self):
        self.img_start = 'pics/start.jpg'
        self.img_loss = 'pics/loss.jpg'
        self.img_win = 'pics/win.jpg'
        self.img_confirm = 'pics/confirm.jpg'
        self.img_end_turn = 'pics/end_turn.jpg'
        self.img_enemy_turn = 'pics/enemy_turn.jpg'
        self.img_my_turn = 'pics/my_turn.jpg'
        self.img_my_turn1 = 'pics/my_turn1.jpg'
        self.img_traditional_game = 'pics/traditional_game.jpg'
        self.img_play = 'pics/play.jpg'
        self.img_battlenet = 'pics/battlenet.jpg'
        self.img_click = 'pics/click.jpg'
        self.log_path = 'G:\Hearthstone\Logs\Power.log'

        self.green = (213, 255, 139)
        self.yellow = (255, 255, 12)
        self.green2 = (208, 233, 97)
        self.red = (255, 255, 126)
        self.confi = 0.8
        self.timeout = 120 # seconds
        self.epsilon = 15

        self.game_window = (0, 0, 1936, 1118)
        self.update(self.game_window)
    
    def update(game_window):
        return