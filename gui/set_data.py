#規定外のフラグの値の時、デフォルト設定にする
from data import get_data #前回設定の読み込み

def set_data():
    flag_graph, flag_sound = get_data()
    if flag_graph > 3 or flag_graph < 1:
        flag_graph = 2
    if flag_sound > 5 or flag_sound < 4:
        flag_sound = 4

    return [flag_graph, flag_sound]