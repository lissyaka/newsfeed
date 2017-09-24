import re

class InputValidator:
    def __init__(self, title, image, body):
        self.title = title
        self.image = image
        self.body = body
        self.errors = {}

    def valid(self):
        self.validate_title()
        self.validate_image()
        self.validate_body()

        if not self.errors:
            return True
        else:
            return False

    def validate_title(self):
        self.validate_empty("title", self.title)

    def validate_image(self):
        self.validate_empty("image", self.image)

    # TODO: validate_body needs to be refactored
    def validate_body(self):
        self.validate_empty("body", self.body)

        valid_tags = ["<p>", "<b>", "<i>", "<strong>", "<em>"]
        temp_list =  re.findall('<.*?>', self.body)
        body_value = []
        check_img = []
        check_iframe = []
        check_without_img_iframe = [] 
        iframe_sites = ["www.youtube.com", "play.md", "vimeo.com"]       

        for el in temp_list:
            if el.startswith("<img"):
                check_img.append(el)
            elif el.startswith("<iframe"):
                check_iframe.append(el)
            elif not el.startswith("</"):
                check_without_img_iframe.append(el)

        for i in check_without_img_iframe:
            if i not in valid_tags:
                body_value.append(" %s tag is not available." % i)

        for i in check_img:
            temp = i.split(" ")
            for el in temp:
                if not (el.startswith("<img") or el.startswith("src=")): 
                    body_value.append("For <img> tag only src= available.")
                    break            

        for i in check_iframe:
            temp = i.split(" ")
            for el in temp:
                if not (el.startswith("<iframe") or el.startswith("src=")): 
                    body_value.append("For <iframe> tag only src= available.")
                    break               
                elif (el.startswith("src=") and not next(iter(re.findall("://(.*?)/", el) or []), None) in iframe_sites):
                    body_value.append("For <iframe src>  available sites are only www.youtube.com, play.md, vimeo.com.")

        if body_value:
            self.errors.update({"body": body_value}) 

    def validate_empty(self, field, value):
        if not value: self.errors.update({field: ["cannot be empty"]})


           
# Tests
#form1 = InputValidator("ahz", "asd", "<div>")
#form2 = InputValidator("ahz", "asd", "dgagasdf <div> dfgsdg sz<p>")
#form3 = InputValidator("ahz", "asd", "<P>")
#form4 = InputValidator("ahz", "asd", "")
#form5 = InputValidator("ahz", "asd", 'gadjgigalsd <div>gsdafgasfdgsd</div>gsaddf <p>gsdfgds  <img src="sdas" alt="adas"> savfasdfa</img> <img>, </img>')
#form6 = InputValidator("ahz", "asd", 'g<img src=>gadjgigalsd gsaddf <p>gsdfgds <iframe src="http:sfaess" alt="dsesrfgds">')
#form7 = InputValidator("ahz", "asd", '<img src=>gadjgigalsd gsaddf <p>gsdfgds <iframe src="http://www.youtube.com/1.html">')

#print form1.valid()
#print form1.errors
#print form2.valid()
#print form2.errors
#print form3.valid()
#print form3.errors
#print form4.valid()
#print form4.errors
#print form5.valid()
#print form5.errors
#print form6.valid()
#print form6.errors
#print form7.valid()
#print form7.errors


