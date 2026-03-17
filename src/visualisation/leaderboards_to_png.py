import matplotlib.pyplot as plt
from matplotlib.table import Table


def leaderboard_to_png(leaderboard_df, color_up, img_path='leaderboard.png'):
    """This function eats a DataFrame and spits out a simple table in the form of png.

    Args:
        leaderboard_df (DataFrame): The DataFrame to write as png
        color_up (Hexadecimal): A given color.
        img_path (the path where to save the pic):
    """

    # Pure data
    data_matrix = leaderboard_df.to_numpy()
    headers = list(leaderboard_df.columns)

    nrows, ncols = data_matrix.shape
    fig, ax = plt.subplots(figsize=(ncols * 1.3, nrows * 0.45 + 0.5))
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    ax.axis('off')

    # Raw matplotlib Table - bulletproof
    tbl = Table(ax, bbox=[0, 0, 1, 1])

    # Add headers (row 0)
    for j, header in enumerate(headers):
        tbl.add_cell(0, j, 1/ncols, 1/(nrows+1), text=header,
                     loc='center', facecolor=color_up)
        tbl[(0, j)].get_text().set(weight='bold', color='white')

    # Add data rows
    for i in range(nrows):
        for j in range(ncols):
            tbl.add_cell(i+1, j, 1/ncols, 1/(nrows+1),
                         text=str(data_matrix[i, j]), loc='center')

    ax.add_table(tbl)
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(10)
    tbl.scale(1, 1)

    plt.savefig(img_path, dpi=500, bbox_inches='tight', pad_inches=0, facecolor='white')
    plt.close()
