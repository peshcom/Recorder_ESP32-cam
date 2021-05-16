#! /usr/bin/env python3

import imageio
import requests
import os
import datetime


class Writer():
	"""
	Запись видео по кадрам

	url = URL с которого брать картинку

	chunks - количество кардров в одном видео
	При fps==20 и chunks == 6000 получается 5 минут записи
	После исчерпания chunks, создается новое видео с новой датой
	"""
	writer = None

	def __init__(self, url = 'http://192.168.4.1/capture', fps = 20, chunks=6000, folder='videos'):
		self.url = url
		self.fps = fps
		self.chunks = chunks
		self.folder = folder

		self.create_writer()

	def close_writer(self):
		self.writer.close()

	def create_writer(self):
		# создаем новый
		self.video_name = os.path.join(
			self.folder,
			datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + '.mp4'
		)
		self.writer = imageio.get_writer(
			self.video_name,
			fps = self.fps,
		)

	def get_image(self):
		return requests.get(self.url).content

	def processing(self):
		number_frames = 0
		while 1:
			number_frames += 1

			# выводим немного инфы, показывая что процесс идет
			if number_frames % 100 == 0:
				print(f"Video: {self.video_name} capture: {number_frames} frames")

			# если достигли предела, создаем новое видео
			if number_frames >= self.chunks:
				self.close_writer()
				self.create_writer()
				number_frames = 0

			# Записываем в видео
			self.writer.append_data(
				imageio.imread(self.get_image())
			)
def main():
	a = Writer()
	a.processing()

if __name__ == '__main__':
	main()