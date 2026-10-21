import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.widgets import Slider, Button
import time

start_time = time.time()

PARTY_COLOURS = {
    "Labour": "#E4003B",
    "Conservative": "#0087DC",
    "Lib Dem": "#FAA61A",
    "Green": "#02A95B",
    "Reform": "#12B6CF",
    "WPB/Others": "#780021",
}

swing_factor = {
    'Labour': 0.65,
    'Conservative': 0.8,
    'Green': 2,
    'Lib Dem': 1,
    'Reform': 2,
    'WPB/Others': 1.2
}

# 2024 actual results for Greater Manchester
actual_2024 = {
    'Labour': {'vote_share': 44.5, 'wards': 145},
    'Conservative': {'vote_share': 17.3, 'wards': 17},
    'Lib Dem': {'vote_share': 11.4, 'wards': 21},
    'Green': {'vote_share': 10.3, 'wards': 5},
    'Reform': {'vote_share': 2.1, 'wards': 0},
    'WPB/Others': {'vote_share': 14.1, 'wards': 27},
}


parties = ['Labour', 'Conservative', 'Green', 'Lib Dem',
           'Reform', 'WPB/Others']
# greater_manchester_boroughs = ['Manchester']
greater_manchester_boroughs = ['Manchester', 'Trafford', 'Tameside',
                               'Stockport', 'Salford', 'Oldham', 'Bury',
                               'Rochdale', 'Bolton', 'Wigan']
model = pd.read_excel('GM LE26 results.xlsx').sort_values('Ward').dropna()
model = model[model['Borough'].isin(greater_manchester_boroughs)]
model['2024 Winner'] = model[parties].idxmax(axis=1)
print("load model --- %s seconds ---" % (time.time() - start_time))


def calculate_projection(current_swing_factors):
    modelled_votes = pd.DataFrame()
    modelled_votes['Ward'] = model['Ward'].copy()
    for party in parties:
        modelled_votes[party] = original_votes[party] * current_swing_factors[party]
    return modelled_votes

def calculate_statistics(modelled_votes):
    """Calculate vote share and ward counts from modelled votes"""
    # Determine winners per ward
    projected_winner = modelled_votes[parties].idxmax(axis=1)

    # Calculate total vote shares
    total_votes = modelled_votes[parties].sum()
    vote_shares = (total_votes / total_votes.sum() * 100).to_dict()

    # Calculate ward counts
    ward_counts = projected_winner.value_counts().to_dict()

    # Ensure all parties are represented
    for party in parties:
        if party not in ward_counts:
            ward_counts[party] = 0
        if party not in vote_shares:
            vote_shares[party] = 0

    return vote_shares, ward_counts

# Store original vote shares for recalculation
original_votes = model[parties].copy()
# Initial map and statistics
def update_map(swing_factors):



    modelled_votes = calculate_projection(swing_factors)
    projected_winner = modelled_votes[parties].idxmax(axis=1)

    # Create mapping dataframe
    model_for_map = pd.DataFrame({
        'Ward': modelled_votes['Ward'],
        'Party': projected_winner
    })

    # Merge with geographic data
    updated_map = gm_ward_map[['geometry', 'LAD24NM', 'WD24NM']].copy()
    updated_map = updated_map.merge(model_for_map, left_on="WD24NM", right_on="Ward", how="left")
    updated_map["colour"] = updated_map["Party"].map(PARTY_COLOURS).fillna("#AAAAAA")

    # Calculate statistics
    vote_shares, ward_counts = calculate_statistics(modelled_votes)
    # Update legend
    legend_patches = [
        mpatches.Patch(color=colour, label=party)
        for party, colour in PARTY_COLOURS.items()
        if party in updated_map["Party"].values
    ]


    return updated_map, vote_shares, ward_counts, legend_patches

