import pygame, win32api, win32con
from copy import copy
from os import _exit
from collections import Counter as mset
pygame.init()
size = width, height = win32api.GetSystemMetrics(win32con.SM_CXSCREEN), win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
ul = 135 * height // 1080
def get_rect(i, pos) :
    j = i.get_rect()
    j.left, j.top = pos
    return j
def draw() :
    print("Draw!!!")
    my_font = pygame.font.SysFont("Consolas", 200)
    time_surf = my_font.render("DRAW!!!", 1, [255, 255, 255])
    gor = time_surf.get_rect()
    gor.center = width / 2, height / 2
    screen.blit(time_surf, gor)
    pygame.display.update()
    running2 = True
    while running2:
        for event2 in pygame.event.get():
            if event2.type == pygame.KEYDOWN:
                if event2.key == pygame.K_ESCAPE:
                    _exit(0)

def refresh() :
    global wking, bking
    wking = None
    bking = None
    for i in rects :
        for j in i :
            if j :
                if type(j) == King :
                    if j.c :
                        wking = j
                    else :
                        bking = j
                else :
                    j.access(rects)
    wking.access(rects)
    bking.access(rects)
def tryout() :
    global canmove
    canmove = False
    for i in rects :
        for j in i :
            if j and j.c == times :
                for k, t in j.acc + j.eat :
                    for i2 in occ :
                        for j2 in range(len(i2)) :
                            i2[j2] = []
                    rects2 = []
                    for x, i2 in enumerate(rects):
                        rects2.append([])
                        for j2 in i2:
                            rects2[x].append(copy(j2))
                    rects2[k][t] = copy(j)
                    rects2[k][t].x, rects2[k][t].y = k, t
                    rects2[j.x][j.y] = None
                    wking = None
                    bking = None
                    for i2 in rects2:
                        for j2 in i2:
                            if j2:
                                if type(j2) == King:
                                    if j2.c:
                                        wking = j2
                                    else:
                                        bking = j2
                                j2.access(rects2)
                    for i2 in rects2 :
                        for j2 in i2 :
                            if j2 and j2.c != times :
                                for k2, t2 in j2.eat :
                                    occ[k2][t2].append(j2)
                    if times :
                        if occ[wking.x][wking.y] :
                            if [k, t] in j.acc :
                                j.acc.remove([k, t])
                            else :
                                j.eat.remove([k, t])
                        else :
                            canmove = True
                    else :
                        if occ[bking.x][bking.y] :
                            a = occ[bking.x][bking.y]
                            if [k, t] in j.acc :
                                j.acc.remove([k, t])
                            else :
                                j.eat.remove([k, t])
                        else :
                            canmove = True
def ok(x, y) :
    return x >= 0 and x < 8 and y >= 0 and y < 8
class Base :
    def __init__(self, c, w, b):
        self.c = c
        if self.c:
            self.img = w
        else:
            self.img = b
        self.x = self.y = 0
        self.acc = []
        self.eat = []
        self.spe = []
        self.pro = []
        self.used = False
    def hint(self):
        for i, j in self.acc :
            htrect.center = pos[i][j].center
            screen.blit(ht, htrect)
        for i, j in self.eat :
            screen.blit(cpht, pos[i][j])
    def access(self, rects):
        pass
    def rookacc(self, rects):
        for i in range(self.x + 1, 8) :
            if rects[i][self.y] :
                if rects[i][self.y].c != self.c :
                    self.eat.append([i, self.y])
                else :
                    self.pro.append([i, self.y])
                break
            self.acc.append([i, self.y])
        for i in range(self.x - 1, -1, -1) :
            if rects[i][self.y] :
                if rects[i][self.y].c != self.c :
                    self.eat.append([i, self.y])
                else :
                    self.pro.append([i, self.y])
                break
            self.acc.append([i, self.y])

        for i in range(self.y + 1, 8) :
            if rects[self.x][i] :
                if rects[self.x][i].c != self.c :
                    self.eat.append([self.x, i])
                else :
                    self.pro.append([self.x, i])
                break
            self.acc.append([self.x, i])
        for i in range(self.y - 1, -1, -1) :
            if rects[self.x][i] :
                if rects[self.x][i].c != self.c :
                    self.eat.append([self.x, i])
                else :
                    self.pro.append([self.x, i])
                break
            self.acc.append([self.x, i])

    def bisacc(self, rects):
        for i in range(self.x + 1, 8) :
            j = self.x + self.y - i
            if not ok(i, j) :
                break
            if rects[i][j] :
                if rects[i][j].c != self.c:
                    self.eat.append([i, j])
                else :
                    self.pro.append([i, j])
                break
            self.acc.append([i, j])
        for i in range(self.x - 1, -1, -1) :
            j = self.x + self.y - i
            if not ok(i, j) :
                break
            if rects[i][j] :
                if rects[i][j].c != self.c :
                    self.eat.append([i, j])
                else :
                    self.pro.append([i, j])
                break
            self.acc.append([i, j])

        for i in range(self.x + 1, 8):
            j = i + self.y - self.x
            if not ok(i, j) :
                break
            if rects[i][j]:
                if rects[i][j].c != self.c:
                    self.eat.append([i, j])
                else :
                    self.pro.append([i, j])
                break
            self.acc.append([i, j])
        for i in range(self.x - 1, -1, -1):
            j = i + self.y - self.x
            if not ok(i, j) :
                break
            if rects[i][j]:
                if rects[i][j].c != self.c:
                    self.eat.append([i, j])
                else :
                    self.pro.append([i, j])
                break
            self.acc.append([i, j])
    # def move(self):

