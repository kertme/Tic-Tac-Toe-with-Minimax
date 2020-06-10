import pygame
import numpy as np

pygame.init()
import math
import time
import sys

import random

SIZE = WIDTH, HEIGHT = 470, 470 #pygame penceresi boyutu
depth_limit = 1                 #başlangıç depthi

# pygame fonksiyonları
def rect(screen, color, x, y, w, h, fill=0):
    pygame.draw.rect(screen, color, (x, y, w, h), fill)

def square(screen, color, x, y, s, fill=0):
    rect(screen, color, x, y, s, s, fill)

def check_win4(board): # 4'lü kazanma durumları için
    n = len(board)

    # verticalCheck1
    for i in range(n):
        if board[0][i] != "" and board[0][i] == board[1][i] == board[2][i] == board[3][i]:
            return board[0][i]

        # verticalCheck2
        if board[1][i] != "" and board[1][i] == board[2][i] == board[3][i] == board[4][i]:
            return board[1][i]

        # horizontalCheck1
        if board[i][0] != "" and board[i][0] == board[i][1] == board[i][2] == board[i][3]:
            return board[i][0]

        # horizontalCheck2
        if board[i][1] != "" and board[i][1] == board[i][2] == board[i][3] == board[i][4]:
            return board[i][1]

    # diagonalCheck1
    if (board[1][1] != "" and board[0][0] == board[1][1] == board[2][2] == board[3][3]) or (
            board[1][1] != "" and board[1][1] == board[2][2] == board[3][3] == board[4][4]):
        return board[1][1]

    # diagonalCheck2
    if board[0][1] != "" and board[0][1] == board[1][2] == board[2][3] == board[3][4]:
        return board[0][1]

    # diagonalCheck3
    if board[1][0] != "" and board[1][0] == board[2][1] == board[3][2] == board[4][3]:
        return board[1][0]

    # diagonalCheck4
    if (board[0][4] != "" and board[0][4] == board[1][3] == board[2][2] == board[3][1]) or (
            board[1][3] != "" and board[1][3] == board[2][2] == board[3][1] == board[4][0]):
        return board[2][2]

    # diagonalCheck5
    if board[0][3] != "" and board[0][3] == board[1][2] == board[2][1] == board[3][0]:
        return board[0][3]

    # diagonalCheck6
    if board[1][4] != "" and board[1][4] == board[2][3] == board[3][2] == board[4][1]:
        return board[1][4]

    # empty space check
    open_spots = 0
    for i in range(n):
        for j in range(n):
            if board[i][j] == "":
                open_spots += 1
    if open_spots == 0:
        return "tie"
    return None


def check_win(board): # 5'lü kazanma durumları için
    n = len(board)
    first = board[0][0]

    diagonal = first != ""
    for i in range(n):
        if board[i][i] != first:
            diagonal = False
            break
    if diagonal:
        return first
    first = board[0][n - 1]
    back_diag = first != ""
    for i in range(1, n + 1):
        if board[i - 1][n - i] != first:
            back_diag = False
            break
    if back_diag:
        return first

    for i in range(n):
        first = board[i][0]
        sideways = first != ""
        for j in range(n):
            if board[i][j] != first:
                sideways = False
        if sideways:
            return first

    for i in range(n):
        first = board[0][i]
        # print(first)
        sideways = first != ""
        for j in range(n):
            if board[j][i] != first:
                sideways = False
        if sideways:
            return first

    open_spots = 0
    for i in range(n):
        for j in range(n):
            if board[i][j] == "":
                open_spots += 1
    if open_spots == 0:
        return "tie"
    return None


