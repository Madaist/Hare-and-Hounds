# TODO sa afisez bine scorul jucatorului si al calculatorului
# TODO sa calculez scorul pentru starile intermediare cum a zis Irina

import time
import copy
import psutil
import os
import sys

# tabla initiala
board = [['#' for x in range(5)] for y in range(3)]
board[0][1] = 'c'
board[1][0] = 'c'
board[2][1] = 'c'
board[1][4] = 'i'
illegal_moves = [(0, 0), (2, 0), (0, 4), (2, 4)]  # colturile matricei care nu vor fi afisate
ADANCIME_MAX = 0
nr_mutari_jucator = 0
nr_mutari_calculator = 0
scor_jucator = 0
scor_calculator = 0
maxMem = 0
nr_mutari_verticale = 0  # numarul de mutari verticale consecutive ale cainilor
t_initial = time.time()


def calcMaxMem():
    global maxMem
    process = psutil.Process(os.getpid())
    memCurenta = process.memory_info()[0]
    if maxMem < memCurenta:
        maxMem = memCurenta


def valid_moves_hounds(linie_curenta, col_curenta, linie_mutare, col_mutare):
    if col_curenta == col_mutare:
        if linie_curenta == linie_mutare - 1 or linie_curenta == linie_mutare + 1:  # muta pe verticala
            return True
    if linie_curenta == linie_mutare and col_mutare == col_curenta + 1:  # muta pe orizontala
        return True
    if linie_curenta == linie_mutare + 1 and col_curenta == col_mutare - 1:  # muta pe diagonala in sus
        return True
    if linie_curenta == linie_mutare - 1 and col_curenta == col_mutare - 1:  # muta pe diagonala in jos
        return True

    return False


def valid_moves_hare(linie_curenta, col_curenta, linie_mutare, col_mutare):
    if abs(linie_curenta - linie_mutare) + abs(col_curenta - col_mutare) == 1:  # mutare sus-jos, stanga-dreapta
        return True
    if linie_curenta == linie_mutare + 1 and col_curenta == col_mutare - 1:  # mutare pe diagonala sprea dreapta in sus
        return True
    if linie_curenta == linie_mutare - 1 and col_curenta == col_mutare - 1:  # mutare pe diagonala spre dreapta in jos
        return True
    if linie_curenta == linie_mutare + 1 and col_curenta == col_mutare + 1:  # muutare pe diagonala sprea stanga in sus
        return True
    if linie_curenta == linie_mutare - 1 and col_curenta == col_mutare + 1:  # muutare pe diagonala sprea stanga in jos
        return True

    return False


def verificare_mutare_verticala(linie_curenta, col_curenta, linie_mutare, col_mutare):
    if col_curenta == col_mutare:
        if linie_curenta == linie_mutare + 1 or linie_curenta == linie_mutare - 1:
            return True
    return False


def d_manhattan(xy1, xy2):
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])  # |x1 - x2| + |y1 - y2|


def verificare_castig(tabla):
    pozitie_iepure = [(index, row.index('i')) for index, row in enumerate(tabla) if 'i' in row]
    pozitii_caini = poz_caini(tabla)

    coloana_iepure = pozitie_iepure[0][1]
    coloana_caine1 = pozitii_caini[0][1]
    coloana_caine2 = pozitii_caini[1][1]
    coloana_caine3 = pozitii_caini[2][1]

    # verificam daca iepurele a ajuns in stanga catelusilor
    if coloana_iepure < coloana_caine1 and coloana_iepure < coloana_caine2 \
            and coloana_iepure < coloana_caine3:
        return 'i'
    # iepurele castiga si daca doi caini sunt in dreapta lui iar unul este pe aceeasi coloana
    if coloana_iepure == coloana_caine1 and coloana_iepure < coloana_caine2 and coloana_iepure < coloana_caine3:
        return 'i'
    if coloana_iepure == coloana_caine2 and coloana_iepure < coloana_caine1 and coloana_iepure < coloana_caine3:
        return 'i'
    if coloana_iepure == coloana_caine3 and coloana_iepure < coloana_caine2 and coloana_iepure < coloana_caine1:
        return 'i'

    # verificam daca iepurele e inchis
    if pozitie_iepure[0] == (1, 4):
        if set(pozitii_caini) == {(0, 3), (1, 3), (2, 3)}:
            return 'c'
    if pozitie_iepure[0] == (0, 2):
        if set(pozitii_caini) == {(0, 1), (0, 3), (1, 2)}:
            return 'c'
    if pozitie_iepure[0] == (2, 2):
        if set(pozitii_caini) == {(2, 1), (1, 2), (2, 3)}:
            return 'c'

    return False


