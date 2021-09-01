from os import remove
import pyautogui as pygu
from time import sleep
import pyperclip
import json

# Anotar pedidos
## verificar se pedido já está anotado
# Preparar pedidos
# Verificar Finalizados, entrega
# Remover pedido da lista

ingredientes = [
    {
        "id": 1,
        "nome": "Café",
        "img": "assets/ing_cafe.JPG"
    },
    {
        "id": 2,
        "nome": "Açucar",
        "img": "assets/ing_acucar.JPG"
    },
    {
        "id": 3,
        "nome": "Chá",
        "img": "assets/ing_cha.JPG"
    }
]

cardapio = [
    {
        "id": 1,
        "nome": 'Café Simples',
        "img": 'assets/cafe_simples.JPG',
        "ingredientes": [1]
    },
    {
        "id": 2,
        "nome": 'Café Doce',
        "img": 'assets/cafe_doce.JPG',
        "ingredientes": [1,2]
    },
    {
        "id": 3,
        "nome": 'Chá Doce',
        "img": 'assets/cha_doce.JPG',
        "ingredientes": [3,2]
    },
    {
        "id": 4,
        "nome": 'Chá Duplo',
        "img": 'assets/cha_duplo.JPG',
        "ingredientes": [3,3]
    },
    {
        "id": 5,
        "nome": 'Café Duplo',
        "img": 'assets/cafe_duplo.JPG',
        "ingredientes": [1,1]
    }
]

cafeteiras = [
    {
        "quantidade": 1,
        "img": "assets/cafeteira.JPG"
    }
]

pedidos = []
preparos = 0


def getQuantidadeCafeteira():
    global cafeteiras

    for c in cafeteiras:
        pos = pygu.locateOnScreen(c['img'], confidence=.8)
        if (pos):
            return c['quantidade']
    return 0

def verificarPedido(pedido, pedidos):
    for p in pedidos:
        if pedido == p:
            return 1
    return 0
        

def anotarPedidos(pedidos):
    print("Anotar Pedidos")

    for c in cardapio:
        pos = pygu.locateOnScreen(c['img'], confidence=.8)
        if (pos):
            print('Pedido encontrado: ' + str(c['nome']))
            pedido = json.dumps({"id":c['id'], "x":str(pos[0]), "y": str(pos[1])})

            if(verificarPedido(pedido, pedidos) == False):
                print("Adicionando pedido a lista")
                pedidos.append(pedido)
            
def getIngrediente(id, ingredientes):
    for i in ingredientes:
        if i['id'] == id:
            return i
    return 0

def getItemCardapio(id, cardapio):
    for c in cardapio:
        if c['id'] == id:
            return c
    return 0

def prepararPedidos(pedidos, cardapio, ingredientes):
    global preparos

    print("Preparando Pedidos")

    for p in pedidos:
        
        qtdCafeteiras = getQuantidadeCafeteira()
        if (preparos >= qtdCafeteiras): return 0
        
        pedido = json.loads(p)
        item = getItemCardapio(pedido['id'], cardapio)
        if (item == False): return 0

        for i in item['ingredientes']:
            ing = getIngrediente(i, ingredientes)
            if (ing == False): return 0

            pos = pygu.locateOnScreen(ing['img'], confidence=.8)
            if (pos):
                print("Adicionando ingrediente: " + ing['nome'])

                pygu.moveTo(pos[0]+(pos[2]/2), pos[1]+(pos[3]/2), duration=0.2)
                sleep(1)
                pygu.click()
                
        pos_preparo = pygu.locateOnScreen("assets/preparo.JPG", confidence=.8)
        if(pos_preparo):

            pygu.moveTo(pos_preparo[0]+(pos_preparo[2]/2), pos_preparo[1]+(pos_preparo[3]/2), duration=0.2)
            sleep(1)
            pygu.click()
            preparos+=1


def entregarFinalizados(pedidos):
    global preparos
    print("Entregando finalizados")

    pos = pygu.locateOnScreen("assets/pronto.JPG", confidence=.8)
    if(pos):

        pygu.moveTo(pos[0]+(pos[2]/2), pos[1]+(pos[3]/2), duration=0.2)
        sleep(1)
        pygu.click()

        print(pedidos)

        pedidos.pop(0)
        preparos-=1

        print(pedidos)

        sleep(1)
    

def removerPedido():
    print("Removendo Pedido")

while 1:
    anotarPedidos(pedidos)
    prepararPedidos(pedidos, cardapio, ingredientes)
    entregarFinalizados(pedidos)

    print(pedidos)

    sleep(5)