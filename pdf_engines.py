import os
from LazyQueryEngineTool import LazyQueryEngineTool
from llama_index.core import StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.readers.file import PDFReader
from pdf_generator import download_pdf_files

download_pdf_files()

def get_index(data, index_name):
    index_path = os.path.join("data", "indexes", index_name)
    if not os.path.exists(index_path):
        print(f"Building index for {index_name}...")
        index = VectorStoreIndex.from_documents(data, show_progress=True)
        index.storage_context.persist(persist_dir=index_path)
    else:
        print(f"Loading existing index for {index_name}...")
        storage_context = StorageContext.from_defaults(persist_dir=index_path)
        index = load_index_from_storage(storage_context)
    return index

def create_pdf_engines():
    folder_path = os.path.join("data", "wiki_files")
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    
    tools = []
    for pdf_file in pdf_files:
        index_name = os.path.splitext(pdf_file)[0]
        pdf_path = os.path.join(folder_path, pdf_file)

        pdf_cache = {}

        def make_loader(path=pdf_path, name=index_name):
            def load_engine():
                if name in pdf_cache:
                    return pdf_cache[name]
                
                print(f"Loading engine for {name}...")
                pdf_data = PDFReader().load_data(file=path)
                index = get_index(pdf_data, name)
                engine = index.as_query_engine()
                pdf_cache[name] = engine
                return engine
            return load_engine

        tools.append(
            LazyQueryEngineTool(
                name=index_name,
                description=f"This tool gives information regarding {index_name}",
                loader_fn=make_loader()
            )
        )
    return tools