def poz_caini(tabla):
    pozitii_caini = []
    for i in range(len(tabla)):
        for j in range(len(tabla[i])):
            if tabla[i][j] == 'c':
                pozitii_caini.append((i, j))
    return pozitii_caini


def dist_iepure_caini(tabla):
    pozitie_iepure = [(index, row.index('i')) for index, row in enumerate(tabla) if 'i' in row]
    pozitii_caini = poz_caini(tabla)

    # calculam distantele Manhattan de la iepure la caini
    d1 = d_manhattan(pozitie_iepure[0], pozitii_caini[0])
    d2 = d_manhattan(pozitie_iepure[0], pozitii_caini[1])
    d3 = d_manhattan(pozitie_iepure[0], pozitii_caini[2])

    return d1 + d2 + d3


class Joc:
    JMIN = None
    JMAX = None
    GOL = '#'

    def __init__(self, tabla=None):
        self.matr = tabla or board

    def final(self):
        return verificare_castig(self.matr)

    def mutari(self, jucator_opus):
        l_mutari = []
        for i in range(len(self.matr)):
            for j in range(len(self.matr[i])):
                if self.matr[i][j] == self.__class__.GOL and (i, j) not in illegal_moves:
                    if jucator_opus == 'i':
                        pozitie_iepure = [(index, row.index('i')) for index, row in enumerate(self.matr) if 'i' in row]
                        if valid_moves_hare(pozitie_iepure[0][0], pozitie_iepure[0][1], i, j):
                            self.creare_tabla_noua(pozitie_iepure[0][0], pozitie_iepure[0][1], i, j, jucator_opus,
                                                   l_mutari)
                    else:
                        pozitii_caini = poz_caini(self.matr)
                        linie1, col1 = pozitii_caini[0]
                        linie2, col2 = pozitii_caini[1]
                        linie3, col3 = pozitii_caini[2]
                        if valid_moves_hounds(linie1, col1, i, j):
                            self.creare_tabla_noua(linie1, col1, i, j, jucator_opus, l_mutari)
                        if valid_moves_hounds(linie2, col2, i, j):
                            self.creare_tabla_noua(linie2, col2, i, j, jucator_opus, l_mutari)
                        if valid_moves_hounds(linie3, col3, i, j):
                            self.creare_tabla_noua(linie3, col3, i, j, jucator_opus, l_mutari)

        return l_mutari

    def creare_tabla_noua(self, linie_curenta, col_curenta, linie_mutare, col_mutare, jucator_opus, l_mutari):
        matr_tabla_noua = copy.deepcopy(self.matr)
        matr_tabla_noua[linie_mutare][col_mutare] = jucator_opus
        matr_tabla_noua[linie_curenta][col_curenta] = Joc.GOL
        l_mutari.append(Joc(matr_tabla_noua))

    # def linii_deschise_iepure(self, lista, jucator):
    #
    #     return 0

    # def estimeaza_scor(self, adancime):
    #     t_final = self.final()
    #     # if (adancime==0):
    #     if t_final == self.__class__.JMAX:
    #         return 99 + adancime
    #     elif t_final == self.__class__.JMIN:
    #         return -99 - adancime
    #     else:
    #         # aici ma gandesc ca ar trebui sa returnez distanta daca jucatorul e JMAX (ca sa fie cat mai mare)
    #         # si sa returnez -distanta daca jucatorul e JMIN (CA sa fie cat mai mica)
    #         # dar in clasa Joc eu nu am acces la jucatorul curent
    #         return self.dist_iepure_caini()

    def __str__(self):
        sir = '\t0\t1\t2\t3\t4\n'
        sir += '  ----------------------\n'
        for i in range(len(self.matr)):
            sir += str(i) + '|\t'
            for j in range(len(self.matr[i])):
                if (i, j) not in illegal_moves:
                    sir += self.matr[i][j] + '\t'
                else:
                    sir += ' \t'
            sir += '\n'
        sir += '-' * 30
        return sir


