"""Pose une question : retrouve les passages utiles puis demande au LLM de répondre."""
import sys

from common import CHAT_MODEL, collection, embed, llm_client

TOP_K = 4

SYSTEM_PROMPT = (
    "Tu es un assistant qui répond UNIQUEMENT à partir du contexte fourni. "
    "Si la réponse n'est pas dans le contexte, réponds : "
    "\"Je ne trouve pas cette information dans les documents.\" "
    "Cite la source entre crochets, par exemple [politique-mots-de-passe.md]."
)


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit('Usage : python ask.py "ta question"')
    question = " ".join(sys.argv[1:])

    client = llm_client()
    results = collection().query(query_embeddings=embed(client, [question]), n_results=TOP_K)

    passages = results["documents"][0]
    sources = [m["source"] for m in results["metadatas"][0]]
    context = "\n\n".join(f"[{s}]\n{p}" for s, p in zip(sources, passages))

    answer = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Contexte :\n{context}\n\nQuestion : {question}"},
        ],
    )
    print(answer.choices[0].message.content)
    print("\nSources consultées :", ", ".join(sorted(set(sources))))


if __name__ == "__main__":
    main()
