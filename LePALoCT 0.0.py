import csv
from json import loads
from pathlib import Path
import re
from typing import List, Dict, Tuple, Union, Any

translations = {'FR': {0: 'LePALoCT n\'est pas au bon fichier.\nIl doit etre dans "Logs" ou dans un tournoi.',
                       10: 'Choisis un ou plusieurs tournois parmis ceux ci (separes par des "-") :\n',
                       11: 'Il faut un ou plusieurs nombres (separes par des "-", exemple : "42-666-512") entre ',
                       12: '\n[numeros] : ',
                       998: 'avec',
                       999: '[Entrer] pour continuer'},
                'EN': {0: 'LePALoCT isn\'t in the good folder.\nIt would be in "Logs" or in a tournament.',
                       10: 'Choose one or several tournaments (separated with "-"):\n',
                       11: 'You need one or several numbers (separated with "-", exemple: "42-666-512") between ',
                       12: '\n[numbers]: ',
                       100: 'area',
                       101: 'category',
                       102: 'player',
                       103: 'craft name',
                       104: 'shot bullet given',
                       105: 'shot bullet received',
                       106: 'shot missile given',
                       107: 'shot missile received',
                       108: 'shot ram given',
                       109: 'shot ram received',
                       110: 'hit bullet given',
                       111: 'hit bullet received',
                       112: 'hit missile given',
                       113: 'hit missile received',
                       114: 'bullet damages given',
                       115: 'bullet damages received',
                       116: 'missile damages given',
                       117: 'missile damages received',
                       118: 'parts rammed given',
                       119: 'parts rammed received',
                       120: 'clean kill bullet given',
                       121: 'clean kill bullet received',
                       122: 'clean kill missile given',
                       123: 'clean kill missile received',
                       124: 'clean kill ram given',
                       125: 'clean kill ram received',
                       126: 'alive',
                       127: 'Suicide',
                       128: 'MIA',
                       129: 'bullets fired',
                       130: 'bullet hit',
                       131: 'death order',
                       132: 'dead time',
                       133: 'HP',
                       134: 'nbr heat',
                       135: 'team',
                       200: 'Longest Heat:',
                       201: 'Shortest Heat:',
                       202: 'Max kills',
                       998: 'with',
                       999: '[Enter] to continue'}}

column_name = ['area', 'cat', 'player', 'craft_name', 'nbr_b_given', 'nbr_b_received',
               'nbr_m_given', 'nbr_m_received', 'nbr_r_given', 'nbr_r_received',
               'hit_b_given', 'hit_b_received', 'hit_m_given', 'hit_m_received',
               'b_damages_given', 'b_damages_received', 'm_damages_given', 'm_damages_received',
               'parts_destructed_r_given', 'parts_destructed_r_received',
               'nbr_clean_kill_b_given', 'nbr_clean_kill_b_received',
               'nbr_clean_kill_m_given', 'nbr_clean_kill_m_received',
               'nbr_clean_kill_r_given', 'nbr_clean_kill_r_received',
               'alive', 'suicide', 'mia', 'b_fired', 'b_hit', 'death_order',
               'dead_time', 'hp', 'nbr heat', 'team']

column_to_nbr: Dict[int, Union[str, Any]] = {}
for i, column in enumerate(column_name):
    column_to_nbr[column] = i


