def rq3_line_chart():
    # Re-import necessary libraries and redefine data after reset
    import matplotlib.pyplot as plt

    # Data setup
    models = ["GPT-4o", "Claude-3.5", "Gemini-1.5", "GLM-4", "Qwen2.5"]
    feedback_types = ["test", "compiler", "llm", "simple"]
    rounds = ["k=1", "k=2", "k=3"]

    # data = {
    #     "GPT-4o": {
    #         "test": [86.6, 92.1, 93.9],
    #         "compiler": [79.4, 80.0, 80.6],
    #         "llm": [73.2, 76.2, 76.2],
    #         "simple": [84.0, 85.2, 85.2]
    #     },
    #     "Claude-3.5": {
    #         "test": [82.3, 86.6, 88.4],
    #         "compiler": [83.1, 85.6, 85.6],
    #         "llm": [81.5, 82.8, 82.8],
    #         "simple": [85.9, 88.5, 89.1]
    #     },
    #     "Gemini-1.5": {
    #         "test": [81.0, 85.3, 87.1],
    #         "compiler": [79.3, 79.9, 79.9],
    #         "llm": [72.6, 77.4, 77.4],
    #         "simple": [78.7, 83.4, 83.4]
    #     },
    #     "GLM-4": {
    #         "test": [82.3, 87.8, 88.4],
    #         "compiler": [74.4, 76.8, 78.1],
    #         "llm": [64.6, 68.9, 72.0],
    #         "simple": [73.2, 76.2, 76.2]
    #     },
    #     "Qwen2.5": {
    #         "test": [82.9, 87.2, 87.2],
    #         "compiler": [78.7, 81.1, 82.3],
    #         "llm": [71.3, 72.6, 75.0],
    #         "simple": [79.9, 82.3, 82.3]
    #     }
    # }
    data = {
        "GPT-4o": {
            "test": [42.7, 45.8, 46.9],
            "compiler": [32.0, 36.1, 37.1],
            "llm": [34.7, 37.9, 39.0],
            "simple": [40.6, 41.7, 42.7]
        },
        "Claude-3.5": {
            "test": [52.1, 58.3, 58.3],
            "compiler": [37.5, 40.6, 40.6],
            "llm": [39.2, 42.3, 42.3],
            "simple": [44.2, 46.3, 47.4]
        },
        "Gemini-1.5": {
            "test": [46.4, 48.5, 48.5],
            "compiler": [34.0, 37.1, 37.1],
            "llm": [32.0, 34.0, 35.1],
            "simple": [39.2, 41.2, 41.2]
        },
        "GLM-4": {
            "test": [42.2, 45.3, 46.4],
            "compiler": [34.0, 37.1, 38.1],
            "llm": [32.0, 36.1, 37.1],
            "simple": [37.2, 38.1, 38.1]
        },
        "Qwen2.5": {
            "test": [39.2, 45.4, 46.4],
            "compiler": [32.0, 36.1, 37.1],
            "llm": [34.0, 37.1, 38.1],
            "simple": [35.1, 36.1, 37.1]
        }
    }

    # Plot setup
    plt.figure(figsize=(9, 6))

    # Define colors for models and markers for feedback types
    model_colors = ['b', 'g', 'r', 'orange', 'purple']
    feedback_markers = ['o', 's', '^', 'D']

    # Plot each model with its own color and each feedback type with a unique marker
    for i, model in enumerate(models):
        for j, feedback in enumerate(feedback_types):
            plt.plot(
                rounds,
                data[model][feedback],
                label=f"{model} - {feedback}",
                color=model_colors[i],
                marker=feedback_markers[j],
                linestyle='-',
                linewidth=1
            )

    # Customize plot appearance
    # plt.title("Model Performance Over Multiple Repair Rounds", fontsize=14)
    # plt.xlabel("Repair Round", fontsize=12)
    plt.ylabel("Repair@k (%)", fontsize=12)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig('rq3-line-chart-coder_eval.pdf', dpi=600, bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    # draw_rq4_bar_chart()
    rq3_line_chart()