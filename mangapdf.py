import requests as req
import argparse 
import threading
import os
from bs4 import BeautifulSoup
from fpdf import FPDF


parser = argparse.ArgumentParser()
parser_group = parser.add_argument_group('required named arguments')
parser_group.add_argument("-u", "--URL", help = "Add Manga URL",required=True)
 
args = parser.parse_args()
 
if args.URL:
    response = req.get(args.URL) 


# %%
iurl = "https://kodansha.us/series/a-silent-voice/"
response = req.get(iurl)


# %%
soup = BeautifulSoup(response.text)
mid = soup.find("manga-reader")["chapter-id"]


# %%
jurl = "https://kodansha.us/wp-content/themes/kodansha-usa/chapter-json.php"
Image_dir = "images/"
Output_dir = "output/"


# %%
payload={'id': mid}
response = req.post(jurl,data=payload)


# %%
data = response.json()
name = data["chapter_volume"]
url_list = data['chapter_pages']


# %%
chapter_img_path = Image_dir+name+"/"
try:
    os.mkdir(chapter_img_path)
except:
    print("Folder Present")


# %%
def download(purl, file_loc):
    img_res = req.get(purl)
    if img_res.status_code == 200:
        with open(file_loc, 'wb') as ifile:
            ifile.write(img_res.content)


# %%
def export_pdf(name):
    pdf = FPDF('P','mm','A4')
    x,y,w,h = 0,0,210,297
    chapter_img_path = Image_dir+name+"/"
    img_list = os.listdir(chapter_img_path)
    img_count = len(img_list)
    for ind in range(img_count):
        page_name = chapter_img_path + str(ind) + ".jpg"
        pdf.add_page()
        pdf.image(page_name,x,y,w,h)

    pdf.output(Output_dir+name+".pdf","F")


# %%
for ind,obj in list(enumerate(url_list)):
    purl = obj['url']
    img_path = chapter_img_path + str(ind) + ".jpg"
    download_thread = threading.Thread(target=download, args=(purl,img_path))
    download_thread.start()

export_pdf(name)


