import requests
import pandas 

months = {'January':'01','February':'02', 'March':'03', 'April':'04', 'May':'05', 'June':'06', 'July':'07', 'August':'08', 'September':'09', 'October':'10','November':'11', 'December':'12'}

def get_http_content(url):
    """
    Gathers the HTTP content of a website.

    Args:
        url: The URL of the website.

    Returns:
        The HTTP content of the website as a string, or None if an error occurs.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

def urlToDict(url,date=None,first=False):
    # Example usage:
    content = get_http_content(url)

    data = {}
    if content:
        #print(content)
        for it in content.split('gen9/'):
            if '.png' in it:
                if '<!doctype html>' in it:
                    continue
                pokemon = it.split('.png')[0]
                if pokemon in data:
                    data[pokemon] += 1
                else:
                    data[pokemon] = 1
    # get date too
    if date is None:
        div = content.split('infobox-text">')[1]
        mydat = div.split(' |')[0]
        parts = mydat.split(' ')
        year = parts[2]
        month = parts[1][0:3]# old way months[parts[1]]
        day = ''
        for c in parts[0]:
            if c in '0123456789':
                day += c
        date = f'{month} {day} {year}'

    sorted_dict = dict(sorted(data.items(), key=lambda item: item[1]))
    sum = 0
    if first:
        final = {'Pokemon':['URL',date]}
    else:
        final = {'Pokemon':date}
    for k,v in sorted_dict.items():
        sum += v
    for k,v in sorted_dict.items():
        #print(f'{k} : {str(v/sum*100)[0:5]}%')
        K = k[0:1].upper() + k[1:]
        if first:
            final[K] = ['https://limitlessvgc.com/wp-content/media/icons/gen9/'+k+'.png',float(str(v/sum*100)[0:5])]
        else:
            final[K] = float(str(v/sum*100)[0:5]) # https://limitlessvgc.com/wp-content/media/icons/gen9/meowscarada.png
    print(f'TOTAL Pokemon: {sum}')
    #print(final)
    return final

def gatherTourneyData(tourneys):
    
    first = True
    for tourney in tourneys:
        print(f'Getting Tourney {tourney}')
        res = urlToDict(f"https://limitlessvgc.com/events/{tourney}/",first=first)
        #print(res)
        if first:
            df = pandas.DataFrame(res)
            first = False
        else:
            for col in res:
                if col not in df.columns:
                    df[col] = None
            df = pandas.concat([df, pandas.DataFrame([res])], ignore_index=True)
            #df.loc[len(df)] = res old method
        #print(df)
        #res = urlToDict("https://limitlessvgc.com/events/297/",'20/01/2023')
        #print(df)
    #df['URL'] = 'https://limitlessvgc.com/wp-content/media/icons/gen9/'+df['Pokemon']+'.png'
    df.loc[0, :] = df.loc[0, :].values
    for col in df.columns:
        df.loc[0, col] = 'https://limitlessvgc.com/wp-content/media/icons/gen9/' + str(col[0:1].lower()) + str(col[1:]) + '.png'

    df.to_csv('regs.csv', index=False)

tourneys = [296,297, # reg A
            298,312,306,299,308,300,310,315, # reg B
            302,313,303,304,307,309,305,311,316,321, # reg C 317 was ommited
            319,322,353,344,# reg D
            354,325,336,326,357,345,337,338,327, # reg E
            328,329,343,346,330,340,341,363,331,356,332,347,362, # reg F
            333,361,360,334,359,355,358 # reg G
            ]
gatherTourneyData(tourneys)