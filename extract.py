import polars as pl
import os


file_path = "data/raw/WFO_Backbone/classification.csv"
clean_path = "data/raw/WFO_Backbone/cleaned_classification.csv"


def clean_invalid_utf8_characters():
    with (
        open(file_path, "r", errors="replace", encoding="utf-8") as infile,
        open(clean_path, "w", errors="replace", encoding="utf-8") as outfile,
    ):
        for line in infile:
            outfile.write(line)


pl.scan_csv(
    "data/raw/WFO_Backbone/cleaned_classification.csv",
    separator="\t",
    infer_schema_length=1000000,
).sink_parquet("./data/raw/df.parquet")
