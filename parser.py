
import requests
from mysql.connector import connect, Error

url = "https://dt.miet.ru/ppo_it_final"

header = {
    'x-auth-token':'kooxicjx'
}
try:
    with connect(
        host="194.147.85.214",
        user="stalker",
        password="FFp[mtlWzXgojK9Z",
        database='stalker'
    )as connection:

        response = requests.get(url, headers=header)

        pixel = 50
        a = response.json()

        print(a)
        print("_____________")
        print(a["message"][0]["swans"][0]["id"])

        truncate_all = """
        SELECT * FROM `anamaly`;
        TRUNCATE `anamaly`;

        """
        values_detector = """
        INSERT INTO `detector`(id, x, y)
        VALUES (%s, %s, %s)
        """
        values_anamaly = """
        INSERT INTO `anamaly` (device, id, rate)
        VALUES (%s, %s, %s)
        """
        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE `anamaly`;")
            cursor.execute("TRUNCATE `detector`;")
            for j in range(len(a['message'])):
                for i in range(len(a['message'][j]['swans'])):
                    print(a['message'][j]['id'], a['message'][j]['swans'][i]['id'], a['message'][j]['swans'][i]['rate'])
                    cursor.execute(values_anamaly, (a['message'][j]['id'], a['message'][j]['swans'][i]['id'], a['message'][j]['swans'][i]['rate']))
            for i in range(len(a['message'])):
                cursor.execute(values_detector, (a['message'][i]['id'], a['message'][i]['coords'][0], a['message'][i]['coords'][1]))
        connection.commit()

except Error as e:
    print(e)