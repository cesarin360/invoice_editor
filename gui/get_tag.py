from html.parser import HTMLParser

ht = []
class MyHTMLParser(HTMLParser):
    def handle_data(self, data):
        ht.append(data)
    def get(html):
    	parser = MyHTMLParser()
    	html_tags =parser.feed(html)
    	ht1 =  []
    	for k, i in enumerate(ht):
    		if 'NIT' in i:
    			ht1.append(k)
    	return ht[ht1[1]+1]