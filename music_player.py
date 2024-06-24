import os
import random
import pygame
import time


class MusicPlayer:
    def __init__(self, music_dir='music'):
        self.music_dir = music_dir
        self.songs = [f for f in os.listdir(music_dir) if f.endswith('.mp3')]
        random.shuffle(self.songs)
        self.current_song_index = 0
        self.paused = False

        pygame.init()
        pygame.mixer.init()

    def play_current_song(self):
        pygame.mixer.music.load(os.path.join(self.music_dir, self.songs[self.current_song_index]))
        pygame.mixer.music.play()

    def next_song(self):
        self.current_song_index = (self.current_song_index + 1) % len(self.songs)
        self.play_current_song()

    def prev_song(self):
        self.current_song_index = (self.current_song_index - 1) % len(self.songs)
        self.play_current_song()

    def pause(self):
        pygame.mixer.music.pause()
        self.paused = True

    def unpause(self):
        pygame.mixer.music.unpause()
        self.paused = False

    def run(self):
        self.play_current_song()

        while True:
            if not self.paused and not pygame.mixer.music.get_busy():
                self.next_song()

            if input_ready():
                command = input("Enter command (next/prev/pause/unpause/quit): ").lower()

                if command == 'next':
                    self.next_song()
                elif command == 'prev':
                    self.prev_song()
                elif command == 'pause':
                    self.pause()
                elif command == 'unpause':
                    self.unpause()
                elif command == 'quit':
                    break
                else:
                    print("Invalid command. Please try again.")

            time.sleep(0.1)  # Short sleep to prevent high CPU usage

        pygame.quit()


def input_ready():
    import select
    import sys
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])


if __name__ == "__main__":
    player = MusicPlayer()
    player.run()