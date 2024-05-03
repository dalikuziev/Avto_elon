import json
import requests

answer = input('Saytga kirasizmi?(yes/no): ').lower()
response_home = None

if answer == 'yes':
    url = 'https://car-shoping.onrender.com/'
    response_home = requests.get(url)
try:
    active_cars_url = response_home.json()['cars']
except:
    print('Saytga kirmadingiz')
else:
    answer_car = input('Mashina sotib olasizmi?(yes/no): ').lower()
    if answer_car == 'yes':
        response_cars = requests.get(active_cars_url)
        cars_list = response_cars.json()
        cars_amount = len(cars_list)
        if cars_amount > 0:
            print(f'Sotuvdagi jami mashinalar soni {cars_amount} ta bular:')
        else:
            print('Sotuvda mashina mavjud emas')
        num = cars_amount
        while num > 0:
            print(f'Mashina nomi: {cars_list[cars_amount - num]["model"]}, narxi: {cars_list[cars_amount - num]["price"]}, id raqami: {cars_list[cars_amount - num]["id"]}')
            num -= 1
        if cars_amount > 0:
            try:
                id_car = int(input('Sotib olmoqchi bo\'lgan mashinangizni idsini kiriting: '))
            except ValueError:
                print('idni xato kiritdingiz')
        for car in cars_list:
            if car['id'] == id_car:
                car_url = f'{active_cars_url}{id_car}/'
                requests.delete(car_url, headers={'Content-Type': 'application/json'})
                car_url = requests.get(car_url).json()
                print(f'{car_url["brand"]} brandining {car_url["model"]} modeli sotildi,\n'
                      f'qo\'shimcha ma\'lumotlar id raqam: {car_url["id"]}, narxi: {car_url["price"]} va yili: {car_url["year"]}')
                break
    else:
        print('Mashina kiriting!')
        username = input('Ismingiz: ')
        brand = input('Mashina brandi: ')
        model = input('Mashina modeli: ')
        year = input('Mashina yili: ')
        price = input('Mashina narxi: ')
        data = {
            'username': username,
            'brand': brand,
            'model': model,
            'year': year,
            'price': price,
            'image': None,
            'is_active': True
        }
        response_add_car = requests.post(active_cars_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
        if response_add_car.ok:
            print('Mashina muvaffaqqiyatli qo\'shildi')
        else:
            print('Sizning mashinangiz qo\'shilmadi')
