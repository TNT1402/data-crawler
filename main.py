from data_handler import crawl_data, save_phone_info
from database import create_connection

if __name__ == "__main__":
    # Call the desired main function based on some condition
    user_input = input("Which function do you want to run? (1 for crawler, 2 for save to DB): ")
    if user_input == "1":
        crawl_data()
    elif user_input == "2":
        connection = create_connection()
        if connection:
            save_phone_info(connection)
        else:
            print("Could not establish connection to database")
    else:
        print("Invalid input")