class Plane:
    def __init__(self, area, cat, player, craft_name,
                 nbr_b_given, nbr_b_received, nbr_m_given, nbr_m_received,
                 nbr_r_given, nbr_r_received,
                 hit_b_given, hit_b_received, hit_m_given, hit_m_received,
                 b_damages_given, b_damages_received, m_damages_given, m_damages_received,
                 parts_destructed_r_given, parts_destructed_r_received,
                 nbr_clean_kill_b_given, nbr_clean_kill_b_received,
                 nbr_clean_kill_m_given, nbr_clean_kill_m_received,
                 nbr_clean_kill_r_given, nbr_clean_kill_r_received,
                 alive, suicide, mia, b_fired, b_hit, death_order, dead_time, hp, nbr_heat_done, team
                 ):
        self.area = area
        self.cat = cat
        self.player = player
        self.craft_name = craft_name
        self.nbr_b_given = nbr_b_given
        self.nbr_b_received = nbr_b_received
        self.nbr_m_given = nbr_m_given
        self.nbr_m_received = nbr_m_received
        self.nbr_r_given = nbr_r_given
        self.nbr_r_received = nbr_r_received
        self.hit_b_given = hit_b_given
        self.hit_b_received = hit_b_received
        self.hit_m_given = hit_m_given
        self.hit_m_received = hit_m_received
        self.b_damages_given = b_damages_given
        self.b_damages_received = b_damages_received
        self.m_damages_given = m_damages_given
        self.m_damages_received = m_damages_received
        self.parts_destructed_r_given = parts_destructed_r_given
        self.parts_destructed_r_received = parts_destructed_r_received
        self.nbr_clean_kill_b_given = nbr_clean_kill_b_given
        self.nbr_clean_kill_b_received = nbr_clean_kill_b_received
        self.nbr_clean_kill_m_given = nbr_clean_kill_m_given
        self.nbr_clean_kill_m_received = nbr_clean_kill_m_received
        self.nbr_clean_kill_r_given = nbr_clean_kill_r_given
        self.nbr_clean_kill_r_received = nbr_clean_kill_r_received
        self.alive = alive
        self.suicide = suicide
        self.mia = mia
        self.b_fired = b_fired
        self.b_hit = b_hit
        self.death_order = death_order
        self.dead_time = dead_time
        self.hp = hp
        self.nbr_heat_done = nbr_heat_done
        self.team = team

    def define_accuracy(self, hit: int, fired: int):
        self.b_hit = hit
        self.b_fired = fired

    def display(self, dictionary: Dict[int, str]):
        return table_diplay(create_table(Tournament(0, 0, {self.name_creator(): self}), dictionary))
    
    def name_creator(self):
        if self.team is None:
            return f'{self.area}-{self.cat}-{self.player}-{self.craft_name}'
        return f'{self.area}-{self.cat}-{self.team}-{self.player}-{self.craft_name}'

    def count_nbr_death(self):
        return self.nbr_clean_kill_b_given + self.nbr_clean_kill_m_given + self.nbr_clean_kill_r_given

    def values_plane(self) -> List[Union[str, int, float]]:
        return [self.area, self.cat, self.player, self.craft_name, self.nbr_b_given, self.nbr_b_received,
                self.nbr_m_given, self.nbr_m_received, self.nbr_r_given, self.nbr_r_received,
                self.hit_b_given, self.hit_b_received, self.hit_m_given, self.hit_m_received,
                self.b_damages_given, self.b_damages_received, self.m_damages_given, self.m_damages_received,
                self.parts_destructed_r_given, self.parts_destructed_r_received,
                self.nbr_clean_kill_b_given, self.nbr_clean_kill_b_received,
                self.nbr_clean_kill_m_given, self.nbr_clean_kill_m_received,
                self.nbr_clean_kill_r_given, self.nbr_clean_kill_r_received,
                self.alive, self.suicide, self.mia, self.b_fired, self.b_hit, self.death_order,
                self.dead_time, self.hp, self.nbr_heat_done, self.team]


class Tournament:
    def __init__(self, duration: int, max_duration: int, planes: Dict[str, Plane]):
        self.duration = duration
        self.max_duration = max_duration
        self.planes = planes


class Heat(Tournament):
    def __init__(self, name: str, duration: int, max_duration: int, planes: Dict[str, Plane]):
        super().__init__(duration, max_duration, planes)
        self.name = name
    
    def death_order_sort(self):
        max_death_order = 0
        for avion in self.planes.values():
            max_death_order = max(avion.death_order, max_death_order)
        for avion in self.planes.values():
            if avion.death_order == -1:
                avion.death_order = max_death_order + 1


