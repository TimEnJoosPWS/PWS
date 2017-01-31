notes = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", 'D', 'E', 'F']
stable_notes = {"Am": ["6", "8", "A", "D","1", "3"],
                "C": ["1", "3", "5", "8", "A", "C"],
                "F": [ "4", "6", "8", "B", "D", "1"],
                "G": ["5", "7", "9", "C", "E", "2"],
                "Em": ["3", "5", "7", "A", "C", "E"],
                "Dm": ["2", "4", "6", "9", "B", "D"]}
                
instable_notes = {"Am": ["7", "9", "B", "C", "E", "2", "4", "5"],
                  "C": ["2", "4", "6", "7", "9", "B", "D", "E"],
                  "F": ["5", "7", "9", "A", "C", "E", "2", "3"],
                  "G": ["6", "8", "A", "B", "D", "1", "3", "4"],
                  "Em": ["4", "6", "8", "9", "B", "D", "1", "2"],
                  "Dm": ["3", "5", "7", "8", "A", "C", "E", "1"]}

def fitness_stable_unstable_notes(chromosome, chord):
    """
        Input: the current chromosome, the current chord
        This function returns the decrease in fitness of a piece of music
        due to an imbalance in stable and unstable notes.
    """
    assert type(chord) is str and type(chromosome) is str, "invalid input"
    
    stable, unstable, fitness = 0, 0, 0
    
    for i in chromosome:
        if i in stable_notes[chord]:
            stable += 1
        elif i in instable_notes[chord]:
            unstable += 1
            
    return stable
    return unstable


def next_tone(chromosome, current_index, return_new_index=False):
    """
        Returns the next gene in the chromosome, or "error" if there is none.
        (because there are characters (0 and F) that need to be ignored)
    """
    assert type(chromosome) is str and len(chromosome) is length_chromosome\
        and current_index < length_chromosome,\
        "invalid chromosome"

    i = current_index + 1
    while re.search(r"[F0]", chromosome[i:i+1:]) is not None and i < length_chromosome:
        i += 1
    if i is 8:
        return "error"
    elif not return_new_index:
        return chromosome[i]
    else:
        return (chromosome[i], i)


def fitness_note_length(chromosome):
    """
    """
    amount_f = chromosome.count("F")
    amount_rest = chromosome.count("0")
    total_rest = chromosome.count("F") + chromosome.count("0")
    

def fitness_note_leaps(chromosome):

    current_note = next_tone(chromosome, -1)
    note_index = next_tone(chromosome, -1, True)[1]
    leaps, steps, fitness = 0, 0, 0

    while current_note != "error" and next_tone(chromosome, note_index) != "error":
        next_note = next_tone(chromosome, note_index)
        interval = abs(notes.index(current_note) - notes.index(next_note)) + 1
        if interval <= 2:
            steps += 1
        else:
            leaps += 1

        if interval is 6:
            amount_sext += 1
        elif interval is 7:
            amount_septime += 1
        elif interval > 8:
            big_leaps += 1
        current_note = next_tone(chromosome, note_index)
        note_index = next_tone(chromosome, note_index, True)[1]

    return steps
    return leaps
    return amount_sext
    return amount_septime
    return big_leaps
                         
