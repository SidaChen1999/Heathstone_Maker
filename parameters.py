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
img_merc_start = 'pics/merc_start.jpg'
img_mercenary = 'pics/mercenary.jpg'
img_travel_point = 'pics/travel_point.jpg'
img_select_travel = 'pics/select_travel.jpg'
img_select_level = 'pics/select_level.jpg'
img_mercenary_level = 'pics/mercenary_level.jpg'
img_lock = 'pics/lock.jpg'
img_ready = 'pics/ready.jpg'
img_fight = 'pics/fight.jpg'
img_victory = 'pics/victory.jpg'
img_acquire = 'pics/acquire.jpg'
img_merc_confirm = 'pics/merc_confirm.jpg'
img_proceed = 'pics/proceed.jpg'
img_no_enemy = 'pics/no_enemy.jpg'
img_open_treasure = 'pics/open_treasure.jpg'
img_treasure = 'pics/treasure.jpg'
img_finish = 'pics/finish.jpg'
img_select_treasure = 'pics/select_treasure.jpg'
img_campfire = 'pics/campfire.jpg'
img_receive = 'pics/receive.jpg'
img_jump = 'pics/jump.jpg'
img_pickup = 'pics/pick_up.jpg'
img_reveal = 'pics/reveal.jpg'
img_buble = 'pics/buble.jpg'

hwnd_name = '炉石传说'
pid_name = 'Hearthstone.exe'

green = (213, 255, 139)
yellow = (255, 255, 30)
green2 = (208, 233, 97)
merc_green = (186, 255, 170)
red = (255, 255, 126)
blue = (55, 222, 255)
gold = (255, 255, 25)
my_turn_color = (200, 160, 0)
my_turn_color2 = (215, 187, 13)
enemy_turn_color = (146, 117, 93)
enemy_turn_color2 = (106, 102, 94)
end_turn_color = (36, 160, 0)
end_turn_color2 = (51, 189, 17)
confi = 0.80
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
        self.epsilon = 15
        screensize = (int(pg.size()[0]/2), int(pg.size()[1]/2))
        self.game_window = (screensize[0]-960-8, screensize[1]-540-30, screensize[0]+960+8, screensize[1]+540+8)
        self.update(self.game_window)
    
    def update(self, game_window):
        # Rect
        self.game_window = game_window
        self.cards = (game_window[0]+650, game_window[1]+980, 600, 40)
        self.minions = (game_window[0]+380, game_window[1]+530, 1050, 30)
        self.enemy_minions = (game_window[0]+420, game_window[1]+345, 1020, 30)
        self.hero = (game_window[0]+780, game_window[1]+800, 460, 30)
        self.mercenary_ability = (game_window[0]+660, game_window[1]+437, 600, 30)
        self.enemy_mercenary = (game_window[0]+460, game_window[1]+230, 1000, 30)
        self.enemy_region = (game_window[0]+300, game_window[1]+70, 970, 920)
        self.treasure_region = (game_window[0]+8, game_window[1]+32, game_window[2]-game_window[0]-16, game_window[3]-game_window[1]-80)
        # point
        self.enemy_hero = (game_window[0]+933, game_window[1]+143)
        self.default_mercenary = ((game_window[0]+game_window[2])/2-20, game_window[1]+330)
        self.waiting_pos = ((game_window[0]+game_window[2])/2, game_window[1]+870)
        self.merc_waiting_pos = ((game_window[0]+game_window[2])/2, game_window[3]-80)
        self.my_turn_point = (game_window[0]+1613, game_window[1]+526)
        self.mid_point = (game_window[0]+game_window[2])/2, (game_window[1]+game_window[3])/2