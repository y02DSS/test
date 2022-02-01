import requests
import sqlite3
import time

def all():
    all_skins = {}

    cookies = {
        "name": "session",
        "value": "1-bMNh7288nmEtx0sI8acpyjsF9SpVDSCoClsWignxuWrs2036684442",
    }

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
    proxies_list = []
    with open("proxy.txt", 'r') as proxy_file:
        for temp_proxy in proxy_file.read().split():
            proxies = {}
            proxies['http'] = temp_proxy
            proxies_list.append(proxies)

    print(proxies_list)

    session = requests.Session()
    session.proxies.update(proxies_list[0])
    session.cookies.set(**cookies)

    db = "Main.db" 
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("""SELECT * from Filter""")

    data_list = []
    records = cur.fetchall()
    n = 0
    nam_proxy = 0
    for row in records:
        Name_stik = row[0]
        ID_gun = row[2].split()
        Place_stik = row[3]
        ID_stik = row[1]
        Price = row[6]
        Scrath = row[5]
        Percent = row[4]
        for gun in ID_gun:
            number_link = f'https://buff.163.com/api/market/goods?game=csgo&page_num=1&category=weapon_{gun}&extra_tag_ids=slot_{Place_stik}_{ID_stik}'
            all_number = session.get(url=number_link).json()['data']['total_page']
            for number in range(1, int(all_number)+1):
                finel_link =  f'https://buff.163.com/api/market/goods?game=csgo&page_num={number}&category=weapon_{gun}&extra_tag_ids=slot_{Place_stik}_{ID_stik}'
                resp_baza = session.get(url=finel_link)
                data_list = resp_baza.json()['data']['items']  # Можно ускорить, если на этом проверять есть ли item в таблице Skin_2
                for data in data_list:
                    min_price_skin_link = f'https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id={data["id"]}&page_num=1&sort_by=default&mode=&allow_tradable_cooldown=1'
                    resp_min_price = session.get(url=min_price_skin_link, headers={'User-Agent': user_agent})
                    print('1 код - ', resp_min_price.status_code)
                    if resp_min_price.status_code == 429:
                        print(resp_skin.headers)
                        print(resp_skin.content.decode('utf-8'))
                        time.sleep(5)
                        print("!!!", nam_proxy)
                        nam_proxy += 1
                        session.proxies.update(proxies_list[nam_proxy])
                        resp_min_price = session.get(url=min_price_skin_link, headers={'User-Agent': user_agent})
                    skin_min_price = resp_min_price.json()['data']['items'][0]['lowest_bargain_price']

                    skin_link = f'https://buff.163.com/api/market/goods/sell_order?game=csgo&goods_id={data["id"]}&page_num=1&sort_by=default&mode=&allow_tradable_cooldown=1&extra_tag_ids=slot_{Place_stik}_{ID_stik}'
                    resp_skin = session.get(url=skin_link, headers={'User-Agent': user_agent})
                    print('2 код - ', resp_skin.status_code)
                    if resp_skin.status_code == 429:
                        print(resp_skin.headers)
                        print(resp_skin.content.decode('utf-8'))
                        time.sleep(5)
                        print("!!!", nam_proxy)
                        nam_proxy += 1
                        session.proxies.update(proxies_list[nam_proxy])
                        resp_skin = session.get(url=skin_link, headers={'User-Agent': user_agent})
                    resp_skin_final = resp_skin.json()
                    skin_final_price = resp_skin_final['data']['items'][0]['price'] # Добавить несколько эллементов, если первый подходит
                    for slot in resp_skin_final['data']['items'][0]['asset_info']['info']['stickers']:
                        if slot['slot'] == Place_stik:
                            skin_final_scrath = slot['wear']
                    if (((1 - float(skin_final_scrath)) >= float(Scrath)) and ((float(skin_min_price)+(float(Price)*0.01*float(Percent))) >= float(skin_final_price))):
                        link = f'https://buff.163.com/goods/{data["id"]}?from=market#tab=selling&extra_tag_ids=slot_{Place_stik}_{ID_stik}'
                        print(link)
                        all_skins[n] = (str(gun) + '\/' + str(skin_final_price) + '\/' + str(Name_stik) + '\/' + str(link))
                    n += 1
                    print(n)
                    print('')
    if all_skins is not None:
        for item in all_skins.values():
            list_item = item.split('\/')
            cur.execute("INSERT INTO Skins(ID, Name, Price, Stikers, Link) VALUES(?, ?, ?, ?, ?)", [1, list_item[0], list_item[1], list_item[2], list_item[3]])

        cur.execute("""SELECT * from Skins""")
        records_1 = cur.fetchall()

        cur.execute("""SELECT * from Skins_2""")
        records_2 = cur.fetchall()

        if len(records_1) > len(records_2):
            for i  in range(len(records_1)-len(records_2)):
                cur.execute(f"""INSERT INTO Skins_2 VALUES (0, 0, 0, 0, 0)""")
        elif len(records_2) > len(records_1):
            for i in range(len(records_2)-len(records_1)):
                cur.execute(f"""INSERT INTO Skins VALUES (0, 0, 0, 0, 0)""")

        rec_1, rec_2 = [], []
        for i in range (len(records_1)):
            rec_1.append(records_1[i])

        for j in range (len(records_2)):
            rec_1.append(records_2[j])

        last_rec = list(set(rec_2 + rec_1))
        dell = list(set(last_rec)-set(rec_1))
        add = list(set(last_rec)-set(rec_2)) 


        for i in range(len(add)):
            cur.execute("""INSERT INTO Skins_2(ID, Name, Price, Stikers, Link) VALUES(?, ?, ?, ?, ?)""", [str(add[i][0]), str(add[i][1]), str(add[i][2]), str(add[i][3]), str(add[i][4])])
        for i in range(len(dell)):
            cur.execute(f"""DELETE FROM Skins_2 WHERE Link = {dell[i][4]}""")  
        cur.execute(f"""DELETE FROM Skins_2 WHERE Link = 0;""")
        cur.execute('DELETE FROM Skins;',)

        cur.execute("""SELECT * from Skins_2""")
        # Удалить дубликаты из Skin_2
        #cur.execute("""DELETE FROM Skins_2 HERE ROWID IN SELECT ROWID FROM Skins_2  SELECT MIN (ROWID) FROM Skins_2 GROUP BY ID, Name, Price, Stikers, Link); """)
        con.commit()
        con.close()
        all_skins = {}
        return(add) #Выводить в телеграмм
