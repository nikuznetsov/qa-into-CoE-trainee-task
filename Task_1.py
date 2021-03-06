# -*- coding: utf-8 -*-

import json

def data_download():
  # Функция загрузки JSON файлов
  with open('TestcaseStructure.json') as f:
    structure = json.load(f)
  with open('Values.json') as f:
    values = json.load(f)
  return structure, values

def check_in_values(dct, id, key):
  # Функция для парсинга ветки values(key='title') 
  # и для получения value напрямую из Values.json(key='value')
  for i in range(len(dct)):
    if dct[i].get('id') == id:
      return dct[i].get(key)
  return ''

def check_in_params(dct, values):
  # Функция для парсинга ветки params
  for i in range(len(dct)):
    if 'params' in dct[i].keys():
      dct[i]['params'] = parsing(dct[i].get('params')[0], values)
  return dct

def parsing(dct, values):
  # Функция для парсинга JSON файла и заполнения value
  try:
    id = dct.get('id') # поулчаем id словаря
  except AttributeError:
    print('Переданный объект не имеет атрибута get. Возможно, проблема с типом данных.')
  assert isinstance(id, int), print('Проблема с элементом id. Возможно, в словаре нет элемента id.')

  value = check_in_values(values, id, 'value') # получаем value по id из Values.json

  if 'values' in dct.keys(): # проверяем, есть ли в словаре ключ values
    dct['value'] = check_in_values(dct.get('values'), value, 'title')
    dct['values'] = check_in_params(dct.get('values'), values)
  else:
    dct['value'] = value
  return dct

try:

  structure, values = data_download()

except:

  with open('error.json', 'w') as outfile:
      json.dump({'error': {"message": "Входные файлы некорректны"}}, outfile, ensure_ascii=False, indent=4)

else:

  structure, values = data_download()

  params = structure.get('params')
  assert isinstance(params, list), print('Неверный тип переменной params (должен быть list). Возможно, проблема со структурой файла.')
  
  values = values.get('values')
  assert isinstance(values, list), print('Неверный тип переменной values (должен быть list). Возможно, проблема со структурой файла.')

  for i in range(len(params)): # проходим по всем элемента списка и парсим их
    params[i] = parsing(params[i], values)

  assert isinstance(params, list), print('Неверный тип переменной params после обработки (должен быть list).')

  with open('StructureWithValues.json', 'w') as outfile: # загружаем обработанные данные в JSON
      json.dump({'params': params}, outfile, ensure_ascii=False, indent=2)
