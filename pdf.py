import os
from llama_index.core import StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.readers.file import PDFReader

def get_index(data, index_name):
    index = None
    if not os.path.exists(index_name):
        print(f"Building index for {index_name}...")
        index = VectorStoreIndex.from_documents(data, show_progress=True)
        index.storage_context.persist(persist_dir=index_name)
    else:
        print(f"Loading existing index for {index_name}...")
        index = load_index_from_storage(StorageContext.from_defaults(persist_dir=index_name))
    return index

def create_engines(base_path, folders):
    engines = {}
    for folder in folders:
        folder_path = os.path.join(base_path, folder)
        pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
        for pdf_file in pdf_files:
            pdf_path = os.path.join(folder_path, pdf_file)
            try:
                pdf_data = PDFReader().load_data(file=pdf_path)
                index_name = os.path.splitext(pdf_file)[0]
                index = get_index(pdf_data, index_name)
                engines[index_name] = index.as_query_engine()
                print(f"Engine created for {pdf_file}")
            except FileNotFoundError:
                print(f"Error: The file {pdf_path} was not found.")
            except Exception as e:
                print(f"Error processing {pdf_file}: {e}")
    return engines

    