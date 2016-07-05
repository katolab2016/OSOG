#想定ではxに画像の表示について,yに警告音についてのフラグを対応させる

def save(x, y):
    x_text = str(x)
    y_text = str(y)
    text_xy = """def get_data():
       x = """ + x_text + """
       y = """ + y_text + """
       return [x, y]"""
    f = open("data.py", "w")
    f.write(text_xy)
    f.close()

if __name__ == "__main__":
    x = 1
    y = 4
    save(x, y)