class King(Base) :
    def __init__(self, c):
        Base.__init__(self, c, wk, bk)

    def access(self, rects):
        self.acc = []
        self.eat = []
        self.pro = []
        self.spe = []
        dir = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        for i, j in dir :
            tx, ty = self.x + i, self.y + j
            if ok(tx, ty) :
                if rects[tx][ty] :
                    if rects[tx][ty].c != self.c :
                        self.eat.append([tx, ty])
                    else :
                        self.pro.append([tx, ty])
                else :
                    self.acc.append([tx, ty])
        t = 7 if self.c else 0
        r1 = rects[0][t]
        r2 = rects[7][t]
        for i2 in occ:
            for j2 in range(len(i2)):
                i2[j2] = []
        for i2 in rects:
            for j2 in i2:
                if j2 and j2.c != times:
                    for k2, t2 in j2.acc:
                        occ[k2][t2].append(j2)
        if not self.used and r1 and not r1.used and not rects[1][t] and not rects[2][t] and not rects[3][t] :
            if not occ[1][t] and not occ[2][t] and not occ[3][t] and not occ[4][t]:
                self.acc.append([2, t])
                self.spe.append([2, t])
        if not self.used and r2 and not r2.used and not rects[5][t] and not rects[6][t] :
            if not occ[4][t] and not occ[5][t] and not occ[6][t] :
                self.acc.append([6, t])
                self.spe.append([6, t])

class Queen(Base) :
    def __init__(self, c):
        Base.__init__(self, c, wq, bq)
    def access(self, rects):
        self.acc = []
        self.eat = []
        self.pro = []
        self.bisacc(rects)
        self.rookacc(rects)

class Bishop(Base) :
    def __init__(self, c):
        Base.__init__(self, c, wb, bb)
    def access(self, rects):
        self.acc = []
        self.eat = []
        self.pro = []
        self.bisacc(rects)

class Knight(Base) :
    def __init__(self, c):
        Base.__init__(self, c, wn, bn)
    def access(self, rects):
        self.acc = []
        self.eat = []
        self.pro = []
        dir = [[-2, -1], [-2, 1], [2, -1], [2, 1], [-1, -2], [1, -2], [-1, 2], [1, 2]]
        for i, j in dir:
            tx, ty = self.x + i, self.y + j
            if ok(tx, ty):
                if rects[tx][ty] :
                    if rects[tx][ty].c != self.c:
                        self.eat.append([tx, ty])
                    else :
                        self.pro.append([tx, ty])
                else:
                    self.acc.append([tx, ty])

class Rook(Base) :
    def __init__(self, c):
        Base.__init__(self, c, wr, br)
    def access(self, rects):
        self.acc = []
        self.eat = []
        self.pro = []
        self.rookacc(rects)

class Pawn(Base) :
    def __init__(self, c):
        Base.__init__(self, c, wp, bp)
    def access(self, rects):
        self.acc = []
        self.eat = []
        self.spe = []
        self.pro = []
        d = 1 if self.c else -1
        if not self.used and not rects[self.x][self.y - 2 * d] and not rects[self.x][self.y - d] :
            self.acc.append([self.x, self.y - 2 * d])
        if ok(self.x, self.y - d) :
            if not rects[self.x][self.y - d] :
                self.acc.append([self.x, self.y - d])
        if self.x > 0 and ok(self.x, self.y - d) :
            if rects[self.x - 1][self.y - d] :
                if rects[self.x - 1][self.y - d].c != self.c :
                    self.eat.append([self.x - 1, self.y - d])
                else :
                    self.pro.append([self.x - 1, self.y - d])
        if self.x < 7 and ok(self.x, self.y - d) :
            if rects[self.x + 1][self.y - d] :
                if rects[self.x + 1][self.y - d].c != self.c :
                    self.eat.append([self.x + 1, self.y - d])
                else :
                    self.pro.append([self.x + 1, self.y - d])
        if lastmove and type(lastmove[0]) == Pawn and lastmove[0].c != self.c and abs(lastmove[0].x - self.x) == 1 and lastmove[1].y == self.y :
            if not self.c and lastmove[0].y == 6 and lastmove[1].y == 4 :
                self.acc.append([lastmove[0].x, 5])
                self.spe.append([lastmove[0].x, 5])
            elif self.c and lastmove[0].y == 1 and lastmove[1].y == 3 :
                self.acc.append([lastmove[0].x, 2])
                self.spe.append([lastmove[0].x, 2])

