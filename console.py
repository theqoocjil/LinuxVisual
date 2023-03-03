import subprocess
import os
from time import sleep


db_info = {
  'mongodb':'MongoDB Подключение из командной строки: $ mongo',
  'mssql-server':
  """QL Server 2019 Developer
  Login: SA
  Password: sqlServer_2019
  Databases
    AdventureWorks2019
    AdventureWorksDW2019
  Инструменты командной строки sqlcmd, bcp
  
  Подключение из командной строки:
    $ sqlcmd -U SA
    <ввести пароль>'
  """,
  'postgresql':"""
  Postgresql
  пользователь связан с учетной записью root
  Имя пользователя: postgre
  Database
    demo  (из скрипта demo_medium.sql)
  """
  }

def progress_bar():
  for i in range(50):
    print('~'* i, end='\r')
    sleep(0.01)
  print("\nВыполнено!")
  sleep(0.5)

def status(index_db):
  try:
    status = str(subprocess.check_output(['systemctl', 'status', index_db]))
    status = status[status.find('Active: ')+8]
    return status
  except(subprocess.CalledProcessError):
  	return 'i'
  
  
def auto_start(index_db):
  try:
    auto_start = str(subprocess.check_output(['systemctl', 'status', index_db]))
    auto_start = auto_start[auto_start.find('loaded'):]
    auto_start = auto_start[auto_start.find(';')+2]
    return auto_start
  except(subprocess.CalledProcessError):
  	return 'i'
  
def submenu_way(index):
  on = True
  os.system('clear')
  print(shapka(status('mongodb'),status('mssql-server'), status('postgresql'), auto_start('mongodb'), auto_start('postgresql'), auto_start('mssql-server')) + menu(f'{index}'))
  while on:
    value = input()
    if value == ('1'):
      subprocess.call(['systemctl', 'restart', f'{index}'])
      progress_bar()
      on = False
      submenu_way(index)
    if value == ('2'):
      if auto_start(index) == 'd':
        subprocess.call(['systemctl', 'enable', f'{index}'])
        progress_bar()
        on = False
        submenu_way(index)
      else:
        subprocess.call(['systemctl', 'disable', f'{index}'])
        progress_bar()
    if value == ('3'):
      subprocess.call(['systemctl', 'stop', f'{index}'])
      progress_bar()
      on = False
      submenu_way(index)
    if value == ('4'):
      print(db_info[index])
      print('-------------------------------------------------')
      print(f"Выберите действие для {index} :")
    if value == ('5'):
      os.system('clear')
      print(shapka(status('mongodb'),status('mssql-server'),status('postgresql'), auto_start('mongodb'), auto_start('postgresql'), auto_start('mssql-server')) + menu('main'))
      break

      
def menu(index):
    if index=="main":
      menu = (
          """
          Выберите СУБД: 
          """
      )
      return menu
    else:
      mode = 'Убрать'
      if auto_start(index) != 'e':
        mode = 'Добавить'
      menu = (
          f"""
          Выберите действие для {index} :

          1. (Пере)запуск сервера {index}
          2. {mode} автозапуск
          3. Остановить {index}
          4. Информация
          5. Вернуться в главное меню
          """
      )
      return menu

def shapka(mongo_status, mssql_status, postgresql_status,auto_mongo, auto_post, auto_mmsql):
  host_ip = str(subprocess.check_output(['ip','a']))
  host_ip_host= host_ip[host_ip.find('3: '):]
  host_ip_host = host_ip_host[host_ip_host.find('inet ')+ 5:]
  host_ip_host = host_ip_host[:host_ip_host.find('/')]
  host_ip_vm= host_ip[host_ip.find('2: '):]
  host_ip_vm = host_ip_vm[host_ip_vm.find('inet ')+5:]
  host_ip_vm = host_ip_vm[:host_ip_vm.find('/')]
  shapka = (
      f"""
      ************************************************************
      ***************** __  __  ____   _   _ *********************
      *****************|  \/  |/ ___| | | | |*********************
      *****************| |\/| |\___ \ | | | |*********************
      *****************| |  | | ___) || |_| |*********************
      *****************|_|  |_||____/  \___/ *********************
      *****************                      *********************
      ************************************************************
      ------------------------------------------------------------
      *********************МЕНЕДЖЕР СУБД**************************
                          IP_HOST: {host_ip_host} 
                          IP_VM: {host_ip_vm}
      ------------------------------------------------------------
            |      СУБД      ||   Статус   ||  авто старт  |
            |----------------||------------||--------------|
            |1. MS SQL Server||      {mssql_status}     ||      {auto_mmsql}       |
            |----------------||------------||--------------|
            |2.   MongoDB    ||      {mongo_status}     ||      {auto_mongo}       |
            |----------------||------------||--------------|
            |3.  PostgresSQL ||      {postgresql_status}     ||      {auto_post}       |
      -------------------------------------------------------------
                          © prod. by theqoocjil
      """
  )
  return shapka

def main():
    os.system('clear')
    print(shapka(status('mongodb'),status('mssql-server'),status('postgresql'), auto_start('mongodb'), auto_start('postgresql'), auto_start('mssql-server')) + menu('main'))
    while True:
      value = input()
      if value == ('1'):
        submenu_way('mssql-server')
      elif value == ('2'):
        submenu_way('mongodb')
      elif value == ('3'):
        submenu_way('postgresql')




if __name__ == "__main__":
  try:
    main()  
  except KeyboardInterrupt:
    pass