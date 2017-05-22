__author__ = "Patrick Huston"
__version__ = "0.1"
__email__ = "patrick@olin.edu"

from contextlib import contextmanager
from mpd import MPDClient

class MPDPlaybackController:
	"""
	Does all the playback control things
	"""

	def __init__(self):
		self.client = MPDClient() 
		self.client.timeout = 20
		self.client.idletimeout = None

		self.playback_action_mapping = {
			"000000":self.play,
			"000001":self.pause,
			"000002":self.next_song,
			"000003":self.previous_song,
			"000004":self.increase_vol,
			"000005":self.decrease_vol,
			"000006":self.stop_playback,
			"000007":self.clear_playlist,
			"000008":self.shuffle_playlist
		}

	@contextmanager
	def connection(self):
		try:
			self.client.connect('localhost', 6600)
			yield
		finally:
			self.client.close()
			self.client.disconnect()


	def handle_action(self, command_code):
		""" 
		Takes in command passed from barcode, and either modifies playback settings
		or plays/queues the music at the URI that maps to the barcode code
		"""
		if (command_code[0] == "0"):
			self.playback_action_mapping[command_code[1:]]()
		elif (command_code[0] == "1"):
			self.handle_playlist_queue(command_code[0])

	def handle_playlist_queue(self, command_code):
		""" Based on state, either plays or queues music """
		with self.connection():
			try:
				self.client.clear()
				self.client.stop()
				self.client.add("spotify:track:2Gy7qnDwt8Z3MNxqat4CsK")
			except:
				pass


	def play(self):
		""" Invokes 'PLAY' function of MPD client """
		with self.connection():
			try:
				self.client.pause(0)
			except:
				pass
				# TODO: Except an actual error 

	def pause(self):
		""" Invokes 'PAUSE' function of MPD client """ 
		with self.connection():
			try:
				self.client.pause(1)
			except:
				pass
				# TODO: Except an actual error 

	def next_song(self):
		""" Invokes 'NEXT' function of MPD client """ 
		with self.connection():
			try:
				self.client.next()
			except:
				pass
				# TODO: Except an actual error 

	def previous_song(self):
		""" Invokes 'PREVIOUS' function of MPD client """ 
		with self.connection():
			try:
				self.client.previous()
			except:
				pass
				# TODO: Except an actual error 

	def increase_vol(self):
		""" Increases volume by 10% of MPD client """ 
		with self.connection():
			try:
				self.client.setvol(self.client.status().volume + 10)
			except:
				pass
				# TODO: Except an actual error 

	def decrease_vol(self):
		""" Decrease volume by 10% of MPD client """
		with self.connection():
			try:
				self.client.setvol(self.client.status().volume - 10)
			except:
				pass
				# TODO: Except an actual error 
		

	def stop_playback(self):
		""" Invokes 'STOP' function of MPD client """
		with self.connection():
			try:
				self.client.stop()
			except:
				pass
				# TODO: Except an actual error 

	def clear_playlist(self):
		""" Invokes 'CLEAR' function of MPD client """
		with self.connection():
			try:
				self.client.clear()
			except:
				pass
				# TODO: Except an actual error 

	def shuffle_playlist(self):
		""" Invokes 'SHUFFLE' function of MPD client """
		with self.connection():
			try:
				self.client.shuffle()
			except:
				pass
				# TODO: Except an actual error 



