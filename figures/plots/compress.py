import os
import pikepdf

def compress_pdf(input_path, output_path):
    """
    Compress a PDF file using pikepdf.
    
    Args:
    - input_path: Path to the input PDF file.
    - output_path: Path to save the compressed PDF.
    """
    try:
        with pikepdf.open(input_path) as pdf:
            pdf.save(output_path)  # Save the file without any additional arguments
        print(f"Compressed: {input_path} -> {output_path}")
    except Exception as e:
        print(f"Error compressing {input_path}: {e}")

def compress_pdfs_in_folder(folder_path):
    """
    Compress all PDFs in the given folder.
    
    Args:
    - folder_path: Path to the folder containing PDF files.
    """
    output_folder = os.path.join(folder_path, "compressed")
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            input_path = os.path.join(folder_path, filename)
            output_path = os.path.join(output_folder, filename)
            compress_pdf(input_path, output_path)

def main():
    # List of folder paths
    folders = ["00", "07", "08", "24"]
    for folder in folders:
        compress_pdfs_in_folder(folder)
        print(f"Processed folder: {folder}")

if __name__ == "__main__":
    main()

