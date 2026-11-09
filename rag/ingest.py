"""Indexe les fichiers .md et .txt de rag/docs/ dans la base vectorielle."""
import chromadb

from common import COLLECTION, ROOT, collection, embed, llm_client

DOCS_DIR = ROOT / "rag" / "docs"
CHUNK_SIZE = 800     # taille d'un morceau, en caractères
OVERLAP = 150        # chevauchement entre deux morceaux


def split(text: str) -> list[str]:
    """Découpe un texte en morceaux qui se chevauchent."""
    chunks, start = [], 0
    while start < len(text):
        chunks.append(text[start:start + CHUNK_SIZE])
        start += CHUNK_SIZE - OVERLAP
    return [c.strip() for c in chunks if c.strip()]


def main() -> None:
    # On repart d'une base vide pour ne pas garder d'anciens morceaux
    db = chromadb.PersistentClient(path=str(ROOT / "rag" / ".chroma"))
    if COLLECTION in [c.name for c in db.list_collections()]:
        db.delete_collection(COLLECTION)
    col = collection()
    client = llm_client()

    files = sorted(p for p in DOCS_DIR.rglob("*") if p.suffix in {".md", ".txt"})
    if not files:
        raise SystemExit(f"Aucun fichier .md ou .txt dans {DOCS_DIR}")

    for path in files:
        chunks = split(path.read_text(encoding="utf-8"))
        for i in range(0, len(chunks), 16):          # par paquets de 16
            batch = chunks[i:i + 16]
            col.add(
                ids=[f"{path.name}-{i + j}" for j in range(len(batch))],
                embeddings=embed(client, batch),
                documents=batch,
                metadatas=[{"source": path.name}] * len(batch),
            )
        print(f"{path.name} : {len(chunks)} morceaux indexés")

    print(f"Total : {col.count()} morceaux dans la base")


if __name__ == "__main__":
    main()
