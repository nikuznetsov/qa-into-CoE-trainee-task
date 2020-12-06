import json

def data_download():
  # Ôóíêöèÿ çàãðóçêè JSON ôàéëîâ
  with open('TestcaseStructure.json') as f:
    structure = json.load(f)
  with open('Values.json') as f:
    values = json.load(f)
  return structure, values

def check_in_values(dct, id, key):
  # Ôóíêöèÿ äëÿ ïàðñèíãà âåòêè values(key='title') 
  # è äëÿ ïîëó÷åíèÿ value íàïðÿìóþ èç Values.json(key='value')
  for i in range(len(dct)):
    if dct[i].get('id') == id:
      return dct[i].get(key)
  return ''

def check_in_params(dct, values):
  # Ôóíêöèÿ äëÿ ïàðñèíãà âåòêè params
  for i in range(len(dct)):
    if 'params' in dct[i].keys():
      dct[i]['params'] = parsing(dct[i].get('params')[0], values)
  return dct

def parsing(dct, values):
  # Ôóíêöèÿ äëÿ ïàðñèíãà JSON ôàéëà è çàïîëíåíèÿ value
  try:
    id = dct.get('id') # ïîóë÷àåì id ñëîâàðÿ
  except AttributeError:
    print('Ïåðåäàííûé îáúåêò íå èìååò àòðèáóòà get. Âîçìîæíî, ïðîáëåìà ñ òèïîì äàííûõ.')
  assert isinstance(id, int), print('Ïðîáëåìà ñ ýëåìåíòîì id. Âîçìîæíî, â ñëîâàðå íåò ýëåìåíòà id.')

  value = check_in_values(values, id, 'value') # ïîëó÷àåì value ïî id èç Values.json

  if 'values' in dct.keys(): # ïðîâåðÿåì, åñòü ëè â ñëîâàðå êëþ÷ values
    dct['value'] = check_in_values(dct.get('values'), value, 'title')
    dct['values'] = check_in_params(dct.get('values'), values)
  else:
    dct['value'] = value
  return dct

try:

  structure, values = data_download()

except:

  with open('error.json', 'w') as outfile:
      json.dump({'error': {"message": "Âõîäíûå ôàéëû íåêîððåêòíû"}}, outfile, ensure_ascii=False, indent=4)

else:

  structure, values = data_download()

  params = structure.get('params')
  assert isinstance(params, list), print('Íåâåðíûé òèï ïåðåìåííîé params (äîëæåí áûòü list). Âîçìîæíî, ïðîáëåìà ñî ñòðóêòóðîé ôàéëà.')
  
  values = values.get('values')
  assert isinstance(values, list), print('Íåâåðíûé òèï ïåðåìåííîé values (äîëæåí áûòü list). Âîçìîæíî, ïðîáëåìà ñî ñòðóêòóðîé ôàéëà.')

  for i in range(len(params)): # ïðîõîäèì ïî âñåì ýëåìåíòà ñïèñêà è ïàðñèì èõ
    params[i] = parsing(params[i], values)

  assert isinstance(params, list), print('Íåâåðíûé òèï ïåðåìåííîé params ïîñëå îáðàáîòêè (äîëæåí áûòü list).')

  with open('StructureWithValues.json', 'w') as outfile: # çàãðóæàåì îáðàáîòàííûå äàííûå â JSON
      json.dump({'params': params}, outfile, ensure_ascii=False, indent=2)
