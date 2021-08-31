from os import remove
import pyautogui as pygu
from time import sleep
import pyperclip
import webbrowser
from datetime import datetime
import httpx
import json

print('Inicinado Food Tycoon Bot')

machines = [
    {
        "amount": 2,
        "img": "img/two_coffee_machine.JPG"
    }
]
ingredients = [
    {
        "id": 1,
        "name": "Coffe",
        "img": "img/ing_coffee.JPG"
    },
    {
        "id": 2,
        "name": "Sugar",
        "img": "img/ing_sugar.JPG"
    },
    {
        "id": 3,
        "name": "Tea",
        "img": "img/ing_tea.JPG"
    }
]
menu = [
    {
        "id": 1,
        "name": "Simple Coffee",
        "img": "img/simple_coffee.JPG",
        "ingredients": [1]
    },
    {
        "id": 2,
        "name": "Sweet Coffee",
        "img": "img/sweet_coffee.JPG",
        "ingredients": [1, 2]
    },
    {
        "id": 3,
        "name": "Simple Tea",
        "img": "img/simple_tea.JPG",
        "ingredients": [3]
    },
    {
        "id": 4,
        "name": "Sweet Tea",
        "img": "img/sweet_tea.JPG",
        "ingredients": [2, 3]
    },
    {
        "id": 5,
        "name": "Big Tea",
        "img": "img/big_tea.JPG",
        "ingredients": [3, 3]
    },
    {
        "id": 6,
        "name": "Big Coffee",
        "img": "img/big_coffee.JPG",
        "ingredients": [1, 1]
    }
]

orders = []

def closeConversation():
    pos = pygu.locateOnScreen("img/conversation.JPG", confidence=.8)
    if (pos):
        print('Fechando conversação')
        pygu.moveTo(pos[0]+(pos[2]/2), pos[1]+(pos[3])+50, duration=0.2)
        sleep(.5)
        pygu.click()

def closeModal():
    pos = pygu.locateOnScreen("img/modal.JPG", confidence=.8)
    if (pos):
        print('Fechando modal')
        pygu.moveTo(pos[0]+(pos[2]/2), pos[1]+(pos[3]/2), duration=0.2)
        sleep(.5)
        pygu.click()

def goMap():
    pos = pygu.locateOnScreen("img/map.JPG", confidence=.8)
    if (pos):
        print('Voltando para o Mapa')
        pygu.moveTo(pos[0]+(pos[2]/2), pos[1]+(pos[3]/2), duration=0.2)
        sleep(.5)
        pygu.click()

def newMachine():
    pos = pygu.locateOnScreen("img/new_machine.JPG", confidence=.8)
    if (pos):
        print('Nova Máquina')
        pygu.moveTo(pos[0]+(pos[2]/2), pos[1]+(pos[3]/2), duration=0.2)
        sleep(.5)
        pygu.click()

def enterStage():
    pos = pygu.locateOnScreen("img/stage.JPG", confidence=.8)
    if (pos):
        print('Entrando na fase')
        pygu.moveTo(pos[0]+(pos[2]/2), pos[1]+(pos[3]/2), duration=0.2)
        sleep(.5)
        pygu.click()
        sleep(.5)

        pos_play = pygu.locateOnScreen("img/play_stage.JPG", confidence=.8)
        if(pos_play):
            print("Iniciando a fase")
            pygu.moveTo(pos_play[0]+(pos_play[2]/2), pos_play[1]+(pos_play[3]/2), duration=0.2)
            sleep(.5)
            pygu.click()
            sleep(.5)

        return 1
    else:
        return 0

def getAmountMachine():
    for m in machines:
        pos = pygu.locateOnScreen(m['img'], confidence=.8)
        if (pos):
            print(m)
            return m['amount']
    return 1

def done():
    global orders

    print('done')
    print(orders)

    pos_done = pygu.locateOnScreen("img/done.JPG", confidence=.8)
    while pos_done:
        print("Entregando o pedido")
        pygu.moveTo(pos_done[0]+(pos_done[2]/2), pos_done[1]+(pos_done[3]/2), duration=0.2)
        sleep(.5)
        pygu.click()
        orders.remove(orders[0])
        print(len(orders))
        sleep(.5)
        pos_done = pygu.locateOnScreen("img/done.JPG", confidence=.8)

