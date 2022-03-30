import math

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.ticker as ticker
import seaborn as sns

action_colors = ['#f7f7f7', '#e0e0e0','#67a9cf','#d1e5f0','#fddbc7','#ef8a62']
CM_ACTION = LinearSegmentedColormap.from_list("hauki", action_colors, N=6)
ACTION_MIN = 0
ACTION_MAX = 5

CM_VALUE = sns.diverging_palette(275, 150, s=70, as_cmap=True)
VALUE_MIN = -1
VALUE_MAX = 1

CM_VALUE_DIFF = sns.color_palette("Blues", as_cmap=True)
VALUE_DIFF_MIN = 0
VALUE_DIFF_MAX = 2

CM_GRAY = sns.cubehelix_palette(start=0.2, rot=0.2, dark=0.25, light=0.75, gamma=0.8, reverse=False, hue=0, as_cmap=True)
GRAY_MIN = 2
GRAY_MAX = 11

CM_DEALER = sns.cubehelix_palette(start=0.2, rot=0.2, dark=0.25, light=0.75, gamma=1.2, reverse=False, hue=1, as_cmap=True)
DEALER_MIN = 2
DEALER_MAX = 11


COLORMAPS = {
    "actions": (CM_ACTION, ACTION_MIN, ACTION_MAX),
    "values": (CM_VALUE, VALUE_MIN, VALUE_MAX),
    "value_diffs": (CM_VALUE_DIFF, VALUE_DIFF_MIN, VALUE_DIFF_MAX),
    "gray": (CM_GRAY, GRAY_MIN, GRAY_MAX),
    "dealer": (CM_DEALER, DEALER_MIN, DEALER_MAX)
}

BLANK = 0

def get_colormap(content_type):
    return COLORMAPS[content_type]

def format_ax(ax, min_xlim, max_xlim, min_ylim, max_ylim, scale_type):

    sns.set_style("white")

    if scale_type == 'LOG':
        ax.set(xscale="log")
    else:
        ax.ticklabel_format(style='plain', axis='x')

    ax.set_xlim(min_xlim, max_xlim)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x)))
    
    ax.set_ylim(min_ylim, max_ylim)

    lines = plt.legend().get_lines()
    for line in lines:
        line.set_linewidth(4)

    ax.legend(loc='upper right', fontsize=10)
    
    sns.despine()


def plot_overlay_plot(data, ax):
    ax = sns.lineplot(data=data, x='player', y='ref_value', hue="dealer", \
                      marker='o', linestyle=':', legend=False, palette=CM_GRAY)
   

    ax.set_xticks(range(4,22))
    ax.set_xlim(3,22)
    ax.set_ylim(-1,1)
    
    sns.despine()
#    ax.get_legend().remove()


def plot_value_subplot(fig, s, data, title):
    
    ax = fig.add_subplot(2, 2, s)

    ax = sns.lineplot(data=data, x='player', y='ref_value', ax=ax, hue="dealer", \
                      marker='o', markersize=4, linestyle=':', legend=False, palette=CM_GRAY)
    ax = sns.lineplot(data=data, x='player', y='value', ax=ax, hue="dealer", legend="full", palette=CM_DEALER,
                     linewidth=1) #, marker='o', markersize=4)
    
    ax.set_xticks(range(4,22))
    ax.set_yticks([ a/2-1 for a in range(0,5)])

    ax.set_xlim(3,22)
    ax.set_ylim(-1,1)
    
    ax.xaxis.set_tick_params(labelsize=9)
    ax.yaxis.set_tick_params(labelsize=9)
    
    ax.set_title(title, fontdict={'fontsize': 10}, y=0.9)
    
    if s % 2 != 0:
        ax.set_ylabel("state-action value")
    else:
        ax.set_ylabel(None)

    if s <= 2:
        ax.set_xlabel(None)
      
    sns.despine()
    ax.get_legend().remove()


def plot_one_heatmap(ax, data, value, *, agent, iteration, soft, content_type):
    
    cm, vmin, vmax = get_colormap(content_type)

    dp = data.loc[(data['agent'] == agent) & (data['iterations'] == iteration) & (data['soft'] == soft)] \
        .pivot_table(index='player',columns='dealer',values=value, fill_value=BLANK, dropna = False)

    dp = dp.reindex(range(4,22), fill_value=BLANK)
    dp = dp.reindex(columns=range(2,12), fill_value=BLANK)
    dp = dp.sort_index(axis=0, ascending=False)
    
    sns.heatmap(dp, cmap=cm, square=True, linewidths=0.01, linecolor='#e0e0e0', rasterized=False, \
                vmin=vmin, vmax=vmax, cbar=False, ax = ax)

    ax.set_title(f"{agent}: {iteration:,} episodes", fontdict={'fontsize': 12})

    plt.yticks(rotation=0) 

    
