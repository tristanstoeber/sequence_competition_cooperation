import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

def get_diverging_colormap(
    vmin=0,
    vmax=3,
    center=1,
    boundary_low=0.95,
    boundary_high=1.05,
    color_center=[1, 1, 0.5, 1]):
    """
    Generate a custom colormap centered around a specified value with a distinct color for a given range.
    
    Parameters:
    - vmin (float): Minimum value of the colormap.
    - vmax (float): Maximum value of the colormap.
    - center (float): Center value of the colormap where the distinct color range starts.
    - boundary_low (float): Lower boundary of the distinct color range.
    - boundary_high (float): Upper boundary of the distinct color range.
    - color_center (list[float, float, float, float]): RGBA values of the distinct color in the center range. Each component should be between 0 and 1.
    
    Returns:
    - newcmp (ListedColormap): A custom colormap object that can be used with matplotlib plotting functions.
    
    Example:
    ```
    custom_cmap = get_custom_colormap(vmin=0, vmax=5, center=2.5, boundary_low=2.45, boundary_high=2.55, color_center=[0.8, 0.8, 0.8, 1])
    plt.pcolormesh(data, cmap=custom_cmap)
    ```
    """
    
    # Calculate the ratio of segments for our custom colormap
    ratio_low = (boundary_low - vmin) / (vmax - vmin)
    ratio_center = (boundary_high - boundary_low) / (vmax - vmin)
    ratio_high = (vmax - boundary_high) / (vmax - vmin)

    # Extract colors from the PRGn colormap for the lower and higher segments
    colors_low = plt.cm.PRGn(np.linspace(0, 0.5, int(256 * ratio_low)))
    colors_high = plt.cm.PRGn(np.linspace(0.5, 1, int(256 * ratio_high)))

    # Create the central segment with the defined color
    colors_center = [color_center for _ in range(int(256 * ratio_center))]

    # Stack all segments to create a new colormap
    newcolors = np.vstack([colors_low, colors_center, colors_high])
    newcmp = ListedColormap(newcolors)

    return newcmp

def get_onesided_colormap(
    vmin=0,
    vmax=1,
    center=1,
    boundary_low=0.95,
    boundary_high=1.05,
    color_center=[1, 1, 0.5, 1]):
    """
    Generate a custom colormap centered around a specified value with a distinct color for a given range.
    
    Parameters:
    - vmin (float): Minimum value of the colormap.
    - vmax (float): Maximum value of the colormap.
    - center (float): Center value of the colormap where the distinct color range starts.
    - boundary_low (float): Lower boundary of the distinct color range.
    - boundary_high (float): Upper boundary of the distinct color range.
    - color_center (list[float, float, float, float]): RGBA values of the distinct color in the center range. Each component should be between 0 and 1.
    
    Returns:
    - newcmp (ListedColormap): A custom colormap object that can be used with matplotlib plotting functions.
    
    Example:
    ```
    custom_cmap = get_custom_colormap(vmin=0, vmax=5, center=2.5, boundary_low=2.45, boundary_high=2.55, color_center=[0.8, 0.8, 0.8, 1])
    plt.pcolormesh(data, cmap=custom_cmap)
    ```
    """
    
    # Calculate the ratio of segments for our custom colormap
    ratio_low = (boundary_low - vmin) / (vmax - vmin)
    ratio_center = (boundary_high - boundary_low) / (vmax - vmin)

    # Extract colors from the PRGn colormap for the lower and higher segments
    colors_low = plt.cm.PRGn(np.linspace(0, 0.5, int(256 * ratio_low)))

    # Create the central segment with the defined color
    colors_center = [color_center for _ in range(int(256 * ratio_center))]

    # Stack all segments to create a new colormap
    newcolors = np.vstack([colors_low, colors_center])
    newcmp = ListedColormap(newcolors)

    return newcmp
