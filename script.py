#!/usr/bin/env python3

# ===== IMPORTS ===== #

import psycopg2
import datetime
import time
import random
import json
import sys
from pyrogram import Client


# ===== GENERAL ===== #

# Читаем настройки скрипта
# with open("/script/src/settings.json", "r", encoding="utf-8") as fj:
with open("settings.json", "r", encoding="utf-8") as fj:
	settings = json.load(fj)

# Читаем текст рассылки
# with open("../res/text.txt") as file:
with open("res/text.txt") as file:
	text_message = file.read()

# Счетчик для подсчета кол-ва отправленных сообщений
counters = {
	"counter_message": 0
}


app = Client("main")

# Подключение к Postgres
try:
	conn = psycopg2.connect(
		database = "tg_users",
		user = "postgres",
		password ="123456",
		port = "25432",
		host = "localhost"
	)
	print("[INFO] Подключение с БД установлено")

	cur = conn.cursor()
	conn.commit()

except:
	print("[INFO] Нет соединения с БД")

# Главная функция рассылки
def sender(user):

	# Отправка сообщений взависимости от дневного лимита на каждый аккаунт
	for i in range(settings["daily_limit"]):

		if counters["counter_message"] == settings["mailing_speed"]:
			break

		app.send_message(user, text_message)

		counters["counter_message"] += 1
		
		# Настройка вывода информации о количестве сообщений при каждой итерации цикла
		if settings["stop_counter"] == False:
			print("Общее кол-во сообщений: ", counters["counter_message"])
		else:
			pass

		# Настройка генератора рандомного интервала
		if settings["random_interval_modes"] == True:

			# Извлекаем из списка с заданным промежутком времени начальную и конечную секунды
			lst_int = settings["random_interval"]

			random_interval = random.randint(lst_int[0], lst_int[1])
			time.sleep(random_interval)
			print("Интервал для", counters["counter_message"], "сообщения равен:", random_interval, "сек")

		else:
			time.sleep(settings["interval"])

with app:

	# Запрос к Postgres (1): узнаем общее количество записей в БД
	try:
		query_n1 = "SELECT COUNT(*) FROM users"
		cur.execute(query_n1)

	except:
		print("[INFO] Не удалось узнать кол-во записей в БД")

	# Получаем кортеж
	var_data_bases = cur.fetchall()
	# Кортеж переводим в список
	tur_db = var_data_bases[0]
	# Элемент списка переводим в int
	number_of_users = int(tur_db[0])

	print("[INFO] Кол-во записей в БД:", number_of_users)
	conn.commit()

	# Запрос к Postgres (2): Извлекаем самих пользователей
	try:
		query_n2 = "SELECT nickname FROM users"
		cur.execute(query_n2)

	except:
		print("[INFO] Контактные данные не были извлечены")


	# Цикл, главным условием которого является общее кол-во сообщений и не превышает ли оно допустимое значение\
	while counters["counter_message"] < settings["mailing_speed"]:

		# Пробегаем по БД построчно
		for i in range(number_of_users):

			# Достаём пользователя из БД
			user = cur.fetchone()
			conn.commit()
			
			# Цикл рассылки для каждого отдельного пользователя
			for user in user:
				sender(user)
	

	print("Рассылка завершена. Всего сообщений: ", counters["counter_message"])
	conn.close()
