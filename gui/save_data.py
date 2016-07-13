#xに画像の表示について,yに警告音について,zに警告音の種別のフラグを対応させる

def save(x, y, z):
    x_text = str(x)
    y_text = str(y)
    z_text = str(z)
    text_xyz = """def get_data():
       x = """ + x_text + """
       y = """ + y_text + """
       z = """ + z_text + """
       return [x, y, z]"""
    f = open("data.py", "w")
    f.write(text_xyz)
    f.close()

if __name__ == "__main__":
    x = 1
    y = 4
    save(x, y)