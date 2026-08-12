from app.ingestion.document_loader import DocumentLoader


def main():
    loader = DocumentLoader("documents")

    documents = loader.load_txt_files()

    print("\n===== DOCUMENT LOADER TEST =====\n")

    print(f"Documents loaded: {len(documents)}\n")

    for document in documents:
        print(f"Source : {document['source']}")
        print("-" * 60)
        print(document["content"])
        print("-" * 60)
        print()


if __name__ == "__main__":
    main()