def draw_separate_bar_charts():
    import matplotlib.pyplot as plt
    import numpy as np

    # --- 左侧子图数据 (原始数据：各模型在两个数据集上的表现) ---
    models = ["Deepseek-R1", "Claude-3.5", "GPT-4o", "Qwen2.5", "GLM-4"]
    human_eval_models = [86.2, 84.6, 83.4, 82.2, 79.2]
    coder_eval_models = [44.8, 40.0, 35.7, 34.0, 31.7]

    # --- 右侧子图数据 (各反馈在两个数据集上的平均得分) ---
    # 这些数据是根据您在第一个问题中提供的表格计算得出的
    feedbacks = ["Mixed", "LLM-Expert", "Test", "Compiler", "Minimal", "LLM-Skilled"]
    human_eval_feedbacks = [90.7, 89.0, 85.9, 81.4, 79.6, 72.1]
    coder_eval_feedbacks = [43.7, 41.1, 40.4, 31.2, 36.1, 30.9]

    width = 0.35  # 柱状宽度

    # --- 绘制第一张图 (各模型表现) ---
    fig1, ax1 = plt.subplots(figsize=(7, 5))
    x_models = np.arange(len(models))

    bars1_left = ax1.bar(
        x_models - width / 2,
        human_eval_models,
        width,
        label="HumanEval",
        color="#1f77b4",
    )
    bars2_left = ax1.bar(
        x_models + width / 2,
        coder_eval_models,
        width,
        label="CoderEval",
        color="#ff7f0e",
    )

    ax1.set_ylabel("Repair@1 (%)")
    ax1.set_xticks(x_models)
    ax1.set_xticklabels(models)

    ax1.yaxis.grid(True, linestyle="--", alpha=0.7)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)

    for bars in [bars1_left, bars2_left]:
        for bar in bars:
            height = bar.get_height()
            ax1.text(
                bar.get_x() + bar.get_width() / 2,
                height + 1,
                f"{height:.1f}",
                ha="center",
                fontsize=10,
            )
    ax1.set_ylim(0, 100)  # 统一y轴范围
    ax1.legend(
        loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=2, frameon=False
    )  # 调整图例位置，使其更靠近图表

    plt.tight_layout()
    plt.savefig("models_bar_chart.pdf", bbox_inches="tight", format="pdf", dpi=300)
    plt.show()

    # --- 绘制第二张图 (各反馈平均分) ---
    fig2, ax2 = plt.subplots(figsize=(7, 5))
    x_feedbacks = np.arange(len(feedbacks))

    bars1_right = ax2.bar(
        x_feedbacks - width / 2,
        human_eval_feedbacks,
        width,
        label="HumanEval",
        color="#1f77b4",
    )
    bars2_right = ax2.bar(
        x_feedbacks + width / 2,
        coder_eval_feedbacks,
        width,
        label="CoderEval",
        color="#ff7f0e",
    )

    ax2.set_ylabel("Repair@1 (%)")
    ax2.set_xticks(x_feedbacks)
    ax2.set_xticklabels(feedbacks)

    ax2.yaxis.grid(True, linestyle="--", alpha=0.7)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)

    for bars in [bars1_right, bars2_right]:
        for bar in bars:
            height = bar.get_height()
            ax2.text(
                bar.get_x() + bar.get_width() / 2,
                height + 1,
                f"{height:.1f}",
                ha="center",
                fontsize=10,
            )
    ax2.set_ylim(0, 100)  # 统一y轴范围
    ax2.legend(
        loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=2, frameon=False
    )  # 调整图例位置，使其更靠近图表

    plt.tight_layout()
    plt.savefig("rq1_feedback.pdf", bbox_inches="tight", format="pdf", dpi=300)
    plt.show()


