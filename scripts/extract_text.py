import fitz  # PyMuPDF
from PIL import Image
import io

def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    
    text = ""
    # Extract text from the first page (you can loop over pages if needed)
    for page_number, page in enumerate(doc, start=1):
        text += page.get_text("text")
        # Close the document
    doc.close()    
    return text

# Function to crop and save the first page image
def extract_and_crop_image(pdf_path, output_image_path):
    doc = fitz.open(pdf_path)
    page = doc.load_page(0)  # Load first page

    # Extract image from the first page
    for img_index, img in enumerate(page.get_images(full=True)):
        print(img_index)
        if img_index == 0:
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            # Save the image
            image = Image.open(io.BytesIO(image_bytes))
            image.save(f"data/test.jpg")
            image.save(f"{output_image_path}_{img_index}.{image_ext}")

    doc.close()

if __name__ == '__main__': 
    print(extract_text_from_pdf("./data/zucchini-bell-pepper-penne-62267e183a4fd16123652b73-117b9e82.pdf"))

