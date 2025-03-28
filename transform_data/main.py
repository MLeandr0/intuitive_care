import camelot
import pandas as pd
from pathlib import Path
import zipfile
import os

ZIP_PATH = Path("../web_scraping/anexos.zip")
EXTRACT_FOLDER = Path("extracted_pdfs")
PDF_PATH = EXTRACT_FOLDER / "anexo_I.pdf"
CSV_FILENAME = "combined_tables.csv"
ZIP_FILENAME = "Teste_matheus_leandro.zip"

def unzip_files():
    if not ZIP_PATH.exists():
        raise FileNotFoundError(f"ZIP file not found: {ZIP_PATH}")

    EXTRACT_FOLDER.mkdir(parents=True, exist_ok=True)

    try:
        with zipfile.ZipFile(ZIP_PATH, "r") as zip_ref:
            zip_ref.extractall(EXTRACT_FOLDER)
        print(f"Files extracted successfully to folder: {EXTRACT_FOLDER}")   
    except Exception as e:
        raise RuntimeError(f"Error extracting files: {e}")

def save_to_zip():
    if not Path(CSV_FILENAME).exists():
        print(f"CSV file {CSV_FILENAME} not found. Skipping ZIP creation.")
        return

    try:
        with zipfile.ZipFile(ZIP_FILENAME, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(CSV_FILENAME)
        print(f"CSV successfully compressed into: {ZIP_FILENAME}")

        os.remove(CSV_FILENAME)
    except Exception as e:
        print(f"Error while zipping CSV: {e}")

def extract_table():
    if not PDF_PATH.exists():
        raise FileNotFoundError(f"PDF file not found: {PDF_PATH}")

    try:
        tables = camelot.read_pdf(PDF_PATH, pages="3-end", process_background=True)
        print(f"Total tables extracted: {tables.n}")

        if tables.n == 0:
            print("No tables found in the PDF.")
            return

        combined_df = pd.concat([table.df for table in tables])
        
        header = combined_df.iloc[0]
        combined_df = combined_df[1:].reset_index(drop=True)
        combined_df.columns = header

        combined_df.rename(columns={"OD": "Seg. Odontológica", "AMB": "Seg. Ambulatorial"}, inplace=True)

        combined_df.to_csv(CSV_FILENAME, index=False)
        print(f"CSV file saved: {CSV_FILENAME}")

        save_to_zip()
    except Exception as e:
        print(f"Error processing PDF tables: {e}")

if __name__ == "__main__":
    unzip_files()
    extract_table()