chessboard = pygame.transform.scale(pygame.image.load("chessboard.png"), (1080, 1080))
bk = pygame.transform.scale(pygame.image.load("bk.png"), (ul, ul))
bq = pygame.transform.scale(pygame.image.load("bq.png"), (ul, ul))
bb = pygame.transform.scale(pygame.image.load("bb.png"), (ul, ul))
bn = pygame.transform.scale(pygame.image.load("bn.png"), (ul, ul))
br = pygame.transform.scale(pygame.image.load("br.png"), (ul, ul))
bp = pygame.transform.scale(pygame.image.load("bp.png"), (ul, ul))
wk = pygame.transform.scale(pygame.image.load("wk.png"), (ul, ul))
wq = pygame.transform.scale(pygame.image.load("wq.png"), (ul, ul))
wb = pygame.transform.scale(pygame.image.load("wb.png"), (ul, ul))
wn = pygame.transform.scale(pygame.image.load("wn.png"), (ul, ul))
wr = pygame.transform.scale(pygame.image.load("wr.png"), (ul, ul))
wp = pygame.transform.scale(pygame.image.load("wp.png"), (ul, ul))
ht = pygame.image.load("hint.png")
htrect = ht.get_rect()
cpht = pygame.image.load("capture-hint.png")
rects = []
pos = []
occ = []
canmove = False
for i in range(8) :
    rects.append([])
    pos.append([])
    occ.append([])
    for j in range(8) :
        occ[i].append([])
        rects[i].append(None)
        recthere = wk.get_rect()
        recthere.left, recthere.top = (width - height) / 2 + ul * i, ul * j
        pos[i].append(recthere)
dir = (1, 0), (-1, 0), (0, 1), (0, -1)
times = 1
lastmove = []
selected = False
npawnm = 0
ncapm = 0
chesslst = []
def scan() :
    tmp2 = []
    for i in rects :
        tmp = []
        for j in i :
            if j :
                tmp.append(type(j))
                yield type(j)
            else :
                tmp.append(j)
        tmp2.append(tmp)
    chesslst.append(tmp2)
def add(i, x, y) :
    i.x, i.y = x - 1, y - 1
    rects[x - 1][y - 1] = i
add(King(0), 5, 1)
add(Queen(0), 4, 1)
add(Bishop(0), 3, 1)
add(Bishop(0), 6, 1)
add(Knight(0), 2, 1)
add(Knight(0), 7, 1)
add(Rook(0), 1, 1)
add(Rook(0), 8, 1)
for i in range(8) :
    add(Pawn(0), i + 1, 2)


add(King(1), 5, 8)
add(Queen(1), 4, 8)
add(Bishop(1), 3, 8)
add(Bishop(1), 6, 8)
add(Knight(1), 2, 8)
add(Knight(1), 7, 8)
add(Rook(1), 1, 8)
add(Rook(1), 8, 8)
for i in range(8) :
    add(Pawn(1), i + 1, 7)
scan()
refresh()
running = True

screen = pygame.display.set_mode(size, flags=pygame.FULLSCREEN)
def animate() :
    screen.blit(chessboard, [(width - height) / 2, 0])
    if selected :
        selected.hint()
    for x, i in enumerate(rects) :
        for y, j in enumerate(i) :
            if j :
                screen.blit(j.img, [(width - height) / 2 + ul * x, ul * y])
    pygame.display.flip()

