"""
数据库导出/导入和分享功能
Database Export/Import and Sharing functionality
"""

import shutil
import tarfile
import json
from pathlib import Path
from typing import Optional
from datetime import datetime
from src.rag.local_rag import LocalRAG


class RAGDatabaseManager:
    """
    管理RAG数据库的导出、导入和分享
    Manage RAG database export, import and sharing
    """

    @staticmethod
    def export_database(
        source_db_path: str,
        output_file: str,
        include_metadata: bool = True
    ) -> Path:
        """
        导出数据库为单个压缩文件
        Export database as single compressed file

        Args:
            source_db_path: Path to ChromaDB directory
            output_file: Output .tar.gz file path
            include_metadata: Include metadata file

        Returns:
            Path to exported file
        """
        source_path = Path(source_db_path)
        output_path = Path(output_file)

        if not source_path.exists():
            raise FileNotFoundError(f"Database not found: {source_path}")

        # Ensure .tar.gz extension
        if not output_path.suffix == '.gz':
            output_path = output_path.with_suffix('.tar.gz')

        print(f"Exporting database from {source_path}...")

        # Create metadata
        if include_metadata:
            rag = LocalRAG(persist_directory=str(source_path))
            stats = rag.get_stats()

            metadata = {
                'export_date': datetime.now().isoformat(),
                'database_path': str(source_path),
                'collections': stats['collections'],
                'total_documents': stats['total_documents'],
                'database_size_mb': stats['database_size_mb'],
                'collections_detail': stats['collections_detail']
            }

            metadata_file = source_path / 'export_metadata.json'
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)

        # Create tar.gz archive
        with tarfile.open(output_path, 'w:gz') as tar:
            tar.add(source_path, arcname=source_path.name)

        # Clean up metadata file
        if include_metadata and metadata_file.exists():
            metadata_file.unlink()

        file_size_mb = output_path.stat().st_size / (1024 * 1024)

        print(f"✅ Database exported successfully!")
        print(f"   File: {output_path}")
        print(f"   Size: {file_size_mb:.2f} MB")

        return output_path

    @staticmethod
    def import_database(
        archive_file: str,
        target_db_path: str,
        overwrite: bool = False
    ) -> Path:
        """
        从压缩文件导入数据库
        Import database from compressed file

        Args:
            archive_file: Path to .tar.gz file
            target_db_path: Target directory for database
            overwrite: Overwrite existing database

        Returns:
            Path to imported database
        """
        archive_path = Path(archive_file)
        target_path = Path(target_db_path)

        if not archive_path.exists():
            raise FileNotFoundError(f"Archive not found: {archive_path}")

        if target_path.exists() and not overwrite:
            raise FileExistsError(
                f"Database already exists at {target_path}. "
                "Use overwrite=True to replace it."
            )

        print(f"Importing database from {archive_path}...")

        # Remove existing if overwrite
        if target_path.exists() and overwrite:
            shutil.rmtree(target_path)

        # Extract archive
        with tarfile.open(archive_path, 'r:gz') as tar:
            # Extract to parent directory
            tar.extractall(path=target_path.parent)

            # Get the extracted directory name
            members = tar.getmembers()
            if members:
                extracted_name = members[0].name.split('/')[0]
                extracted_path = target_path.parent / extracted_name

                # Rename if needed
                if extracted_path != target_path:
                    if target_path.exists():
                        shutil.rmtree(target_path)
                    extracted_path.rename(target_path)

        # Load and display metadata
        metadata_file = target_path / 'export_metadata.json'
        if metadata_file.exists():
            with open(metadata_file) as f:
                metadata = json.load(f)

            print(f"✅ Database imported successfully!")
            print(f"   Target: {target_path}")
            print(f"   Collections: {metadata.get('collections', 'N/A')}")
            print(f"   Documents: {metadata.get('total_documents', 'N/A')}")
            print(f"   Export date: {metadata.get('export_date', 'N/A')}")

            # Clean up metadata file
            metadata_file.unlink()
        else:
            print(f"✅ Database imported to {target_path}")

        return target_path

    @staticmethod
    def copy_database(
        source_db_path: str,
        target_db_path: str,
        overwrite: bool = False
    ) -> Path:
        """
        复制数据库（快速，适合本地使用）
        Copy database (fast, for local use)

        Args:
            source_db_path: Source database directory
            target_db_path: Target database directory
            overwrite: Overwrite existing database

        Returns:
            Path to copied database
        """
        source_path = Path(source_db_path)
        target_path = Path(target_db_path)

        if not source_path.exists():
            raise FileNotFoundError(f"Database not found: {source_path}")

        if target_path.exists() and not overwrite:
            raise FileExistsError(
                f"Database already exists at {target_path}. "
                "Use overwrite=True to replace it."
            )

        print(f"Copying database from {source_path} to {target_path}...")

        if target_path.exists() and overwrite:
            shutil.rmtree(target_path)

        shutil.copytree(source_path, target_path)

        print(f"✅ Database copied successfully to {target_path}")

        return target_path

    @staticmethod
    def get_database_info(db_path: str) -> dict:
        """
        获取数据库信息
        Get database information

        Args:
            db_path: Database directory path

        Returns:
            Database statistics
        """
        rag = LocalRAG(persist_directory=db_path)
        return rag.get_stats()

    @staticmethod
    def merge_databases(
        db_paths: list,
        target_db_path: str,
        new_collection_name: Optional[str] = None
    ):
        """
        合并多个数据库
        Merge multiple databases

        Args:
            db_paths: List of database paths to merge
            target_db_path: Target merged database path
            new_collection_name: Optional name for merged collection
        """
        print(f"Merging {len(db_paths)} databases...")

        target_rag = LocalRAG(persist_directory=target_db_path)

        if new_collection_name:
            target_rag.create_collection(new_collection_name)

        total_docs = 0

        for db_path in db_paths:
            source_rag = LocalRAG(persist_directory=str(db_path))
            source_collections = source_rag.list_collections()

            for collection in source_collections:
                coll_name = collection['name']
                print(f"  Merging collection: {coll_name}")

                # Get source collection
                source_coll = source_rag.chroma_client.get_collection(coll_name)

                # Get all documents
                results = source_coll.get(
                    include=['embeddings', 'documents', 'metadatas']
                )

                if results['documents']:
                    # Add to target collection
                    target_coll_name = new_collection_name or coll_name
                    target_rag.create_collection(target_coll_name)
                    target_coll = target_rag.chroma_client.get_collection(target_coll_name)

                    target_coll.add(
                        embeddings=results['embeddings'],
                        documents=results['documents'],
                        metadatas=results['metadatas'],
                        ids=[f"{db_path}_{id}" for id in results['ids']]
                    )

                    total_docs += len(results['documents'])

        print(f"✅ Merged {total_docs} documents into {target_db_path}")


