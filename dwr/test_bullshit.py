words_with_position = []
words = ['feel', 'graduate', 'movie', 'fashionable', 'bacon',
         'drop', 'produce', 'acquisition', 'cheap', 'strength',
         'master', 'perception', 'noise', 'strange', 'am']

for nume, word in enumerate(words, start=1):
    words_with_position.append((word, nume))

print(words_with_position)