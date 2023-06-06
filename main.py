#fatto da Michele Beccarini
#giugno 2023
#I1AC, Scuola Arti e Mestieri di Trevano





import pygame
from time import sleep, time
from random import randint
import webbrowser


pygame.init()
#controller
pygame.joystick.init()

#controlla se ha un controller collegato oppure  no
try:
    js = pygame.joystick.Joystick(0)
except:
    pass

#finestra
screen_width = 1280
screen_height = 720
schermo = pygame.display.set_mode((screen_width, screen_height),pygame.FULLSCREEN)
pygame.display.set_caption("Flappy Plane")


#giocatore
plane = pygame.image.load("assets/player/default.png")
player = plane.get_rect()
player.x = 100
player.y = screen_height/2
orologio = pygame.time.Clock()
punteggio = 0

#Gestione dei salvataggi
#funzione che critpa il salvataggio, https://stackoverflow.com/questions/20557999/xor-python-text-encryption-decryption e CIOCCI

def xor(data, key): 
    return bytearray(a^b for a, b in zip(*map(bytearray, [data, key]))) 
def salva():
    #salva
    f = open("usersave.wintry", "w")
    f.write(xor(str(record).encode(),key.encode()).decode())
    f.close()
key = "g0ki-khbp-ahb6-mon2"


try:
    f = open("usersave.wintry", "r")
    record = str(f.read())

    record = int(xor(record.encode(),key.encode()).decode())
except:
    f = open("usersave.wintry", "w")
    f.write(xor(str(0).encode(),key.encode()).decode())
    f.close()
    f = open("usersave.wintry", "r")
    record = str(f.read())

    record = int(xor(record.encode(),key.encode()).decode())

punteggio_dato = False






#variabili per il funzionamento del gioco e menu
morto = False
started = False
orologio = pygame.time.Clock()
tempo_render_ostacoli = 1
esecuzione = True
opzioni = False
scelta_difficolta = False
gravitY = 1


#carica il font e i colori
font = pygame.font.Font("assets/menu/pixel.ttf", 100)
small = pygame.font.Font("assets/menu/pixel.ttf",25)
medium = pygame.font.Font("assets/menu/pixel.ttf",50)

alt = font.get_height()

button_color_hover = (98,154,206)
colore_scritte_menu = (217, 59, 59)
colore_record = (250,167,75)

#punteggio
punteggio_testo = medium.render(str(punteggio),True,"white")
punteggio_rect = punteggio_testo.get_rect()
punteggio_rect.x = 10
punteggio_rect.y = 10

#record 
record_immagine = pygame.image.load("assets/menu/trophy.png")
record_immagine_rect = record_immagine.get_rect()
record_immagine_rect.x = punteggio_rect.x + punteggio_testo.get_width() + 50

record_testo = medium.render(str(record),True,colore_record)
record_rect = record_testo.get_rect()
record_rect.x = record_immagine_rect.x + record_immagine.get_width()+ 10
record_rect.y = 10

# Mette in memoria il menu principale, ho usato chatGPT per aiutarmi con il posizionamento centrale


menu_options = ['PLAY', "MODES", 'QUIT']

testo_mio = small.render("BY WINTRYMICHI", True, (217, 59, 59))
testo_mio_rect = testo_mio.get_rect()
testo_mio_rect.y = screen_height - small.get_height()


font_height = font.get_height()
menu_height = font_height * len(menu_options)
menu_y = (screen_height - menu_height) // 2 + 150
menu_x = screen_width / 2

gioca_button = font.render(menu_options[0], True, (colore_scritte_menu))
gioca_button_rect = gioca_button.get_rect(center=(menu_x, menu_y))
opzioni_button = font.render(menu_options[1], True, (colore_scritte_menu))
opzioni_button_rect = opzioni_button.get_rect(center=(menu_x, menu_y + font_height))
esci_button = font.render(menu_options[2], True, (colore_scritte_menu))
esci_button_rect = esci_button.get_rect(center=(menu_x, menu_y + font_height * 2))

