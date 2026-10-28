import numpy as np
import matplotlib.pyplot as plt

DEFAULT_DEFINITIONS = ["WHO Global", "De Jure", "De Facto", "Optimal"]
CMAP_NAME = "RdYlGn"
COLORBAR_LABEL = "PHC spending (% of CHE)"


def ask_list(prompt, default=None):
    """Спрашивает список через запятую. Пустой ввод = значение по умолчанию (если оно есть)."""
    while True:
        raw = input(prompt).strip()
        if not raw and default:
            return default
        items = [x.strip() for x in raw.split(",") if x.strip()]
        if items:
            return items
        print("Нужно ввести хотя бы одно значение.")


def ask_row(country, n_columns):
    """Спрашивает числа для одной страны через пробел и проверяет их количество."""
    while True:
        raw = input(f"  {country}: ").replace(",", ".").split()
        try:
            values = [float(x) for x in raw]
        except ValueError:
            print("  Ошибка: вводи только числа через пробел.")
            continue
        if len(values) != n_columns:
            print(f"  Ошибка: нужно {n_columns} чисел, введено {len(values)}.")
            continue
        return values


def read_data():
    countries = ask_list("Страны через запятую: ")
    definitions = ask_list(
        f"Определения через запятую (Enter = {', '.join(DEFAULT_DEFINITIONS)}): ",
        default=DEFAULT_DEFINITIONS,
    )

    print(f"\nВведи {len(definitions)} чисел через пробел для каждой страны.")
    print(f"Порядок: {', '.join(definitions)}")
    data = np.array([ask_row(c, len(definitions)) for c in countries], dtype=float)
    return countries, definitions, data


def text_color_for(im, value):
    """Чёрный текст на светлой ячейке, белый на тёмной (по яркости цвета ячейки)."""
    r, g, b, _ = im.cmap(im.norm(value))
    brightness = 0.299 * r + 0.587 * g + 0.114 * b
    return "black" if brightness > 0.5 else "white"


def plot_heatmap(countries, definitions, data):
    fig, ax = plt.subplots(figsize=(7.5, 5.2), dpi=200)

    # границы шкалы берём из самих данных
    im = ax.imshow(data, cmap=CMAP_NAME, vmin=data.min(), vmax=data.max(), aspect="auto")

    for edge in ["top", "bottom", "left", "right"]:
        ax.spines[edge].set_visible(False)
    ax.tick_params(axis="both", which="both", length=0)

    # белая сетка между ячейками
    ax.set_xticks(np.arange(-0.5, len(definitions), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(countries), 1), minor=True)
    ax.grid(which="minor", color="white", linestyle="-", linewidth=2, clip_on=False)
    ax.tick_params(which="minor", bottom=False, left=False)

    ax.set_xticks(np.arange(len(definitions)))
    ax.set_yticks(np.arange(len(countries)))
    ax.set_xticklabels(definitions)
    ax.set_yticklabels(countries)

    # значения внутри ячеек
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            val = data[i, j]
            ax.text(j, i, f"{val:.0f}", ha="center", va="center",
                    fontsize=8, color=text_color_for(im, val))

    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label(COLORBAR_LABEL, fontsize=10)
    cbar.ax.tick_params(labelsize=7, direction="in", length=3)

    fig.tight_layout()
    return fig


def main():
    countries, definitions, data = read_data()
    fig = plot_heatmap(countries, definitions, data)

    fig.savefig("phc_heatmap.png", dpi=600, bbox_inches="tight")
    fig.savefig("phc_heatmap.pdf", bbox_inches="tight")
    print("\nСохранено: phc_heatmap.png и phc_heatmap.pdf")

    plt.show()


if __name__ == "__main__":
    main()
