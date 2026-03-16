import requests
from bs4 import BeautifulSoup

def get_brvm_reports(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content,"html.parser")
    pdf_links = []
    for link in soup.find_all("a"):
        href = link.get("href")
        if href and ".pdf" in href:
            pdf_links.append(href)
    return pdf_links

def download_pdf_text(pdf_url):
    import pdfplumber
    import requests
    r = requests.get(pdf_url)
    with open("temp.pdf","wb") as f:
        f.write(r.content)
    text = ""
    with pdfplumber.open("temp.pdf") as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text