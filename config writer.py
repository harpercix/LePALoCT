from json import dumps
from typing import Dict, Union, Tuple, List

scoring_table_extracted: List[Tuple[Union[int, float], Dict[str, Union[int, float]]]] = \
    [(0.5, {'player': 0, 'craft_name': 0, 'cat': 0, 'area': 0, 'team': 0,
            'dead_time': 0.001,
            'alive': 0.25,
            'death_order': 0.5,
            'hp': 0,
            'suicide': -0.25,
            'mia': 0}),
     (2, {'nbr_bul_given': 0.1,
          'bul_damages': 0.0002,
          'parts_destructed_bul_given': 0,
          'bul_fired': 0,
          'bul_hit': 0,
          'accuracy': 0,
          'kill_steal_bul_given': 0.5,
          'headshot_bul_given': 1,
          'nbr_clean_kill_bul_given': 2}),
     (-0.2, {'nbr_bul_received': 0.1,
             'bul_damages_received': 0.0002,
             'parts_destructed_bul_received': 0,
             'kill_steal_bul_received': 0.5,
             'headshot_bul_received': 1,
             'nbr_clean_kill_bul_received': 2}),
     (1, {'nbr_mis_given': 0.1,
          'mis_damages_given': 0.0002,
          'parts_destructed_mis_given': 0,
          'hit_mis_given': 0,
          'kill_steal_mis_given': 0.5,
          'headshot_mis_given': 1,
          'nbr_clean_kill_mis_given': 2}),
     (-0.2, {'nbr_mis_received': 0.1,
             'mis_damages_received': 0.0002,
             'parts_destructed_mis_received': 0,
             'kill_steal_mis_received': 0.5,
             'headshot_mis_received': 1,
             'nbr_clean_kill_mis_received': 2}),
     (1, {'nbr_ram_given': 0.1,
          'parts_destructed_ram_given': 0,
          'kill_steal_roc_given': 0.5,
          'headshot_ram_given': 1,
          'nbr_clean_kill_ram_given': 2}),
     (-0.2, {'nbr_ram_received': 0.1,
             'parts_destructed_ram_received': 0,
             'kill_steal_ram_received': 0.5,
             'headshot_ram_received': 1,
             'nbr_clean_kill_ram_received': 2}),
     (1, {'nbr_roc_given': 0.1,
          'roc_damages_given': 0.0002,
          'parts_destructed_roc_given': 0,
          'hit_roc_given': 0,
          'kill_steal_roc_given': 0.5,
          'headshot_roc_given': 1,
          'nbr_clean_kill_roc_given': 2}),
     (-0.2, {'nbr_roc_received': 0.1,
             'roc_damages_received': 0.0002,
             'parts_destructed_roc_received': 0,
             'kill_steal_roc_received': 0.5,
             'headshot_roc_received': 1,
             'nbr_clean_kill_roc_received': 2})
     ]


def convert_table_extracted_to_scoring(table: List[Tuple[Union[int, float], Dict[str, Union[int, float]]]]) \
        -> Dict[str, Union[float, int]]:
    scoring_dict = {}
    for global_scoring, local_scoring_dict in table:
        for key, value in local_scoring_dict.items():
            scoring_dict[key] = round(value * global_scoring, 5)
    return scoring_dict


def write_config(scoring_dict: Dict[str, Union[float, int]]):
    with open('LePALoCT config.json', mode='w') as config_file:
        config_file.write(dumps(scoring_dict, sort_keys=True, indent=2))