def plot_two_heatmaps(fig, data, values, *, agent, iteration, soft, content_types):

    ax = fig.add_subplot(1, 2, 1)
    plot_one_heatmap(ax, data, values[0], agent=agent, iteration=iteration,
                 soft=soft, content_type=content_types[0])

    ax = fig.add_subplot(1, 2, 2)
    plot_one_heatmap(ax, data, values[1], agent=agent, iteration=iteration,
                 soft=soft, content_type=content_types[1])


def get_heatmaps_imgsize(items, size_unit = 0.4):

    w_ratio = 10 + 2
    h_ratio = 18 + 2

    if items > 9:
        cols = 4
    else:
        cols = 3
    
    rows = int(math.ceil(items / cols))
    
    fig_w = size_unit * w_ratio * cols
    fig_h = size_unit * h_ratio * rows

    return fig_w, fig_h


def get_sidebyside_imgsize(cols, rows, size_unit = 0.4):
    w_ratio = 10 + 2
    h_ratio = 18 + 2
    
    fig_w = size_unit * w_ratio * cols
    fig_h = size_unit * h_ratio * rows

    return fig_w, fig_h


def plot_heatmaps(fig, data, value, *, agent, iterations, soft, content_type):

    if len(iterations) > 9:
        cols = 4
    else:
        cols = 3
    
    rows = int(math.ceil(len(iterations) / cols))

    for i, r in enumerate(iterations):
        ax = fig.add_subplot(rows, cols, i+1)
        plot_one_heatmap(ax, data, value, agent=agent, iteration=r, soft=soft, content_type=content_type)


def plot_heatmaps_sidebyside(fig, data, value, *, agents, iterations, soft, content_type):

    rows = len(iterations)
    cols = len(agents)

    for i, r in enumerate(iterations):
        for j, a in enumerate(agents):
            ax = fig.add_subplot(rows, cols, i*cols+j+1)
            plot_one_heatmap(ax, data, value, agent=a['name'], iteration=r, soft=soft, content_type=content_type)


def plot_detail_valuefunc(fig, rows, cols, ddp, ref_change_points):

    colors = ['#67a9cf', '#ef8a62']

    for i, d in enumerate(range(2,12)):

        for soft in (False, True):

            ind = 2 * i + 1 + soft
            ax = fig.add_subplot(rows, cols, ind)

            cp = ref_change_points.loc[(ref_change_points['action'] == True) &
                                       (ref_change_points['soft'] == soft) &
                                       (ref_change_points['dealer'] == d),'change_point']   

            plt.axvline(int(cp) + 0.5, -1,1,color="#d0d0d0",linestyle=':')

            data = ddp.loc[(ddp['dealer'] == d) & (ddp['soft'] == soft)]

            data = data.replace({'action': {False: "Stand", True: "Hit"}})

            data_right = data.loc[(data['a_is_max'] == data['ref_a_is_max'])]
            data_wrong = data.loc[(data['a_is_max'] != data['ref_a_is_max'])]

            hue_order = ['Stand','Hit']

            ax = sns.lineplot(data=data, x='player', y='ref_value', hue="action", hue_order=hue_order, palette=colors, 
                              linestyle=':', ax=ax, legend=False)

            ax = sns.lineplot(data=data, x='player', y='value', hue="action", hue_order=hue_order,  palette=colors,
                              marker='', linestyle='-', ax=ax, legend='full')
            ax = sns.lineplot(data=data_right, x='player', y='value', hue="action", hue_order=hue_order, palette=colors,
                              marker='o', linestyle='', legend=False, ax=ax)
            ax = sns.lineplot(data=data_wrong, x='player', y='value', hue="action", hue_order=hue_order, palette=colors,
                              marker='X', markersize=10, linestyle='', legend=False, ax=ax)

            ax.set_xticks(range(4,22))
            ax.set_yticks([ a/2-1 for a in range(0,5)])

            ax.xaxis.set_tick_params(labelsize=9)
            ax.yaxis.set_tick_params(labelsize=9)

            ax.set_xlim(3,22)
            ax.set_ylim(-1,1)

            if ind % 2 != 0:
                ax.set_ylabel("state-action value")
            else:
                ax.set_ylabel(None)

            if ind <= rows * cols - cols:
                ax.set_xlabel(None)

            ax.legend(loc='upper left', fontsize=8)
            ax.set_title(f"Dealer: {d}, Soft: {soft}", fontdict={'fontsize': 10}, y=0.9)


            sns.despine()   