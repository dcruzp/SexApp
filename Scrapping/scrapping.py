

import requests ,bs4 
from pprint import pprint




def get_posturas ():
    
  res = requests.get('https://www.menshealth.com/es/sexo-relaciones-pareja/g36405604/50-mejores-posturas-sexuales-hombre/')
  res.raise_for_status()
  sexSould = bs4.BeautifulSoup(res.text)

  # file = open ('webscrappingexample.html') 
  # sexSould = bs4.BeautifulSoup(file.read())
  # elems = sexSould.select('span[class="listicle-slide-hed-text"]')

  elementos = sexSould.find_all("div", class_="listicle-slide")
  posturas = [] 
  
  for item in elementos:
    subelement = bs4.BeautifulSoup(str(item), 'html.parser')
    
    number = subelement.find_all("span" , class_= "listicle-slide-hed-number")[0].getText()

    postura = subelement.find_all("span" , class_= "listicle-slide-hed-text")[0].getText()
    
    picture_img = subelement.select_one('picture > img')
    data_src = picture_img.get('data-src')
    src = picture_img.get('src')
    img = data_src
    if data_src is None: img = src 

    desc = subelement.find_all("div", class_= "listicle-slide-dek")[0].getText()
    desc = desc.replace('\"','')
    description = desc.replace('\n', '')
    posturas.append((number, postura, img, description))
  return posturas

