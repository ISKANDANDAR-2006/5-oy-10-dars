import psycopg2

def connect_db():
    return psycopg2.connect(
        host="localhost",
        database="AVTOSALON",
        user="postgres",
        password="1"
    )

def display_table(data, headers):
    print("\n" + "-" * 50)
    print(" | ".join(headers))
    print("-" * 50)
    for row in data:
        print(" | ".join(map(str, row)))
    print("-" * 50)

def process_query():
    conn = connect_db()
    cursor = conn.cursor()

    while True:
        print("\n[1] Barcha modellarni brand nomi va rangi bilan chiqarish")
        print("[2] Xodimlar va buyurtmachilarning email'larini birlashtirish")
        print("[3] Har bir davlatda nechtadan buyurtmachi borligini hisoblash")
        print("[4] Har bir davlatda nechtadan xodim borligini hisoblash")
        print("[5] Har bir brandda nechtadan model borligini chiqarish")
        print("[6] Modellar 5 tadan ko'p bo'lgan brandlarni chiqarish")
        print("[7] Orders'ni customers, employees va models bilan birlashtirish")
        print("[8] Avtomobillarning umumiy narxini chiqarish")
        print("[9] Jami brandlar sonini chiqarish")
        print("[10] Yangi ma'lumot qo'shish")
        print("[11] Dasturni to'xtatish")

        choice = input("Buyruq raqamini kiriting: ").strip()

        if choice == "1":
            query = """
            SELECT models.name AS Model, brands.name AS Brand, models.color AS Color
            FROM models
            JOIN brands ON models.brand_id = brands.id;
            """
            cursor.execute(query)
            data = cursor.fetchall()
            display_table(data, ["Model", "Brand", "Color"])

        elif choice == "2":
            query = """
            SELECT email FROM employees
            UNION
            SELECT email FROM customers;
            """
            cursor.execute(query)
            data = cursor.fetchall()
            display_table(data, ["Emails"])

        elif choice == "3":
            query = """
            SELECT country, COUNT(*) AS Customer_Count
            FROM customers
            GROUP BY country
            ORDER BY Customer_Count DESC;
            """
            cursor.execute(query)
            data = cursor.fetchall()
            display_table(data, ["Country", "Customer Count"])

        elif choice == "4":
            query = """
            SELECT country, COUNT(*) AS Employee_Count
            FROM employees
            GROUP BY country
            ORDER BY Employee_Count DESC;
            """
            cursor.execute(query)
            data = cursor.fetchall()
            display_table(data, ["Country", "Employee Count"])

        elif choice == "5":
            query = """
            SELECT brands.name AS Brand, COUNT(models.id) AS Model_Count
            FROM brands
            JOIN models ON brands.id = models.brand_id
            GROUP BY brands.id;
            """
            cursor.execute(query)
            data = cursor.fetchall()
            display_table(data, ["Brand", "Model Count"])

        elif choice == "6":
            query = """
            SELECT brands.name AS Brand, COUNT(models.id) AS Model_Count
            FROM brands
            JOIN models ON brands.id = models.brand_id
            GROUP BY brands.id
            HAVING COUNT(models.id) > 5;
            """
            cursor.execute(query)
            data = cursor.fetchall()
            display_table(data, ["Brand", "Model Count"])

        elif choice == "7":
            query = """
            SELECT orders.id, customers.name AS Customer, employees.name AS Employee, models.name AS Model
            FROM orders
            JOIN customers ON orders.customer_id = customers.id
            JOIN employees ON orders.employee_id = employees.id
            JOIN models ON orders.model_id = models.id;
            """
            cursor.execute(query)
            data = cursor.fetchall()
            display_table(data, ["Order ID", "Customer", "Employee", "Model"])

        elif choice == "8":
            query = "SELECT SUM(price) AS Total_Price FROM models;"
            cursor.execute(query)
            total_price = cursor.fetchone()[0]
            print(f"\nAvtomobillarning umumiy narxi: {total_price}")

        elif choice == "9":
            query = "SELECT COUNT(*) AS Brand_Count FROM brands;"
            cursor.execute(query)
            brand_count = cursor.fetchone()[0]
            print(f"\nJami brandlar soni: {brand_count}")

        elif choice == "10":
            table = input("Qaysi jadvalga ma'lumot qo'shmoqchisiz (brands/models/customers/employees/orders)? ").strip()
            if table == "brands":
                name = input("Brand nomini kiriting: ").strip()
                cursor.execute("INSERT INTO brands (name) VALUES (%s);", (name,))
            elif table == "models":
                name = input("Model nomini kiriting: ").strip()
                brand_id = int(input("Brand ID kiriting: ").strip())
                color = input("Rangini kiriting: ").strip()
                price = float(input("Narxini kiriting: ").strip())
                cursor.execute("INSERT INTO models (name, brand_id, color, price) VALUES (%s, %s, %s, %s);",
                               (name, brand_id, color, price))
            elif table == "customers":
                name = input("Buyurtmachi nomini kiriting: ").strip()
                email = input("Emailni kiriting: ").strip()
                country = input("Davlatini kiriting: ").strip()
                cursor.execute("INSERT INTO customers (name, email, country) VALUES (%s, %s, %s);",
                               (name, email, country))
            elif table == "employees":
                name = input("Xodim nomini kiriting: ").strip()
                email = input("Emailni kiriting: ").strip()
                country = input("Davlatini kiriting: ").strip()
                cursor.execute("INSERT INTO employees (name, email, country) VALUES (%s, %s, %s);",
                               (name, email, country))
            elif table == "orders":
                customer_id = int(input("Buyurtmachi ID ni kiriting: ").strip())
                employee_id = int(input("Xodim ID ni kiriting: ").strip())
                model_id = int(input("Model ID ni kiriting: ").strip())
                cursor.execute("INSERT INTO orders (customer_id, employee_id, model_id) VALUES (%s, %s, %s);",
                               (customer_id, employee_id, model_id))
            else:
                print("Noto'g'ri jadval nomi!")
                continue
            conn.commit()
            print("Ma'lumot muvaffaqiyatli qo'shildi!")

        elif choice == "11":
            print("Dastur to'xtatildi.")
            break

        else:
            print("Noto'g'ri buyruq, qaytadan kiriting!")

    conn.close()

if __name__ == "__main__":
    process_query()
