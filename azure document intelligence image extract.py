import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
load_dotenv()


# Azure Credentials
endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
key = os.getenv("AZURE_FORM_RECOGNIZER_KEY")
form_url = os.getenv("SAMPLE_PDF_URL")

# Initialize Azure Document Intelligence Client
document_intelligence_client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))

# Define the path for the sample PDF file
path_to_sample_documents = "africas_manufacturing_puzzle-compressed.pdf"  # Update with the actual PDF path

# Define the output directory for extracted images
output_dir = os.path.join(os.getcwd(), "markdown_pages", "images")
os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists

# Analyze document
with open(path_to_sample_documents, "rb") as f:
    poller = document_intelligence_client.begin_analyze_document(
        "prebuilt-layout",
        body=f,
        output=["figures"],  # Updated output parameter
    )

result = poller.result()
operation_id = poller.details["operation_id"]

# Process figures and save them to the markdown_pages/images folder
if result.figures:
    for figure in result.figures:
        if figure.id:
            response = document_intelligence_client.get_analyze_result_figure(
                model_id=result.model_id, result_id=operation_id, figure_id=figure.id
            )

            image_path = os.path.join(output_dir, f"{figure.id}.png")
            with open(image_path, "wb") as writer:
                writer.writelines(response)

            print(f"Saved image: {image_path}")

else:
    print("No figures found.")
