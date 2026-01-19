import os
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

data_file_path = "./data/"

labels = {
    "sd": "Strongly Disagree",
    "d": "Disagree",
    "n/us": "Neutral/Unsure",
    "a": "Agree",
    "sa": "Strongly Agree",
}


def load_all_data():
    """Load all CSV files once and return a dictionary."""
    data_dict = {}
    files = [
        f
        for f in os.listdir(data_file_path)
        if f.endswith(".csv") and f != "original.csv"
    ]

    for file in files:
        df = pd.read_csv(data_file_path + file)
        df.replace(np.nan, 0, inplace=True)
        questions = df["question"]
        df_numeric = df.drop(columns=["question"]).astype(int)
        df_numeric["question"] = questions
        data_dict[file[:-4]] = df_numeric

    return data_dict


def generate_question_pie_charts(data_dict):
    """Generate pie charts for each question."""
    colors = {
        "sd": "#d62728",
        "d": "#ff7f0e",
        "n/us": "#2ca02c",
        "a": "#1f77b4",
        "sa": "#9467bd",
    }

    for category, df in data_dict.items():
        questions = df["question"]
        df_numeric = df.drop(columns=["question"])

        for idx, q in enumerate(questions):
            data = df_numeric.iloc[idx]
            data = data[data > 0]
            total = data.sum()

            color_list = [colors[col] for col in data.index]

            fig = plt.figure(figsize=(10, 7), facecolor="white")
            plt.pie(
                data,
                labels=[labels[col] for col in data.index],
                autopct="%1.1f%%",
                startangle=140,
                colors=color_list,
                shadow=False,
                textprops={"fontsize": 11, "weight": "bold"},
            )

            for autotext in plt.gca().get_children():
                if hasattr(autotext, "set_color"):
                    try:
                        if autotext.get_text().endswith("%"):
                            autotext.set_color("white")
                            autotext.set_fontsize(10)
                            autotext.set_weight("bold")
                    except:
                        pass

            legend_labels = [f"{labels[col]}: {int(data[col])}" for col in data.index]
            plt.legend(legend_labels, loc="lower right", bbox_to_anchor=(1, 0, 0.5, 1))

            plt.title(q, fontsize=12, weight="bold", loc="center")
            plt.axis("off")
            plt.text(
                0.5,
                -0.1,
                f"Total Respondents: {int(total)}",
                ha="center",
                transform=plt.gca().transAxes,
                fontsize=11,
                weight="bold",
            )
            plt.savefig(
                f"./charts/{category}_{idx+1}.png",
                dpi=300,
                bbox_inches="tight",
            )
            plt.close()


def create_individual_category_pie_charts(data_dict):
    """Create individual category pie charts."""
    colors = {
        "sd": "#d62728",
        "d": "#ff7f0e",
        "n/us": "#2ca02c",
        "a": "#1f77b4",
        "sa": "#9467bd",
    }

    for category, df in data_dict.items():
        df_numeric = df.drop(columns=["question"])
        data = df_numeric.iloc[0]
        data = data[data > 0]
        total = data.sum()

        color_list = [colors[col] for col in data.index]

        fig = plt.figure(figsize=(10, 7), facecolor="white")
        plt.pie(
            data,
            labels=[labels[col] for col in data.index],
            autopct="%1.1f%%",
            startangle=140,
            colors=color_list,
            shadow=False,
            textprops={"fontsize": 11, "weight": "bold"},
        )

        for autotext in plt.gca().get_children():
            if hasattr(autotext, "set_color"):
                try:
                    if autotext.get_text().endswith("%"):
                        autotext.set_color("white")
                        autotext.set_fontsize(10)
                        autotext.set_weight("bold")
                except:
                    pass

        legend_labels = [f"{labels[col]}: {int(data[col])}" for col in data.index]
        plt.legend(legend_labels, loc="lower right", bbox_to_anchor=(1, 0, 0.5, 1))

        plt.title(
            f"Overall Response Distribution for {category.capitalize()}",
            fontsize=14,
            weight="bold",
        )
        plt.axis("off")
        plt.text(
            0.5,
            -0.1,
            f"Total Respondents: {int(total)}",
            ha="center",
            transform=plt.gca().transAxes,
            fontsize=11,
            weight="bold",
        )
        plt.savefig(f"./charts/{category}.png", dpi=300, bbox_inches="tight")
        plt.close()


def create_total_pie_chart(data_dict):
    """Create pie chart aggregating all responses."""
    colors = {
        "sd": "#d62728",
        "d": "#ff7f0e",
        "n/us": "#2ca02c",
        "a": "#1f77b4",
        "sa": "#9467bd",
    }

    total_data = {}
    total_respondents = 0

    for df in data_dict.values():
        df_numeric = df.drop(columns=["question"])
        total_respondents = max(total_respondents, df_numeric.sum(axis=1).max())

        for col in df_numeric.columns:
            if col not in total_data:
                total_data[col] = 0
            total_data[col] += df_numeric[col].sum()

    data = pd.Series(total_data)
    data = data[data > 0]

    color_list = [colors[col] for col in data.index]

    fig = plt.figure(figsize=(10, 7), facecolor="white")
    plt.pie(
        data,
        labels=[labels[col] for col in data.index],
        autopct="%1.1f%%",
        startangle=140,
        colors=color_list,
        shadow=False,
        textprops={"fontsize": 11, "weight": "bold"},
    )

    for autotext in plt.gca().get_children():
        if hasattr(autotext, "set_color"):
            try:
                if autotext.get_text().endswith("%"):
                    autotext.set_color("white")
                    autotext.set_fontsize(10)
                    autotext.set_weight("bold")
            except:
                pass

    legend_labels = [f"{labels[col]}: {int(data[col])}" for col in data.index]
    plt.legend(legend_labels, loc="lower right", bbox_to_anchor=(1, 0, 0.5, 1))

    plt.title(
        "Overall Response Distribution (All Categories)", fontsize=14, weight="bold"
    )
    plt.axis("off")
    plt.text(
        0.5,
        -0.1,
        f"Total Responses: {int(total_respondents)}",
        ha="center",
        transform=plt.gca().transAxes,
        fontsize=11,
        weight="bold",
    )

    plt.savefig("./charts/all_categories.png", dpi=300, bbox_inches="tight")
    plt.close()


# Load data once and pass to all functions
data_dict = load_all_data()

generate_question_pie_charts(data_dict)
create_individual_category_pie_charts(data_dict)
create_total_pie_chart(data_dict)
