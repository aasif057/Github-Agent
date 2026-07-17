from app.vectorstore.config import (
    VectorStoreConfig,
)

from app.vectorstore.factory import (
    VectorStoreFactory,
)


def main():

    config = VectorStoreConfig(

        collection_name="github_code",

        embedding_dimension=768,

        recreate_collection=False,

        host="localhost",

        port=6333,
    )

    store = VectorStoreFactory.get(
        "qdrant",
        config,
    )

    store.ensure_collection()

    print()

    print(
        "Collection exists:",
        store.collection_exists()
    )

    print(
        "Vector count:",
        store.count()
    )


if __name__ == "__main__":

    main()