def best_move(board, player, opponent): # en iyi hamleyi bulan fonksiyon
    n = len(board) #board'un boyutu
    best_score = -math.inf # initialize ederken en küçük değer
    best_winning_count = 0 # en iyi hamlenin alt ağaçlardaki kazanma sayısı
    move = (0, 0)
    best_moves = list() # en iyi skorlu hamlelerin listesi
    best_moves.append(move)
    winning_count = 0 # alt ağaçlardaki kazanma sayısı

    for i in range(n): # boardda dolanan for
        for j in range(n): # boardda dolanan for
            if board[i][j] == "": # boş isev
                winning_count = 0
                board[i][j] = player # hamle oynanıyor
                score, winning_count = minimax(board, 0, False, len(board), winning_count, player= player, opponent= opponent) # oynanan hamleye karşı minimax çağırılıyor
                board[i][j] = "" # hamle geri alınıyor
                if score > best_score: # oynanan hamle en iyi skordan iyiyse best_moves listesi sıfırlanıp oynanan hamle konuluyor
                    best_moves.clear()
                    best_score = score
                    best_winning_count = winning_count
                    move = (i, j)
                    best_moves.append(move)

                elif score == best_score: # oynanan hamlenin skoru mevcut en iyi hamlenin skoruyla eş ise alt ağaçlardaki kazanma sayısı karşılaştırılıyor
                    if winning_count > best_winning_count: # kazanma sayısı daha iyi olan seçiliyor, eğer kazanma sayısı eşit ise best_moves clearlanmadan eklenyior.
                        best_moves.clear()
                        best_score = score
                        best_winning_count = winning_count
                        move = (i, j)
                        best_moves.append(move)
                    elif winning_count == best_winning_count:
                        move = (i, j)
                        best_moves.append(move)


    move_index = random.randint(0, len(best_moves)-1) # en iyi hamlelerden biri seçiliyor (rastgele)
    move = best_moves[move_index]
    board[move[0]][move[1]] = player
    print(str(player)+":"+str(move)+" played") # oynana hamle yazdırılıyor
    return board # yeni board döndürülüyor

scores = {  # player "O" için skor tablosu
    "x": -10,  
    "o": 10,
    "tie": 0
}




def minimax(board, depth, is_max, n, winning_count, alpha=-math.inf, beta=math.inf, player="x", opponent="o"): # minimax algoritması

    winner = check_win(board) # kazanan var mı kontrol ediliyor
    if winner: 
        if winner == player: # kazanan player ise artı puan veriliyor
            winning_count += 1
        if player == "o": # player "O" ise skor tablosu normal kullanılıyor
            return scores[winner], winning_count
        # # player "x" ise skor tablosu -1 ile çarpılıyor
        return scores[winner] * -1, winning_count
    if depth > depth_limit: # derinlik kontrolü
        return 0, winning_count
    if is_max: # minimax'in max kolu
        best_score = -math.inf
        for i in range(n): # board dolaşılıyor
            for j in range(n):
                if board[i][j] == "":
                    board[i][j] = player
                    score, winning_count = minimax(board, depth + 1, False, n, winning_count, alpha, beta, player=player, opponent=opponent) #player için minimaxin mini
                    board[i][j] = ""
                    best_score = max(score, best_score)
                    alpha = max(alpha, score)
                    if beta <= alpha: #ağacı budayıp gereksiz hesaplardan kurtarmak için
                        break
        return best_score / (depth + 2), winning_count # skor döndürülüyor, derinlik+2'ye bölünüyor çünkü daha az hamlede bitirmesini istedik
    else:
        best_score = math.inf
        for i in range(n):
            for j in range(n):
                if board[i][j] == "":
                    board[i][j] = opponent
                    score, winning_count = minimax(board, depth + 1, True, n, winning_count, alpha, beta, player=player, opponent=opponent) #rakip için minimaxin maxi
                    board[i][j] = ""
                    best_score = min(score, best_score)
                    beta = min(beta, score)
                    if beta <= alpha: #ağacı budayıp gereksiz hesaplardan kurtarmak için
                        break
        return best_score / (depth + 2), winning_count


def reset(n): # reset fonksiyonu
    board = [["" for i in range(n)] for j in range(n)]
    loop = True
    return board, loop, None, True, "x", "o", False


class button(): # button sınıfı
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.pressed = False

    def draw(self, win, outline=None): # buttonları çizen fonksiyon
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 30)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos): # mouse buttonun üstündeyse true döndüren fonksiyon
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False

