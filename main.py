import mysql.connector
import logging

# Configure logging
logging.basicConfig(filename='bank_management.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Database connection
mydb = mysql.connector.connect(host='localhost', user='root', password='root', database='BANK_MANAGEMENT')


def execute_query(query, params):
    """Helper function to execute database queries."""
    try:
        x = mydb.cursor()
        x.execute(query, params)
        return x
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        logging.error(f"Database Error: {err}")
        return None


def openacc():
    while True:  # Loop to ensure a unique account number is entered
        ac = input("Enter The Account No (numeric): ")
        if not ac.isdigit():
            print("Invalid input! Please enter a numeric account number.")
            continue

        # Check if the account number already exists
        check_sql = 'SELECT * FROM account WHERE AccNo = %s'
        result = execute_query(check_sql, (ac,)).fetchone()

        if result:
            print(f"An account with account number {ac} already exists. Please try again.")
        else:
            break  # Exit loop if account number is unique

    # Proceed to collect remaining details
    n = input("Enter Your Name: ")
    db = input("Enter Your Date of Birth: ")
    add = input("Enter Your Address: ")
    cn = input("Enter Your Contact Number: ")
    ob = input("Enter Your Opening Balance: ")

    if not ob.isdigit():
        print("Opening balance must be a numeric value.")
        return

    ob = int(ob)
    data1 = (n, ac, db, add, cn, ob)
    data2 = (n, ac, ob)

    sql1 = 'INSERT INTO account VALUES (%s, %s, %s, %s, %s, %s)'
    sql2 = 'INSERT INTO amount VALUES (%s, %s, %s)'
    x = execute_query(sql1, data1)
    if x:
        execute_query(sql2, data2)
        mydb.commit()
        print("Data Entered Successfully.")
        logging.info(f"New account created: {ac}, Name: {n}")

    main()


def depo_amo():
    amount = input("Enter the Amount you want to deposit: ")
    if not amount.isdigit():
        print("Amount must be numeric.")
        return

    ac = input("Enter the account number: ")
    amount = int(amount)

    a = 'SELECT balance FROM amount WHERE AccNo = %s'
    result = execute_query(a, (ac,)).fetchone()

    if not result:
        print("Account not found.")
        return

    t = result[0] + amount
    sql = 'UPDATE amount SET balance = %s WHERE AccNo = %s'
    execute_query(sql, (t, ac))
    mydb.commit()
    print("Amount Deposited Successfully.")
    logging.info(f"Deposited {amount} to account {ac}")
    main()


def withdraw_amount():
    amount = input("Enter the Amount you want to withdraw: ")
    if not amount.isdigit():
        print("Amount must be numeric.")
        return

    ac = input("Enter the account number: ")
    amount = int(amount)

    a = 'SELECT balance FROM amount WHERE AccNo = %s'
    result = execute_query(a, (ac,)).fetchone()

    if not result:
        print("Account not found.")
        return

    if amount > result[0]:
        print("Insufficient balance!")
        return

    t = result[0] - amount
    sql = 'UPDATE amount SET balance = %s WHERE AccNo = %s'
    execute_query(sql, (t, ac))
    mydb.commit()
    print("Amount Withdrawn Successfully.")
    logging.info(f"Withdrawn {amount} from account {ac}")
    main()


def bal_enq():
    ac = input("Enter the account number: ")
    a = 'SELECT * FROM amount WHERE AccNo = %s'
    result = execute_query(a, (ac,)).fetchone()

    if not result:
        print("Account not found.")
        return

    print(f"Balance for account {ac} is {result[-1]}")
    logging.info(f"Balance enquiry for account {ac}: {result[-1]}")
    main()


def dis_details():
    ac = input("Enter the account number: ")
    a = 'SELECT * FROM account WHERE AccNo = %s'
    result = execute_query(a, (ac,)).fetchone()

    if not result:
        print("Account not found.")
        return

    print("Customer Details:")
    print(
        f"Name: {result[0]}\nAccount Number: {result[1]}\nDate of Birth: {result[2]}\nAddress: {result[3]}\nContact: {result[4]}\nBalance: {result[5]}")
    logging.info(f"Displayed details for account {ac}")
    main()


def close_acc():
    ac = input("Enter the account number: ")
    sql1 = 'DELETE FROM account WHERE AccNo = %s'
    sql2 = 'DELETE FROM amount WHERE AccNo = %s'
    x1 = execute_query(sql1, (ac,))
    x2 = execute_query(sql2, (ac,))

    if x1 and x2:
        mydb.commit()
        print("Account Closed Successfully.")
        logging.info(f"Closed account {ac}")
    else:
        print("Failed to close account. Please try again.")
    main()


def main():
    print('''
               1. OPEN NEW ACCOUNT
               2. DEPOSIT AMOUNT
               3. WITHDRAW AMOUNT
               4. BALANCE ENQUIRY
               5. DISPLAY CUSTOMER DETAILS
               6. CLOSE AN ACCOUNT
               7. EXIT''')

    choice = input("Enter The Task You Want To Perform: ")

    if choice == '1':
        openacc()
    elif choice == '2':
        depo_amo()
    elif choice == '3':
        withdraw_amount()
    elif choice == '4':
        bal_enq()
    elif choice == '5':
        dis_details()
    elif choice == '6':
        close_acc()
    elif choice == '7':
        print("Exiting the program. Goodbye!")
        logging.info("Program exited.")
        exit()
    else:
        print("Invalid Choice. Please try again.")
        main()


main()
