__author__ = "Patrick Huston"
__version__ = "0.1"
__email__ = "patrick@olin.edu"

from MPDPlaybackController import MPDPlaybackController

NICE = "spotify:track:2Gy7qnDwt8Z3MNxqat4CsK"
GETON = "spotify:track:39l1UORIhuHvUWfxG53tRZ"


if __name__ == '__main__': 

	playback_controller = MPDPlaybackController()

	controller_mapping = {
		"0":playback_controller
	}


	while True:
		command = str(raw_input("SCAN >> "))
		controller_mapping[command[0]].handle_action(command[1:])
		