def name_separator(name: str) -> Tuple[str, str, str, str, Union[str, None], str]:
    m = re.match('(?P<area>[^-]+)-(?P<cat>[^-]+)-(?P<player>[^-]+)-(?P<craft_name>[^-]+)', name)
    team = None
    if m is None:
        m = re.match('(?P<area>[^-]+)-(?P<cat>[^-]+)-(?P<team>[^-]+)-(?P<player>[^-]+)-(?P<craft_name>[^-]+)', name)
        if m is None:
            debug = f'#ERROR incorect name : "{name}"\n'
            return 'NA', 'NA', 'NA', name, None, debug
        team = m['team']
    n = re.match('(?P<craft_name>[^_]+)_(?P<nbr>.+)', m['craft_name'])
    if n is None:
        return m['area'], m['cat'], m['player'], m['craft_name'], team, ''
    return m['area'], m['cat'], m['player'], n['craft_name'], team, ''


def create_plane(name: str, dead_time: float, nbr_heat: int) -> Tuple[Plane, str]:
    area, cat, player, craft_name, team, debug = name_separator(name)
    return Plane(area, cat, player, craft_name, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, dead_time, 0, nbr_heat, team), debug


def analyse_several_crafts(event: str) -> Tuple[str, float, Tuple[str, float], List[Tuple[str, float]]]:
    m = re.match(r'(?P<victim>[^:]+):(?P<queue>.+)$', event)
    victim: str = m['victim']
    total_damages: float = 0
    killers: List[Tuple[str, float]] = []
    n = re.match(r'(?P<damages>[^:]+):(?P<killer>[^:]+):(?P<queue>.+)$', m['queue'])
    if n is None:
        m = re.match(r'(?P<damages>[^:]+):(?P<killer>.+)$', m['queue'])
        return victim, float(m['damages']), (m['killer'], float(m['damages'])), []
    m = n
    while n is not None:
        m = n
        total_damages += float(n['damages'])
        killers.append((n['killer'], float(n['damages'])))
        n = re.match(r'(?P<damages>[^:]+):(?P<killer>[^:]+):(?P<queue>.+)$', m['queue'])
    m = re.match(r'(?P<damages>[^:]+):(?P<killer>.+)$', m['queue'])
    total_damages += float(m['damages'])
    killers.append((m['killer'], float(m['damages'])))
    return victim, total_damages, killers[0], killers[1:]


