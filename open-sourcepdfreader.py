from diagrams import Diagram,Cluster
from diagrams.custom import Custom
import os

output_folder = "diagram_output"
os.makedirs(output_folder,exist_ok=True)
images_folder="images"
custom_images={
    "request_cover":os.path.join(images_folder,"requests_cover.png"),
    "images_icon": os.path.join(images_folder, "imgicon.png"),
    "pdf_image": os.path.join(images_folder, "pdfimage.png"),
    "pymupdf": os.path.join(images_folder, "pymupdf.png"),
    "tables": os.path.join(images_folder, "tables.png"),
    "textimg": os.path.join(images_folder, "textimg.png"),
    "camelot": os.path.join(images_folder, "camelor.png")

}
missing_file = [key for key,path in custom_images.items() if not os.path.exists(path)]
if missing_file:
    raise FileNotFoundError(f" the following required image file are missing:{','.join(missing_file)}")

org_dir = os.getcwd()
os.chdir(output_folder)
with Diagram(
        "Custom diagram for pdf reader",
        filename="open_source_pdf_reader",
        show="false",
        direction="LR"
    ):
    cc_request=Custom("Web Request",custom_images["request_cover"])
    with Cluster("PDF Reader"):

        cc_pdf_image=Custom("PDF",custom_images["pdf_image"])
        cc_pymupdf=Custom("Pymupdf",custom_images["pymupdf"])
        cc_camelot=Custom("Camelot",custom_images["camelot"])
        cc_images=Custom("Image",custom_images["images_icon"])
        cc_textimg=Custom("Text",custom_images["textimg"])
        cc_tables=Custom("Tables",custom_images["tables"])

        cc_pdf_image>> cc_pymupdf >> cc_images
        cc_pdf_image>> cc_pymupdf >> cc_textimg
        cc_pdf_image>> cc_camelot >> cc_tables

    cc_request >> cc_pdf_image
    os.chdir(org_dir)