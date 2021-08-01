class Plane:
    # 0 area, 1 stock_mod, 2 cat, 3 player, 4 craft_name, 5 nbr_b_gived, 6 nbr_b_received, 7 nbr_m_gived, 8 nbr_m_received, 9 nbr_r_gived, 10 nbr_r_received, 11 b_damages_gived, 12 b_damages_received, 13 m_damages_gived, 14 m_damages_received, 15 parts_destructed_r_gived, 16 parts_destructed_r_received, 17 nbr_clean_kill_b_gived, 18 nbr_clean_kill_b_received, 19 nbr_clean_kill_m_gived, 20 nbr_clean_kill_m_received, 21 nbr_clean_kill_r_gived, 22 nbr_clean_kill_r_received, 23 suicide, 24 mia, 25 b_fired, 26 b_hit, 27 death_order, 28 podium, 29 dead_time, 30 team
    def __init__(self, area, stock_mod, cat, player, craft_name,
                 nbr_b_gived, nbr_b_received, nbr_m_gived, nbr_m_received,
                 nbr_r_gived, nbr_r_received,
                 b_damages_gived, b_damages_received, m_damages_gived, m_damages_received,
                 parts_destructed_r_gived, parts_destructed_r_received,
                 nbr_clean_kill_b_gived, nbr_clean_kill_b_received,
                 nbr_clean_kill_m_gived, nbr_clean_kill_m_received,
                 nbr_clean_kill_r_gived, nbr_clean_kill_r_received,
                 suicide, mia, b_fired, b_hit, death_order, podium, dead_time, team
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
        self.team = team

