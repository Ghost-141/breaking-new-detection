import mysql.connector
import json
from typing import List, Dict, Any


db_config: Dict[str, str] = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "newschannel",
}


def fetch_first_zero_status_news() -> List[Dict[str, Any]]:

    conn = None
    cursor = None
    data_list: List[Dict[str, Any]] = []

    try:

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        sql_first_scrape_id_query = """
        SELECT
            L.id,
            L.newspaper_name,
            L.title,
            L.link,
            L.published_time,
            L.scrape_id
        FROM
            latest_news AS L
        WHERE
            L.scrape_id = (
                -- Subquery: final_table থেকে প্রথম scrape_id (status=0) খুঁজে বের করা
                SELECT 
                    scrape_id 
                FROM 
                    final_table 
                WHERE 
                    status = 0
                ORDER BY 
                    scrape_id ASC  
                LIMIT 1
            );
        """

        cursor.execute(sql_first_scrape_id_query)

        column_names = [i[0] for i in cursor.description]  # type: ignore

        results = cursor.fetchall()

        for row in results:
            data_dict = dict(zip(column_names, row))
            data_list.append(data_dict)

        return data_list

    except mysql.connector.Error as err:
        print(f"Error fetching data: {err}")
        return []

    finally:

        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


fetched_data = fetch_first_zero_status_news()

if fetched_data:

    json_output = json.dumps(fetched_data, indent=4, ensure_ascii=False)

    with open("db_data.json", "w", encoding="utf8") as f:
        json.dump(fetched_data, f, indent=4, ensure_ascii=False)

    print("--- JSON Output for the FIRST scrape_id with status 0 ---")
    print(json_output)



    
else:
    print("--- No data found or connection error occurred. ---")
