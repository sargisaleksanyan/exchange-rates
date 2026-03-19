from src.data.business_logos import business_logos
from src.data.company_data import exchange_companies_data
from src.db.db_handler import DatabaseHandler
from src.util.common_classes.common_name import DbCollectionNames


def read_business_logos():
    db_handler = DatabaseHandler(DbCollectionNames.BUSINESS_LOGOS)
    db_handler.make_unique_index('url')

    data = {}

    for business_logo in business_logos:
        logo_text = business_logo['logos']
        logos = logo_text.split(',')
        data[business_logo['url']] = logos

    return data


def insert_companies():
    db_handler = DatabaseHandler(DbCollectionNames.UAE_RATES)
    company_logos = read_business_logos()
    db_handler.make_unique_index('url')
    # db_handler.make_unique_index('id')

    # db_handler.make_unique_index('url')

    for exchange_company in exchange_companies_data:
        try:
            url = exchange_company['url']
            if url in company_logos:
                exchange_company['logos'] = company_logos[url]
                db_handler.upsert_company_data(exchange_company)
            else:
                print('Url', url)
        except Exception as e:
            print(f"Error: while inserting data {e}")

    print('Inserted business logos successfully')
    db_handler.close_connection()
