docker build -f retriever/Dockerfile -t iran_retriver:1.0 .
docker build -f preprocessor/Dockerfile -t iran_preprocess:1.0 .
docker build -f enricher/Dockerfile -t iran_enricher:1.0 .
docker build -f persister/Dockerfile -t iran_persister:1.0 .
docker build -f dataRetrieval/Dockerfile -t data_retrieval:1.0 .
docker compose up -d