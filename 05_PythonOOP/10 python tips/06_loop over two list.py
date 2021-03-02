names = ['peter parker', 'clark kent', 'wade wilson', 'bruce wayne']
heroes = ['spiderman', 'superman', 'deadpool', 'batman']
universes = ['Marvel','DC', 'Marvel', 'DC']

for index, name in enumerate(names):
    hero = heroes[index]
    print(f'{name} is actually {hero}')

print('*'*50)

for name, hero in zip(names, heroes):
    print(f'{name} is actually {hero}')

print('*'*50)

for name, hero, universe in zip(names, heroes, universes):
    print(f'{name} is actually {hero} from {universe}')







