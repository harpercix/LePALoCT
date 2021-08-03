from pathlib import Path
import re
from typing import List, Dict, Tuple, Union

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
    # 0 area, 1 stock_mod, 2 cat, 3 player, 4 craft_name, 5 nbr_b_gived, 6 nbr_b_received, 7 nbr_m_gived, 8 nbr_m_received, 9 nbr_r_gived, 10 nbr_r_received, 11 b_damages_gived, 12 b_damages_received, 13 m_damages_gived, 14 m_damages_received, 15 parts_destructed_r_gived, 16 parts_destructed_r_received, 17 nbr_clean_kill_b_gived, 18 nbr_clean_kill_b_received, 19 nbr_clean_kill_m_gived, 20 nbr_clean_kill_m_received, 21 nbr_clean_kill_r_gived, 22 nbr_clean_kill_r_received, 23 alive, 24 suicide, 25 mia, 26 b_fired, 27 b_hit, 28 death_order, 29 dead_time, 30 hp, 31 team
    def __init__(self, area, stock_mod, cat, player, craft_name,
                 nbr_b_gived, nbr_b_received, nbr_m_gived, nbr_m_received,
                 nbr_r_gived, nbr_r_received,
                 b_damages_gived, b_damages_received, m_damages_gived, m_damages_received,
                 parts_destructed_r_gived, parts_destructed_r_received,
                 nbr_clean_kill_b_gived, nbr_clean_kill_b_received,
                 nbr_clean_kill_m_gived, nbr_clean_kill_m_received,
                 nbr_clean_kill_r_gived, nbr_clean_kill_r_received,
                 alive, suicide, mia, b_fired, b_hit, death_order, dead_time, hp, team
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
        self.alive = alive
        self.suicide = suicide
        self.mia = mia
        self.b_fired = b_fired
        self.b_hit = b_hit
        self.death_order = death_order
        self.dead_time = dead_time
        self.hp = hp
        self.team = team


class Tournament:
    def __init__(self, duration: int, max_duration: int, planes: Dict[str, Plane]):
        self.duration = duration
        self.max_duration = max_duration
        self.planes = planes


class Heat(Tournament):
    def __init__(self, duration: int, max_duration: int, planes: Dict[str, Plane]):
        super().__init__(duration, max_duration, planes)


def name_separator(name: str) -> Tuple[str, str, str, str, Union[str, None]]:
    m = re.match('(?P<area>[^-]+)-(?P<cat>[^-]+)-(?P<player>[^-]+)-(?P<craft_name>[^-]+)', name)
    team = None
    if m is None:
        m = re.match('(?P<area>[^-]+)-(?P<cat>[^-]+)-(?P<team>[^-]+)-(?P<player>[^-]+)-(?P<craft_name>[^-]+)', name)
        if m is None:
            print(f'#ERROR incorect name : "{name}"')
            return 'NA', 'NA', 'NA', name, None
    else:
        team = m['team']
    n = re.match('(?P<craft_name>[^_]+)_(?P<nbr>.+)', m['craft_name'])
    if n is None:
        return m['area'], m['cat'], m['player'], m['craft_name'], team
    return m['area'], m['cat'], m['player'], n['craft_name'], team


def analyse_regular_line(line: str, heat: Heat) -> Heat:
    m = re.match(r'\[.+]: (?P<e_type>[A-Z]+):(?P<event>.+)$', line)
    if m is None:
        print(f'#ERROR analyse_regular_line: "{line}"')
        return heat
    e_type = m['e_type']
    event = m['event']
    print(f'#{e_type} {event}')
    if e_type == 'ALIVE':
        if event[:7] not in ('Débris', 'DÃ©bris') and event[-5:] not in ('Avion', 'avion'):
            heat.planes[event].dead_time = -1
            heat.planes[event] = Plane()
    if e_type == 'DEAD':
        m = re.match(r'(?P<death_order>\d+):(?P<s>\d+).(?P<ds>\d+):(?P<name>.*)$', event)
        heat.planes[m['name']].dead_time = int(m['s']) + int(m['ds']) * 0.1
        heat.planes[m['name']].suicide = 1
    if e_type == 'MIA':
        pass

    return heat


def analyse_first_line(line: str, heat: Heat) -> Heat:
    m = re.match(r'\[[^:]*:(?P<tag>\d+)]: '
                 r'Dumping Results after (?P<duration>\d+)s \(of (?P<max_duration>.+)s\) at '
                 r'(?P<date>\d{4}-\d{2}-\d{2}) (?P<hour>\d{2}:\d{2}:\d{2}) [+-]\d{2}:\d{2}$', line)
    heat.duration += int(m['duration'])
    heat.max_duration += int(m['max_duration'])
    return heat


def heat_f(p: Path, tournament: Tournament, tag: str, nbr: str):
    print(f'##{p.name}')
    file = []
    with open(p) as file_read:
        for line in file_read:
            file.append(line)
    heat = Heat(-1, -1, {})
    heat = analyse_first_line(file[0], heat)
    for line in file[1:]:
        heat = analyse_regular_line(line, heat)


def round_f(p: Path, tournament: Tournament):
    print(f'##{p.name}')
    for f in p.iterdir():
        filename = f.name
        print(f'#{filename}')
        m = re.match(r'(?P<tag>\d{8})-Heat (?P<nbr>\d+)\.log$', filename)
        if m is not None:
            heat_f(f, tournament, m['tag'], m['nbr'])


def tournament_f(p: Path, dictonary: Dict[int, str]):
    """2"""
    print('##Tournament')
    tournament = Tournament(0, 0, {})
    for f in p.iterdir():
        filename = f.name
        print(f'#{filename}')
        m = re.match(r'Round (?P<nbr>\d+)', filename)
        if m is not None:
            round_f(f, tournament)


def creat_multi_tournament(p: Path, list_tournaments: List) -> Path:
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


def search_tournament(p: Path, dictonary: Dict[int, str]) -> Path:
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
        if m is not None:
            return True
        m = re.match('Total Tournament (?P<nbrs>.+)', name)
        return m is not None

    p = Path.cwd()
    dictionary: Dict[int, str] = translations['EN']
    if p.parts[-1] == 'Logs':
        p = search_tournament(p, dictionary)
    if is_a_tournament(p.parts[-1]):
        tournament_f(p, dictionary)
    else:
        print(dictionary[0])
        input(dictionary[999])
    input(f'#{p}')


if __name__ == '__main__':
    main()
