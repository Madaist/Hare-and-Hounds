import time
import copy

board = [['#' for x in range(5)] for y in range(3)]
board[0][1] = 'c'
board[1][0] = 'c'
board[2][1] = 'c'
board[1][4] = 'i'
illegal_moves = [(0, 0), (2, 0), (0, 4), (2, 4)]
ADANCIME_MAX = 6


def valid_moves_hounds(linie_curenta, col_curenta, linie_mutare, col_mutare):
    if col_curenta == col_mutare:
        if linie_curenta == linie_mutare - 1 or linie_curenta == linie_mutare + 1:  # muta pe verticala
            return True
    if linie_curenta == linie_mutare and col_mutare == col_curenta + 1:  # muta pe orizontala
        return True
    if linie_curenta == linie_mutare + 1 and col_curenta == col_mutare - 1:  # muta pe diagonala
        return True

    return False


def valid_moves_hare(linie_curenta, col_curenta, linie_mutare, col_mutare):
    if abs(linie_curenta - linie_mutare) + abs(col_curenta - col_mutare) == 1:
        return True
    if linie_curenta == linie_mutare + 1 and col_curenta == col_mutare + 1:
        return True
    if linie_curenta == linie_mutare - 1 and col_curenta == col_mutare + 1:
        return True

    return False


def d_manhattan(xy1, xy2):
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])  # |x1 - x2| + |y1 - y2|


def verificare_castig(board):
    pozitie_iepure = [(index, row.index('i')) for index, row in enumerate(board) if 'i' in row]

    pozitii_caini = poz_caini(board)

    # verificam daca iepurele a ajuns in stanga catelusilor
    coloana_iepure = pozitie_iepure[0][1]
    coloana_caine1 = pozitii_caini[0][1]
    coloana_caine2 = pozitii_caini[1][1]
    coloana_caine3 = pozitii_caini[2][1]
    linie_caine1 = pozitii_caini[0][0]
    linie_caine2 = pozitii_caini[1][0]
    linie_caine3 = pozitii_caini[2][0]
    if coloana_iepure < coloana_caine1 and coloana_iepure < coloana_caine2 \
            and coloana_iepure < coloana_caine3:
        return 'i'

    if pozitie_iepure == (1, 4) and coloana_caine1 == coloana_caine2 == coloana_caine3 == 3:
        if linie_caine1 == 0 and linie_caine2 == 1 and linie_caine3 == 2:
            return True
        if linie_caine1 == 1 and linie_caine2 == 2 and linie_caine3 == 0:
            return True
        if linie_caine1 == 2 and linie_caine2 == 1 and linie_caine3 == 0:
            return True

    if pozitie_iepure == (0, 2):
        if pozitii_caini[0] == (0, 1) and pozitii_caini[1] == (0, 3) and pozitii_caini[2] == (1, 2):
            return True
        if pozitii_caini[0] == (0, 3) and pozitii_caini[1] == (1, 2) and pozitii_caini[2] == (0, 1):
            return True
        if pozitii_caini[0] == (1, 2) and pozitii_caini[1] == (0, 1) and pozitii_caini[2] == (0, 3):
            return True

    if pozitie_iepure == (2, 2):
        if pozitii_caini[0] == (2, 1) and pozitii_caini[1] == (1, 2) and pozitii_caini[2] == (2, 3):
            return True
        if pozitii_caini[0] == (1, 2) and pozitii_caini[1] == (2, 3) and pozitii_caini[2] == (2, 1):
            return True
        if pozitii_caini[0] == (2, 3) and pozitii_caini[1] == (2, 1) and pozitii_caini[2] == (1, 2):
            return True

    return False