all_wards = gpd.read_file("WD_DEC_24_UK_BGC.shp")
gm_ward_map = all_wards[all_wards["LAD24NM"].isin(greater_manchester_boroughs)].copy()

# Fix duplicate ward names across boroughs
gm_ward_map.loc[2558, 'WD24NM'] = 'Manchester Brooklands'
gm_ward_map.loc[5918, 'WD24NM'] = 'Stockport Manor'
gm_ward_map.loc[6133, 'WD24NM'] = 'Trafford Brooklands'
gm_ward_map.loc[6142, 'WD24NM'] = 'Trafford Manor'

if (gm_ward_map[gm_ward_map['WD24NM'].duplicated(keep=False)][['LAD24NM', 'WD24NM']].shape[0]) != 0:
    print('DUPLICATE FOUND')
    print(gm_ward_map[gm_ward_map['WD24NM'].duplicated(keep=False)][['LAD24NM', 'WD24NM']])

#
# # --- Create interactive plot with GridSpec layout ---
# Bar charts on the right
fig = plt.figure(figsize=(18, 10))
gs = fig.add_gridspec(2, 3, hspace=0.4, wspace=0.3, bottom=0.35)

# Map on the left (takes up 2 columns)
ax_map = fig.add_subplot(gs[:, 0:2])

ax_vote_share = fig.add_subplot(gs[0, 2])
ax_ward_count = fig.add_subplot(gs[1, 2])

def redraw_charts(vote_shares, ward_counts):
    """Clear and redraw the bar charts"""
    # Vote share chart
    ax_vote_share.clear()

    parties_ordered = ['WPB/Others','Lib Dem','Conservative','Green','Reform','Labour']
    actual_votes = [actual_2024[p]['vote_share'] for p in parties_ordered]
    projected_votes = [vote_shares.get(p, 0) for p in parties_ordered]

    y_pos = np.arange(len(parties_ordered))
    bar_height = 0.35

    # Plot actual results (lighter shade)
    ax_vote_share.barh(y_pos - bar_height / 2, actual_votes, bar_height,
                       label='2024 Actual', alpha=0.6,
                       color=[PARTY_COLOURS[p] for p in parties_ordered])

    # Plot projected results (darker shade)
    ax_vote_share.barh(y_pos + bar_height / 2, projected_votes, bar_height,
                       label='Projected', alpha=1.0,
                       color=[PARTY_COLOURS[p] for p in parties_ordered])

    # Formatting
    ax_vote_share.set_yticks(y_pos)
    ax_vote_share.set_yticklabels(parties_ordered, fontsize=7)
    ax_vote_share.set_xlabel('Vote Share (%)', fontsize=8)
    ax_vote_share.set_title('Vote Share Comparison', fontsize=8)
    ax_vote_share.set_xlim(0, 50)
    ax_vote_share.grid(axis='x', alpha=0.3)

    # Add value labels on bars
    for i, (actual, projected) in enumerate(zip(actual_votes, projected_votes)):
        ax_vote_share.text(actual + 1, i - bar_height / 2, f'{actual:.1f}%',
                           va='center', fontsize=8, alpha=0.7)
        ax_vote_share.text(projected + 1, i + bar_height / 2, f'{projected:.1f}%',
                           va='center', fontsize=8, fontweight='bold')

    # Ward count chart
    ax_ward_count.clear()

    actual_wards = [actual_2024[p]['wards'] for p in parties_ordered]
    projected_wards = [ward_counts.get(p, 0) for p in parties_ordered]

    # Plot actual results
    ax_ward_count.barh(y_pos - bar_height / 2, actual_wards, bar_height,
                       label='2024 Actual', alpha=0.6,
                       color=[PARTY_COLOURS[p] for p in parties_ordered])

    # Plot projected results
    ax_ward_count.barh(y_pos + bar_height / 2, projected_wards, bar_height,
                       label='Projected', alpha=1.0,
                       color=[PARTY_COLOURS[p] for p in parties_ordered])

    # Formatting
    ax_ward_count.set_yticks(y_pos)
    ax_ward_count.set_yticklabels(parties_ordered, fontsize=7)
    ax_ward_count.set_xlabel('Councillors', fontsize=8)
    ax_ward_count.set_title('Councillor Count Comparison', fontsize=8)
    # ax_ward_count.legend(fontsize=8, loc='lower right')
    ax_ward_count.set_xlim(0, 160)
    ax_ward_count.grid(axis='x', alpha=0.3)

    # Add value labels on bars
    for i, (actual, projected) in enumerate(zip(actual_wards, projected_wards)):
        ax_ward_count.text(actual + 2, i - bar_height / 2, f'{int(actual)}',
                           va='center', fontsize=8, alpha=0.7)
        ax_ward_count.text(projected + 2, i + bar_height / 2, f'{int(projected)}',
                           va='center', fontsize=8, fontweight='bold')

    print("redraw chart --- %s seconds ---" % (time.time() - start_time))

