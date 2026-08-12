from app.ingestion.chunker import TextChunker


def main():
    text = """
Acme Corporation Employee Handbook

Working Hours
Employees are expected to work from 9:00 AM to 5:00 PM, Monday through Friday.

Vacation Policy
Employees receive 20 days of paid vacation each year.

Remote Work
Employees may work remotely up to three days per week with manager approval.

Code Reviews
All production code must be reviewed by at least one other engineer before deployment.

Software Development
FastAPI is the preferred framework for building internal AI services.
"""

    chunker = TextChunker(chunk_size=100, chunk_overlap=20)

    chunks = chunker.chunk_text(text)

    print("\n===== CHUNKER TEST =====\n")
    print(f"Number of chunks: {len(chunks)}\n")

    for i, chunk in enumerate(chunks, start=1):
        print(f"Chunk {i}")
        print("-" * 50)
        print(chunk)
        print("-" * 50)
        print()


if __name__ == "__main__":
    main()