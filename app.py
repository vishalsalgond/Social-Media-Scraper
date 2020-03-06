from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import re

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():

    if (request.method == 'POST' and request.form.get('choices-single-default')=='Twitter'):
        query = request.form['query']

        url = 'https://mobile.twitter.com/hashtag/' + query
        page = requests.get(url)

        soup = BeautifulSoup(page.text, 'html.parser')

        tweet = []
        newlink = []

        for tag in soup.find_all('a'):
            try:
                temp = (tag['href'])
                temp = temp[:-4]
                temp = 'https://twitter.com' + temp
                tweet.append(temp)
            except:
                pass

        for element in tweet:
            if 'status' in element:
                element = re.sub(':','%3A', element)
                element = re.sub('/', '%2F', element)
                newlink.append(element)

        newlink = list(set(newlink))

        browser = webdriver.Firefox()
        # # Step 2) Navigate to Facebook
        
        final = []

        for element in newlink:
            try:
                url1 = 'https://publish.twitter.com/?query=' + element + '&widget=Tweet'
                browser.get(url1)

                x = browser.find_element_by_xpath('//code[@class="EmbedCode-code"]')
                final.append(x.text)

            except:
                pass


        return render_template('twitter.html', data=final)




        # url = 'https://mobile.twitter.com/hashtag/' + query
        # page = requests.get(url)

        # soup = BeautifulSoup(page.text, 'html.parser')

        # tweet = []
        # username = []

        # for tag in soup.find_all('div', {'class':'tweet-text'}):
        #     tweet.append(tag.text)

        # for tag in soup.find_all('div', {'class':'username'}):
        #     username.append(tag.text)

        # username = username[:len(tweet)]
        # dict1 = {}
        # for i in range(len(tweet)):
        #     dict1.update({username[i]: tweet[i]})
        #         #return username[i], tweet[i]
        # return render_template('twitter.html', data=dict1)


    elif (request.method == 'POST' and request.form.get('choices-single-default')=='Facebook'):
        # Step 1) Open Firefox 
        browser = webdriver.Firefox()
        # Step 2) Navigate to Facebook
        browser.get("http://www.facebook.com")
        # Step 3) Search & Enter the Email or Phone field & Enter Password
        username = browser.find_element_by_id("email")
        password = browser.find_element_by_id("pass")
        submit   = browser.find_element_by_id("loginbutton")
        username.send_keys("vssalgond@yahoo.com")
        password.send_keys("Vishal@27")
        # Step 4) Click Login
        submit.click()

        query = request.form['query']

        url = "https://www.facebook.com/search/posts/?q=%23" + query
        browser.get(url)
        #browser.find_element_by_xpath('//a[@class="_6ojs"]').click()


        #elements = browser.findElements(By.className("_6-cm"))
        text = browser.find_element_by_xpath('//div[@class="_1qkq _1qkx"]')

        #text = browser.find_element_by_xpath('//div[@class="_6-cp"]')

        return(text.text)
    
    elif (request.method == 'POST' and request.form.get('choices-single-default')=='Instagram'):

        #from firebase import firebase
        browser = webdriver.Firefox()
        query = request.form['query']

        url = "https://www.instagram.com/explore/tags/" + query + "/top/"
        browser.get(url)
        link = []
        link.append(query)
        #soup = BeautifulSoup(page.text, 'html.parser')

        #temp = browser.find_elements_by_xpath("//div[contains(concat(' ', normalize-space(@class), ' '), 'KL4Bh')]")
        temp = browser.find_elements_by_xpath('//img[@class="FFVAD"]')

        
        for element in temp:
            link.append(element.get_attribute("src"))

        return render_template('insta.html', data = link)
                
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)