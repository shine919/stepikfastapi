from config import load_config
from fastapi import FastAPI
from logger import logger
from pydantic import BaseModel


app = FastAPI()
config = load_config()

if config.debug:
    app.debug = True
else:
    app.debug = False


class Nums(BaseModel):
    num1: int = 1
    num2: int = 1


@app.get("/")
async def root():
    logger.info(f"Connecting to database: {config.db.database_url}")
    return {"database_url": config.db.database_url}


@app.post("/calculate/")
async def calculate(nums: Nums):
    return nums.num1 + nums.num2
