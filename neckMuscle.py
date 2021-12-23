import requests
from bs4 import BeautifulSoup


def get_list_of_muscles_group():
    categories_url = 'https://iq-body.ru/exercises/category'
    response = requests.get(categories_url)
    soup = BeautifulSoup(response.text, 'lxml')
    items = soup.find_all('div', class_='col-xs-3')
    count = 0
    for i in items:
        count += 1
        title = i.find('span', class_='post-title mod_2 text-uppercase')
        print(str(count) + ') ' + title.text)
    group_of_muscles = int(input('Введите категорию '))
    if (group_of_muscles < 1 or group_of_muscles > len(items)):
        print('invalid param')
        exit()
    print(str(group_of_muscles) + ") " + items[group_of_muscles - 1].text)
    list_of_exercises = items[group_of_muscles - 1].find('a').get('href')
    return list_of_exercises


def get_exercise_description(exercise_link):
    start_link = 'https://iq-body.ru/'
    response_exercise = requests.get(start_link + exercise_link)
    soup_exercise = BeautifulSoup(response_exercise.text, 'lxml')
    items_exercise = soup_exercise.find('div', class_='flex-container')

    information = soup_exercise.find('div', class_='upr__info')
    print('----- ' + information.find('h3').text + ' -----')
    subdata_title = information.find_all('span', class_='subdata-title')
    subdata_description = information.find_all('span', class_='subdata-description')
    for i in range(0, len(subdata_title) - 1):
        print(subdata_title[i].text + subdata_description[i].text)

    description = items_exercise.find('p')
    print('----- Описание -----')
    print(description.text)

    print('----- Выполнение -----')
    instruction = items_exercise.find_all('li')
    num_step = 0
    for step in instruction:
        num_step += 1
        print(str(num_step) + '. ' + step.text)
    print('')


def get_list_of_exercises(group):
    site = 'https://iq-body.ru'
    url = site + group
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    items = soup.find_all('div', class_='training-content')

    count = 0
    for item in items:
        count += 1

        exercise_name = item.find('a').text
        print(str(count) + ") " + exercise_name)

        exercise_link = item.find('a').get('href')
        get_exercise_description(exercise_link)


