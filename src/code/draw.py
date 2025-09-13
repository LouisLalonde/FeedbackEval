def rq3_line_chart_upper_left_legend():
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    # 数据部分与之前相同，保持不变
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
            "Test": [86.6, 92.1, 93.9],
            "Compiler": [79.4, 80.0, 80.6],
            "LLM-Skilled": [73.2, 76.2, 76.2],
            "LLM-Expert": [90.1, 95.1, 95.7],
            "Minimal": [84.0, 85.2, 85.2],
            "Mixed": [90.2, 95.1, 95.7],
        },
        "Claude-3.5": {
            "Test": [82.3, 86.6, 88.4],
            "Compiler": [83.1, 85.6, 85.6],
            "LLM-Skilled": [81.5, 82.8, 82.8],
            "LLM-Expert": [89.6, 92.1, 93.3],
            "Minimal": [85.9, 88.5, 89.1],
            "Mixed": [91.5, 95.7, 95.7],
        },
        "Deepseek-R1": {
            "Test": [95.5, 98.1, 98.1],
            "Compiler": [86.6, 88.7, 89.4],
            "LLM-Skilled": [84.6, 86.6, 86.6],
            "LLM-Expert": [96.8, 97.4, 99.4],
            "Minimal": [91.6, 92.3, 93.0],
            "Mixed": [98.7, 99.3, 100.0],
        },
        "GLM-4": {
            "Test": [82.3, 87.8, 88.1],
            "Compiler": [74.4, 76.8, 78.1],
            "LLM-Skilled": [64.6, 68.9, 72.0],
            "LLM-Expert": [85.4, 92.7, 93.9],
            "Minimal": [73.2, 76.2, 76.2],
            "Mixed": [87.7, 92.7, 95.1],
        },
        "Qwen2.5": {
            "Test": [82.9, 87.2, 87.2],
            "Compiler": [78.7, 81.1, 82.3],
            "LLM-Skilled": [71.3, 72.6, 75.0],
            "LLM-Expert": [87.8, 92.7, 94.5],
            "Minimal": [79.9, 82.3, 82.3],
            "Mixed": [89.6, 93.3, 94.5],
        },
    }

    # Plot setup
    fig, ax = plt.subplots(figsize=(7, 6))  # 减小图形高度

    # 定义颜色和标记
    model_colors = ["b", "g", "r", "orange", "purple"]
    feedback_markers = ["o", "s", "^", "D", "P", "X"]

    # 绘制所有数据线
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

    # 自定义图表外观
    ax.set_ylabel("Repair@k (%)", fontsize=12)
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.set_ylim(60, 100)  # 设置y轴范围以更好地展示数据

    # --- 创建并放置自定义图例在图表下方，每行一个图例 ---
    # 1. 为 "Model" (颜色) 创建图例
    model_handles = [Line2D([0], [0], color=c, lw=2) for c in model_colors]
    legend1 = ax.legend(
        model_handles,
        models,
        title="Model",
        loc="upper center",
        bbox_to_anchor=(0.5, -0.05),  # 靠近图表的第一行
        ncol=len(models),  # 所有模型放在一行
        frameon=True,
        facecolor="white",
        framealpha=0.8,
        columnspacing=1,  # 减少列间距
        handletextpad=0.5,  # 减少图例标记和文本间距
    )

    # 2. 为 "Feedback" (标记) 创建图例
    feedback_handles = [
        Line2D([0], [0], marker=m, color="gray", linestyle="None", markersize=6)
        for m in feedback_markers
    ]
    legend2 = ax.legend(
        feedback_handles,
        feedback_types,
        title="Feedback",
        loc="upper center",
        bbox_to_anchor=(0.5, -0.15),  # 靠近图表的第二行
        ncol=len(feedback_types),  # 所有反馈类型放在一行
        frameon=True,
        facecolor="white",
        framealpha=0.8,
        columnspacing=1,  # 减少列间距
        handletextpad=0.5,  # 减少图例标记和文本间距
        handlelength=1.5,  # 减少图例线长度
    )

    # 手动将第一个图例(legend1)重新添加回图表中
    ax.add_artist(legend1)

    # 调整整体布局，为底部图例留出空间
    fig.tight_layout()
    plt.subplots_adjust(bottom=0.2)  # 减少底部边距

    plt.savefig(
        "rq3-line-chart-human_eval.pdf", dpi=600, bbox_inches="tight"
    )
    plt.show()


# 运行函数
rq3_line_chart_upper_left_legend()
