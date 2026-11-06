import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

from data_passport import process_and_sign_data

load_dotenv()


class GraphIngestor:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI"),
            auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD")),
        )

    def close(self):
        self.driver.close()

    def ingest_passports(self, passports):
        query = """
        MERGE (c:Chunk {chunk_id: $chunk_id})
        SET c.content = $content,
            c.source_document = $source_document,
            c.cryptographic_hash = $cryptographic_hash

        MERGE (cl:ClearanceLevel {level: $clearance_level})

        MERGE (c)-[:REQUIRES_CLEARANCE]->(cl)
        """
        with self.driver.session() as session:
            for passport in passports:
                session.run(
                    query,
                    chunk_id=passport.chunk_id,
                    content=passport.content,
                    source_document=passport.source_document,
                    cryptographic_hash=passport.cryptographic_hash,
                    clearance_level=passport.clearance_level,
                )
                print(f"Ingested chunk: {passport.chunk_id} -> {passport.clearance_level}")


if __name__ == "__main__":
    sample_documents = [
        ("chunk_001", "Project Falcon will launch in Q2 2027 with a $50M budget.", "board_minutes_2026.txt"),
        ("chunk_002", "The Merger with Acme Corp is under review by Legal and Finance.", "deal_memo_internal.pdf"),
        ("chunk_003", "Employee Sarah Chen is being promoted to Senior Engineer effective January.", "hr_update_emails.eml"),
        ("chunk_004", "Q3 revenue reached $42.7 million, exceeding analyst projections by 8%.", "earnings_report_q3.pdf"),
    ]

    passports = [
        process_and_sign_data(chunk_id, content, source, "EXECUTIVE_ONLY")
        for chunk_id, content, source in sample_documents
    ]

    ingestor = GraphIngestor()
    try:
        ingestor.ingest_passports(passports)
        print("Successfully ingested all passports into Neo4j.")
    finally:
        ingestor.close()
