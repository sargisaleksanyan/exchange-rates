from src.data.business_logos import business_logos
from src.db.db_handler import DatabaseHandler
from src.util.common_classes.common_name import DbCollectionNames


def insert_business_logos():
    db_handler = DatabaseHandler(DbCollectionNames.BUSINESS_LOGOS)

    db_handler.make_unique_index('url')

    for business_logo in business_logos:
        logo_text = business_logo['logos']
        logos = logo_text.split(',')
        business_logo['logos'] = logos
        db_handler.replace_data({'url': business_logo['url']}, business_logo)

    print('Inserted business logos successfully')
    db_handler.close_connection()
