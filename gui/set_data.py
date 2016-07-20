#規定外のフラグの値の時、デフォルト設定にする
from osog.gui.data import get_data #前回設定の読み込み

def set_data():
    flag_graph, flag_sound, flag_alarm = get_data()
    if flag_graph > 3 or flag_graph < 1:
        flag_graph = 2
    if flag_sound > 5 or flag_sound < 4:
        flag_sound = 4
    if flag_alarm > 10 or flag_alarm < 6:
        flag_alarm = 6

    return [flag_graph, flag_sound, flag_alarm]