from selenium import webdriver
import openpyxl

WD = webdriver.Chrome("chromedriver.exe")

WD.get("https://ridibooks.com/bestsellers/general")

WB = openpyxl.load_workbook("B_Result.xlsx")
WS = WB.active

while True:
    B_Title = WD.find_elements_by_class_name("title_text")  # 책제목의 Class Name
    B_Link = WD.find_elements_by_class_name("thumbnail_btn")  # 링크주소
    B_IMG = WD.find_elements_by_class_name("thumbnail")  # 이미지
    B_Author = WD.find_elements_by_class_name("author")  # 저자
    B_Star = WD.find_elements_by_class_name("RSGBookMetadata_StarRate")  # 별점
    B_Price = WD.find_elements_by_class_name("meta_price_info")  # 가격

    for i in range (0,len(B_Title)):
        try:
            WS.append ([B_Title[i].text,B_Link[i].get_attribute("href"),
                        B_IMG[i].get_attribute("src"), B_Author[i].text,
                        B_Star[i*2].find_element_by_class_name("StarRate_Score").get_attribute("textContent"), B_Price[i].text])
        except:
            WS.append([B_Title[i].text, B_Link[i].get_attribute("href"),
                       B_IMG[i].get_attribute("src"), B_Author[i].text,"",B_Price[i].text])
    try:
        WD.find_element_by_class_name("btn_next").click()
    except:
        break

WB.save("Result.xlsx")
WD.quit()