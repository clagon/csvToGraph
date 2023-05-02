import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os


def stress_strain_curve_log(area_0, length_0, filename, *, dir="./input", ignoreTail=None):
    df = pd.read_csv(f'{dir}/{filename}', skiprows=4, usecols=[
        1, 3], names=['kajyuu', 'nobi'], encoding="shift-jis", float_precision="high")
    print(f"load{filename}")

    # 公称応力と公称ひずみを計算
    df["ouryoku"] = df["kajyuu"] / area_0
    df["hizumi"] = df["nobi"] / length_0
    # 真応力と真ひずみを計算
    df["shinHizumi"] = np.log((df["hizumi"]+1))
    df["shinOuryoku"] = df["ouryoku"]*(df["hizumi"] + 1)

    df = df.head(ignoreTail*-1)

    fig = plt.figure(filename)
    plt.rcParams['font.family'] = "Meiryo"
    plt.grid(which="both")

    fig = plt.figure(filename)
    ax = fig.add_subplot(1, 1, 1,
        xlabel="真ひずみ",
        ylabel="真応力[MPa]",
        title="真応力-真ひずみ曲線",
        xlim=(0, df["shinHizumi"].max()* 1.05),
        ylim=(0, df["shinOuryoku"]*1.05)
    )

    ax.tick_params(direction='in')
    ax.plot(df["shinHizumi"], df["shinOuryoku"],
            ".", color="black", markersize=1.5)

    name, _ = os.path.splitext(filename)
    plt.savefig(f'./output/log/{name.replace("output/csv/", "")}-log.png')
    plt.show()
    plt.close()


stress_strain_curve_log(47.20, 50.04, "Al.csv", ignoreTail=6)
stress_strain_curve_log(37.9, 49.92, "SS400_3.csv", ignoreTail=6)
stress_strain_curve_log(33.55, 51.58, "SS400_1.csv", ignoreTail=7)
