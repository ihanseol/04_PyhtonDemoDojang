import bs4

html_str = """
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Title</title>
    </head>
    <body>
    <ul class="greet">
        <li>hello</li>
        <li>world</li>
        <li>who</li>        
        <li>are</li>
        <li>you</li>
    </ul>
    
    <ul class="reply">
        <li>ok</li>
        <li>no</li>
        <li>sure</li>
    </ul>
    
    </body>
</html>
"""

bs_obj = bs4.BeautifulSoup(html_str, "html.parser")

# lis = bs_obj.find_all("li")

# for li in lis:
#     print(li)


ul_find = bs_obj.find("ul",{'class':'reply'})
print(ul_find)

lis = ul_find.find_all("li")
print(lis)