class Stare:

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, scor=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent

        # adancimea in arborele de stari
        self.adancime = adancime

        # scorul starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.scor = scor

        # lista de mutari posibile din starea curenta
        self.mutari_posibile = []

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa = None

    def estimeaza_scor(self, adancime):
        t_final = Joc.final(self.tabla_joc)
        if t_final == Joc.JMAX:
            return 99 + adancime
        elif t_final == Joc.JMIN:
            return -99 - adancime
        else:
            return dist_iepure_caini(self.tabla_joc.matr)  # TODO aici trebuie schimbat cu ce a zis Irina

    def jucator_opus(self):
        if self.j_curent == Joc.JMIN:
            return Joc.JMAX
        else:
            return Joc.JMIN

    def mutari(self):
        l_mutari = self.tabla_joc.mutari(self.j_curent)
        juc_opus = self.jucator_opus()
        l_stari_mutari = [Stare(mutare, juc_opus, self.adancime - 1, parinte=self) for mutare in l_mutari]

        return l_stari_mutari

    def __str__(self):
        sir = str(self.tabla_joc) + "\n(Jucator curent:" + self.j_curent + ")\n"
        return sir


""" Algoritmul MinMax """


def min_max(stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.scor = stare.estimeaza_scor(stare.adancime)
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutari_scor = [min_max(mutare) for mutare in stare.mutari_posibile]

    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu scorul maxim
        stare.stare_aleasa = max(mutari_scor, key=lambda x: x.scor)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu scorul minim
        stare.stare_aleasa = min(mutari_scor, key=lambda x: x.scor)
    stare.scor = stare.stare_aleasa.scor
    calcMaxMem()
    return stare


def alpha_beta(alpha, beta, stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.scor = stare.estimeaza_scor(stare.adancime)
        return stare

    if alpha > beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()

    if stare.j_curent == Joc.JMAX:
        scor_curent = float('-inf')

        for mutare in stare.mutari_posibile:
            # calculeaza scorul
            stare_noua = alpha_beta(alpha, beta, mutare)

            if scor_curent < stare_noua.scor:
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor
            if alpha < stare_noua.scor:
                alpha = stare_noua.scor
                if alpha >= beta:
                    break

    elif stare.j_curent == Joc.JMIN:
        scor_curent = float('inf')

        for mutare in stare.mutari_posibile:

            stare_noua = alpha_beta(alpha, beta, mutare)

            if scor_curent > stare_noua.scor:
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor

            if beta > stare_noua.scor:
                beta = stare_noua.scor
                if alpha >= beta:
                    break
    stare.scor = stare.stare_aleasa.scor
    calcMaxMem()
    return stare


def afis_daca_final(stare_curenta):
    final = stare_curenta.tabla_joc.final()
    if final:
        if final == "remiza":
            print("Remiza!")
        else:
            if final == 'i':
                print("A castigat IEPURELE")
            else:
                print("Au castigat CATELUSII")
            print("Scor jucator: ", scor_jucator)
            print("Scor calculator: ", scor_calculator)
            print("Numar mutari jucator: ", nr_mutari_jucator)
            print("Numar mutari calculator: ", nr_mutari_calculator)

        return True

    return False


def verif_mutare_verticala_matrici(matrice_anterioara, matrice_actualizata):
    poz_caini_anterioara = poz_caini(matrice_anterioara)
    poz_caini_actual = poz_caini(matrice_actualizata)

    prev_pos = [x for x in poz_caini_anterioara if x not in poz_caini_actual]
    actual_pos = [x for x in poz_caini_actual if x not in poz_caini_anterioara]

    if verificare_mutare_verticala(prev_pos[0][0], prev_pos[0][1], actual_pos[0][0], actual_pos[0][1]):
        return True
    return False


def main():
    global nr_mutari_jucator
    global nr_mutari_calculator
    global scor_calculator
    global scor_jucator
    global nr_mutari_verticale
    # initializare algoritm
    tip_algoritm = citire_tip_algoritm()
    # initializare jucatori
    citire_jucator()
    alege_dificultate()

    # initializare tabla
    tabla_curenta = Joc()
    print("Tabla initiala")
    print(str(tabla_curenta))

    # creare stare initiala
    stare_curenta = Stare(tabla_curenta, 'c', ADANCIME_MAX)

    while True:
        if stare_curenta.j_curent == Joc.JMIN:
            # check_if_exit() # TODO TREBUIE DECOMENTATA.
            # muta jucatorul
            if Joc.JMIN == 'c':
                linie_de_mutat, col_de_mutat = ce_caine_mut(stare_curenta)  # pe cine mut
                coloana, linie = obtine_linie_coloana(stare_curenta)  # unde mut
                while not valid_moves_hounds(linie_de_mutat, col_de_mutat, linie, coloana):
                    print("Catelusii pot merge doar verticala, orizontala si diagonala de la stanga la dreapta")
                    coloana, linie = obtine_linie_coloana(stare_curenta)
                if verificare_mutare_verticala(linie_de_mutat, col_de_mutat, linie, coloana):
                    nr_mutari_verticale += 1
                else:
                    nr_mutari_verticale = 0
                if nr_mutari_verticale == 10:
                    print('Iepurele a castigat. Cainii au mutat de 10 ori consecutiv pe verticala')
                    break  # TODO MAI TREBUIE AFISAT SI SCORUL
                stare_curenta.tabla_joc.matr[linie][coloana] = Joc.JMIN
                stare_curenta.tabla_joc.matr[linie_de_mutat][col_de_mutat] = Joc.GOL
            else:
                pozitie_iepure = [(index, row.index('i'))
                                  for index, row in enumerate(stare_curenta.tabla_joc.matr) if 'i' in row]
                coloana, linie = obtine_linie_coloana(stare_curenta)
                while not valid_moves_hare(pozitie_iepure[0][0], pozitie_iepure[0][1], linie, coloana):
                    print("Iepurele poate sari o singura piesa")
                    coloana, linie = obtine_linie_coloana(stare_curenta)
                stare_curenta.tabla_joc.matr[linie][coloana] = Joc.JMIN
                stare_curenta.tabla_joc.matr[pozitie_iepure[0][0]][pozitie_iepure[0][1]] = Joc.GOL
            print("\nTabla dupa mutarea jucatorului")
            print(str(stare_curenta))
            nr_mutari_jucator += 1
            scor_jucator += int(stare_curenta.scor or 0)

            if not afis_daca_final(stare_curenta):
                stare_curenta.j_curent = stare_curenta.jucator_opus()
            else:
                break

        # --------------------------------
        else:  # jucatorul e JMAX (calculatorul)
            # Mutare calculator

            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))
            if tip_algoritm == '1':
                stare_actualizata = min_max(stare_curenta)
            else:  # tip_algoritm==2
                stare_actualizata = alpha_beta(-500, 500, stare_curenta)
            matrice_curenta = copy.deepcopy(stare_curenta.tabla_joc.matr)
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
            matrice_actualizata = copy.deepcopy(stare_curenta.tabla_joc.matr)
            if verif_mutare_verticala_matrici(matrice_curenta, matrice_actualizata):
                nr_mutari_verticale += 1
            else:
                nr_mutari_verticale = 0
            if nr_mutari_verticale == 10:
                print('Iepurele a castigat. Cainii au mutat de 10 ori consecutiv pe verticala')
                break  # TODO MAI TREBUIE AFISAT SI SCORUL
            print("Tabla dupa mutarea calculatorului")
            print(str(stare_curenta))
            nr_mutari_calculator += 1
            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            print("Calculatorul a \"gandit\" timp de " + str((t_dupa - t_inainte)/1000) + " secunde.")
            print("Memoria folosita pentru mutare", maxMem)
            scor_calculator += stare_curenta.scor
            if afis_daca_final(stare_curenta):
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = stare_curenta.jucator_opus()