def analyse_regular_line(line: str, heat: Heat) -> Heat:
    m = re.match(r'\[.+]: (?P<e_type>[A-Z]+):(?P<event>.+)$', line)
    if m is None:
        input(f'#ERROR analyse_regular_line: "{line}"')
        return heat
    e_type = m['e_type']
    event = m['event']
    if e_type == 'ALIVE':
        if event[:7] not in ('Débris', 'DÃ©bris') and event[-5:] not in (
        'Avion', 'avion', 'Probe') and event in heat.planes:
            heat.planes[event].dead_time = heat.duration
    elif e_type == 'DEAD':
        m = re.match(r'(?P<death_order>\d+):(?P<s>\d+).(?P<ds>\d+):(?P<name>.*)$', event)
        heat.planes[m['name']].dead_time = int(m['s']) + int(m['ds']) * 0.1
        heat.planes[m['name']].death_order = int(m['death_order']) + 1
        heat.planes[m['name']].suicide = 1
    elif e_type == 'MIA':
        pass
    elif e_type == 'ACCURACY':
        m = re.match(r'(?P<name>[^:]+):(?P<hit>\d+)/(?P<fired>\d+)', event)
        heat.planes[m['name']].define_accuracy(int(m['hit']), int(m['fired']))
    elif e_type == 'WHOSHOTWHO':
        victim, damages_received, killer, accomplices = analyse_several_crafts(event)
        heat.planes[victim].hit_b_received += damages_received
        heat.planes[victim].nbr_b_received += 1
        for name, damages in [killer] + accomplices:
            heat.planes[name].hit_b_given += damages
            heat.planes[name].nbr_b_given += 1
    elif e_type == 'WHOHITWHOWITHMISSILES':
        victim, damages_received, killer, accomplices = analyse_several_crafts(event)
        heat.planes[victim].hit_m_received += damages_received
        heat.planes[victim].nbr_m_received += 1
        for name, damages in [killer] + accomplices:
            heat.planes[name].hit_m_given += damages
            heat.planes[name].nbr_m_given += 1
    elif e_type == 'WHORAMMEDWHO':
        victim, damages_received, killer, accomplices = analyse_several_crafts(event)
        heat.planes[victim].parts_destructed_r_received += damages_received
        heat.planes[victim].nbr_r_received += 1
        for name, damages in [killer] + accomplices:
            heat.planes[name].parts_destructed_r_given += damages
            heat.planes[name].nbr_r_given += 1
    elif e_type == 'CLEANKILL':
        m = re.match(r'(?P<victim>[^:]+):(?P<killer>.+)', event)
        heat.planes[m['victim']].nbr_clean_kill_b_received += 1
        heat.planes[m['victim']].suicide = 0
        heat.planes[m['killer']].nbr_clean_kill_b_given += 1
    elif e_type == 'CLEANMISSILEKILL':
        m = re.match(r'(?P<victim>[^:]+):(?P<killer>.+)', event)
        heat.planes[m['victim']].nbr_clean_kill_m_received += 1
        heat.planes[m['victim']].suicide = 0
        heat.planes[m['killer']].nbr_clean_kill_m_given += 1
    elif e_type == 'CLEANRAM':
        m = re.match(r'(?P<victim>[^:]+):(?P<killer>.+)', event)
        heat.planes[m['victim']].nbr_clean_kill_r_received += 1
        heat.planes[m['victim']].suicide = 0
        heat.planes[m['killer']].nbr_clean_kill_r_given += 1
    elif e_type == 'WHODAMAGEDWHOWITHBULLETS':
        victim, damages_received, killer, accomplices = analyse_several_crafts(event)
        heat.planes[victim].b_damages_received += damages_received
        for name, damages in [killer] + accomplices:
            heat.planes[name].b_damages_given += damages
    elif e_type == 'WHODAMAGEDWHOWITHMISSILES':
        victim, damages_received, killer, accomplices = analyse_several_crafts(event)
        heat.planes[victim].m_damages_received += damages_received
        for name, damages in [killer] + accomplices:
            heat.planes[name].m_damages_given += damages
    elif e_type == 'HPLEFT':
        m = re.match(r'(?P<name>[^:]+):(?P<hp>.+)', event)
        heat.planes[m['name']].hp = float(m['hp'])
    elif e_type == 'RESULT':
        if event == 'Mutual Annihilation':
            return heat
        m = re.match(r'(?P<result>[^:]+):(?P<team>.+)$', event)
        if m['result'] == 'Draw':
            list_team = loads(m['team'])  # It looks like json
            for team_text in list_team:
                for name_plane in team_text['members']:
                    if name_plane not in heat.planes:
                        heat.planes[name_plane], debug = create_plane(name_plane, -4, 1)
        elif m['result'] == 'Win':
            team_text = loads(m['team'])
            if type(team_text) == dict:
                for name_plane in team_text['members']:
                    if name_plane not in heat.planes:
                        heat.planes[name_plane], debug = create_plane(name_plane, -4, 1)
                return heat
            for dictionnary in team_text:
                for name_plane in dictionnary['members']:
                    if name_plane not in heat.planes:
                        heat.planes[name_plane], debug = create_plane(name_plane, -4, 1)
    elif e_type == 'DEADTEAMS':
        list_team = loads(event)  # It look like json
        for team_text in list_team:
            for name_plane in team_text['members']:
                if name_plane not in heat.planes:
                    heat.planes[name_plane], debug = create_plane(name_plane, -3, 1)
    else:
        input(f'#ERROR analyse_regular_line: "{line}"')
    return heat


def analyse_first_line(line: str, heat: Heat) -> Heat:
    m = re.match(r'\[[^:]*:(?P<tag>\d+)]: '
                 r'Dumping Results after (?P<duration>\d+)s \(of (?P<max_duration>.+)s\) at '
                 r'(?P<date>\d{4}-\d{2}-\d{2}) (?P<hour>\d{2}:\d{2}:\d{2}) [+-]\d{2}:\d{2}$', line)
    heat.duration += int(m['duration'])
    heat.max_duration += int(m['max_duration'])
    return heat


