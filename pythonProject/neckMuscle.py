import psycopg2
import requests
from bs4 import BeautifulSoup

titles = []

def get_list_of_muscles_group():
    global titles
    categories_url = 'https://iq-body.ru/exercises/category'
    response = requests.get(categories_url)
    soup = BeautifulSoup(response.text, 'lxml')
    items = soup.find_all('div', class_='col-xs-3')
    count = 0
    groups = []
    for i in items:
        title = i.find('span', class_='post-title mod_2 text-uppercase')
        titles.append(title.text)
        groups.append(items[count].find('a').get('href'))
        count += 1
    return groups


def get_list_of_exercises(groups):
    global titles
    connection = psycopg2.connect(
        database="SportExercises",
        user="postgres",
        password="postgres",
        host="127.0.0.1",
        port="5432"
    )

    print("Database opened successfully")

    for group in groups:
        site = 'https://iq-body.ru'
        url = site + group
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        items = soup.find_all('div', class_='training-content')

        count = 0
        for item in items:
            type = titles[count]
            count += 1

            exercise_name = item.find('a').text

            exercise_link = item.find('a').get('href')
            start_link = 'https://iq-body.ru/'
            response_exercise = requests.get(start_link + exercise_link)
            soup_exercise = BeautifulSoup(response_exercise.text, 'lxml')
            items_exercise = soup_exercise.find('div', class_='flex-container')

            information = soup_exercise.find('div', class_='upr__info')
            subdata_title = information.find_all('span', class_='subdata-title') #подзаголовки
            subdata_description = information.find_all('span', class_='subdata-description')
            info = ""
            for i in range(0, len(subdata_title) - 1):
                info += subdata_title[i].text + subdata_description[i].text
            if info.find("Участвующие мышцы:") != -1:
                substr = info.partition("Целевые мышцы:")
                substr = substr[2].partition("Участвующие мышцы:")
                target_muscles = substr[0]
                substr = substr[2].partition("Инвентарь:")
                involved_muscles = substr[0]
                equipment = substr[2]
            else:
                substr = info.partition("Целевые мышцы:")
                substr = substr[2].partition("Инвентарь:")
                target_muscles = substr[0]
                equipment = substr[2]
                involved_muscles = ""

            description = items_exercise.find('p').text

            instruction = items_exercise.find_all('li')
            num_step = 0
            inst = ""
            for step in instruction:
                num_step += 1
                inst += str(num_step) + '. ' + step.text + '\n'

            insertExercise = connection.cursor()
            insertExercise.execute(
                "INSERT INTO EXERCISES (type, target_muscles, title, involved_muscles, equipment, description, instruction) " +
                "VALUES ('" + type + "', '" + target_muscles + "', '" + exercise_name + "', '" + involved_muscles + "', '" + equipment + "', '" + description + "', '" + inst + "')"
            )

            connection.commit()
            print(str(count) + ". Record inserted successfully")

    connection.close()
