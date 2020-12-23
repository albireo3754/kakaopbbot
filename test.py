from restApiMain import Data, Bot

data = Data()
bot = Bot()
print(bot.makeMatchListItem({'_id': '1606372810492',
    'champion': {'en': 'Akali', 'ko': '아칼리'}, 
    'statPerk': ['5008', '5008', '5002'], 
    'proInf': {'name': 'Jiin', 'team': 'No Team', 'summonername': '엔터키를빼고게임'}}))