def create_complet_plane(values: Tuple):
    area, cat, player, craft_name, nbr_b_given, nbr_b_received, \
    nbr_m_given, nbr_m_received, nbr_r_given, nbr_r_received, \
    hit_b_given, hit_b_received, hit_m_given, hit_m_received, \
    b_damages_given, b_damages_received, m_damages_given, m_damages_received, \
    parts_destructed_r_given, parts_destructed_r_received, \
    nbr_clean_kill_b_given, nbr_clean_kill_b_received, \
    nbr_clean_kill_m_given, nbr_clean_kill_m_received, \
    nbr_clean_kill_r_given, nbr_clean_kill_r_received, \
    alive, suicide, mia, b_fired, b_hit, death_order, \
    dead_time, hp, nbr_heat_done, team = values
    return Plane(area, cat, player, craft_name, nbr_b_given, nbr_b_received,
                 nbr_m_given, nbr_m_received, nbr_r_given, nbr_r_received,
                 hit_b_given, hit_b_received, hit_m_given, hit_m_received,
                 b_damages_given, b_damages_received, m_damages_given, m_damages_received,
                 parts_destructed_r_given, parts_destructed_r_received,
                 nbr_clean_kill_b_given, nbr_clean_kill_b_received,
                 nbr_clean_kill_m_given, nbr_clean_kill_m_received,
                 nbr_clean_kill_r_given, nbr_clean_kill_r_received,
                 alive, suicide, mia, b_fired, b_hit, death_order,
                 dead_time, hp, nbr_heat_done, team)


def add_heat_to_tournament(heat: Heat, tournament: Tournament) -> Tournament:
    tournament.duration += heat.duration
    debug = ''
    tournament.max_duration += heat.max_duration
    for name, plane_h in heat.planes.items():
        if name not in tournament.planes:
            tournament.planes[name], d = create_plane(name, 0, 0)
            debug += d
        list_values_t = tournament.planes[name].values_plane()
        list_values_h = plane_h.values_plane()
        for i in range(3, len(list_values_t)):
            if type(list_values_h[i]) == int or type(list_values_h[i]) == float:
                list_values_t[i] += list_values_h[i]
        tournament.planes[name] = create_complet_plane(tuple(list_values_t))
    return tournament


def heat_f(p: Path) -> Tuple[Heat, str]:
    debug = f'##Heat {p}\n'
    file = []
    with p.open() as file_read:
        for line in file_read:
            file.append(line)
    heat = Heat(p.name, -1, -1, {})
    heat = analyse_first_line(file[0], heat)
    for line in file[1:]:
        if line != "\n":
            heat = analyse_regular_line(line, heat)
    return heat, debug


def round_f(p: Path, tournament: Tournament) -> Tuple[Tournament, List[Heat], str]:
    debug = f'##Round {p}\n'
    heats_list = []
    for f in p.iterdir():
        filename = f.name
        m = re.fullmatch(r'(?P<tag>\d{8})-Heat (?P<round_nbr>\d+)\.log', filename)
        if m is not None:
            heat, d = heat_f(f)
            heat.death_order_sort()
            tournament = add_heat_to_tournament(heat, tournament)
            heats_list.append(heat)
            debug += d
    return tournament, heats_list, debug


def create_table(tournament: Tournament, dictionary: Dict[int, str]) -> List[List[str]]:
    """10"""
    column_organisation = column_name[:]
    columns = []
    for name, plane in tournament.planes.items():
        values_of_planes = {}
        for i, value in enumerate(plane.values_plane()):
            values_of_planes[column_name[i]] = (i, value)
        columns.append(values_of_planes)
    table: List[List[str]] = []
    first_line: List[str] = []
    for column_title in column_organisation:
        first_line.append(dictionary[100 + column_to_nbr[column_title]])
    table.append(first_line)
    for plane_line in columns:
        line: List[Union[str]] = []
        for columns_title in column_organisation:
            line.append(str(plane_line[columns_title][1]))
        table.append(line)
    return table


def table_diplay(table: List[List[str]]) -> Tuple[str, str]:
    list_lenght_columns = [0] * len(table[0])
    for line in table:
        for i, case in enumerate(line):
            if list_lenght_columns[i] < len(case):
                list_lenght_columns[i] = len(case)
    debug = f'#table_display {list_lenght_columns}\n'
    aff = ''
    for line in table:
        for i, case in enumerate(line):
            aff += case + ' ' * (list_lenght_columns[i] - len(case)) + ' : '
        aff += '\n'
    return aff, debug


