import polars as pl


df = pl.read_parquet("data/raw/df.parquet")


def get_major_group(df: pl.DataFrame) -> list:
    """
    Get the major group from the DataFrame.
    """
    mg = df.select("majorGroup").unique().sort("majorGroup").to_series().to_list()
    return [item for item in mg if item is not None]


def get_num_of_family_alphabetically() -> pl.DataFrame:
    return (
        df.select(["majorGroup", "family"])
        .unique()
        .filter(pl.col("majorGroup") == "A")
        .sort("family")
        .with_columns(pl.col("family").str.slice(0, 1).alias("first_letter"))
        .group_by("first_letter")
        .len()
    )
