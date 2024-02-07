# Import necessary functions and variables from the rag module
from rag import chunk_processing, embeddings, generation, OPENAI_KEY

# Prompt user for the filepath of the PDF file to process
pdf_path = input("Filepath: ")
print("PDF filepath:", pdf_path)

# Open the PDF file in binary mode
pdf = open(pdf_path, 'rb')

# Process the PDF file into chunks
processed_chunks = chunk_processing(pdf)

# Embed the processed chunks using OpenAI embeddings
embedded_chunks = embeddings(processed_chunks)

# Generate responses based on the embedded chunks
generated_response = generation(embedded_chunks)

# Print the generated response
print(generated_response)
