from bs4 import BeautifulSoup
import requests
import re

class get_product_details:
    def get_title(self,soup):

        try:

            links = soup.find_all("span", attrs={'class':'a-size-large product-title-word-break'})
            

            title=links[0].get_text(strip=True)


            title_string = title

        except (AttributeError,IndexError):
            return "no title found"

        return title_string


    def get_price(self,soup):
        try:
            price = soup.find_all("div",attrs={"class":"a-section a-spacing-none aok-align-center aok-relative"})
            pricing=price[0].text.strip()
            match = re.search(r"₹[\d,]+", pricing)
            Price = match.group(0) 
        except (AttributeError,IndexError):
            return "Not able to fetch the price"
        
        return Price
    def get_description(self,soup):

        try:
            features=soup.find_all("div",attrs={"class":"a-section a-spacing-medium a-spacing-top-small"})[0].text.strip()
            lines=features.strip().split('\n')
            
        except (AttributeError,IndexError):
            return "not description available"

        return lines

    def get_rating(self,soup):

        try:
            links = soup.find_all("a", attrs={'class':'a-popover-trigger a-declarative'})
            ratings=links[0].find('span',attrs={'class':'a-icon-alt'}).get_text(strip=True)
        except (AttributeError,IndexError):
            return "No rating"
        return ratings


    def get_rating_count(self,soup):
        try:
            count = soup.find_all("div",attrs={"class":"a-row a-spacing-medium averageStarRatingNumerical"})
            rating_count=count[0].text.strip()
        except (AttributeError,IndexError):
            return "zero counts"	

        return rating_count

def main():
    HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})

    URL = "https://www.amazon.in/Daikin-Fixed-Copper-Filter-FTL28U/dp/B09R4SF5SP/ref=sr_1_2?_encoding=UTF8&content-id=amzn1.sym.58c90a12-100b-4a2f-8e15-7c06f1abe2be&dib=eyJ2IjoiMSJ9.LpujZ4uISPUK8sa_6yNGVa_NjOCUQKpUI8WFpHZUHewO6FmLy13sfeLIwPEZa99KSndOI4NEzbUgndQLwiGg4VgGcvda8e6GJx6aDLnzqJpsxpWmilywAgddWWPWHacJvdmJG69P-YBmaD3mdwchH2fr9rzPRwQFab2_vH4V5hPUa449m7OtKvFwd58Ua8HfMgux_DePJ6pg4_dxjo9ZJMIuXXcMoeBMtVGgFSyCJipchKSfYGtG40Ni_CIEh0ktgyqg41ewqrg0gs3sWVyqHdcViCB_8k1l7vhC2f-MJ2k.l0RcKXufxf28BbaHFgUJuAGKxpJvitrp4fBfBJ5wHhk&dib_tag=se&pd_rd_r=e375f93c-adbc-4831-accf-fe0ce15653fb&pd_rd_w=NfMTh&pd_rd_wg=JYzCf&pf_rd_p=58c90a12-100b-4a2f-8e15-7c06f1abe2be&pf_rd_r=Q2GX98FPDEZ5DGHG5ZGN&qid=1732168361&refinements=p_85%3A10440599031&rps=1&s=kitchen&sr=1-2"

    webpage = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(webpage.text, "html.parser")

    scraper=get_product_details()
    ratings=scraper.get_rating(soup)
    description=scraper.get_description(soup)
    price=scraper.get_price(soup)
    title=scraper.get_title(soup)
    print(description)
    print(ratings)
    print(price)
    print(title)


if __name__ == '__main__':
    main()
    
   