def poz_caini(board):
    pozitii_caini = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 'c':
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
    """
    Clasa care defineste jocul. Se va schimba de la un joc la altul.
    """
    JMIN = None
    JMAX = None
    GOL = '#'

    def __init__(self, tabla=None):
        self.matr = tabla or board

    def final(self):
        return verificare_castig(self.matr)

    def mutari(self, jucator_opus): # daca e caine, gandesc pt iepure
        # jucator_curent = 'c' if jucator_opus == 'i' else 'i'

        l_mutari = []
        for i in range(len(self.matr)):
            for j in range(len(self.matr[i])):
                if self.matr[i][j] == self.__class__.GOL and (i, j) not in illegal_moves:
                    if jucator_opus == 'i':
                        pozitie_iepure = [(index, row.index('i')) for index, row in enumerate(self.matr) if 'i' in row]
                        # print("Iepure:", pozitie_iepure)
                        if valid_moves_hare(pozitie_iepure[0][0], pozitie_iepure[0][1], i, j):
                            matr_tabla_noua = copy.deepcopy(self.matr)
                            matr_tabla_noua[i][j] = jucator_opus
                            matr_tabla_noua[pozitie_iepure[0][0]][pozitie_iepure[0][1]] = Joc.GOL
                            l_mutari.append(Joc(matr_tabla_noua))
                    else:
                        pozitii_caini = poz_caini(self.matr)
                        # print("Caini: ", pozitii_caini)
                        linie1, col1 = pozitii_caini[0]
                        linie2, col2 = pozitii_caini[1]
                        linie3, col3 = pozitii_caini[2]
                        if valid_moves_hounds(linie1, col1, i, j):
                            matr_tabla_noua = copy.deepcopy(self.matr)
                            matr_tabla_noua[i][j] = jucator_opus
                            matr_tabla_noua[linie1][col1] = Joc.GOL
                            l_mutari.append(Joc(matr_tabla_noua))
                        if valid_moves_hounds(linie2, col2, i, j):
                            matr_tabla_noua = copy.deepcopy(self.matr)
                            matr_tabla_noua[i][j] = jucator_opus
                            matr_tabla_noua[linie2][col2] = Joc.GOL
                            l_mutari.append(Joc(matr_tabla_noua))
                        if valid_moves_hounds(linie3, col3, i, j):
                            matr_tabla_noua = copy.deepcopy(self.matr)
                            matr_tabla_noua[i][j] = jucator_opus
                            matr_tabla_noua[linie3][col3] = Joc.GOL
                            l_mutari.append(Joc(matr_tabla_noua))

        return l_mutari

    def linii_deschise_iepure(self, lista, jucator):

        return 0






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
        for i in range(len(board)):
            sir += str(i) + '|\t'
            for j in range(len(board[i])):
                if (i, j) not in illegal_moves:
                    sir += board[i][j] + '\t'
                else:
                    sir += ' \t'
            sir += '\n'
        sir += '-' * 30
        return sir


class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu configuratiile posibile
    in urma mutarii unui jucator
    """

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
            # return 0
            return dist_iepure_caini(self.tabla_joc.matr)  # aici trebuie schimbat oricum

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
        sir = str(self.tabla_joc) + "\n(Juc curent:" + self.j_curent + ")\n"
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

    return stare


def afis_daca_final(stare_curenta):
    final = stare_curenta.tabla_joc.final()
    if final:
        if final == "remiza":
            print("Remiza!")
        else:
            print("A castigat " + final)

        return True

    return False


def main():
    # initializare algoritm
    raspuns_valid = False
    while not raspuns_valid:
        tip_algoritm = input("Algorimul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-beta\n ")
        if tip_algoritm in ['1', '2']:
            raspuns_valid = True
        else:
            print("Nu ati ales o varianta corecta.")
    # initializare jucatori
    raspuns_valid = False
    while not raspuns_valid:
        Joc.JMIN = input("Doriti sa jucati cu c sau cu i? ").lower()
        if Joc.JMIN in ['c', 'i']:
            raspuns_valid = True
        else:
            print("Raspunsul trebuie sa fie c sau i.")
    Joc.JMAX = 'i' if Joc.JMIN == 'c' else 'c'

    # initializare tabla
    tabla_curenta = Joc()
    print("Tabla initiala")
    print(str(tabla_curenta))

    # creare stare initiala
    stare_curenta = Stare(tabla_curenta, 'c', ADANCIME_MAX)

    while True:
        if stare_curenta.j_curent == Joc.JMIN:
            # muta jucatorul
            if Joc.JMIN == 'c':
                linie_de_mutat, col_de_mutat = ce_caine_mut(stare_curenta)
                coloana, linie = obtine_linie_coloana(stare_curenta)
                while not valid_moves_hounds(linie_de_mutat, col_de_mutat, linie, coloana):
                    print("Catelusii pot merge doar verticala, orizontala si diagonala de la stanga la dreapta")
                    coloana, linie = obtine_linie_coloana(stare_curenta)
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
                stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
                print("Tabla dupa mutarea calculatorului")
                print(str(stare_curenta))

                # preiau timpul in milisecunde de dupa mutare
                t_dupa = int(round(time.time() * 1000))
                print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")

                if afis_daca_final(stare_curenta):
                    break

                # S-a realizat o mutare. Schimb jucatorul cu cel opus
                stare_curenta.j_curent = stare_curenta.jucator_opus()


def ce_caine_mut(stare_curenta):
    raspuns_valid_mutare_caine = False
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