def redraw_map(updated_map):
    """Clear and redraw the map with new data"""
    new_colors = updated_map["colour"].values
    ward_plot.collections[0].set_facecolor(new_colors)
    # ax_map.clear()
    #
    # Plot wards

    updated_map.plot(
        ax=ax_map,
        color=updated_map["colour"],
        edgecolor="white",
        linewidth=0.5
    )

    borough_boundaries.plot(
        ax=ax_map,
        color="black",
        linewidth=2.5
    )
    ax_map.set_axis_off()
    ax_map.set_title("Greater Manchester 2026 Projected Results", fontsize=14, pad=12)

    ax_map.legend(handles=legend_patches, loc="lower right", fontsize=9)
    print("redraw map --- %s seconds ---" % (time.time() - start_time))

slider_height = 0.02
slider_y_start = 0.25
slider_spacing = 0.03

slider_range = {
    "Labour": [0.4,1.0],
    "Conservative": [0.6,1.2],
    "Green": [1.0,3.0],
    "Reform": [1.0,3.0],
    "Lib Dem": [0.8, 1.5],
    "WPB/Others": [0.8,1.5]
}
sliders = {}
for i, party in enumerate(parties):
    ax_slider = plt.axes([0.2, slider_y_start - (i * slider_spacing), 0.6, slider_height])
    slider = Slider(
        ax_slider,
        party,
        slider_range[party][0],
        slider_range[party][1],  # Range from 0.5x to 2.5x original vote share
        valinit=swing_factor[party],
        valstep=0.01,
        color=PARTY_COLOURS[party]
    )
    sliders[party] = slider

def reset(event):
    for slider in sliders.values():
        slider.reset()

ax_button = plt.axes([0.85,0.15,0.05,0.1])
button = Button(ax_button,"RESET")
button.on_clicked(reset)

def update(val):
    """Update function called when any slider changes"""
    current_swing = {party: sliders[party].val for party in parties}
    print("start redraw --- %s seconds ---" % (time.time() - start_time))

    updated_map, vote_shares, ward_counts, legend_patches = update_map(current_swing)
    redraw_map(updated_map)
    redraw_charts(vote_shares, ward_counts)
    fig.canvas.draw_idle()


# Connect sliders to update function
for slider in sliders.values():
    slider.on_changed(update)

# Initial draw
current_map, current_vote_shares, current_ward_counts, legend_patches = update_map(swing_factor)
print(type(current_map))
print("calculate model --- %s seconds ---" % (time.time() - start_time))

ward_plot = current_map.plot(
    ax=ax_map,
    color=current_map["colour"],
    edgecolor="white",
    linewidth=0.5
)
borough_boundaries = gm_ward_map.dissolve(by="LAD24NM").boundary
redraw_map(current_map)
redraw_charts(current_vote_shares, current_ward_counts)

print("interactive setup --- %s seconds ---" % (time.time() - start_time))

plt.show()