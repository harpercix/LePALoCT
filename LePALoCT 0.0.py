from pathlib import Path
import re
from typing import List, Dict

translations = {'FR': {0: 'LePALoCT n\'est pas au bon fichier.\nIl doit etre dans "Logs" ou dans un tournoi.',
                       10: 'Choisis un ou plusieurs tournois parmis ceux ci (separes par des "-") :\n',
                       11: 'Il faut un ou plusieurs nombres (separes par des "-", exemple : "42-666-512") entre ',
                       12: '\n[numeros] : ',
                       999: '[Entrer] pour continuer'},
                'EN': {0: 'LePALoCT isn\'t in the good folder.\nIt would be in "Logs" or in a tournament.',
                       10: 'Choose one or several tournaments (separated with "-"):\n',
                       11: 'You need one or several numbers (separated with "-", exemple: "42-666-512") between ',
                       12: '\n[numbers]: ',
                       999: '[Enter] to continue'}}


class Plane:
    # 0 area, 1 stock_mod, 2 cat, 3 player, 4 craft_name, 5 nbr_b_gived, 6 nbr_b_received, 7 nbr_m_gived, 8 nbr_m_received, 9 nbr_r_gived, 10 nbr_r_received, 11 b_damages_gived, 12 b_damages_received, 13 m_damages_gived, 14 m_damages_received, 15 parts_destructed_r_gived, 16 parts_destructed_r_received, 17 nbr_clean_kill_b_gived, 18 nbr_clean_kill_b_received, 19 nbr_clean_kill_m_gived, 20 nbr_clean_kill_m_received, 21 nbr_clean_kill_r_gived, 22 nbr_clean_kill_r_received, 23 suicide, 24 mia, 25 b_fired, 26 b_hit, 27 death_order, 28 podium, 29 dead_time, 30 hp, 31 team
    def __init__(self, area, stock_mod, cat, player, craft_name,
                 nbr_b_gived, nbr_b_received, nbr_m_gived, nbr_m_received,
                 nbr_r_gived, nbr_r_received,
                 b_damages_gived, b_damages_received, m_damages_gived, m_damages_received,
                 parts_destructed_r_gived, parts_destructed_r_received,
                 nbr_clean_kill_b_gived, nbr_clean_kill_b_received,
                 nbr_clean_kill_m_gived, nbr_clean_kill_m_received,
                 nbr_clean_kill_r_gived, nbr_clean_kill_r_received,
                 suicide, mia, b_fired, b_hit, death_order, podium, dead_time, hp, team
                 ):
        self.area = area
        self.stock_mod = stock_mod
        self.cat = cat
        self.player = player
        self.craft_name = craft_name
        self.nbr_b_gived = nbr_b_gived
        self.nbr_b_received = nbr_b_received
        self.nbr_m_gived = nbr_m_gived
        self.nbr_m_received = nbr_m_received
        self.nbr_r_gived = nbr_r_gived
        self.nbr_r_received = nbr_r_received
        self.b_damages_gived = b_damages_gived
        self.b_damages_received = b_damages_received
        self.m_damages_gived = m_damages_gived
        self.m_damages_received = m_damages_received
        self.parts_destructed_r_gived = parts_destructed_r_gived
        self.parts_destructed_r_received = parts_destructed_r_received
        self.nbr_clean_kill_b_gived = nbr_clean_kill_b_gived
        self.nbr_clean_kill_b_received = nbr_clean_kill_b_received
        self.nbr_clean_kill_m_gived = nbr_clean_kill_m_gived
        self.nbr_clean_kill_m_received = nbr_clean_kill_m_received
        self.nbr_clean_kill_r_gived = nbr_clean_kill_r_gived
        self.nbr_clean_kill_r_received = nbr_clean_kill_r_received
        self.suicide = suicide
        self.mia = mia
        self.b_fired = b_fired
        self.b_hit = b_hit
        self.death_order = death_order
        self.podium = podium
        self.dead_time = dead_time
        self.hp = hp
        self.team = team


def creat_multi_tournament(p: Path, list_tournaments: List):
    total_name = 'Total Tournament '
    for t in list_tournaments:
        m = re.match(r'Tournament (?P<nbrs>\d+)', t.name)
        total_name += m['nbrs'] + ' '
    total_name = total_name[0:-1]
    fic_here = []
    for n in p.iterdir():
        fic_here.append(n)
    p_tt = p / total_name
    if p_tt not in fic_here:
        Path.mkdir(p_tt)
    nbr_r = 0
    rounds = []
    for t in list_tournaments:
        for round_n in t.iterdir():
            m = re.match(r'Round (?P<nbrs>\d+)', round_n.name)
            if m is None:
                continue
            for heat_n in round_n.iterdir():
                m = re.match(r'(?P<nbrs>\d+)-Heat (?P<nbr>\d+)', heat_n.name)
                if m is None:
                    continue
                with heat_n.open('r') as file:
                    heat_log = file.read().split('\n')
                    while len(rounds) - 1 < nbr_r:
                        rounds.append([])
                    rounds[nbr_r].append((heat_n.name, heat_log))
            nbr_r += 1
    fic_here = []
    for n in p_tt.iterdir():
        fic_here.append(n)
    for i in range(nbr_r):
        p_r = p_tt / f'Round {i}'
        if p_r not in fic_here:
            Path.mkdir(p_r)
        for name, text in rounds[i]:
            with open(p_r / name, mode='w') as txt:
                for line in text:
                    txt.write(line + '\n')
    return p_tt


def search_tournament(p: Path, dictonary: Dict[int, str]):
    """1"""
    def set_list(text, nbr_tournaments):
        separated_text = text.split('-')
        numbers = []
        for carac in separated_text:
            n = carac.strip()
            m = re.match(r'(?P<n>\d+)$', n)
            if m is None:
                return None
            if 0 > int(m['n']) > nbr_tournaments:
                return None
            numbers.append(int(m['n']))
        return numbers

    tournois = []
    for f in p.iterdir():
        if str(f.parts[-1])[0:11] == 'Tournament ' and len(str(f.parts[-1])) == 19:
            tournois.append(f)
    aff = dictonary[10]
    for i, t in enumerate(tournois):
        aff += f'[{i}] : {str(t.parts[-1])}\n'
    aff += dictonary[12]
    answere = None
    while answere is None:
        answere = set_list(input(aff), len(tournois) - 1)
        if answere is None:
            print(dictonary[11] + '[0;{len(tournois) - 1}]')
    tournois_selectionnes = []
    for i in answere:
        tournois_selectionnes.append(tournois[i])
    if len(tournois_selectionnes) == 1:
        return tournois_selectionnes[0]
    return creat_multi_tournament(p, tournois_selectionnes)


def main():
    """0"""
    def is_a_tournament(name: str) -> bool:
        m = re.match(r'Tournament (?P<nbr>\d+)', name)
        return m['nbr'] is not None

    p = Path.cwd()
    dictionary: Dict[int, str] = translations['EN']
    if p.parts[-1] == 'Logs':
        p = search_tournament(p, dictionary)
    if is_a_tournament(p.parts[-1]):
        pass
    else:
        print(dictionary[0])
        input(dictionary[999])
    input(f'#{p}')


if __name__ == '__main__':
    main()
