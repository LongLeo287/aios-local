import sys
import os

# Append root
sys.path.append(os.environ.get("AOS_ROOT", "."))

from plugins.LightRAG.lightrag_adapter import get_lightrag
import logging

logging.basicConfig(level=logging.INFO)

def main():
    print("ðŸš€ Initializing LightRAG Knowledge Graph Pipeline...")
    rag = get_lightrag()

    status = rag.status()
    print("STATUS:", status)

    if not status.get("ready"):
        print("âŒ LightRAG is in NOOP mode. Please ensure 'lightrag-hku' is installed and Ollama has pulled models.")
        return

    thesis_path = r"<AI_OS_ROOT>\brain\shared-context\THESIS.md"
    print(f"\nðŸ“¥ Inserting file into Graph: {thesis_path}")
    success = rag.insert_file(thesis_path)

    if success:
        print("âœ… Inserted successfully. Now building graph nodes/edges.")
        print("\nðŸ”Ž Testing Hybrid Query...")

        try:
            res = rag.hybrid_query("What is the core thesis or philosophy of AI OS Corp?")
            print("\n================== GRAPH RESULT ==================")
            print(res)
            print("==================================================")
        except Exception as e:
            print(f"âŒ Query failed: {e}")
    else:
        print("âŒ Failed to insert file.")

if __name__ == "__main__":
    main()

