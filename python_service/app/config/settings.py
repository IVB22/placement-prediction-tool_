from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    HOST: str = "127.0.0.1"
    PORT: int = 5000
    DEBUG: bool = True

    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB: str = "futurepath"
    MONGO_COLLECTION_RUNS: str = "runs"

    DATA_DIR: str = "data"
    MODEL_DIR: str = "models"
    PLACEMENT_MODEL_PATH: str = "models/placement_model.pkl"
    JOBS_CSV_PATH: str = "data/jobs_and_skills.csv"