def citire_jucator():
    raspuns_valid = False
    while not raspuns_valid:
        Joc.JMIN = input("Doriti sa jucati cu c sau cu i? ").lower()
        if Joc.JMIN in ['c', 'i']:
            raspuns_valid = True
        else:
            print("Raspunsul trebuie sa fie c sau i.")
    Joc.JMAX = 'i' if Joc.JMIN == 'c' else 'c'


def citire_tip_algoritm():
    raspuns_valid = False
    tip_algoritm = None
    while not raspuns_valid:
        tip_algoritm = input("Algoritmul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-beta\n ")
        if tip_algoritm in ['1', '2']:
            raspuns_valid = True
        else:
            print("Nu ati ales o varianta corecta.")
    return tip_algoritm


def check_if_exit():
    exit = ''
    while exit.lower() not in ['da', 'nu']:
        exit = input("Vreti sa iesiti din joc? Raspundeti cu da sau nu.\n")
    if exit.lower() == 'da':
        print("Scor jucator: ", scor_jucator)
        print("Scor calculator: ", scor_calculator)
        sys.exit(0)


def alege_dificultate():
    global ADANCIME_MAX
    dificultate = 0
    while dificultate not in ['1', '2', '3']:
        dificultate = input("Alegeti nivelul de dificultate. Introduceti 1 pentru incepator, 2 pentru mediu sau 3 "
                            "pentru avansat.\n")

    if dificultate == 1:
        ADANCIME_MAX = 3
    elif dificultate == 2:
        ADANCIME_MAX = 6
    else:
        ADANCIME_MAX = 9


