import aiosqlite

DB_NAME = "data/game.db"

async def create_database():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE,
            username TEXT,
            nickname TEXT,
            class TEXT,
            level INTEGER DEFAULT 1,
            exp INTEGER DEFAULT 0,
            gold INTEGER DEFAULT 100,
            hp INTEGER DEFAULT 100,
            max_hp INTEGER DEFAULT 100,
            attack INTEGER DEFAULT 10,
            defense INTEGER DEFAULT 5,
            crystals INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        await db.commit()


async def player_exists(telegram_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT telegram_id FROM players WHERE telegram_id=?",
            (telegram_id,)
        )

        player = await cursor.fetchone()
        return player is not None


async def create_player(telegram_id, username, nickname):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        INSERT INTO players
        (telegram_id, username, nickname)
        VALUES (?, ?, ?)
        """, (telegram_id, username, nickname))

        await db.commit()


async def get_player(telegram_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
        SELECT *
        FROM players
        WHERE telegram_id=?
        """, (telegram_id,))

        return await cursor.fetchone()
