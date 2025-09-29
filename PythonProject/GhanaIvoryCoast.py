import os
import sys
import pandas as pd
import matplotlib.pyplot as plt


def load_and_clean(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"CSV not found: {path}")
    df = pd.read_csv(path, encoding="utf-8")
    # normalize column names
    df.columns = df.columns.str.strip()
    # strip string columns we care about
    for col in ["Item", "Area", "Element"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
    # coerce numeric
    if "Year" in df.columns:
        df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    if "Value" in df.columns:
        df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
    return df


def subset(df, area_mask, element_name):
    """
    Return rows for 'Cocoa, beans' (robust matching), the requested element, and the given area mask.
    """
    item_mask = (
        df["Item"].astype(str).str.contains("cocoa", case=False, na=False)
        & df["Item"].astype(str).str.contains("bean", case=False, na=False)
    )
    elem_mask = df["Element"].astype(str).str.contains(element_name, case=False, na=False)
    sel = df[item_mask & elem_mask & area_mask].dropna(subset=["Year", "Value"]).copy()
    return sel.sort_values("Year")


def create_2x2(df, save_pdf=True, pdf_path="cocoa_2x2.pdf"):
    # robust area matching for Ghana and Ivory Coast variants
    gh_mask = df["Area"].astype(str).str.contains("Ghana", case=False, na=False)
    iv_mask = df["Area"].astype(str).str.contains(r"Ivory|Cote|Côte|d'Ivoire|Cote d'Ivoire", case=False, na=False)

    gh_yield = subset(df, gh_mask, "Yield")
    iv_yield = subset(df, iv_mask, "Yield")

    gh_area = subset(df, gh_mask, "Area harvested")
    iv_area = subset(df, iv_mask, "Area harvested")

    fig, axes = plt.subplots(2, 2, figsize=(14, 10), constrained_layout=True)
    fig.suptitle("Ghana vs Ivory Coast Production Trends", fontsize=16, color="green")

    # Ghana Yield (scatter)
    ax = axes[0, 0]
    if not gh_yield.empty:
        ax.scatter(gh_yield["Year"], gh_yield["Value"], marker="o", label="Ghana Yield")
    else:
        ax.text(0.5, 0.5, "No data for Ghana Yield", transform=ax.transAxes, ha="center", va="center")
    ax.set_title("Ghana — Yield", fontsize=12, color="saddlebrown")  # valid color
    ax.set_xlabel("Year", color="orange")
    ax.set_ylabel("Yield (hg/ha)", color="orange")
    ax.grid(True, linestyle="--", alpha=0.4)

    # Ivory Coast Yield (scatter)
    ax = axes[0, 1]
    if not iv_yield.empty:
        ax.scatter(iv_yield["Year"], iv_yield["Value"], marker="s", label="Ivory Coast Yield")
    else:
        ax.text(0.5, 0.5, "No data for Ivory Coast Yield", transform=ax.transAxes, ha="center", va="center")
    ax.set_title("Ivory Coast — Yield", fontsize=12, color="magenta")
    ax.set_xlabel("Year", color="orange")
    ax.set_ylabel("Yield (hg/ha)", color="orange")
    ax.grid(True, linestyle="--", alpha=0.4)

    # Ghana Area harvested (bar)
    ax = axes[1, 0]
    if not gh_area.empty:
        # convert years to integers for nice bar x-axis ticks
        years = gh_area["Year"].astype(int)
        ax.bar(years, gh_area["Value"], color="blue", label="Ghana Area harvested")
    else:
        ax.text(0.5, 0.5, "No data for Ghana Area", transform=ax.transAxes, ha="center", va="center")
    ax.set_title("Ghana — Area harvested", fontsize=12, color="saddlebrown")
    ax.set_xlabel("Year", color="orange")
    ax.set_ylabel("Area harvested (ha)", color="orange")
    ax.grid(True, linestyle="--", alpha=0.4)

    # Ivory Coast Area harvested (bar)
    ax = axes[1, 1]
    if not iv_area.empty:
        years = iv_area["Year"].astype(int)
        ax.bar(years, iv_area["Value"], color="crimson", label="Ivory Coast Area harvested")
    else:
        ax.text(0.5, 0.5, "No data for Ivory Coast Area", transform=ax.transAxes, ha="center", va="center")
    ax.set_title("Ivory Coast — Area harvested", fontsize=12, color="magenta")
    ax.set_xlabel("Year", color="orange")
    ax.set_ylabel("Area harvested (ha)", color="orange")
    ax.grid(True, linestyle="--", alpha=0.4)

    # rotate x tick labels to avoid overlap
    for ax in axes.flat:
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

    if save_pdf:
        fig.savefig(pdf_path, bbox_inches="tight")
        print(f"Saved figure to: {pdf_path}")
    plt.show()


def main():
    file_path = r"C:\Users\Administrator\Documents\FAOSTAT_data_7-23-2022 (1).csv"
    try:
        df = load_and_clean(file_path)
    except Exception as exc:
        print("Error loading data:", exc, file=sys.stderr)
        sys.exit(1)

    required = {"Item", "Area", "Element", "Year", "Value"}
    if not required.issubset(set(df.columns)):
        print(
            "CSV is missing one of the required columns: Item, Area, Element, Year, Value",
            file=sys.stderr,
        )
        print("Columns found:", df.columns.tolist(), file=sys.stderr)
        sys.exit(1)

    create_2x2(df, pdf_path="cocoa_2x2.pdf")


if __name__ == "__main__":
    main()