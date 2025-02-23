import asyncio

from fastapi import FastAPI
from sqlalchemy import text

from mimicry.config import CONFIG
from mimicry.repository import ReferenceRepository


app = FastAPI()


@app.get('/')
async def get_root():
    return {'status': 'Hello, World'}


async def main():
    repository = ReferenceRepository()

    query = text('SELECT VERSION()')
    async with repository.session() as session:
        version = (await session.execute(query)).scalar()

    print(version)


if __name__ == '__main__':
    print(CONFIG.database)
    print(CONFIG.database.url)

    asyncio.run(main())