def export_for_sharing():
    """导出数据库用于分享 / Export database for sharing"""
    import sys

    if len(sys.argv) < 3:
        print("Usage: python database_manager.py export <db_path> <output_file>")
        sys.exit(1)

    db_path = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) > 3 else "rag_database.tar.gz"

    manager = RAGDatabaseManager()
    exported_file = manager.export_database(db_path, output_file)

    print(f"\n📦 Database ready for sharing!")
    print(f"   File: {exported_file}")
    print(f"\nShare this file with others. They can import it with:")
    print(f"   python database_manager.py import {exported_file} ./their_database")


def import_shared_database():
    """导入分享的数据库 / Import shared database"""
    import sys

    if len(sys.argv) < 3:
        print("Usage: python database_manager.py import <archive_file> <target_path>")
        sys.exit(1)

    archive_file = sys.argv[2]
    target_path = sys.argv[3] if len(sys.argv) > 3 else "./imported_database"

    manager = RAGDatabaseManager()
    imported_path = manager.import_database(archive_file, target_path)

    print(f"\n🎉 Database imported successfully!")
    print(f"   Location: {imported_path}")
    print(f"\nYou can now use it:")
    print(f"   python -m streamlit run streamlit_app.py")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("RAG Database Manager")
        print("\nCommands:")
        print("  export <db_path> <output_file>     - Export database for sharing")
        print("  import <archive> <target_path>     - Import shared database")
        print("  copy <source> <target>             - Copy database locally")
        print("  info <db_path>                     - Show database info")
        print("\nExamples:")
        print("  python database_manager.py export ./chroma_db my_rag.tar.gz")
        print("  python database_manager.py import my_rag.tar.gz ./new_db")
        sys.exit(0)

    command = sys.argv[1]
    manager = RAGDatabaseManager()

    if command == "export":
        export_for_sharing()

    elif command == "import":
        import_shared_database()

    elif command == "copy":
        if len(sys.argv) < 4:
            print("Usage: python database_manager.py copy <source> <target>")
            sys.exit(1)
        source = sys.argv[2]
        target = sys.argv[3]
        manager.copy_database(source, target)

    elif command == "info":
        if len(sys.argv) < 3:
            print("Usage: python database_manager.py info <db_path>")
            sys.exit(1)
        db_path = sys.argv[2]
        info = manager.get_database_info(db_path)
        print(json.dumps(info, indent=2))

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
