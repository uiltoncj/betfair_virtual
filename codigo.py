from requests_html import HTMLSession as requests
from csv import DictWriter as csv
from re import search
import pandas as pd
from time import gmtime, strftime

hora = strftime("%Y-%m-%d %H:%M:%S", gmtime())
dta = hora[8:10]
def get_games():
    url = 'https://www.betfair.com/sport/virtuals-results?sport=SOCCER_WORLD_CUP&day=2022-07-'+str(dta)
    html = requests().get(url).html

    game_list = html.find('#mod-virtuals-results-list-1002',
                          first = True).find('.result-list-wrapper',
                                             first = True).find('.result-item')

    data = []
    for game in game_list:
        text = game.text
        for inutil in ['All markets Show less',
                            'Market',
                            'Result',
                            'Correct Score',
                            'Total Goals']:
            text = ''.join(text.split(inutil))
        info = text.split('\n')
        hour = search(r'\d{,}:\d{,}', info[0]).group()
        player1 = search(r'\w{,}$', info[0]).group()
        player2 = info[2]
        placar = info[1].split('-')
        totalgoals = info[len(info)-1]

        data.append(dict(
            hour = hour,
            player1 = player1,
            player2 = player2,
            player1_goals = int(placar[0].strip()),
            player2_goals = int(placar[1].strip()),
            totalgoals = totalgoals,

        ))

    with open('results.csv', "a", newline='') as csvfile:
        writer = csv(csvfile, fieldnames=[
            'hour',
            'player1',
            'player2',
            'player1_goals',
            'player2_goals',
            'totalgoals'
        ])

        writer.writeheader()
        for game in data:
            writer.writerow(game)


if __name__ == '__main__':
    from time import sleep

    hora = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    dta = hora[8:10]
    while True:
        try:
            conta = 0
            while 1:
                print(f':: buscando dados {conta}')
                conta = conta + 1
                get_games()
                df = pd.read_csv("C:/Users/UILTO/OneDrive/Área de Trabalho/alert/results.csv", encoding='utf-8', delimiter=',')
                df = df.drop_duplicates()
                print(df)
                df.to_csv('exemplo.csv')
                sleep (0.3)
        except:
            print('Algum erro está acontecenco')
