import os
from csv import DictReader
import csv

tag_sound_associations = {}

def get_all_available_files(path):
    mp3_files = []
    for files in os.listdir(path):
        if files.endswith(".mp3"):
            mp3_files.append(files)

    return mp3_files

def read_tag_characters_into_list():
    with open("tag_characters.csv", 'r') as f:
        dict_reader = DictReader(f)
        list_of_dict = list(dict_reader)
    
    return list_of_dict

if __name__ == '__main__':
    with open("sound_associations.csv", "a", newline='') as sound_file:
            sound_writer = csv.writer(sound_file, delimiter=',')
            sound_writer.writerow(['Tag', 'Sound', 'Reader'])
    path = './sounds'

    possible_sounds = get_all_available_files(path)
    # print(possible_sounds)
    tag_characters = read_tag_characters_into_list()

    # go over each character one by one and prompt
    for association in tag_characters:
        print("Please choose a sound for the character " + association['Character'] + ". You have the following options: ")
        print(possible_sounds)
        chosen_sound = input("Please select a sound file\n")
        chosen_rfid = input("Please choose which reader you want this sound to play on [1/2/3]\n")
        new_line = {association['Tag']: {'Sound': chosen_sound, 'Reader': chosen_rfid}}
        tag_sound_associations.update(new_line)

        with open("sound_associations.csv", "a", newline='') as sound_file:
            sound_writer = csv.writer(sound_file, delimiter=',')
            sound_writer.writerow([association['Tag'], chosen_sound, chosen_rfid])

    

