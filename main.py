import os
import fitz  # PyMuPDF
import camelot
import requests

def download_pdf(url, output_path):
    """Download PDF from a URL and save it locally."""
    response = requests.get(url)
    if response.status_code == 200:
        with open(output_path, "wb") as pdf_file:
            pdf_file.write(response.content)
        print(f"PDF downloaded successfully and saved to {output_path}")
    else:
        raise Exception(f"Failed to download PDF. Status code: {response.status_code}")

def extract_text_from_pdf(file_path, output_folder):
    """Extract text from PDF and save to .txt files."""
    try:
        with fitz.open(file_path) as pdf_document:
            for page_num in range(len(pdf_document)):
                text = pdf_document[page_num].get_text()
                text_filename = os.path.join(output_folder, f"page_{page_num + 1}_text.txt")
                with open(text_filename, "w", encoding="utf-8") as text_file:
                    text_file.write(text)
        print(f"Text extracted to {output_folder}")
    except Exception as e:
        print(f"Error extracting text: {e}")

def extract_images_from_pdf(file_path, output_folder):
    """Extract images from PDF and save to image files."""
    try:
        pdf_document = fitz.open(file_path)
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            for img_index, img in enumerate(page.get_images(full=True)):
                xref = img[0]
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                image_filename = os.path.join(output_folder, f"page_{page_num + 1}_img_{img_index + 1}.{image_ext}")
                with open(image_filename, "wb") as img_file:
                    img_file.write(image_bytes)
        pdf_document.close()
        print(f"Images extracted to {output_folder}")
    except Exception as e:
        print(f"Error extracting images: {e}")

def extract_tables_from_pdf(file_path, output_folder):
    """Extract tables from PDF and save to CSV files."""
    try:
        tables = camelot.read_pdf(file_path, pages="all", flavor="stream")
        for i, table in enumerate(tables):
            table_filename = os.path.join(output_folder, f"table_{i + 1}.csv")
            table.to_csv(table_filename)
        print(f"{len(tables)} tables extracted to {output_folder}")
    except Exception as e:
        print(f"Error extracting tables: {e}")

def extract_all_from_pdf(file_path, output_folder):
    """Extract text, images, and tables from a PDF."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    print("Starting extraction...")

    # Extract text
    print("Extracting text...")
    extract_text_from_pdf(file_path, output_folder)

    # Extract images
    print("Extracting images...")
    extract_images_from_pdf(file_path, output_folder)

    # Extract tables
    print("Extracting tables...")
    extract_tables_from_pdf(file_path, output_folder)

    print(f"Extraction completed! All data saved in {output_folder}")

# Main script
if __name__ == "__main__":
    # Define relative paths
    project_root = os.path.dirname(os.path.abspath(__file__))  # Get the project root
    downloaded_pdf_path = os.path.join(project_root, "downloaded.pdf")
    output_dir = os.path.join(project_root, "output_data")
    pdf_url = "https://arxiv.org/pdf/2408.09869"

    try:
        # Step 1: Download PDF
        print("Downloading PDF...")
        download_pdf(pdf_url, downloaded_pdf_path)

        # Step 2: Extract all data
        print("Extracting data from PDF...")
        extract_all_from_pdf(downloaded_pdf_path, output_dir)

    except Exception as e:
        print(f"Error: {e}")
