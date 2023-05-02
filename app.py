import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os


def stress_strain_curve(area_0, length_0, filename, *, dir="./input", ignoreTail=None):
    df = pd.read_csv(f'{dir}/{filename}', skiprows=4, usecols=[
        1, 3], names=['kajyuu', 'nobi'], encoding="shift-jis", float_precision="high")
    print(f"load {filename}")

    if ignoreTail is None:
        ignoreTail = len(df)

    df["ouryoku"] = df["kajyuu"] / area_0
    df["hizumi"] = df["nobi"] / length_0
    df["shinHizumi"] = np.log((df["hizumi"]+1))
    df["shinOuryoku"] = df["ouryoku"]*(df["hizumi"] + 1)

    df = df.head(ignoreTail*-1)  # 後ろからignoreTail個を削除

    targets = [
        [
            (df["nobi"], "伸び", "mm"),
            (df["kajyuu"], "荷重", "N")
        ],
        [
            (df["hizumi"], "公称ひずみ", ""),
            (df["ouryoku"], "公称応力", "MPa")
        ],
        [
            (df["shinHizumi"], "真ひずみ", ""),
            (df["shinOuryoku"], "真応力", "MPa")
        ]
    ]
    # df.to_csv(f"./output/csv/{filename[:-4]}_out.csv")

    for i, target in enumerate(targets):

        plt.rcParams['font.family'] = "Meiryo"

        # xlabel = {target[i][0][1]}{'['+starget[i][0][2]+']' if target[i][0][2] != '' else ''}
        if target[0][2] != '':
            xlabel = f"{target[0][1]}[{target[0][2]}]"
        else:
            xlabel = f"{target[0][1]}"
        ylabel = f"{target[1][1]}[{target[1][2]}]"
        title = f"{target[1][1]} - {target[0][1]}線図"

        fig = plt.figure(filename)
        ax = fig.add_subplot(1, 1, 1,
            xlabel=xlabel,
            ylabel=ylabel,
            title=title,
            # x軸の0以下の値を描画しない
            xlim=(0, target[0][0].max()*1.05),
            # y軸の0以下の値を描画しない
            ylim=(0, target[1][0].max()*1.05),
    )

        ax.tick_params(direction='in') # 目盛線を内側に表示
        ax.grid(True)
        ax.plot(target[0][0], target[1][0], ".", color="black", markersize=1.5)

        name, _ = os.path.splitext(filename)
        plt.savefig(f'./output/{name}-{title.replace(" ", "")}.png')
        plt.show()
        plt.close()


print("Hi")
stress_strain_curve(47.20, 50.04, "Al.csv", ignoreTail=6)
stress_strain_curve(37.9, 49.92, "SS400_3.csv", ignoreTail=6)
stress_strain_curve(33.55, 51.58, "SS400_1.csv", ignoreTail=7)
