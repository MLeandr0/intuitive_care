import requests
from bs4 import BeautifulSoup
import zipfile
from urllib.parse import urljoin
from typing import Dict, List
from pathlib import Path

SITE_URL = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
ANEXOS_FOLDER = Path("web_scraping/anexos")
KEYWORDS = ["Anexo I", "Anexo II"]
ZIP_NAME = ANEXOS_FOLDER / "anexos.zip"

def get_pdf_links(url: str, keywords: List[str]) -> Dict:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise SystemExit(f"Error accessing the URL: {e}")

    soup = BeautifulSoup(response.text, 'html.parser')
    pdf_links = {}

    for link in soup.find_all('a'):
        link_text = link.get_text(strip=True)
        cleaned_text = link_text.rstrip('.')
        
        for keyword in keywords:
            cleaned_keyword = keyword.rstrip('.')
            if cleaned_text == cleaned_keyword and link.get('href') and link['href'].endswith('.pdf'):
                href = link['href'].strip()
                pdf_links[keyword] = href if href.startswith('http') else urljoin(url, href)
                break

    return pdf_links

def download_file(url: str, save_path: Path) -> bool:
    ANEXOS_FOLDER.mkdir(parents=True, exist_ok=True)
    try:
        with requests.get(url, stream=True, timeout=30) as response:
            response.raise_for_status()
            
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
            
            print(f"Download completed: {save_path}")
            return True
            
    except requests.RequestException as e:
        print(f"Error trying to download {url}: {e}")
        return False

def zip_files(file_paths: List[Path], zip_path: Path) -> bool:
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in file_paths:
                if file.exists():
                    zipf.write(file, file.name)
                    file.unlink()
                else:
                    print(f"File not found: {file}")
        
        print(f"Files compressed into: {zip_path}")
        return True
        
    except Exception as e:
        print(f"Failed to create ZIP file: {e}")
        return False

def main():
    try:
        print("Starting search for anexos...")
        pdf_links = get_pdf_links(SITE_URL, KEYWORDS)
        
        if not pdf_links:
            raise SystemExit("No anexos found on the site.")
        
        print(f"Encontrados {len(pdf_links)} anexo(s):")
        for keyword, link in pdf_links.items():
            print(f"- {keyword}: {link}")
        
        downloaded_files = []
        for keyword, link in pdf_links.items():
            filename = ANEXOS_FOLDER / f"{keyword.replace(' ', '_')}.pdf"
            if download_file(link, filename):
                downloaded_files.append(filename)
        
        if downloaded_files:
            if not zip_files(downloaded_files, ZIP_NAME):
                print("Files were downloaded but not compressed.")
        else:
            print("No files were successfully downloaded.")
            
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        print("Process completed!")

if __name__ == "__main__":
    main()