def csv_creator(p, table: List[List[str]]):
    file_name = p / Path(f'table {p.name}.csv')
    with open(file_name, mode='w') as csv_table:
        table_writer = csv.writer(csv_table, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, dialect='unix')
        for line in table:
            table_writer.writerow(line)


def tournament_f(p: Path, dictonary: Dict[int, str]):
    """2"""
    heats_list = []
    debug = '##Tournament\n'
    print('Progress bar:\n|' + '-' * 98 + '|')
    nbr_file = len(list(p.iterdir()))
    tournament = Tournament(0, 0, {})
    j = 0
    for f in p.iterdir():
        filename = f.name
        debug += f'#{filename}\n'
        m = re.match(r'Round (?P<nbr>\d+)', filename)
        if m is not None:
            tournament, hl, d = round_f(f, tournament)
            heats_list.extend(hl)
            debug += d
        j += 1
        for i in range(round((j - 1) / nbr_file * 100), round(j / nbr_file * 100)):
            if i % 10 == 0:
                print('|', end='')
            elif i % 5 == 0:
                print(':', end='')
            else:
                print('.', end='')
    print()
    table = create_table(tournament, dictonary)
    display, d = table_diplay(table)
    debug += d
    print(debug)
    input(display)
    csv_creator(p, table)
    success_f(heats_list, tournament.planes, dictonary)
    input()


def count_nbr_death(plane: Plane):
    return plane.nbr_clean_kill_b_given + plane.nbr_clean_kill_m_given + plane.nbr_clean_kill_r_given


def success_f(heats_list: List[Heat], planes: Dict[str, Plane], dictionary: Dict[int, str]):
    print("\n\nSUCCESS:")
    maxi_duration = 0
    heat_name = 'Non rien de rien'
    for heat in heats_list:
        if maxi_duration < heat.duration:
            maxi_duration = heat.duration
            heat_name = heat.name
        elif maxi_duration == heat.max_duration:
            break
    else:
        if heat_name != 'Non rien de rien':
            print(f'{dictionary[200]} {heat_name} {dictionary[998]} {maxi_duration}s')
    mini_duration = 0
    heat_name = 'Non rien de rien'
    for heat in heats_list:
        if mini_duration > heat.duration:
            mini_duration = heat.duration
            heat_name = heat.name
        elif mini_duration == heat.max_duration:
            break
    else:
        if heat_name != 'Non rien de rien':
            print(f'{dictionary[201]} {heat_name} {dictionary[998]} {mini_duration}s')
    craft_name = 'Non rien de rien'
    nbr_dead = 0
    for plane in planes.values():
        if count_nbr_death(plane) > nbr_dead:
            nbr_dead += count_nbr_death(plane)
            craft_name = plane.name_creator()
        elif nbr_dead == count_nbr_death(plane):
            break
    else:
        if heat_name != 'Non rien de rien':
            print(f'{dictionary[202]} {craft_name} {dictionary[998]} {nbr_dead}')


def creat_multi_tournament(p: Path, list_tournaments: List[Path]) -> Path:
    total_name = 'Total Tournament '
    for t in list_tournaments:
        m = re.match(r'Tournament (?P<nbrs>\d+)', t.name)
        total_name += m['nbrs'] + ' '
    total_name = total_name.strip()
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
                with heat_n.open() as file:
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
        if f.name[0:11] == 'Tournament ' and len(f.name) == 19:
            tournois.append(f)
    aff = dictonary[10]
    for i, t in enumerate(tournois):
        aff += f'[{i}] : {t.name}\n'
    aff += dictonary[12]
    answere = None
    while answere is None:
        answere = set_list(input(aff), len(tournois) - 1)
        if answere is None:
            print(dictonary[11] + f'[0;{len(tournois) - 1}]')
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
    if p.name == 'Logs':
        p = search_tournament(p, dictionary)
    if is_a_tournament(p.name):
        tournament_f(p, dictionary)
    else:
        print(dictionary[0])
        input(dictionary[999])


if __name__ == '__main__':
    main()
