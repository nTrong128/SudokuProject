import matplotlib.pyplot as plt


def draw_graph_scores(best_data, worst_data):
    # Create a new figure of size 8x6 points, using 100 dots per inch
    # plt.figure(figsize=(8, 6), dpi=80)
    plt.plot(best_data, label="Best solution score", color="blue", linewidth=1.0, linestyle="-")
    plt.plot(worst_data, label="Worst solution score", color="red", linewidth=1.0, linestyle="-")
    plt.ylabel('Evaluation value')
    plt.xlabel('Number of generations')
    plt.ylim(0, worst_data[0])
    plt.xlim(0, len(best_data))
    plt.legend()
    plt.show()