def verifyOrder(pos):
    global orders
    for o in orders:
        if str(o) == str(pos):
            return 1
    return 0            


def takeOrder ():
    global orders

    # varrendo menu, procurando por pedidos
    for m in menu:
        pos = pygu.locateOnScreen(m['img'], confidence=.8)
        if (pos):

            # verificando se o pedido já está na lista
            if (verifyOrder(pos)): return 0

            orders.append(str(pos))

def getOrder (amount):
    global orders

    if len(orders)>=amount:
        return 0

    count = 0
    for m in menu:
        pos = pygu.locateOnScreen(m['img'], confidence=.8)
        if (pos):

            if(verifyOrder(m['id']) == False):

                orders.append(str(pos))

                # print(orders)
            
                print("Order " + str(m['name']))
                pygu.moveTo(pos[0]+(pos[2]/2), pos[1]+(pos[3]/2), duration=0.2)
                sleep(.5)

                for i in m['ingredients']:
                    # usando lambda pra manipular a interação
                    ing = list(filter(lambda x: x['id']==i, ingredients))
                    # print(ing)

                    pos_ing = pygu.locateOnScreen(ing[0]['img'], confidence=.8)
                    if (pos_ing):
                        print('Adicionando ingrediente ' + str(ing[0]['name']))
                        # centralizando o ponteiro no centro do item
                        pygu.moveTo(pos_ing[0]+(pos_ing[2]/2), pos_ing[1]+(pos_ing[3]/2), duration=0.2)
                        sleep(.3)
                        pygu.click()
                        pygu.moveTo(pos_ing[0], pos_ing[1]-20, duration=0.2)
                
                pos_start = pygu.locateOnScreen("img/start.JPG", confidence=.8)
                if (pos_start):
                    print("Iniciando Preparo")
                    pygu.moveTo(pos_start[0]+(pos_start[2]/2), pos_start[1]+(pos_start[3]/2), duration=0.2)
                    sleep(.3)
                    pygu.click()
                
                count+=1
                if (count>=amount):
                    return 1
                    
                    # sleep(5)
                    # pos_done = pygu.locateOnScreen("img/done.JPG", confidence=.8)
                    # if (pos_done):
                    #     print("Entregando o pedido")
                    #     pygu.moveTo(pos_done[0]+(pos_done[2]/2), pos_done[1]+(pos_done[3]/2), duration=0.5)
                    #     sleep(1)
                    #     pygu.click()

def exitStage():
    pos = pygu.locateOnScreen("img/continue_stage.JPG", confidence=.8)
    if (pos):
        print("Concluindo fase")
        pygu.moveTo(pos[0]+(pos[2]/2), pos[1]+(pos[3]/2), duration=0.2)
        sleep(.5)
        pygu.click()

def newCharacter():
    pos = pygu.locateOnScreen("img/continue_character.JPG", confidence=.8)
    if (pos):
        print("Novo personagem")
        pygu.moveTo(pos[0]+(pos[2]/2), pos[1]+(pos[3]/2), duration=0.2)
        sleep(.5)
        pygu.click()

def stock():
    pos = pygu.locateOnScreen("img/stock.JPG", confidence=.8)
    if (pos):
        print("Novo estoque")
        pygu.moveTo(pos[0]+(pos[2]/2), pos[1]+(pos[3]/2), duration=0.5)
        sleep(1)
        pygu.click()
        pos_pay = pygu.locateOnScreen("img/pay_coin.JPG", confidence=.8)
        if (pos_pay):
            print("Comprando")
            pygu.moveTo(pos_pay[0]+(pos_pay[2]/2), pos_pay[1]+(pos_pay[3]/2), duration=0.2)
            sleep(.5)
            pygu.click()

while 1:
    enterStage()
    # pegando a quantidade de máquinas
    amount = getAmountMachine()
    getOrder(amount)
    done()
    exitStage()
    newCharacter()
    # stock()
    # closeConversation()
    # closeModal()
    # goMap()
    # newMachine()

    # sleep(.5)