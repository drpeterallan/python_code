import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from numpy import shape, array, arange, diag, sqrt
from scipy.optimize import curve_fit
from esp.pysrc.utils.array_functions import search_array
from esp.pysrc.utils.fit_functions import sigmoid_function


def read_image_file(path_to_file):
    # Function to read image file and return in format you would get real image
    # Read in image file and convert to a numpy array
    # pixel_vals = array(plt.imread(path_to_file), dtype=float)
    pixel_vals = mpimg.imread(path_to_file)
    # pixel_vals = image[::-1, :]  # Correct for reversal of data in y axis

    # Create time, and spatial axes
    image_len_x = shape(pixel_vals)[1]
    image_len_y = shape(pixel_vals)[0]
    x_axis = array(range(image_len_x))
    y_axis = array(range(image_len_y))

    return x_axis, y_axis, pixel_vals


def contour_image_plot(x_axis, y_axis, pixel_vals):
    # Function to plot data
    plt.contourf(x_axis, y_axis, pixel_vals, 50)
    plt.xlabel("Time")
    plt.ylabel("Space")


def get_yaxis_lineout(y_axis, pixel_vals, y_lineout_position):
    # Function to get a lineout in the y axis
    # Search y_axis for user requested position
    y_index_pos = search_array(y_axis, y_lineout_position)
    return pixel_vals[y_index_pos, :]


def fit_edge_profile(x_array, y_array):

    # Find edge position
    coefs_int = [0.0, 1.0, 1.0, 1.0]  # Initial guess of parameters
    coefs, cov = curve_fit(sigmoid_function, x_array, y_array, coefs_int)
    errors = sqrt(diag(cov))

    return coefs, errors


if __name__ == "__main__":

    # Get and read in the image data
    image_location = "../data/raw/streak_test_image.png"
    time, space, data = read_image_file(image_location)
    print(time.shape, space.shape, data.shape)
    contour_image_plot(time, space, data)
    plt.show()

    # Define the positions to take lineouts
    lineout_positions = arange(0, 100, 10)

    # Create empty arrays and loop over image
    edge_times = []
    edge_times_errors = []
    for lineout_position in lineout_positions:

        # Pull a lineout from the image
        # TODO: select max and min y (event clicker) and loop over lineouts in this region
        lineout_vals = get_yaxis_lineout(space, data, lineout_position)

        # Find the edge by fitting a sigmoid
        coefs, errors = fit_edge_profile(time, lineout_vals)
        edge_times.append(coefs[2])
        edge_times_errors.append(errors[2])

        # Plot data and fit
        plt.plot(time, lineout_vals, "b-", lw=2)
        p0 = [0, 1, ]
        y_fit = sigmoid_function(time, *p0)
        plt.plot(time, y_fit, "r-", lw=1)
        plt.title(coefs[2])
        plt.show()

    # Convert to numpy array
    edge_times = array(edge_times, dtype=float)
    edge_times_errors = array(edge_times_errors, dtype=float) * 10

    # Plot the image and overlay the edge positions
    contour_image_plot(time, space, data)
    plt.errorbar(edge_times, lineout_positions, xerr=edge_times_errors, lw=0)
    plt.show()

    # Plot the edge positions
    plt.errorbar(edge_times, lineout_positions, fmt="o", xerr=edge_times_errors, lw=0)
    plt.show()