def main():
    padding = 10
    n = 5
    s = int((WIDTH - padding * 2) // (1.5 * n))
    board = [["" for i in range(n)] for j in range(n)]

    FPS = 5  # frames per second ayarı
    fpsClock = pygame.time.Clock()

    turn = "x"
    player = "x"
    opponent = "o"

    x_image = pygame.image.load(r"ex.png") # x resmi
    x_image = pygame.transform.scale(x_image, (s, s))
    o_image = pygame.image.load(r"o.png") # o resmi
    o_image = pygame.transform.scale(o_image, (s, s))

    loop = True
    sleeptime = 0
    frame_count = 0
    human_played = False
    ai_vs_ai = False
    winner = False
    restarted = False
    global depth_limit
    running = True
    board = best_move(board, player="x", opponent="o")
    turn = "x" if turn == "o" else "o"
    player, opponent = opponent, player # hamle değişimi
    restartPressed = False

    screen = pygame.display.set_mode(SIZE)  # pygame display ekranı 

    # Menü ögeleri
    ai_vs_ai_Button = button((0, 255, 0), 350, 50, 80, 30, "AI vs AI")
    resetButton = button((0, 255, 0), 350, 100, 80, 30, "Restart")
    depthButton = button((0, 255, 0), 20, 320, 150, 30, "Depth Options")
    depth1Button = button((255, 0, 0), 40, 360, 20, 25, "1")
    depth2Button = button((0, 255, 0), 80, 360, 20, 25, "3")
    depth3Button = button((0, 255, 0), 120, 360, 20, 25, "5")

    sizeButton = button((0, 255, 0), 20, 400, 150, 30, "Size Options")
    sizeButton3 = button((0, 255, 0), 40, 440, 20, 25, "3")
    sizeButton4 = button((0, 255, 0), 80, 440, 20, 25, "4")
    sizeButton5 = button((255, 0, 0), 120, 440, 20, 25, "5")

    speedButton = button((0, 255, 0), 200, 320, 150, 30, "Speed Options")
    speed1Button = button((0, 255, 0), 240, 360, 20, 25, "-")
    speed2Button = button((0, 255, 0), 280, 360, 20, 25, "+")

    selectPLayerButton = button((0, 255, 0), 200, 400, 150, 30, "Select")
    selectPLayerButtonX = button((0, 255, 0), 240, 440, 20, 25, "X")
    selectPLayerButtonO = button((0, 255, 0), 280, 440, 20, 25, "O")

    winnerButton = button((255,127,80), 350, 150, 90, 25, "")

    while running: # boardu devamlı çizdiren while loopu
        for i in range(n):
            for j in range(n):
                item = board[i][j]
                if item == "x":
                    screen.blit(x_image, (j * s + padding, i * s + padding))
                elif item == "o":
                    screen.blit(o_image, (j * s + padding, i * s + padding))
                square(screen, (0, 0, 0), j * s + padding, i * s + padding, s, 3)

        ai_vs_ai_Button.draw(screen, (0, 0, 0))
        resetButton.draw(screen, (0, 0, 0))
        depthButton.draw(screen, (0, 0, 0))
        depth1Button.draw(screen, (0, 0, 0))
        depth2Button.draw(screen, (0, 0, 0))
        depth3Button.draw(screen, (0, 0, 0))
        speedButton.draw(screen, (0, 0, 0))
        speed1Button.draw(screen, (0, 0, 0))
        speed2Button.draw(screen, (0, 0, 0))
        sizeButton.draw(screen,(0,0,0))
        sizeButton3.draw(screen,(0,0,0))
        sizeButton4.draw(screen,(0,0,0)) 
        sizeButton5.draw(screen,(0,0,0))

        if restartPressed:
            selectPLayerButton.draw(screen,(0,0,0))
            selectPLayerButtonX.draw(screen,(0,0,0)) 
            selectPLayerButtonO.draw(screen,(0,0,0))

        if winner:
            if winner == "tie":
                winnerButton.text = winner.upper()
                winnerButton.draw(screen)
            else:
                winnerButton.text = winner.upper() + " WINS!"
                winnerButton.draw(screen)

        pygame.display.update()
        fpsClock.tick(FPS)

        if ai_vs_ai == True:
            human_played = True
        prev = frame_count
        Mouse_x, Mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:  
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if resetButton.isOver(pos):
                    if ai_vs_ai_Button.color != (255,0,0):
                        restartPressed = True
                    else:
                        board, loop, winner, restarted, player, opponent, human_played = reset(n)

                if selectPLayerButtonX.isOver(pos):
                    board, loop, winner, restarted, player, opponent, human_played = reset(n)
                    player = "x"
                    opponent = "o"
                    restartPressed = False
                if selectPLayerButtonO.isOver(pos):
                    board, loop, winner, restarted, player, opponent, human_played = reset(n)
                    player = "o"
                    opponent = "x"
                    restartPressed = False


                if speed1Button.isOver(pos) and FPS >= 2: # oyun zaman ayarlaması yapılmasını sağlayan kısım
                    FPS -= 1
                    print("FPS:"+str(FPS))
                if speed2Button.isOver(pos):
                    FPS += 1
                    print("FPS:" + str(FPS))

                if ai_vs_ai_Button.isOver(pos):
                    if ai_vs_ai == False:
                        print("ai vs ai aktif")
                        ai_vs_ai = True
                        ai_vs_ai_Button.color = (255,0,0)

                    else:
                        print("ai vs ai deaktif")
                        ai_vs_ai = False
                        ai_vs_ai_Button.color = (0,255,0)

                if depth1Button.isOver(pos):
                    depth1Button.color = (255,0,0)
                    depth2Button.color = (0,255,0)
                    depth3Button.color = (0,255,0)
                    depth_limit = 1

                elif depth2Button.isOver(pos):
                    depth1Button.color = (0,255,0)
                    depth2Button.color = (255,0,0)
                    depth3Button.color = (0,255,0)
                    depth_limit = 3

                elif depth3Button.isOver(pos):
                    depth1Button.color = (0,255,0)
                    depth2Button.color = (0,255,0)
                    depth3Button.color = (255,0,0)
                    depth_limit = 5
                
                elif sizeButton3.isOver(pos):
                    sizeButton3.color = (255,0,0)
                    sizeButton4.color = (0,255,0)
                    sizeButton5.color = (0,255,0)
                    n = 3
                    board, loop, winner, restarted, player, opponent, human_played = reset(n)
                
                elif sizeButton4.isOver(pos):
                    sizeButton3.color = (0,255,0)
                    sizeButton4.color = (255,0,0)
                    sizeButton5.color = (0,255,0)
                    n = 4
                    board, loop, winner, restarted, player, opponent, human_played = reset(n)
                
                elif sizeButton5.isOver(pos):
                    sizeButton3.color = (0,255,0)
                    sizeButton4.color = (0,255,0)
                    sizeButton5.color = (255,0,0)
                    n = 5
                    board, loop, winner, restarted, player, opponent, human_played = reset(n)

                if ai_vs_ai == False and loop == True:
                    j = int(Mouse_x // s)
                    i = int(Mouse_y // s)
                    if i < n and j < n:
                        if board[i][j] == "":
                            board[i][j] = turn
                            turn = "x" if turn == "o" else "o"
                            player, opponent = opponent, player
                            human_played = True
                        winner = check_win(board)
                else:
                    if human_played == False:
                        human_played = True

        if loop: # oyunun oynandığı loop
            rect(screen, (255, 255, 255), padding, padding, WIDTH - padding * 2, HEIGHT - padding * 2)

            if not winner:
                winner = check_win(board)
            if winner: # oyun bittiğinde ekranı güncelleme
                if winner == "tie":
                    print(winner.upper() + "!")
                else:
                    print(winner.upper(), "Wins!")
                print("Press 'r' to restart")
                loop = False

            if restarted and player == "o":
                turn = "x"
                player = "x"
                opponent = "o"
                board = best_move(board, player=player, opponent=opponent)
                turn = "x" if turn == "o" else "o"
                player, opponent = opponent, player
                restarted = False

            if restarted and player == "x":
                turn = "x"
                opponent = "o"
                restarted = False

            if human_played and loop == True:
                #if ai_vs_ai == True:
                    #pygame.time.wait(sleeptime*1000)
                board = best_move(board, player=player, opponent=opponent)
                turn = "x" if turn == "o" else "o"
                player, opponent = opponent, player
                human_played = False
            frame_count += 1
            screen.fill((255, 255, 255))

    pygame.quit() 

if __name__ == "__main__":
    main()
