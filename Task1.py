import json

def data_download():
  # ������� �������� JSON ������
  with open('TestcaseStructure.json') as f:
    structure = json.load(f)
  with open('Values.json') as f:
    values = json.load(f)
  return structure, values

def check_in_values(dct, id, key):
  # ������� ��� �������� ����� values(key='title') 
  # � ��� ��������� value �������� �� Values.json(key='value')
  for i in range(len(dct)):
    if dct[i].get('id') == id:
      return dct[i].get(key)
  return ''

def check_in_params(dct, values):
  # ������� ��� �������� ����� params
  for i in range(len(dct)):
    if 'params' in dct[i].keys():
      dct[i]['params'] = parsing(dct[i].get('params')[0], values)
  return dct

def parsing(dct, values):
  # ������� ��� �������� JSON ����� � ���������� value
  try:
    id = dct.get('id') # �������� id �������
  except AttributeError:
    print('���������� ������ �� ����� �������� get. ��������, �������� � ����� ������.')
  assert isinstance(id, int), print('�������� � ��������� id. ��������, � ������� ��� �������� id.')

  value = check_in_values(values, id, 'value') # �������� value �� id �� Values.json

  if 'values' in dct.keys(): # ���������, ���� �� � ������� ���� values
    dct['value'] = check_in_values(dct.get('values'), value, 'title')
    dct['values'] = check_in_params(dct.get('values'), values)
  else:
    dct['value'] = value
  return dct

try:

  structure, values = data_download()

except:

  with open('error.json', 'w') as outfile:
      json.dump({'error': {"message": "������� ����� �����������"}}, outfile, ensure_ascii=False, indent=4)

else:

  structure, values = data_download()

  params = structure.get('params')
  assert isinstance(params, list), print('�������� ��� ���������� params (������ ���� list). ��������, �������� �� ���������� �����.')
  
  values = values.get('values')
  assert isinstance(values, list), print('�������� ��� ���������� values (������ ���� list). ��������, �������� �� ���������� �����.')

  for i in range(len(params)): # �������� �� ���� �������� ������ � ������ ��
    params[i] = parsing(params[i], values)

  assert isinstance(params, list), print('�������� ��� ���������� params ����� ��������� (������ ���� list).')

  with open('StructureWithValues.json', 'w') as outfile: # ��������� ������������ ������ � JSON
      json.dump({'params': params}, outfile, ensure_ascii=False, indent=2)