def rq3_line_chart():
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    # Data for the CoderEval metric from the provided table
    models = ["GPT-4o", "Claude-3.5", "Deepseek-R1", "GLM-4", "Qwen2.5"]
    feedback_types = [
        "Compiler",
        "Test",
        "Minimal",
        "LLM-Skilled",
        "LLM-Expert",
        "Mixed",
    ]
    rounds = ["k=1", "k=2", "k=3"]

    data = {
        "GPT-4o": {
            "Test": [40.0, 42.7, 45.0],
            "Compiler": [30.3, 34.8, 35.6],
            "LLM-Skilled": [28.8, 31.1, 32.4],
            "LLM-Expert": [38.9, 48.9, 51.6],
            "Minimal": [35.5, 37.3, 39.1],
            "Mixed": [41.6, 50.7, 52.5],
        },
        "Claude-3.5": {
            "Test": [44.6, 52.3, 53.2],
            "Compiler": [33.8, 37.9, 37.9],
            "LLM-Skilled": [34.8, 36.2, 37.1],
            "LLM-Expert": [42.5, 50.2, 52.0],
            "Minimal": [38.1, 41.3, 42.7],
            "Mixed": [47.1, 53.4, 57.5],
        },
        "Deepseek-R1": {
            "Test": [50.3, 58.7, 59.8],
            "Compiler": [41.3, 42.4, 43.9],
            "LLM-Skilled": [37.8, 40.0, 40.5],
            "LLM-Expert": [48.7, 55.6, 57.7],
            "Minimal": [42.8, 48.9, 50.6],
            "Mixed": [55.9, 66.0, 67.0],
        },
        "GLM-4": {
            "Test": [35.8, 39.4, 40.3],
            "Compiler": [28.1, 30.8, 30.8],
            "LLM-Skilled": [27.2, 29.9, 30.3],
            "LLM-Expert": [35.8, 44.3, 47.5],
            "Minimal": [31.5, 33.8, 34.7],
            "Mixed": [37.7, 46.8, 50.5],
        },
        "Qwen2.5": {
            "Test": [36.4, 41.8, 47.3],
            "Compiler": [30.0, 32.7, 32.7],
            "LLM-Skilled": [29.1, 30.5, 32.3],
            "LLM-Expert": [39.1, 41.8, 47.3],
            "Minimal": [32.6, 34.4, 34.8],
            "Mixed": [39.6, 43.4, 48.0],
        },
    }

    # Plot setup
    fig, ax = plt.subplots(figsize=(7, 6))

    # Define colors and markers
    model_colors = ["b", "g", "r", "orange", "purple"]
    feedback_markers = ["o", "s", "^", "D", "P", "X"]

    # Plot all data lines
    for i, model in enumerate(models):
        for j, feedback in enumerate(feedback_types):
            ax.plot(
                rounds,
                data[model][feedback],
                color=model_colors[i],
                marker=feedback_markers[j],
                linestyle="-",
                linewidth=1,
            )

    # Custom chart appearance
    ax.set_ylabel("Repair@k (%)", fontsize=12)
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.set_ylim(25, 70)  # Adjust y-axis range to better display CoderEval data

    # --- Create and place custom legends below the chart ---
    # 1. Create legend for "Model" (colors)
    model_handles = [Line2D([0], [0], color=c, lw=2) for c in model_colors]
    legend1 = ax.legend(
        model_handles,
        models,
        title="Model",
        loc="upper center",
        bbox_to_anchor=(0.5, -0.05),
        ncol=len(models),
        frameon=True,
        facecolor="white",
        framealpha=0.8,
        columnspacing=1,
        handletextpad=0.5,
    )

    # 2. Create legend for "Feedback" (markers)
    feedback_handles = [
        Line2D([0], [0], marker=m, color="gray", linestyle="None", markersize=6)
        for m in feedback_markers
    ]
    legend2 = ax.legend(
        feedback_handles,
        feedback_types,
        title="Feedback",
        loc="upper center",
        bbox_to_anchor=(0.5, -0.15),
        ncol=len(feedback_types),
        frameon=True,
        facecolor="white",
        framealpha=0.8,
        columnspacing=1,
        handletextpad=0.5,
        handlelength=1.5,
    )

    # Manually add the first legend back to the chart
    ax.add_artist(legend1)

    # Adjust overall layout to make room for the legends at the bottom
    fig.tight_layout()
    plt.subplots_adjust(bottom=0.2)

    plt.savefig("rq3-line-chart-coder_eval.pdf", dpi=600, bbox_inches="tight")
    plt.show()


import matplotlib.pyplot as plt
import numpy as np


