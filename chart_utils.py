import matplotlib.pyplot as plt 
import pandas as pd
from config import PIE_COLORS, BAR_COLOR, OTHERS_LABEL
from helpers import wrap_labels

# This function makes a pie chart and saves it as a picture
def save_pie_jpg(values_pct: pd.Series, outfile: str):
   
    # If there's nothing to draw, we just leave
    if len(values_pct) == 0:
        return

    # Turn percentages into slices of pie
    fracs = (values_pct / 100.0).values

    # Wrap labels so they don't overflow
    #raw_labels = [f"{idx} ({val:.1f}%)"]    

    # Make labels like "Apple (25.0%)"
    # Using warp_labels to ensure they don't overflow outside the chart area
    raw_labels = [f"{idx} ({val:.1f}%)" for idx, val in values_pct.items()]
    labels = wrap_labels(raw_labels, wrap_width=30, max_chars=60)
    #labels = [f"{idx} ({val:.1f}%)" for idx, val in values_pct.items()]

    # Pick colors for each slice
    colors = PIE_COLORS[:len(values_pct)]

    # Make a square canvas to draw on
    fig, ax = plt.subplots(figsize=(9, 9))

    # Draw the pie with labels and colors
    ax.pie(
        fracs,
        labels=labels,
        startangle=90,  # Start from the top
        colors=colors,
        textprops={'fontsize': 10},
        wedgeprops={'linewidth': 1, 'edgecolor': 'white'}  # Make slices look clean
    )

    # Make sure the pie is round and centered
    ax.axis('equal')

    # Adjust the space around the pie so it fits nicely
    plt.subplots_adjust(left=0.20, right=0.80, top=0.80, bottom=0.20)

    # Save the pie chart as a JPG picture
    plt.savefig(outfile, format="jpg", dpi=200)

    # Clean up so we’re ready for the next drawing
    plt.close()

# This function makes a horizontal bar chart and saves it as a picture
def save_bar_jpg(values_pct: pd.Series, outfile: str):
    
    # If there's nothing to draw, we just leave
    if len(values_pct) == 0:
        return

    # If there's a slice called "Outros", we move it to the end
    if OTHERS_LABEL in values_pct.index:
        outros_val = values_pct[OTHERS_LABEL]
        values_pct = pd.concat([values_pct.drop(OTHERS_LABEL), pd.Series({OTHERS_LABEL: outros_val})])

    # Flip the order so the first item is at the bottom
    values_pct = values_pct[::-1]

    # Get the names and values to draw
    labels = list(values_pct.index)
    vals = list(values_pct.values)

    # Make a wide canvas to draw on
    plt.figure(figsize=(12, 8))
    ax = plt.gca()

    # Draw horizontal bars
    bars = ax.barh(range(len(vals)), vals, color=BAR_COLOR)

    # Put labels on the side
    ax.set_yticks(range(len(vals)))
    ax.set_yticklabels(wrap_labels(labels), fontsize=10)

    # Label the x-axis so people know it's percentages
    ax.set_xlabel("Porcentagem (%)")

    # Hide the borders we don’t need
    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)

    # Write the percentage at the end of each bar
    for rect, v in zip(bars, vals):
        ax.text(rect.get_width() + 0.5, rect.get_y() + rect.get_height()/2, f"{v:.1f}%", va="center", fontsize=9)

    # Adjust the space so labels fit nicely
    plt.subplots_adjust(left=0.35, right=0.95, top=0.95, bottom=0.1)

    # Save the bar chart as a JPG picture
    plt.savefig(outfile, format="jpg", dpi=200)

    # Clean up so we’re ready for the next drawing
    plt.close()