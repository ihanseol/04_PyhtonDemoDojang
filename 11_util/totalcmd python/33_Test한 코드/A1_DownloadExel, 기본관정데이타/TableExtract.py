# pip install beautifulsoup4
# first remove </br> tag
# and find value of data

# simdo
# well_diameter
# Q
# HP
# tochool
# yongdo
# sebu_yongdo


from bs4 import BeautifulSoup
import os


def get_latest_filename():
    directory = 'c:/Users/minhwasoo/Downloads/'
    files = os.listdir(directory)
    files = [file for file in files if os.path.isfile(os.path.join(directory, file))]
    files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)), reverse=True)
    latest_file = files[0] if files else None
    full_path = os.path.join(directory, latest_file)
    print("Latest file:", full_path)
    return full_path


def get_well_spec(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data = file.read().replace('</br>', '')

    # print all inside file
    # print(data)

    soup = BeautifulSoup(data, 'html.parser')

    # simdo = soup.find('th', string='굴착심도(m)').find_next_sibling('td').text
    # well_diameter = soup.find('th', string='굴착직경(mm)').find_next_sibling('td').text

    yongdo = soup.find('th', string='지하수용도')
    if yongdo is not None:
        yongdo = yongdo.find_next_sibling('td').text
    else:
        yongdo = None


    sebu_yongdo = soup.find('th', string='지하수세부용도')
    if sebu_yongdo is not None:
        sebu_yongdo = sebu_yongdo.find_next_sibling('td').text
    else:
        sebu_yongdo = None


    simdo = soup.find('th', string='굴착심도(m)')
    if simdo is not None:
        simdo = simdo.find_next_sibling('td').text
    else:
        simdo = None


    well_diameter = soup.find('th', string='굴착직경(mm)')
    if well_diameter is not None:
        well_diameter = well_diameter.find_next_sibling('td').text
    else:
        well_diameter = None

    Q = soup.find('th', string='양수능력(㎥/일)')
    if Q is not None:
        Q = Q.find_next_sibling('td').text
    else:
        Q = None

    HP = soup.find('th', string='동력장치마력(마력)')
    if HP is not None:
        HP = HP.find_next_sibling('td').text
    else:
        HP = None

    tochool = soup.find('th', string='토출관 직경(mm)')
    if tochool is not None:
        tochool = tochool.find_next_sibling('td').text
    else:
        tochool = None

    # 값 출력

    if HP.startswith('.'):
        HP = '0' + HP

    print('*' * 50)
    print("Yongdo        :", yongdo)
    print("SebuYongdo    :", sebu_yongdo)
    print("simdo         :", simdo)
    print("well_diameter :", well_diameter)
    print("HP            :", HP)
    print("Q             :", Q)
    print("tochool       :", tochool)

    result = []
    result.append(yongdo)
    result.append(sebu_yongdo)
    result.append(simdo)
    result.append(well_diameter)
    result.append(HP)
    result.append(Q)
    result.append(tochool)

    return result


def save_to_csv(my_list, csv_file='data.CSV'):
    directory = 'd:/05_Send/'
    my_string = ' ,'.join(my_list)

    # Check if the filename contains a path separator
    if os.path.sep in csv_file:
        # If the filename already contains a path, use it directly
        file_path = csv_file
    else:
        # If the filename does not contain a path, prepend the directory path
        file_path = os.path.join(directory, csv_file)

    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        file.write(my_string)

    print(f"List saved to '{csv_file}' successfully.")


def main():
    file_name = get_latest_filename()
    result = get_well_spec(file_name)

    print('*'*50)
    print(result)
    print('*' * 50)
    save_to_csv(result)


if __name__ == "__main__":
    main()


