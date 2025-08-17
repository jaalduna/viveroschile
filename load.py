from fastapi import FastAPI
from transform import get_major_group, df
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/major-groups")
def major_groups():
    """
    Returns the list of major groups from the dataset.
    """
    return {"major_groups": get_major_group(df)}
