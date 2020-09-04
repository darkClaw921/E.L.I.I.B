
# 
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
from PIL import Image, ImageDraw, ImageFont

# VK API import
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from vk_api import VkUpload 

# OS import
import time
import os
from threading import Thread

# Help files import
import setings

# VK settings
vk_session = vk_api.VkApi(token = setings.vkDdkgtaApi)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

# Global parametrs
usersId = [] # список людей которые уже учавствуют или уже прошли тест
usersId.append(0) # добавляем фантомного пльзователя 
otvet = "" # Знакомтесь Костыль
colume = 1 # столбец
rowId = 2 # от куда начинать строки
rowName = 2
rowSecondName = 2
rowQuestions1 = 2
rowQuestions2 = 2
rowQuestions3 = 2
rowWork = 2

# Create sheet
print('Создание таблицы ...')
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive'] # что то для чего-то нужно Костыль
creds = ServiceAccountCredentials.from_json_keyfile_name('ViktorinaProfkom-50c0fbdcd821.json', scope) # Секретынй файл json для доступа к API
client = gspread.authorize(creds)
sheet = client.open('ViktorinaProfkom').sheet1 # Имя таблицы
pp = pprint.PrettyPrinter # хз
sheet.update_cell(1, 1, "id пользователя")
sheet.update_cell(1, 2, "Имя ")
sheet.update_cell(1, 3, "Фамилия")
sheet.update_cell(1, 4, "Вопрос 1")
sheet.update_cell(1, 5, "Вопрос 2")
sheet.update_cell(1, 6, "Вопрос 3")
sheet.update_cell(1, 7, "Задание 1")
print('Таблица создана')

# Functional
def getMessege (stringOtvet, user_id): # Получаем сообщение от конкретного пользователя
    for event in longpoll.listen(): # цикл для каждго ивента сервера
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.user_id == user_id: # ждать ответа от данного юзера 
            vk.messages.getConversations(offset = 0, count = 1)  
    
            if event.text == stringOtvet: # если событие текст и он равен сообщению которое отправил пользователь
                return True

            return False
        

def sendMessege (User_id, random_id, Message): #Отпровляем сообщение пользователю 
    vk.messages.send( 
                    user_id = User_id,
                    random_id = random_id,
                    message = Message
		            )
    return 0 

def keyboardCreater(ButtonText1, ButtonText2, ButtonText3, ButtonText4): 
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(ButtonText1)
    keyboard.add_line()
    keyboard.add_button(ButtonText2)
    keyboard.add_line()
    keyboard.add_button(ButtonText3)
    keyboard.add_line()
    keyboard.add_button(ButtonText4)

    return keyboard

def getQuestion(randomId, userID):
    global rowId, rowQuestions1, rowName, rowSecondName, rowWork

    userInfo = vk.users.get(user_ids = userID) # Получили ответ в виде массива из одного списка
    userInfo = userInfo[0] 
    
    keyboard = keyboardCreater("13", "2", "123", "9")
    
    sheet.update_cell(rowId, 1, f"""vk.com/id{userID}""")
    sheet.update_cell(rowName, 2, userInfo["first_name"])
    rowName += 1
    sheet.update_cell(rowSecondName, 3, userInfo["last_name"])
    rowSecondName += 1

    rowId += 1
    countPoint = 0 # cчётчик праильных ответов

    vk.messages.send( #Отправляем сообщение
                    user_id = userID,
                    random_id = randomId,
                    #attachment='photo-194390511_457239038', # ссылк фото из альбома сообщества
                    message = """
Сколько членов квартиры 84 ?
                            """,
                    keyboard = keyboard.get_keyboard()
		            )
    
    otvetQvestions = getMessege("9", userID) # Ответ который получили от пользователя 

    if otvetQvestions :
        countPoint += 1
        print("getQuestion: ", countPoint)

        sheet.update_cell(rowQuestions1, 4, "1")
        rowQuestions1 += 1
    else: 
        print("getQuestion: ", countPoint)

        sheet.update_cell(rowQuestions1, 4, "0")
        rowQuestions1 += 1

    countPoint += getQuestion2(randomId, userID)

    sendMessege(userID, randomId, "Не,ра,страий,ся")
    print("Finish getQuestion: ", countPoint)

def getQuestion2(randomId, userID):
    global rowQuestions2

    keyboard = keyboardCreater("ППО", "Квартира", "84", "CТО")

    countPoint = 0

    vk.messages.send( #Отправляем сообщение
                    user_id = userID,
                    random_id = randomId,
                    # attachment = 'photo-194390511_457239038',
                    message="""
Что такое Квартира 84 ?
                            """,
                    keyboard = keyboard.get_keyboard()
		            )

    otvetQvestions = getMessege("ППО", userID)

    if otvetQvestions:
        countPoint += 1
        print("getQuestion2: ", countPoint)

        sheet.update_cell(rowQuestions2, 5, "1")
        rowQuestions2 += 1 
        
    else: 
        sheet.update_cell(rowQuestions2, 5, "0")
        rowQuestions2 += 1 
        print("getQuestion2: ", countPoint)

    countPoint += getQuestion3(randomId, userID)
    
    return countPoint

def getQuestion3(randomId, userID):
    global rowQuestions3

    keyboard = keyboardCreater("Один дома", "27 Стренджовят", "Война бесконечности", "Миша")

    countPoint = 0

    vk.messages.send( #Отправляем сообщение
                    user_id = userID,
                    random_id = randomId,
                    attachment = 'photo-194390511_457239097',
                    message="""
Из какого это фильма?
                            """,
                    keyboard = keyboard.get_keyboard()
		            )

    otvetQvestions = getMessege("Война бесконечности", userID)

    if otvetQvestions :
        countPoint += 1
        print("getQuestion3: ", countPoint)

        sheet.update_cell(rowQuestions3, 6, "1")
        rowQuestions3 += 1 
    else :
        print("getQuestion3: ", countPoint)
        sheet.update_cell(rowQuestions3, 6, "0")
        rowQuestions3 += 1 
    
    getQuestion4(randomId, userID)

    return countPoint

def getQuestion4(randomId, userID):
    global rowQuestions2, rowWork

    vk.messages.send( #Отправляем сообщение
                    user_id = userID,
                    random_id = randomId,
                    #attachment = 'photo-194390511_457239038',
                    message="""
Отправь любое фото
                            """
		            )
    getMessege("", userID)

    photoGet = vk.messages.getHistoryAttachments(peer_id = userID ,media_type='photo', start_from = 'photo', cout=1 ) # Получить от пользователя последние фото
    
    void = photoGet['items'] # распарсили ответ от photoGet
    void =  void[0]
    void =  void['attachment']
    void =  void['photo']
    void =  void['sizes']
    void =  void.pop() # последний элемент списка
    void =  void['url']

    print(void)

    sheet.update_cell(rowWork, 7, f"""=IMAGE("{str(void)}")""")
    rowWork += 1
                  
def newUser():
    print("Проверка подключения")

    for userId in usersId: # Перебираем список с пользователями 
        if event.user_id == userId:
            print("Старый пользователь...")
            return False 

    print("Новый пользователь...")

    return True

# %% [Run Server] 

for event in longpoll.listen():
    
    print(event.type)

    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:

        whoUser = newUser()

        if whoUser:
            print("Новый пользователь")
            usersId.append(event.user_id)

            Thread(target=getQuestion, args=(event.random_id, event.user_id)).start() # Запуск нового потока для нового пользвоателя
        else:
            print("Старый пользователь")


           
