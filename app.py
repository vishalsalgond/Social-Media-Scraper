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
        newlink1 = []
        for element in newlink:
            y = re.search(".*[0-9]$", element)
            if (y):
                if "=" not in element and "?" not in element and "_" not in element:
                    newlink1.append(element)

        for element in newlink1:
            try:
                url1 = 'https://publish.twitter.com/?query=' + element + '&widget=Tweet'
                browser.get(url1)

                x = browser.find_element_by_xpath('//code[@class="EmbedCode-code"]')
                final.append(x.text)

            except:
                pass

        print(newlink1)

        f = open("templates/twitter.html", "w", encoding='utf-8')
        f.write('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><style>body{display: table;margin: auto;}</style><link rel="icon" href="https://cdn0.iconfinder.com/data/icons/social-flat-rounded-rects/512/twitter-512.png" type="image/icon type"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Twitter</title></head><body>')
        f.write('<img src="{{ url_for("static", filename="images/twitter-logo.png")}}" alt="logo" height="60px" width="200px"><br>')
        f.write("<h1>Showing results for " + query + "</h1>")
        for element in final:
            f.write(element)
            f.write("<br>")
        f.write("</body></html>")
        f.close()

        browser.quit()

        return render_template('twitter.html')




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
        username.send_keys("facia.helman@gmail.com")
        password.send_keys("facebook@123")
        # Step 4) Click Login
        submit.click()
        query = request.form['query']

        url = "https://www.facebook.com/search/posts/?q=%23" + query + "&epa=SERP_TAB"
        browser.get(url)
        # browser.find_element_by_xpath('//a[@class="_6ojs"]').click()
        # browser.implicitly_wait(10)

        #temp = browser.find_elements_by_xpath("//div[contains(concat(' ', normalize-space(@class), ' '), 'KL4Bh')]")
        temp = browser.find_elements_by_xpath('//a')
        
        link = []
        newlink = []
        for element in temp:
            link.append(str(element.get_attribute("href")))

        #print(link)

        for element in link:
            try:
                if "posts" in element and "#" not in element and "=" not in element:
                    newlink.append(element)
            except:
                pass

        newlink = list(set(newlink))
        newlink.insert(0,query)
        browser.quit()
        #print(newlink)
        return render_template('facebook.html', data = newlink)
    
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

        browser.quit()
        return render_template('insta.html', data = link)
                
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)