#mette in memoria il menu "difficolta", ho usato chatGPT per aiutarmi con il posizionamento centrale
difficolta_options = ["EASY","MEDIUM","HARD"]

facile_button = font.render(difficolta_options[0], True, (colore_scritte_menu))
facile_button_rect = facile_button.get_rect(center=(menu_x, menu_y))
medio_button = font.render(difficolta_options[1], True, (colore_scritte_menu))
medio_button_rect = medio_button.get_rect(center=(menu_x, menu_y + font_height))
difficile_button = font.render(difficolta_options[2], True, (colore_scritte_menu))
difficile_button_rect = difficile_button.get_rect(center=(menu_x, menu_y + font_height * 2))

difficolta_settata = False

#Mette in memoria il logo
logo_img = pygame.image.load("assets/menu/logo.png")
logo_rect = logo_img.get_rect()
logo_rect.x = ((screen_width/2) - (logo_img.get_width()/2))
logo_rect.y = 80

#musica e suoni
pygame.mixer.set_num_channels(8)


pygame.mixer.music.load("assets/sound/soundtrack.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)

death_sound = pygame.mixer.Sound("assets/sound/death.mp3")
death_sound_played = False
#hover
hover_sound = pygame.mixer.Sound("assets/sound/hover.mp3")
hover_sound.set_volume(0.1)


#click
click_sound = pygame.mixer.Sound("assets/sound/click.mp3")

#engine
record_sound_channel = pygame.mixer.Channel(1)
death_sound_channel = pygame.mixer.Channel(2)
engine_sound = pygame.mixer.Sound("assets/sound/engine.mp3")
engine_sound.set_volume(0.2)
timer_motore = time()*1000
timer_motore_delay = 1000

#bools menu
hover_sound_played_play = False
hover_sound_played_modes = False
hover_sound_played_quit = False


#bools modes
hover_sound_played_easy = False
hover_sound_played_medium = False
hover_sound_played_hard = False

# record
record_sound_played = False
record_sound = pygame.mixer.Sound("assets/sound/record.wav")



#variabili per gli ostacoli
timer_ostacoli = time()*1000
timer_delay = 1*1000
ostacolo_sotto_img = pygame.image.load("assets/environment/ostacle_down.png")
ostacolo_sopra_img = pygame.image.load("assets/environment/ostacle_up.png")
ostacoli_sotto = []
ostacoli_sopra = []
beccato_ostacolo = False
distanza_ostacoli = 200


#variabili dell'ambiente
sky_img = pygame.image.load("assets/environment/sky.jpg").convert() #comprime il file per prevenire un gameplay lento

sky_rect = sky_img.get_rect()
up_sky = pygame.image.load("assets/environment/upsky.png")
up_skyrect = up_sky.get_rect()
up_skyrect.y = -1

grass_img = pygame.image.load("assets/environment/grass.jpg")
grass_rect = grass_img.get_rect()
grass_rect.y = screen_height-grass_img.get_height()

flag_img = pygame.image.load("assets/environment/record.png")
flag_rect = flag_img.get_rect()
flag_rect.x = screen_width
flag_blittata = False

mouse_pos = [0,0]
mouse_pos_fisico_prec = [0,0]
controller = False

record_iniziale= record


while esecuzione:
    schermo.blit(sky_img,sky_rect)

    #tasti e mouse
    mouse = pygame.mouse.get_pressed()

    tasti = pygame.key.get_pressed()

    #controller

    try:
        x_pad = js.get_button(0)
        o_pad = js.get_button(1)
        square_pad = js.get_button(2)

        d_pad = js.get_hat(0)[1]
    except:
        x_pad = False
        o_pad = False
        square_pad = False

        d_pad = 0
    #controller o mouse?
    mouse_pos_fisico = pygame.mouse.get_pos()

    #controlla se il mouse è stato mosso
    if mouse_pos_fisico_prec != mouse_pos_fisico:
        controller= False
    mouse_pos_fisico_prec = pygame.mouse.get_pos()


    if d_pad == 0  and not(controller):
        mouse_pos = pygame.mouse.get_pos()
        
    else:
        if not(controller):
            mouse_pos = [650,350]
            controller = True

    if controller:
        if d_pad == -1 and mouse_pos[1]<=550:
            mouse_pos[1]+=10
        elif d_pad == 1 and mouse_pos[1]>=320:
            mouse_pos[1]-=10
    
    #crea un rect 1x1 dove l'utente clicca, di modo da gestire in modo facile le "collisioni" con pulsanti
    
    mouse_pos_rect = pygame.Rect(mouse_pos[0],mouse_pos[1],1,1)

    #Condizione che verifica quale opzione del menu l'utente ha scelto

    #In questo caso è nel caso l'utente ha premuto su "gioca"

    if started:
        if difficolta_settata == False:
            started = False
            opzioni = True
        else:
            

            
            #permette di tornare al menu
            if tasti[pygame.K_ESCAPE] or o_pad:
                started = False
                player.y = screen_height/2
                death_sound_played = False
                gravitY = 1
                morto=False
                plane = pygame.image.load("assets/player/default.png")
                ostacoli_sotto = []
                ostacoli_sotto_temp = []
                ostacoli_sopra = []
                ostacoli_sopra_temp = []
                beccato_ostacolo = False
                punteggio = 0
                player.x = 100
                flag_rect.x = screen_width
                flag_blittata = False
                record_sound_played = False
                

            #incolla a schermo tutti i protagonisti
            
           

            #gestisce lo spawn degli ostacoli sotto
            if timer_ostacoli+timer_delay < time()*1000:
                ostacolo_sotto_temp = ostacolo_sotto_img.get_rect()
                ostacolo_sotto_temp.x = screen_width
                ostacolo_sotto_temp.y = randint(200,600)
                #gestisce la cordinata y della bandiera
                if not(flag_blittata):
                    flag_rect.y = ostacolo_sotto_temp.y - flag_img.get_height()
                ostacoli_sotto.append(ostacolo_sotto_temp)

            #sopra
                ostacolo_sopra_temp = ostacolo_sopra_img.get_rect()
                ostacolo_sopra_temp.x = screen_width
                ostacolo_sopra_temp.y = ostacolo_sotto_temp.y - ostacolo_sotto_img.get_height() - distanza_ostacoli
                ostacoli_sopra.append(ostacolo_sopra_temp)

                timer_ostacoli = time()*1000 

            if punteggio + len(ostacoli_sopra) >= record and record_iniziale != 0:
                schermo.blit(flag_img,flag_rect)
                flag_blittata = True
            #sotto
            ostacoli_sotto_temp = ostacoli_sotto.copy()
            for ostacolo_sotto in ostacoli_sotto:
                schermo.blit(ostacolo_sotto_img,ostacolo_sotto)
                if not(morto):
                    ostacolo_sotto.x -=5
                if ostacolo_sotto.colliderect(player):
                    beccato_ostacolo = True
                if ostacolo_sotto.x < - ostacolo_sotto_img.get_height():
                    ostacoli_sotto_temp.remove(ostacolo_sotto)

            #Mi ha aiutato Matteo Ciocci, evita il flickering degli ostacoli
            del ostacoli_sotto
            ostacoli_sotto = ostacoli_sotto_temp
            del ostacoli_sotto_temp


            #sopra
            ostacoli_sopra_temp = ostacoli_sopra.copy()
            for ostacolo_sopra in ostacoli_sopra:
                schermo.blit(ostacolo_sopra_img,ostacolo_sopra)
                if not(morto):
                    ostacolo_sopra.x -=5
                if ostacolo_sopra.colliderect(player):
                    beccato_ostacolo = True
                if ostacolo_sopra.x < -ostacolo_sopra_img.get_width():
                    ostacoli_sopra_temp.remove(ostacolo_sopra)
                    punteggio_dato = False
                
                #gestione del punteggio
                if ostacolo_sopra.x <= player.x and not(punteggio_dato):
                    punteggio+=1
                    if punteggio >= record:
                        record = punteggio
                    punteggio_dato = True
            #Mi ha aiutato Matteo Ciocci, evita il flickering degli ostacoli
            del ostacoli_sopra
            ostacoli_sopra = ostacoli_sopra_temp
            del ostacoli_sopra_temp


            


           
            schermo.blit(up_sky,up_skyrect)

            schermo.blit(plane,player)
            schermo.blit(grass_img,grass_rect)
            schermo.blit(punteggio_testo,punteggio_rect)
            schermo.blit(record_testo,record_rect)
            schermo.blit(record_immagine,record_immagine_rect)
            #aggiorna il punteggio
            punteggio_testo = medium.render(str(punteggio),True,"white")
            record_testo = medium.render(str(record),True,colore_record)

            #gestione del salto e del movimento dell'ambiente
            if not(morto):
                if flag_blittata:
                    flag_rect.x -=5
                grass_rect.x -=5
                sky_rect.x-=1
                if sky_rect.x == -1280:
                    sky_rect.x = 2
                if grass_rect.x <= -1280:
                    grass_rect.x = 0
                player.y += 0.3
                player.y -= gravitY
                if mouse[0] or x_pad:
                    gravitY += 0.8
                gravitY-=0.3
                if punteggio == record and not(record_sound_played):
                    record_sound_channel.play(record_sound)
                    record_sound_played = True

                #vibrazione leggera se si supera il record
                if record_sound_channel.get_busy():
                    try:
                        js.rumble(0,1,100)
                        pass
                    except:
                        pass
                    

            



                


        

            #game over
            if player.colliderect(grass_rect) or player.colliderect(up_skyrect) or beccato_ostacolo:
                morto = True
                
            if morto:
                #vibrazione
                if death_sound_channel.get_busy():
                    try:
                        js.rumble(1,1,100)
                    except:
                        pass
                
                salva()
                record_iniziale = record
                #impedisce al suono della morte di ripetersi
                if death_sound_played == False:
                    death_sound_channel.play(death_sound)
                    #aumenta la posizione del player, per un fattore estetico, dato che l'aereo orizzontale ha meno larghezza
                    player.x = 150
                    death_sound_played = True
                

                testo1 = font.render("YOU LOST!", True, (colore_scritte_menu))
                testo1_rect = testo1.get_rect(center=(screen_width/2, (screen_height/2-alt/2)))
                testo2 = font.render("PRESS RIGHT BUTTON...",True,(colore_scritte_menu))
                testo2_rect = testo2.get_rect(center=(screen_width/2,(screen_height/2)+alt/2))
                schermo.blit(testo1, testo1_rect)
                schermo.blit(testo2,testo2_rect)

                #blitta l'animazione di morte
                plane = pygame.image.load("assets/player/dead.png")

                if not (player.colliderect(grass_rect)):
                    player.y+=10
                #tasto sinistro per riprovare
                if mouse[2] or square_pad:
                    player.y = screen_height/2
                    death_sound_played = False
                    gravitY = 1
                    morto=False
                    plane = pygame.image.load("assets/player/default.png")
                    indice_esplosione = 0
                    ostacoli_sotto = []
                    ostacoli_sotto_temp = []
                    ostacoli_sopra = []
                    ostacoli_sopra_temp = []
                    beccato_ostacolo = False
                    punteggio = 0
                    player.x = 100
                    flag_rect.x = screen_width
                    flag_blittata = False
                    record_sound_played = False

    #se l'utente preme su difficolta
    elif opzioni:
        difficolta_settata = True
        if tasti[pygame.K_ESCAPE] or o_pad:
            opzioni = False
            player.y = screen_height/2
            gravitY = 1
            morto=False
        schermo.blit(logo_img,logo_rect)
        schermo.blit(facile_button, facile_button_rect)
        schermo.blit(medio_button, medio_button_rect)
        schermo.blit(difficile_button, difficile_button_rect)
        schermo.blit(testo_mio, testo_mio_rect)

        #se l'utente preme un bottone, gestisce anche i suoni
        if mouse[0] or x_pad: 
            if facile_button_rect.colliderect(mouse_pos_rect):
                click_sound.play()
                r_delay = 1.3*1000
                opzioni = False
                distanza_ostacoli = 350
                sleep(0.2)
            elif medio_button_rect.colliderect(mouse_pos_rect):
                click_sound.play()
                timer_delay = 1*1000
                opzioni = False
                distanza_ostacoli = 250
                sleep(0.2)
            elif difficile_button_rect.colliderect(mouse_pos_rect):
                click_sound.play()
                timer_delay = 0.8*1000
                distanza_ostacoli = 230
                opzioni = False
                sleep(0.2)
            


        #se l'utente passa sopra un bottone senza cliccare, gestisce anche i suoni
        else:
            
            if facile_button_rect.colliderect(mouse_pos_rect):

                if not(hover_sound_played_easy):
                    hover_sound.play()
                    hover_sound_played_easy = True

                facile_button = font.render(difficolta_options[0], True, button_color_hover)
            else:
                hover_sound_played_easy = False

                facile_button = font.render(difficolta_options[0], True, (colore_scritte_menu))

            if medio_button_rect.colliderect(mouse_pos_rect):

                if not(hover_sound_played_medium):
                    hover_sound.play()
                    hover_sound_played_medium = True

                medio_button = font.render(difficolta_options[1], True, button_color_hover)
            else:
                hover_sound_played_medium = False

                medio_button = font.render(difficolta_options[1], True, (colore_scritte_menu))

            if difficile_button_rect.colliderect(mouse_pos_rect):

                if not(hover_sound_played_hard):
                    hover_sound.play()
                    hover_sound_played_hard = True

                difficile_button = font.render(difficolta_options[2], True, button_color_hover)
            else:
                hover_sound_played_hard = False

                difficile_button = font.render(difficolta_options[2], True, (colore_scritte_menu))

    #se l'utente non preme niente, quindi c'è il menu
    else:
        schermo.blit(gioca_button, gioca_button_rect)
        schermo.blit(opzioni_button, opzioni_button_rect)
        schermo.blit(esci_button, esci_button_rect)
        schermo.blit(logo_img,logo_rect)
        schermo.blit(testo_mio, testo_mio_rect)

        #se l'utente preme un bottone, gestisce anche i suoni
        if mouse[0] or x_pad: 
            if gioca_button_rect.colliderect(mouse_pos_rect):
                click_sound.play()
                started = True
                sleep(0.2)
            elif esci_button_rect.colliderect(mouse_pos_rect):
                click_sound.play()
                esecuzione = False

            elif opzioni_button_rect.colliderect(mouse_pos_rect):
                click_sound.play()
                opzioni = True
                sleep(0.2)
            elif testo_mio_rect.colliderect(mouse_pos_rect):
                webbrowser.open("https://wintrymichi.ch/rickroll.mp4")
                sleep(1)

        #se l'utente passa sopra un bottone senza cliccare, gestisce anche i suoni
        else:
            if gioca_button_rect.colliderect(mouse_pos_rect):

                if not(hover_sound_played_play):
                    hover_sound.play()
                    hover_sound_played_play = True
                gioca_button = font.render(menu_options[0], True, button_color_hover)

                
            else:
                hover_sound_played_play = False
                
                gioca_button = font.render(menu_options[0], True, (colore_scritte_menu))


            if opzioni_button_rect.colliderect(mouse_pos_rect):

                if not(hover_sound_played_modes):
                    hover_sound.play()
                    hover_sound_played_modes = True


                opzioni_button = font.render(menu_options[1], True, button_color_hover)


            else:

                hover_sound_played_modes = False

                opzioni_button = font.render(menu_options[1], True, (colore_scritte_menu))
                
            if esci_button_rect.colliderect(mouse_pos_rect):
                
                if not(hover_sound_played_quit):
                    hover_sound.play()
                    hover_sound_played_quit = True

                esci_button = font.render(menu_options[2], True, button_color_hover)

            else:

                hover_sound_played_quit = False
                esci_button = font.render(menu_options[2], True, (colore_scritte_menu))

    pygame.display.flip()
    #blocca il framerate al 90 fps
    orologio.tick(90)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            esecuzione = False