
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

# VK setings
vk_session = vk_api.VkApi(token = setings.vkProfkomApi2)
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
rowQuestions4 = 2
rowQuestions5 = 2
rowQuestions6 = 2
rowWork = 2
photoGet = ['a']
void = 0

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
sheet.update_cell(1, 7, "Вопрос 4")
sheet.update_cell(1, 8, "Вопрос 5")
sheet.update_cell(1, 9, "Вопрос 6")
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
    global rowId, rowQuestions1, rowName, rowSecondName, rowWork, void, photoGet, rowQuestions2, rowQuestions3, rowQuestions4, rowQuestions5, rowQuestions6

    userInfo = vk.users.get(user_ids = userID) # Получили ответ в виде массива из одного списка
    userInfo = userInfo[0] 
    
    sheet.update_cell(rowId, 1, f"""vk.com/id{userID}""")
    sheet.update_cell(rowName, 2, userInfo["first_name"])
    rowName += 1
    sheet.update_cell(rowSecondName, 3, userInfo["last_name"])
    rowSecondName += 1

    rowQuestions1ForUsers = rowQuestions1
    rowQuestions2ForUsers = rowQuestions2
    rowQuestions3ForUsers = rowQuestions3
    rowQuestions4ForUsers = rowQuestions4
    rowQuestions5ForUsers = rowQuestions5
    rowQuestions6ForUsers = rowQuestions6
    rowQuestions1 += 1
    rowQuestions2 += 1
    rowQuestions3 += 1
    rowQuestions4 += 1
    rowQuestions5 += 1
    rowQuestions6 += 1    



    rowId += 1
    countPoint = 0 # cчётчик праильных ответов

    vk.messages.send( #Отправляем сообщение
                    user_id = userID,
                    random_id = randomId,
                    #attachment='photo-194390511_457239038', # ссылк фото из альбома сообщества
                    message = """
Привет, первокурсник. Этот квест создан для того, чтобы ты улыбнулся, немного поднапряг извилины и сделал на своем смартфоне пару прикольных фото. Если не будешь лениться - закончишь КГТА. А если не будешь лениться в квесте - получишь приз! Удачи! Держи первое задание:
                            """,
                    # keyboard = keyboard.get_keyboard()
		            )

    vk.messages.send( #Отправляем сообщение
                    user_id = userID,
                    random_id = randomId,
                    #attachment='photo-194390511_457239038', # ссылк фото из альбома сообщества
                    message = """
Вчера на собрании каждому студенту-первокурснику давали навигатор по вузу. Сделай селфи с ним. Фото присылай сюда!
                            """,
                    # keyboard = keyboard.get_keyboard()
		            )
    getMessege("", userID)
    time.sleep(0)
    messageID = vk.messages.getHistory(user_id = userID, count = 1)
    print(messageID['items'])
    messageID = messageID['items']
    messageID = messageID[0]
    messageID = messageID['attachments']
    messageID = messageID[0]
    messageID = messageID['photo']
    messageID = messageID['sizes']
    messageID = messageID.pop()
    messageID = messageID['url']
    print('history ', messageID )

    print("получение фото от 1 вопроса")
   

    sheet.update_cell(rowQuestions1ForUsers, 4, f"""=IMAGE("{str(messageID)}")""")
    # rowQuestions1 += 1
    
    void = 0
    photoGet = ['a']
    countPoint += getQuestion2(randomId, userID,rowQuestions2ForUsers,rowQuestions3ForUsers,rowQuestions4ForUsers,rowQuestions5ForUsers,rowQuestions6ForUsers)

    sendMessege(userID, randomId, "Поздравляю! Все испытания позади! Если ты был честен, умен и креативен со мной, то жди сообщение о призе. Твой бот – Валера. Надеюсь еще спишемся")
    print("Finish getQuestion: ", countPoint)

def getQuestion2(randomId, userID,rowQuestions2ForUsers,rowQuestions3ForUsers,rowQuestions4ForUsers,rowQuestions5ForUsers,rowQuestions6ForUsers):
    global rowQuestions2

    keyboard = keyboardCreater("87", "90", "72", "88")

    countPoint = 0

    vk.messages.send( #Отправляем сообщение
                    user_id = userID,
                    random_id = randomId,
                    attachment = 'photo-194390511_457239113',
                    message="""
Не хотелось тебя грузить чем-то сложным, поэтому вот тебе детская задачка. Какой номер у паковочного места под машиной
                            """,
                    keyboard = keyboard.get_keyboard()
		            )

    otvetQvestions = getMessege("87", userID)

    
    if otvetQvestions:
        countPoint += 1
        print("getQuestion2: ", countPoint)

        sheet.update_cell(rowQuestions2ForUsers, 5, "1")
        # rowQuestions2 += 1 
        
    else: 
        sheet.update_cell(rowQuestions2ForUsers, 5, "0")
        # rowQuestions2 += 1 
        print("getQuestion2: ", countPoint)

    countPoint += getQuestion3(randomId, userID,rowQuestions3ForUsers,rowQuestions4ForUsers,rowQuestions5ForUsers,rowQuestions6ForUsers)
    
    return countPoint

