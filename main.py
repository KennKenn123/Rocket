from algonova import *

def setup():
    global screen
    global window_size
    global rocket
    global event 
    global enemies
    global mode
    global score
    global score_text
    global wait
    global health
    global health_text
    global music

    window_size = (1080, 720)
    health = 3
    health_text = Text("Health: 3", 60, "white", None)
    health_text.set_align(window_size, "right top")
    wait = 30
    score = 0
    score_text =  Text("Score:0", 60, "white", None)
    score_text.set_align(window_size,"left top")
    event = Event()
    screen =  Screen("Rocket Game", "galaxy.jpg", window_size)
    rocket = GameSprite("rocket.png", 512, 640, 70, 70, 10)
    enemies = SpriteGroup()
    for i in range(5):
        enemies.add(GameSprite("asteroid.png", random.randint(0, 1010), 0, 70, 70, random.randint(5, 10)))
    music = Music("space.ogg")
    music.play()
    mode ="play"

def loop():
    global mode
    global score
    global wait
    global health
    
    if mode == "play":
        screen.update()
        rocket.update()
        rocket.reset(screen)
        rocket.limit_movement(window_size)
        enemies.show(screen)
        score_text.show_text(screen)
        health_text.show_text(screen)
        for i in enemies.sprite_group:
            i.fall_down_behaviour(window_size)
        if event.onKey(event.w):
            rocket.move("up")
        if event.onKey(event.s):
            rocket.move("down")
        if event.onKey(event.a):
            rocket.move("left")
        if event.onKey(event.d):
            rocket.move("right")
        collide,index =enemies.collideSingleSpriteWith(rocket)
        if collide:
            if health <= 0:
                mode = "over"
                music.stop()
            else:
                enemies.sprite_group[index].position.x = random.randint(0, 1030)
                enemies.sprite_group[index].position.y = 0
                health  -= 1
                health_text.change_text("health:" + str(health))


        if wait == 0:
            score += 1
            score_text.change_text("Score: "+ str(score))
            wait = 30
        wait -= 1
    if mode == "over":
            screen.set_background("red")
            screen.update()
            text = Text("Kamu kalah",100, "white", None)
            text.set_align(window_size, "top")
            text.show_text(screen)
            highscore = open("highscore.txt", "r").read()
            if int(highscore) < score:
                with open("highscore.txt", "w")as file:
                    file.write(str(score))
                highscore = str(None)
            show_score = Text("Your score :"+ str(score) + " | Highscore:" + highscore, 60, "white", None)
            show_score.set_align(window_size, "center")
            show_score.show_text(screen)
            button = Button(width=150, color=(120, 255, 120))
            button.set_hover_effect("green","black")
            button.set_align(window_size, "bottom")
            button.button_configure("Play again!",text_color="black")
            button.on_click(setup)
            button.show_button(screen)

app = System (30)
app.start(setup, loop)