def create_repair_results_chart():
    # Data from the table
    models = ["GPT-4o", "Claude-3.5", "Deepseek-R1", "GLM-4", "Qwen2.5"]
    feedback_types = ["Test", "Compiler", "LLM", "LLM_GT", "Simple", "Mixed"]
    rounds = ["k=1", "k=2", "k=3"]

    # HumanEval data
    humaneval_data = {
        "GPT-4o": {
            "Test": [86.6, 92.1, 93.9],
            "Compiler": [79.4, 80.0, 80.6],
            "LLM": [73.2, 76.2, 76.2],
            "LLM_GT": [90.1, 95.1, 95.7],
            "Simple": [84.0, 85.2, 85.2],
            "Mixed": [90.2, 95.1, 95.7],
        },
        "Claude-3.5": {
            "Test": [82.3, 86.6, 88.4],
            "Compiler": [83.1, 85.6, 85.6],
            "LLM": [81.5, 82.8, 82.8],
            "LLM_GT": [89.6, 92.1, 93.3],
            "Simple": [85.9, 88.5, 89.1],
            "Mixed": [91.5, 95.7, 95.7],
        },
        "Deepseek-R1": {
            "Test": [95.5, 98.1, 98.1],
            "Compiler": [86.6, 88.7, 89.4],
            "LLM": [84.6, 86.6, 86.6],
            "LLM_GT": [96.8, 97.4, 99.4],
            "Simple": [91.6, 92.3, 93.0],
            "Mixed": [98.7, 99.3, 100.0],
        },
        "GLM-4": {
            "Test": [82.3, 87.8, 88.1],
            "Compiler": [74.4, 76.8, 78.1],
            "LLM": [64.6, 68.9, 72.0],
            "LLM_GT": [85.4, 92.7, 93.9],
            "Simple": [73.2, 76.2, 76.2],
            "Mixed": [87.8, 92.7, 95.1],
        },
        "Qwen2.5": {
            "Test": [82.9, 87.2, 87.2],
            "Compiler": [78.7, 81.1, 82.3],
            "LLM": [71.3, 72.6, 75.0],
            "LLM_GT": [87.8, 92.7, 94.5],
            "Simple": [79.9, 82.3, 82.3],
            "Mixed": [89.6, 93.3, 94.5],
        },
    }

    # CoderEval data
    codereval_data = {
        "GPT-4o": {
            "Test": [40.0, 42.7, 45.0],
            "Compiler": [30.3, 34.8, 35.6],
            "LLM": [28.8, 31.1, 32.4],
            "LLM_GT": [38.9, 48.9, 51.6],
            "Simple": [35.5, 37.3, 39.1],
            "Mixed": [41.6, 50.7, 52.5],
        },
        "Claude-3.5": {
            "Test": [44.6, 52.3, 53.2],
            "Compiler": [33.8, 37.9, 37.9],
            "LLM": [34.8, 36.2, 37.1],
            "LLM_GT": [42.5, 50.2, 52.0],
            "Simple": [38.1, 41.3, 42.7],
            "Mixed": [47.1, 53.4, 57.5],
        },
        "Deepseek-R1": {
            "Test": [50.3, 58.7, 59.8],
            "Compiler": [41.3, 42.4, 43.9],
            "LLM": [37.8, 40.0, 40.5],
            "LLM_GT": [48.7, 55.6, 57.7],
            "Simple": [42.8, 48.9, 50.6],
            "Mixed": [55.9, 66.0, 67.0],
        },
        "GLM-4": {
            "Test": [35.8, 39.4, 40.3],
            "Compiler": [28.1, 30.8, 30.8],
            "LLM": [27.2, 29.9, 30.3],
            "LLM_GT": [35.8, 44.3, 47.5],
            "Simple": [31.5, 33.8, 34.7],
            "Mixed": [37.7, 46.8, 50.5],
        },
        "Qwen2.5": {
            "Test": [36.4, 41.8, 47.3],
            "Compiler": [30.0, 32.7, 32.7],
            "LLM": [29.1, 30.5, 32.3],
            "LLM_GT": [39.1, 41.8, 47.3],
            "Simple": [32.6, 34.4, 34.8],
            "Mixed": [38.0, 43.4, 48.0],
        },
    }

    # Define colors for models and markers for feedback types
    model_colors = {
        "GPT-4o": "#3498db",
        "Claude-3.5": "#2ecc71",
        "Deepseek-R1": "#e74c3c",
        "GLM-4": "#f39c12",
        "Qwen2.5": "#9b59b6",
    }

    feedback_markers = {
        "Test": "o",
        "Compiler": "s",
        "LLM": "^",
        "LLM_GT": "D",
        "Simple": "*",
        "Mixed": "+",
    }

    # Create subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    # Plot HumanEval
    for model in models:
        for feedback in feedback_types:
            ax1.plot(
                rounds,
                humaneval_data[model][feedback],
                color=model_colors[model],
                marker=feedback_markers[feedback],
                markersize=6,
                linewidth=2,
                label=f"{model}-{feedback}",
            )

    ax1.set_title("HumanEval", fontsize=16, fontweight="bold")
    ax1.set_xlabel("Repair Round", fontsize=12)
    ax1.set_ylabel("Repair@k (%)", fontsize=12)
    ax1.grid(True, linestyle="--", alpha=0.6)
    ax1.set_ylim(60, 102)

    # Plot CoderEval
    for model in models:
        for feedback in feedback_types:
            ax2.plot(
                rounds,
                codereval_data[model][feedback],
                color=model_colors[model],
                marker=feedback_markers[feedback],
                markersize=6,
                linewidth=2,
                label=f"{model}-{feedback}",
            )

    ax2.set_title("CoderEval", fontsize=16, fontweight="bold")
    ax2.set_xlabel("Repair Round", fontsize=12)
    ax2.set_ylabel("Repair@k (%)", fontsize=12)
    ax2.grid(True, linestyle="--", alpha=0.6)
    ax2.set_ylim(25, 70)

    # Create custom legend
    # Model legend (colors)
    model_handles = []
    for model in models:
        model_handles.append(
            plt.Line2D([0], [0], color=model_colors[model], linewidth=3, label=model)
        )

    # Feedback legend (markers)
    feedback_handles = []
    for feedback in feedback_types:
        feedback_handles.append(
            plt.Line2D(
                [0],
                [0],
                color="black",
                marker=feedback_markers[feedback],
                markersize=8,
                linewidth=0,
                label=feedback,
            )
        )

    # Add legends
    model_legend = fig.legend(
        handles=model_handles,
        title="Models",
        loc="upper center",
        bbox_to_anchor=(0.3, 0.02),
        ncol=5,
        fontsize=10,
    )
    feedback_legend = fig.legend(
        handles=feedback_handles,
        title="Feedback Types",
        loc="upper center",
        bbox_to_anchor=(0.7, 0.02),
        ncol=6,
        fontsize=10,
    )

    # Style the legend titles
    model_legend.get_title().set_fontweight("bold")
    feedback_legend.get_title().set_fontweight("bold")

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.15)

    # Save the figure
    plt.savefig("multi_round_repair_results.pdf", dpi=600, bbox_inches="tight")
    plt.savefig("multi_round_repair_results.png", dpi=300, bbox_inches="tight")
    plt.show()


