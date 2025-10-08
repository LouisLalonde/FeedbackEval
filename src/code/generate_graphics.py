import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

CODER_EVAL_DIR = 'FeedbackEval/results/GPT/CoderEval/single/'
HUMAN_EVAL_DIR = 'FeedbackEval/results/GPT/HumanEval/single/'


# --- Charger les fichiers ---
with open(HUMAN_EVAL_DIR + "scores.json") as f:
    human_data = json.load(f)

with open(CODER_EVAL_DIR + "scores.json") as f:
    coder_data = json.load(f)

# --- Préparer les données ---
def parse_results(data, dataset_name):
    formatted = []
    for key, value in data.items():
        feedback_type = key.split("_")[-2]
        formatted.append({
            "Dataset": dataset_name,
            "Feedback": feedback_type.replace("skilled", "Human").replace('minimal', 'simple'),
            "Score": float(value)
        })
    return pd.DataFrame(formatted)

human_df = parse_results(human_data, "HumanEval")
coder_df = parse_results(coder_data, "CoderEval")

# Fusion pour calculs globaux
df = pd.concat([human_df, coder_df])

# =======================================================
# TABLEAU RQ1 — Moyenne GPT-4o par feedback
# =======================================================
rq1_df = df.groupby("Feedback")["Score"].mean().round(2).reset_index()
rq1_df.loc[len(rq1_df)] = ["Average", rq1_df["Score"].mean().round(2)]

fig, ax = plt.subplots(figsize=(3.5, 1.5 + 0.35 * len(rq1_df)))
ax.axis("off")
table = ax.table(cellText=rq1_df.values,
                 colLabels=["Feedback", "GPT-4o"],
                 loc="center",
                 cellLoc="center",
                 colColours=["#f2f2f2", "#f2f2f2"])
table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1.2, 1.2)
plt.title("Table 3: Average Repair@1 on FeedbackEval for GPT-4o", fontsize=13, weight="bold", pad=10)
plt.tight_layout()
plt.savefig("Tableau_RQ1.png", dpi=300, bbox_inches="tight")
plt.close()

# =======================================================
# TABLEAU RQ2 — Scores GPT-4o par dataset et feedback
# =======================================================
pivot_df = df.pivot(index="Feedback", columns="Dataset", values="Score").round(2)
pivot_df.loc["Average"] = pivot_df.mean().round(2)
pivot_df = pivot_df.reset_index()

# Créer la figure
fig, ax = plt.subplots(figsize=(5.5, 2 + 0.4 * len(pivot_df)))
ax.axis("off")

# --- Dessiner la "table" manuellement pour ajouter un double en-tête ---
# Largeur des colonnes (Feedback | HumanEval | CoderEval)
col_widths = [0.3, 0.35, 0.35]
row_height = 0.4
n_rows = len(pivot_df) + 2  # +2 pour les 2 lignes d'en-tête

# Position de départ (coordonnées normalisées)
x0, y0 = 0, 0

# Dessiner le fond blanc
ax.add_patch(Rectangle((x0, y0), sum(col_widths), n_rows * row_height, color="white"))

# --- Première ligne d'en-tête ---
ax.text(x0 + col_widths[0] / 2, y0 + (n_rows - 1) * row_height + 0.15, "Feedback",
        ha="center", va="center", fontsize=11, fontweight="bold")

# Cellule fusionnée pour GPT-4o
ax.add_patch(Rectangle((x0 + col_widths[0], y0 + (n_rows - 1) * row_height),
                       col_widths[1] + col_widths[2], row_height,
                       facecolor="#f2f2f2", edgecolor="black"))
ax.text(x0 + col_widths[0] + (col_widths[1] + col_widths[2]) / 2,
        y0 + (n_rows - 1) * row_height + 0.15,
        "GPT-4o", ha="center", va="center", fontsize=11, fontweight="bold")

# --- Deuxième ligne d'en-tête ---
ax.add_patch(Rectangle((x0, y0 + (n_rows - 2) * row_height), col_widths[0], row_height,
                       facecolor="#f2f2f2", edgecolor="black"))
ax.add_patch(Rectangle((x0 + col_widths[0], y0 + (n_rows - 2) * row_height), col_widths[1], row_height,
                       facecolor="#f2f2f2", edgecolor="black"))
ax.add_patch(Rectangle((x0 + col_widths[0] + col_widths[1], y0 + (n_rows - 2) * row_height), col_widths[2], row_height,
                       facecolor="#f2f2f2", edgecolor="black"))

ax.text(x0 + col_widths[0] / 2, y0 + (n_rows - 2) * row_height + 0.15, "", ha="center", va="center", fontsize=10)
ax.text(x0 + col_widths[0] + col_widths[1] / 2, y0 + (n_rows - 2) * row_height + 0.15, "HumanEval", ha="center", va="center", fontsize=10)
ax.text(x0 + col_widths[0] + col_widths[1] + col_widths[2] / 2, y0 + (n_rows - 2) * row_height + 0.15, "CoderEval", ha="center", va="center", fontsize=10)

# --- Remplir les lignes de données ---
for i, row in pivot_df.iterrows():
    y = y0 + (n_rows - 3 - i) * row_height
    # Feedback
    ax.add_patch(Rectangle((x0, y), col_widths[0], row_height, edgecolor="black", facecolor="white"))
    ax.text(x0 + col_widths[0] / 2, y + row_height / 2, row["Feedback"], ha="center", va="center", fontsize=10)
    # HumanEval
    ax.add_patch(Rectangle((x0 + col_widths[0], y), col_widths[1], row_height, edgecolor="black", facecolor="white"))
    ax.text(x0 + col_widths[0] + col_widths[1] / 2, y + row_height / 2, f"{row['HumanEval']:.2f}", ha="center", va="center", fontsize=10)
    # CoderEval
    ax.add_patch(Rectangle((x0 + col_widths[0] + col_widths[1], y), col_widths[2], row_height, edgecolor="black", facecolor="white"))
    ax.text(x0 + col_widths[0] + col_widths[1] + col_widths[2] / 2, y + row_height / 2, f"{row['CoderEval']:.2f}", ha="center", va="center", fontsize=10)

plt.xlim(0, sum(col_widths))
plt.ylim(0, n_rows * row_height)
plt.axis("off")
plt.title("Table 4: Repair@1 Results of GPT-4o on Code Repair Tasks with Various Feedback", fontsize=13, weight="bold", pad=10)
plt.tight_layout()
plt.savefig("Tableau_RQ2_Feedback.png", dpi=300, bbox_inches="tight")
plt.close()

# =======================================================
# GRAPHIQUE — Comparaison HumanEval vs CoderEval avec valeurs
# =======================================================
mean_human = human_df["Score"].mean().round(2)
mean_coder = coder_df["Score"].mean().round(2)

labels = ["GPT-4o"]
x = range(len(labels))
bar_width = 0.35

plt.figure(figsize=(5, 4))
bars1 = plt.bar([i - bar_width/2 for i in x], [mean_human], width=bar_width, label="HumanEval", alpha=0.85)
bars2 = plt.bar([i + bar_width/2 for i in x], [mean_coder], width=bar_width, label="CoderEval", alpha=0.85)

plt.xticks(x, labels)
plt.ylabel("Score moyen (%)")
plt.title("Comparaison globale GPT-4o (HumanEval vs CoderEval)", fontsize=13, weight="bold")
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.6)

# Ajouter les valeurs au-dessus des barres
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height + 1, f"{height:.1f}", ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig("Graphique_RQ1.png", dpi=300, bbox_inches='tight')
plt.close()
