from src.data.currency_data import currency_codes
from src.db.db_handler import DatabaseHandler
from src.util.common_classes.common_name import DbCollectionNames


def insert_currency_codes():
    db_handler = DatabaseHandler(DbCollectionNames.CURRENCY_CODES)

    db_handler.make_unique_index('url')

    for currency_code in currency_codes:
        filter = {"code": currency_code['code']}
        db_handler.replace_data(query=filter ,data= currency_code)

    print('Inserted currency codes successfully')
    db_handler.close_connection()


insert_currency_codes()