def rq4_ablate_chart():
    # 数据
    categories = [
        "baseline",
        "guideline",
        "context",
        "docstring",
        "role-play",
    ]
    values = [
        49.5,
        48.5,
        48.5,
        47.4,
        47.4
    ]

    # 设置论文风格
    plt.style.use("seaborn-v0_8-paper")

    # 画布大小
    fig, ax = plt.subplots(figsize=(6, 4))

    # 绘制柱状图
    bars = ax.bar(
        categories,
        values,
        color="#1f77b4",
        edgecolor="black",
        width=0.5,
        alpha=0.8,
        label="Repair@1 (%)",
    )

    # 添加数值标签
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 1,
            f"{height:.1f}",
            ha="center",
            fontsize=10,
        )

    # 轴标签
    ax.set_ylabel("Repair@1 (%)", fontsize=12, fontname="Times New Roman", labelpad=10)
    ax.set_ylim(0, 60)  # 调整 Y 轴范围以适应数值标签

    # X 轴标签旋转避免重叠
    plt.xticks(fontsize=10)

    # 添加横向网格线
    ax.yaxis.grid(True, linestyle="--", alpha=0.7)

    # 去除顶部和右侧边框
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # 调整布局
    plt.tight_layout()

    # 保存高质量矢量图
    plt.savefig("abalation_score.pdf", format="pdf", dpi=300, bbox_inches="tight")

    plt.show()


def rq4_enhance_chart():
    # 数据
    # 数据按从高到低排序
    categories = [
        "RR",
        "COT",
        "ES-Shot",
        "few-shot",
        "baseline",
        "SBP",
        "SA",
        "SG_ICL",
    ]
    values = [52.6, 52.6, 51.6, 50.5, 49.5, 48.5, 48.5, 46.4]

    # 设置论文风格
    plt.style.use("seaborn-v0_8-paper")

    # 画布大小
    fig, ax = plt.subplots(figsize=(6, 4))

    # 绘制柱状图
    bars = ax.bar(
        categories,
        values,
        color="#1f77b4",
        edgecolor="black",
        width=0.5,
        alpha=0.8,
        label="Repair@1 (%)",
    )

    # 添加数值标签
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 1,
            f"{height:.1f}",
            ha="center",
            fontsize=10,
        )

    # 轴标签
    ax.set_ylabel("Repair@1 (%)", fontsize=12, fontname="Times New Roman", labelpad=10)
    ax.set_ylim(0, 60)  # 调整 Y 轴范围以适应数值标签

    # X 轴标签旋转避免重叠
    plt.xticks(rotation=20, fontsize=10)

    # 添加横向网格线
    ax.yaxis.grid(True, linestyle="--", alpha=0.7)

    # 去除顶部和右侧边框
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # 调整布局
    plt.tight_layout()

    # 保存高质量矢量图
    plt.savefig("enhancement_score.pdf", format="pdf", dpi=300, bbox_inches="tight")

    plt.show()


# Run the function
if __name__ == "__main__":
    rq4_enhance_chart()
