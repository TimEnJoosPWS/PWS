import winsound
import re
import time

note_representation = {
                       "0": "-",  # rust
                       "1": "C3",
                       "2": "D3",
                       "3": "E3",
                       "4": "F3",
                       "5": "G3",
                       "6": "A3",
                       "7": "B3",
                       "8": "C4",
                       "9": "D4",
                       "A": "E4",
                       "B": "F4",
                       "C": "G4",
                       "D": "A4",
                       "E": "B4",
                       "F": "."  # aanhouden van de noot
                       }

note_frequency = {
                  "C3": 131,
                  "D3": 147,
                  "E3": 165,
                  "F3": 174,
                  "G3": 196,
                  "A3": 220,
                  "B3": 247,
                  "C4": 262,
                  "D4": 294,
                  "E4": 330,
                  "F4": 349,
                  "G4": 392,
                  "A4": 440,
                  "B4": 494
                  }


def play_note(note, duration):
    assert re.search(r'[^1-9A-E]^C', note) is None, "invalid note"
    winsound.Beep(note_frequency[note], duration * 125)
    print(note)

    
def play_music(music):
    assert re.search(r'[^0-9A-F]', music) is None, "invalid music"

    music = [note_representation[representation] for representation in music]

    if music[0] is ".":
        music[0] = "-"
    
    for note_index in range(len(music)):
        
        if music[note_index] is "-":
            time.sleep(1/4)
        else:
            if music[note_index] is ".":
                continue
            
            length = 1
            i = 1
            
            if note_index + i >= len(music) - 1:
                    play_note(music[note_index], length)
                    break
                
            while music[note_index + i] is ".":
                length += 1
                i += 1
                if note_index + i >= len(music) - 1:
                    break
                
            play_note(music[note_index], length)
            

if __name__ is "__main__":
    #play_music("8FFF09F0AF08F008F09F0AF08F00AF0BF0CF000AF0BF0CF000CDCBA0008F00CDCBA0008F008F05F08F008F05F08FFFFFFFFFF")
    play_music('B0C508C1A637D5C71B429319A56F7DC2B3B383B0E9E241C46FF8FA329D1210AD')