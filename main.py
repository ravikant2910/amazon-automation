import requests
from bs4 import BeautifulSoup
from selenium import webdriver
#from msedge.selenium_tools import Edge,EdgeOptions
#from selenium.webdriver.edge.options import Options
import csv
import pandas as pd
import webbrowser

def generate_link(need):
  x = need.replace(' ','+')
  link = 'https://www.amazon.in/s?k='+x.strip()+'&sprefix=bags%2Caps%2C197&ref=nb_sb_p_1'
  return link

def new_csv(need):
    fields = ['Name','Price','Rating','Review','URL']
    filename = need.replace(' ','_')+'.csv'
    with open(filename, 'w') as csvfile: 
    # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
            
        # writing the fields 
        csvwriter.writerow(fields) 
    return filename

def input_csv(filename,data):
    
    data1 = {
        'URL': [data[0]],
        'Name': [data[1]],
        'price(INR)': [data[2]],
        'rating': [data[3]],
        'reviews':[data[4]]
    }
     
    # Make data frame of above data
    df = pd.DataFrame(data1)
     
    # append data frame to CSV file
    df.to_csv(filename, mode='a', index=False, header=False)
    
        
    

def extract(filename,item):
    atag = item.h2.a
    dec = atag.text.strip()
   
    link = 'https://www.amazon.in'+atag.get('href')
    
    try:
        price_parent = item.find('span','a-price')
        price = price_parent.find('span','a-offscreen').text
        price = price[1:]
    except AttributeError:
        return
    
    try:
        
        rating =item.i.text
        
        review_count = (item.find('span',{'class':'a-size-base s-underline-text'}).text)
    except AttributeError:
        rating = ''
        review_count = ''
    if '(' in review_count:
        review_count=review_count[1:-1]
            
    data = [dec,price,rating[:1],review_count,link]

    input_csv(filename,data)

def read(filename):
  
  data = pd.read_csv(filename)
  name = data['Name'].tolist()
  price= data['Price'].tolist()
  rate= data['Rating'].tolist()
  Review = data['Review'].tolist()
  url= data['URL'].tolist()
  
  l = len(name)
  for i in range(l):
    print(i+1)
    print(name[i])
    print('Price(in Rs) : ',price[i],'Rate out of 5 : ',rate[i],'Review : ',Review[i])
    print('\n')
  return url
  

if __name__ == '__main__'  :
    
    #options = EdgeOptions()
    #options.use_chromium = True
    print('1. Search')
    print('2. Exit')
    i = int(input())
    if(i==1):
        need = str(input('Enter the Product Required:  '))
    elif(i==2):
        break
    else:
        print('Enter a valid option')
    #driver = Edge(options = options)
    url = generate_link(need)
    filename = new_csv(need)
    for i in range(20):
        if(i!=0):
            url = url.replace('page='+str(i),'page='+str(i+1))
            url = url.replace('sr_pg_'+str(i+1),'sr_pg_'+str(i))
            

        headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}
        driver = requests.get(url,headers =headers)
        soup1 = BeautifulSoup(driver.content,'html.parser')
        #soup2 = BeautifulSoup(soup1.prettify(),'html.parser')
        results = soup1.find_all('div',{'data-component-type':'s-search-result'})

        
        for item in results:
            extract(filename,item)
    url = read(filename)
    while(True):
        print('1:\tSelect the Product\n2:\tExit')
        i = int(input('Enter the option : '))
        if(i == 1):
          j = int(input('Enter Product Number : '))
          webbrowser.open(url[j-1])
        elif(i == 2):
          break
        else:
          print('Enter a valid option!!!')
        