def getQuestion3(randomId, userID,rowQuestions3ForUsers,rowQuestions4ForUsers,rowQuestions5ForUsers,rowQuestions6ForUsers):
    global rowQuestions3, void, photoGet

    countPoint = 0

    vk.messages.send( #Отправляем сообщение
                    user_id = userID,
                    random_id = randomId,
                    # attachment = 'photo-194390511_457239113',
                    message="""
Знаешь своего студенческого тьютора? Тот старшекурсник, который прикреплен к твоей группе. У каждой группы он свой. Дружи с ним. Давай начнем с ним общаться. Найди своего тьютора в вк. Напиши какое-нибудь сообщение и дождись ответа. Скрин вашей переписки закинь сюда, и задание будет выполнено.
                            """,
                    # keyboard = keyboard.get_keyboard()
		            )

    getMessege("", userID)
    time.sleep(0)

    messageID = vk.messages.getHistory(user_id = userID, count = 1)
    print(messageID['items'])
    messageID = messageID['items']
    messageID = messageID[0]
    messageID = messageID['attachments']
    messageID = messageID[0]
    messageID = messageID['photo']
    messageID = messageID['sizes']
    messageID = messageID.pop()
    messageID = messageID['url']
    print('history ', messageID )

    print("получение фото от 2 вопроса")
   

    sheet.update_cell(rowQuestions3ForUsers, 6, f"""=IMAGE("{str(messageID)}")""")
    # rowQuestions3 += 1
    void = 0
    photoGet = 0
    
    getQuestion4(randomId, userID,rowQuestions4ForUsers,rowQuestions5ForUsers,rowQuestions6ForUsers)

    return countPoint

def getQuestion4(randomId, userID,rowQuestions4ForUsers,rowQuestions5ForUsers,rowQuestions6ForUsers):
    global rowQuestions4
    
    countPoint = 0

    keyboard = keyboardCreater("30p", "27p", "20p", "У нас есть буфет?")

    vk.messages.send( #Отправляем сообщение
                    user_id = userID,
                    random_id = randomId,
                    #attachment = 'photo-194390511_457239038',
                    message="""
Молодец, не прошло и дня. Пора подкрепиться в студенческом буфете. Кстати, именно там ты справишься со следующим заданием. Узнай, сколько стоит лимонад в студенческом буфете:
                            """,
                    keyboard = keyboard.get_keyboard()
		            )

    otvetQvestions = getMessege("30p", userID)

    if otvetQvestions :
        countPoint += 1
        print("getQuestion4: ", countPoint)

        sheet.update_cell(rowQuestions4ForUsers, 7, "1")
        # rowQuestions4 += 1 
    else :
        print("getQuestion4: ", countPoint)
        sheet.update_cell(rowQuestions4ForUsers, 7, "0")
        # rowQuestions4 += 1 

    getQuestion5(randomId, userID,rowQuestions5ForUsers,rowQuestions6ForUsers)

def getQuestion5(randomId, userID,rowQuestions5ForUsers,rowQuestions6ForUsers):
    global rowQuestions5

    vk.messages.send( #Отправляем сообщение
                    user_id = userID,
                    random_id = randomId,
                    # attachment = 'photo-194390511_457239038',
                    message="""
Первокурсник, ты не устал? Еще немного. Это задание – вообще элементарное. Напиши чего ты ждешь от своей студенческой жизни? (Одним собщением)
                            """,
                    # keyboard = keyboard.get_keyboard()
		            )

    def getMessege1 (stringOtvet, user_id): # Получаем сообщение от конкретного пользователя
        for event in longpoll.listen(): # цикл для каждго ивента сервера
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.user_id == user_id: # ждать ответа от данного юзера 
                vk.messages.getConversations(offset = 0, count = 1)  
        
                if event.text == stringOtvet: # если событие текст и он равен сообщению которое отправил пользователь
                    return event.text

                return event.text

    otvetQvestions5 = getMessege1("", userID)

    sheet.update_cell(rowQuestions5ForUsers,8,otvetQvestions5)
    # rowQuestions5 += 1

    getQuestion6(randomId, userID,rowQuestions6ForUsers)

def getQuestion6(randomId, userID,rowQuestions6ForUsers):
    global rowQuestions6

    vk.messages.send( #Отправляем сообщение
                    user_id = userID,
                    random_id = randomId,
                    #attachment = 'photo-194390511_457239038',
                    message="""
Есть инстаграмм? Если нет - самое время попробовать завести. Сними в нем сторис, отметь @profkom_kgta, скрин пришли сюда!
                            """
		            )

    getMessege("", userID)
    time.sleep(0)

    messageID = vk.messages.getHistory(user_id = userID, count = 1)
    print(messageID['items'])
    messageID = messageID['items']
    messageID = messageID[0]
    messageID = messageID['attachments']
    messageID = messageID[0]
    messageID = messageID['photo']
    messageID = messageID['sizes']
    messageID = messageID.pop()
    messageID = messageID['url']

    print('history ', messageID )

    print("получение фото от 1 вопроса")
   

    sheet.update_cell(rowQuestions6ForUsers, 9, f"""=IMAGE("{str(messageID)}")""")
    # rowQuestions6 += 1

def newUser():
    print("Проверка подключения")

    for userId in usersId: # Перебираем список с пользователями 
        if event.user_id == userId:
            print("Старый пользователь...")
            return False 

    print("Новый пользователь...")

    return True

# %% [Run Server] 
# start = False
for event in longpoll.listen():
    
    print(event.type)
    
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        vk.messages.getConversations(offset = 0, count = 1)  
        if event.text == "2020":
            start = True
        
        # start = getMessege("2020", event.user_id)

        if start:
            whoUser = newUser()
        
            if whoUser:
                print("Новый пользователь")
                # usersId.append(event.user_id)
                usersId.append(event.user_id)
                Thread(target=getQuestion, args=(event.random_id, event.user_id)).start() # Запуск нового потока для нового пользвоателя
            else:
                print("Старый пользователь")


           
