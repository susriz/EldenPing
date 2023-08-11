import pygame
import random
pygame.init()

screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Elden Ping")

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, keys):
        super().__init__()
        self.image = pygame.image.load("src/hirvio.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5
        self.score = 0
        self.keys = keys
        # hitboxit
        self.rect.width, self.rect.height = self.image.get_size()  

    def update(self, keys):
        if keys[self.keys[0]]:
            self.rect.move_ip(0, -self.speed)
        elif keys[self.keys[1]]:
            self.rect.move_ip(0, self.speed)

        # pysytään hitboxien sisällä
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
    
    def mirror_image(self): # jotta pelaajat 'katsovat' toisiaan
        self.image = pygame.transform.flip(self.image, True, False)


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("src/kolikko.png")
        self.rect = self.image.get_rect()
        self.rect.width, self.rect.height = self.image.get_size()  
        self.rect.x = screen_width / 2 - self.rect.width / 2
        self.rect.y = screen_height / 2 - self.rect.height / 2
        self.vel_x = random.choice([-6, 6])
        self.vel_y = random.choice([random.randint(-6,-1), random.randint(1,6)])

    def update(self, player1, player2):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        # törmäykset reunojen kanssa
        if self.rect.y <= 0 or self.rect.y >= screen_height - self.rect.height:
            self.vel_y = -self.vel_y
        if self.rect.x <= 0:
            player2.score += 1
            self.reset()
        if self.rect.x >= screen_width - self.rect.width:
            player1.score += 1
            self.reset()

        # törmäykset pelaajiin
        if self.rect.colliderect(player1.rect):
            self.vel_x = abs(self.vel_x)
        elif self.rect.colliderect(player2.rect):
            self.vel_x = -abs(self.vel_x)
        # pisteet
        if self.rect.left <= 0:
            self.rect.center = (screen_width/2, screen_height/2)
            self.speed = -self.speed
            player2.score += 1
        elif self.rect.right >= screen_width:
            self.rect.center = (screen_width/2, screen_height/2)
            self.speed = -self.speed
            player1.score += 1

    def reset(self):
        self.rect.x = screen_width / 2 - self.rect.width / 2
        self.rect.y = screen_height / 2 - self.rect.height / 2
        self.vel_x = random.choice([-6, 6])
        self.vel_y = random.choice([random.randint(-6,-1), random.randint(1,6)])

# este ilmestyy randomiin kohtaan 5-20 sekunnin välein
# joskus pallo kuitenkin menee esteen läpi
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surface_height = random.randint(50, 150)
        self.image = pygame.Surface((75, self.surface_height))
        self.image.fill((237, 171, 28))
        self.rect = self.image.get_rect()
        self.rect.width, self.rect.height = self.image.get_size()  
        self.rect.x = screen_width / 2 - self.rect.width / 2
        self.rect.y = screen_height / 2 - self.rect.height / 2
        self.rect.x = -100  # aluksi ruudun ulkopuolella

    def spawn(self):
        self.rect.x = random.randint(50, 590)
        self.rect.y = random.randint(50, 430)

# itse peli
class Elden_Ping():
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen_width, self.screen_height = 640, 480
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.font = pygame.font.Font(None, 32)

        self.player1_score = 0
        self.player2_score = 0
        self.start_ticks = pygame.time.get_ticks()
        self.last_score_time = pygame.time.get_ticks()

        self.sprites = pygame.sprite.Group()
        self.obstacle_spawn_time = random.randint(5000, 20000)
        self.obstacle = None
        self.player1 = Player(70, self.screen_height / 2 - 50, (pygame.K_w, pygame.K_s))
        self.player2 = Player(self.screen_width - 70, self.screen_height / 2 - 50, (pygame.K_UP, pygame.K_DOWN))
        self.ball = Ball()
        self.sprites.add(self.player1, self.player2, self.ball)

    def spawn_obstacle(self):
        self.obstacle = Obstacle()
        self.obstacle.spawn()
        
    def reset_obstacle(self):
        if self.obstacle:
            self.obstacle.kill()
        self.obstacle = None

    def check_score_time(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.last_score_time
        if elapsed_time > self.obstacle_spawn_time:
            self.obstacle.spawn()
            self.last_score_time = current_time

    def start_screen(self):
        running = True
        font = pygame.font.Font(None, 28)
        title_font = pygame.font.Font(None, 32)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = False

            self.screen.fill((0, 0, 0))
            title = title_font.render(f"Elden Ping", True, (224, 155, 7))
            how_to1 = font.render("Tämä on kahden pelaajan pingpong-peli.", True, (245, 223, 171))
            how_to2 = font.render("Ensimmäinen 10 pistettä saanut on voittaja!", True, (245, 223, 171))
            controls = font.render("Pelaaja 1 käyttää WASD-näppäimiä ja Pelaaja 2 nuolinäppäimiä.", True, (245, 223, 171))
            start_game = font.render("Aloita painamalla välilyöntiä!", True, (245, 223, 171))

            self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, self.screen_height // 4))
            self.screen.blit(how_to1, (self.screen_width // 2 - how_to1.get_width() // 2, self.screen_height // 4 + 50))
            self.screen.blit(how_to2, (self.screen_width // 2 - how_to2.get_width() // 2, self.screen_height // 4 + 75))
            self.screen.blit(controls, (self.screen_width // 2 - controls.get_width() // 2, self.screen_height // 4 + 100))
            self.screen.blit(start_game, (self.screen_width // 2 - start_game.get_width() // 2, self.screen_height // 2 + 40))
            
            pygame.display.flip()
            self.clock.tick(60)

    def show_winner(self, winner_text):
        winner = self.font.render(winner_text, True, (245, 223, 171))
        new_game = self.font.render(f"Paina välilyöntiä pelataksesi uudelleen!", True, (245, 223, 171))
        screen.blit(winner, (self.screen_width / 2 - winner.get_width() / 2, self.screen_height / 2 - winner.get_height() / 2 - 40))
        screen.blit(new_game, (self.screen_width / 2 - new_game.get_width() / 2, self.screen_height / 2 - new_game.get_height() / 2 + 50))
        pygame.display.flip()
        pygame.event.clear()  

    def reset_game(self):
        self.player1.score = 0
        self.player2.score = 0
        self.player1.rect.center = (70, self.screen_height / 2 - 50)
        self.player2.rect.center = (self.screen_width - 70, self.screen_height / 2 - 50)
        self.ball.reset()
        self.reset_obstacle()
        self.start_ticks = pygame.time.get_ticks()

    def play_game(self):
        self.start_screen()

        running = True
        ball_speed_timer = 0
        ball_speed_interval = random.randint(6000, 18000) # pallon nopeuden muutosaika
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            keys = pygame.key.get_pressed()
            
            # pallon liiketilan muutokset
            if self.ball.rect.left <= 0:
                self.player2.score += 1
                self.last_score_time = pygame.time.get_ticks()
                self.ball.reset()
            elif self.ball.rect.right >= self.screen_width:
                self.player1.score += 1
                self.last_score_time = pygame.time.get_ticks()
                self.ball.reset()

            # pallon nopeus (ja suunta) muuttuu 6-18 sekunnin välein
            ball_speed_timer += self.clock.get_time()
            if ball_speed_timer >= ball_speed_interval:
                self.ball.vel_x = random.choice([-10, 10])
                self.ball.vel_y = random.choice([random.randint(-10,-1), random.randint(1,10)])#random.randint(-14, 14)
                ball_speed_timer = 0

            # esteen spawnajat
            elapsed_time = pygame.time.get_ticks() - self.last_score_time
            if elapsed_time > self.obstacle_spawn_time and self.obstacle is None:
                self.spawn_obstacle()
            
            # pallon osuminen esteeseen
            if self.obstacle:
                self.obstacle.update()
                self.sprites.add(self.obstacle)
                if self.ball.rect.colliderect(self.obstacle.rect):
                    self.ball.vel_x = -self.ball.vel_x
                    self.ball.vel_y = -abs(self.ball.vel_y)
                    
            self.check_score_time()
            
            # scoret
            score_text = self.font.render(f"Pelaaja 1: {self.player1.score}  Pelaaja 2: {self.player2.score}", True, (255, 255, 255))
            if self.player1.score >= 10 or self.player2.score >= 10:
                if self.player1.score >= 10:
                    self.show_winner("Pelaaja 1 voitti!")
                elif self.player2.score >= 10:
                    self.show_winner("Pelaaja 2 voitti!")

                spacebar_pressed = False
                while not spacebar_pressed:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            return
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                self.player1.score = 0
                                self.player2.score = 0
                                self.reset_game()
                                spacebar_pressed = True
                ball_speed_timer = 0

            
            self.screen.fill((5, 5, 5))
            self.player1.update(keys)
            self.player2.update(keys)
            self.ball.update(self.player1, self.player2)

            self.sprites.draw(self.screen)
            #self.draw_clock()

            score_x = self.screen_width / 2 - score_text.get_width() / 2
            score_y = 10
            self.screen.blit(score_text, (score_x, score_y))

            pygame.display.flip()
            self.clock.tick(60)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return


pong_game = Elden_Ping()
pong_game.player1.mirror_image() 
pong_game.play_game()