def ce_caine_mut(stare_curenta):
    raspuns_valid_mutare_caine = False
    linie_de_mutat, col_de_mutat = None, None
    while not raspuns_valid_mutare_caine:
        try:
            linie_de_mutat = int(input("Linia catelului de mutat = "))
            col_de_mutat = int(input("Coloana catelului de mutat = "))
            if linie_de_mutat in range(0, 3) and col_de_mutat in range(0, 5) \
                    and (linie_de_mutat, col_de_mutat) not in illegal_moves:
                # trebuie sa verific ca pozitia sa nu fie in illegal moves
                if stare_curenta.tabla_joc.matr[linie_de_mutat][col_de_mutat] != 'c':
                    print("Nu exista caine pe pozitia data")
                else:
                    raspuns_valid_mutare_caine = True
            else:
                print("Linie sau coloana invalida (trebuie sa fie unul dintre numerele 0,1,2).")
        except ValueError:
            print("Linia si coloana trebuie sa fie numere intregi")
    return linie_de_mutat, col_de_mutat


def obtine_linie_coloana(stare_curenta):
    raspuns_valid = False
    coloana, linie = None, None
    while not raspuns_valid:
        try:
            linie = int(input("linie="))
            coloana = int(input("coloana="))

            if linie in range(0, 3) and coloana in range(0, 5) and (linie, coloana) not in illegal_moves:
                if stare_curenta.tabla_joc.matr[linie][coloana] == Joc.GOL:
                    raspuns_valid = True
                else:
                    print("Exista deja un simbol in pozitia ceruta.")
            else:
                print("Linie sau coloana invalida (trebuie sa fie unul dintre numerele 0,1,2).")

        except ValueError:
            print("Linia si coloana trebuie sa fie numere intregi")
    return coloana, linie


if __name__ == "__main__":
    main()
    t_final = time.time()
    milis = round(1000 * (t_final - t_initial))
    print("Timp total rulare program: {} secunde".format(milis/1000))