while running :
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN :
            mousex, mousey = pygame.mouse.get_pos()
            x = y = z = j = False
            for y, i in enumerate(rects) :
                for z, j in enumerate(i) :
                    if pos[y][z].collidepoint(mousex, mousey):
                        x = j
                        break
                if pos[y][z].collidepoint(mousex, mousey):
                    break
            if x is False :
                continue
            if selected :
                if [y, z] in selected.acc or [y, z] in selected.eat :
                    if type(rects[y][z]) == Pawn :
                        npawnm = 0
                    else :
                        npawnm += 1
                    if [y, z] in selected.eat :
                        ncapm = 0
                    else :
                        ncapm += 1
                    lastmove = []
                    selected.used = True
                    lastmove.append(copy(selected))
                    rects[y][z] = selected
                    rects[selected.x][selected.y] = None
                    rects[y][z].x, rects[y][z].y = y, z
                    lastmove.append(rects[y][z])
                    if [y, z] in selected.spe :
                        if type(selected) == Pawn :
                            if selected.c :
                                rects[y][3] = None
                            else :
                                rects[y][4] = None
                        else :
                            rects[5 if y == 6 else 3][z] = rects[7 if y == 6 else 0][z]
                            rects[5 if y == 6 else 3][z].x, rects[5 if y == 6 else 3][z].y = 5 if y == 6 else 3, z
                            rects[7 if y == 6 else 0][z] = None
                    selected = False
                    if type(rects[y][z]) == Pawn and z == (not rects[y][z].c) * 7:
                        running2 = True
                        animate()
                        recthere = []
                        for i in range(4) :
                            if not rects[y][z].c :
                                recthere.append(get_rect(wq, (pos[y][z].left, 1080 - ul * i - ul)))
                            else :
                                recthere.append(get_rect(wq, (pos[y][z].left, ul * i)))
                        if rects[y][z].c :
                            lsthere = [wq, wn, wr, wb]
                            lsthere2 = [Queen(1), Knight(1), Rook(1), Bishop(1)]
                        else :
                            lsthere = [bq, bn, br, bb]
                            lsthere2 = [Queen(0), Knight(0), Rook(0), Bishop(0)]
                        while running2 :
                            for event2 in pygame.event.get() :
                                if event2.type == pygame.MOUSEBUTTONDOWN:
                                    mousex2, mousey2 = pygame.mouse.get_pos()
                                    for i, k in zip(recthere, lsthere2) :
                                        if i.collidepoint(mousex2, mousey2):
                                            rects[y][z] = k
                                            rects[y][z].x, rects[y][z].y = y, z
                                            running2 = False

                            if not rects[y][z].c :
                                pygame.draw.rect(screen, (255, 255, 255), ((pos[y][z].left, 540), (ul, ul * 4)))
                                for j, i in enumerate(lsthere, 1) :
                                    screen.blit(i, (pos[y][z].left, 1080 - ul * j))
                            else :
                                pygame.draw.rect(screen, (255, 255, 255), ((pos[y][z].left, 0), (ul, ul * 4)))
                                for j, i in enumerate(lsthere) :
                                    screen.blit(i, (pos[y][z].left, ul * j))
                            pygame.display.flip()
                    times ^= 1
                    refresh()
                    tryout()
                    for i2 in occ :
                        for j2 in range(len(i2)) :
                            i2[j2] = []
                    for i in rects:
                        for j in i:
                            if j:
                                for k, t in j.eat:
                                    occ[k][t].append(j)
                    animate()
                    scanlst = scan()
                    c = mset()
                    c.update(scanlst)
                    if not canmove :
                        if occ[(wking if times else bking).x][(wking if times else bking).y] :
                            print("Black" if times else "White", "check!!!")
                            my_font = pygame.font.SysFont("Consolas", 200)
                            time_surf = my_font.render("BLACK WIN!!!" if times else "WHITE WIN!!!", 1, [255, 255, 255])
                            gor = time_surf.get_rect()
                            gor.center = width / 2, height / 2
                            screen.blit(time_surf, gor)
                            pygame.display.update()
                            running2 = True
                            while running2:
                                for event2 in pygame.event.get():
                                    if event2.type == pygame.KEYDOWN:
                                        if event2.key == pygame.K_ESCAPE:
                                            _exit(0)
                        else :
                            draw()
                    elif npawnm >= 50 and ncapm >= 50 :
                        draw()
                    elif len(list(scanlst)) == 2 or c == mset([King, King, Knight]) or c == mset([King, King, Bishop])  :
                        draw()
                    elif c == mset([King, King, Bishop, Bishop]) :
                        tmp = []
                        for i in rects :
                            for j in i :
                                if type(j) == Bishop :
                                    tmp.append(j)
                        if (tmp[0].x + tmp[0].y) % 2 == (tmp[1].x + tmp[1].y) % 2 :
                            draw()
                    elif chesslst.count(chesslst[-1]) == 3 :
                        draw()

                elif x :
                    if x.c == times :
                        selected = x
                    else :
                        selected = False
                else :
                    selected = False
            else:
                if x :
                    if x.c == times :
                        selected = x

    animate()
pygame.quit()
