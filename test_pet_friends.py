from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_invalid_key(email=valid_email, password='12345'):
    """Провряем что запрос API ключа для неправильного пароля не возвращает статус 200"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученный результат с нашими ожиданиями
    assert status != 200
    print(status)

def test_get_api_key_for_invalid_user(email='1111111111@mail.ru', password=valid_password):
    """Провряем что запрос API ключа для неправильного логина не возвращает статус 200"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученный результат с нашими ожиданиями
    assert status != 200
    print(status)

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Провряем что запрос API ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученный результат с нашими ожиданиями
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этот ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0



def test_add_new_pet_with_valid_data(name='Дейма', animal_type='Sibirian',
                                     age='1', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_add_new_pet_with_invalid_data_name(name='', animal_type='Sibirian',
                                     age='1', pet_photo='images/cat1.jpg'):
    """Проверяем что нельзя добавить питомца с некорректными данными - не указав данные в обязательном поле 'имя питомца' """

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status != 200
    print(status)

def test_add_new_pet_with_invalid_data_age(name='Бобик', animal_type='дворняга',
                                     age='', pet_photo='images/cat1.jpg'):
    """Проверяем что нельзя добавить питомца с некорректными данными - не указав данные в обязательном поле 'возраст' """

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status != 200
    print(status)

def test_add_new_pet_with_invalid_data_animal_type(name='Торик', animal_type='',
                                     age='1', pet_photo='images/cat1.jpg'):
    """Проверяем что нельзя добавить питомца с некорректными данными - не указав данные в обязательном поле 'порода' """

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status != 200
    print(status)

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_unsuccessful_update_self_pet_info_without_name(name='', animal_type='Котик', age=4):
    """Проверяем невозможность обновления информации о питомце c некорректными данными -
    невозможность передать пустое поле 'имя питомца' """

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status != 200
        print(status)
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_unsuccessful_update_self_pet_info_without_age(name='Birka', animal_type='Котик', age=''):
    """Проверяем невозможность обновления информации о питомце c некорректными данными -
    невозможность передать пустое поле 'возраст питомца' """

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status != 200
        print(status)
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_add_new_pet_without_photo_with_valid_data(name='Моби-Дик', animal_type='Котэ',
                                     age='2'):
    """Проверяем что можно добавить питомца без фото с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

def test_add_new_pet_without_photo_with_invalid_data_name(name='', animal_type='Котэ',
                                     age='2'):
    """Проверяем что нельзя добавить питомца без фото с некорректными данными -
    невозможность передать пустое поле 'имя питомца' """

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status != 200
    print(status)

def test_add_new_pet_without_photo_with_invalid_data_age(name='Kesha', animal_type='Котэ',
                                     age=''):
    """Проверяем что нельзя добавить питомца без фото с некорректными данными -
        невозможность передать пустое поле 'возраст' """

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status != 200
    print(status)

def test_add_new_pet_without_photo_with_invalid_data_animal_type(name='Kesha', animal_type='',
                                     age='3'):
    """Проверяем что нельзя добавить питомца без фото с некорректными данными -
        невозможность передать пустое поле 'порода' """

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status != 200
    print(status)

def test_add_pet_photo_with_valid_data(pet_photo='images/123.jpg'):
    """Проверяем что можно добавить фото питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Добавляем фото
    status, result = pf.add_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['pet_photo'] != 0

def test_get_my_pets_with_valid_key(filter='my_pets'):
    """ Проверяем что запрос моих питомцев, при наличии моих питомцев на сайте, возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этот ключ
    запрашиваем список моих питомцев и проверяем что список не пустой.
    Значение параметра filter - 'my_pets' """

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем нового питомца, для уверенности, что список питомцев на сайте не пустой.
    pf.add_new_pet(auth_key, "Бэримор", "кот", "2", "images/cat1.jpg")

    # Получаем список питомцев
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Проверяем ожидаемый результат
    assert status == 200
    assert len(result['pets']) > 0

# Как уже говорилось ранее, вы можете протестировать сервис негативными тестами,
# и он должен отвечать на это ошибкой, код которой возвращается в response.status_code.
# В assert мы можем проверить, что полученный код соответствует нашим ожиданиям.

# Но не всегда стоит верить статусу 200, потому что сервер может получить запрос и корректно его распознать,
# но некорректно провести его дальнейшую обработку,
# поэтому обязательно нужно проверять результат в response.text или в response.json().
# Либо если мы ожидаем, что вернётся код, отличный от 200, то необходимо также проверить текст ошибки в о
