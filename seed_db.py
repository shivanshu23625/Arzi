import asyncio
import asyncpg
from sentence_transformers import SentenceTransformer

async def main():
    print("Generating vector embedding for knowledge base...")
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    content = "Project status is on schedule with all architectural components operational."
    embedding = model.encode(content, convert_to_numpy=True, normalize_embeddings=True).tolist()

    print("Connecting to PostgreSQL...")
    conn = await asyncpg.connect(
        user="postgres",
        password="postgres_secure_pass",
        database="mldb",
        host="postgres",
        port=5432
    )

    await conn.execute(
        "INSERT INTO document_knowledge_base (content, embedding) VALUES ($1, $2::vector);",
        content,
        str(embedding)
    )
    await conn.close()
    print("✅ Knowledge base successfully seeded with high-dimensional vector embeddings!")

if __name__ == "__main__":
    asyncio.run(main())