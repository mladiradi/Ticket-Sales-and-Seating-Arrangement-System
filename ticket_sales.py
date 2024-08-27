import datetime
import random


def get_dates():
    while True:
        try:
            start_date = input("Въведете начална дата за продажба на билети (ГГГГ-ММ-ДД): ")
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            end_date = input("Въведете крайна дата за продажба на билети (ГГГГ-ММ-ДД): ")
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
            if start_date > end_date:
                print("Началната дата трябва да е преди крайната дата. Моля, опитайте отново.")
            else:
                return start_date, end_date
        except ValueError:
            print("Невалиден формат на дата. Моля, използвайте формат ГГГГ-ММ-ДД.")


def get_seat_info():
    while True:
        try:
            rows = int(input("Въведете брой редове: "))
            seats_per_row = int(input("Въведете брой места на всеки ред: "))
            if rows <= 0 or seats_per_row <= 0:
                print("Броят на редовете и местата трябва да е положителен. Моля, опитайте отново.")
            else:
                return rows, seats_per_row
        except ValueError:
            print("Моля, въведете валидни числа за редове и места.")


def get_client_info(used_ticket_numbers, sale_count):
    while True:
        name = input("Въведете име на клиента: ")
        if not name.strip():
            print("Името не може да бъде празно. Моля, опитайте отново.")
            continue

        is_disabled_input = input("Инвалид (да/не): ").strip().lower()
        if is_disabled_input not in ['да', 'не']:
            print("Моля, въведете 'да' или 'не' за инвалид.")
            continue
        is_disabled = is_disabled_input == 'да'

        try:
            height = int(input("Въведете височина (см): "))
            if height <= 0:
                print("Височината трябва да е положителна. Моля, опитайте отново.")
                continue
        except ValueError:
            print("Моля, въведете валидно число за височина.")
            continue

        ticket_number = generate_ticket_number(used_ticket_numbers)
        sale_number = f"x{sale_count}"

        return {
            'ticket_number': ticket_number,
            'sale_number': sale_number,
            'name': name,
            'is_disabled': is_disabled,
            'height': height
        }


def is_sale_period_valid(start_date, end_date):
    current_date = datetime.datetime.now()
    return start_date <= current_date <= end_date


def generate_ticket_number(used_numbers):
    while True:
        ticket_number = str(random.randint(1000000000, 9999999999))
        if ticket_number not in used_numbers:
            used_numbers.add(ticket_number)
            return ticket_number


def sort_clients(seating_info):
    return sorted(seating_info, key=lambda x: (not x['is_disabled'], x['height']))


def arrange_seating(seating_info, rows, seats_per_row):
    seating_chart = [[None for _ in range(seats_per_row)] for _ in range(rows)]

    # Отделяме клиентите с увреждания и останалите
    disabled_clients = [client for client in seating_info if client['is_disabled']]
    other_clients = [client for client in seating_info if not client['is_disabled']]

    # Разпределение на клиентите с увреждания
    for row in range(rows):
        left_idx = 0
        right_idx = seats_per_row - 1
        assign_left = True

        while disabled_clients and (left_idx <= right_idx):
            if assign_left:
                seating_chart[row][left_idx] = disabled_clients.pop(0)
                seating_chart[row][left_idx]['row'] = row + 1
                seating_chart[row][left_idx]['seat'] = left_idx + 1
                left_idx += 1
            else:
                seating_chart[row][right_idx] = disabled_clients.pop(0)
                seating_chart[row][right_idx]['row'] = row + 1
                seating_chart[row][right_idx]['seat'] = right_idx + 1
                right_idx -= 1
            assign_left = not assign_left

    # Разпределение на останалите клиенти
    for row in range(rows):
        current_row_clients = other_clients[row * seats_per_row: (row + 1) * seats_per_row]
        if not current_row_clients:
            break

        mid_index = seats_per_row // 2
        left_idx = mid_index - 1
        right_idx = mid_index if seats_per_row % 2 == 1 else mid_index + 1

        if current_row_clients:
            seating_chart[row][mid_index] = current_row_clients.pop(0)
            seating_chart[row][mid_index]['row'] = row + 1
            seating_chart[row][mid_index]['seat'] = mid_index + 1

        assign_left = True
        while current_row_clients:
            if assign_left and left_idx >= 0:
                seating_chart[row][left_idx] = current_row_clients.pop(0)
                seating_chart[row][left_idx]['row'] = row + 1
                seating_chart[row][left_idx]['seat'] = left_idx + 1
                left_idx -= 1
            elif right_idx < seats_per_row:
                seating_chart[row][right_idx] = current_row_clients.pop(0)
                seating_chart[row][right_idx]['row'] = row + 1
                seating_chart[row][right_idx]['seat'] = right_idx + 1
                right_idx += 1
            assign_left = not assign_left

    return seating_chart


def display_seating_chart(seating_chart, rows, seats_per_row):
    print("\nТекущо състояние на схемата на местата:")
    for row in range(rows):
        row_display = ""
        for seat in range(seats_per_row):
            if seating_chart[row][seat]:
                client = seating_chart[row][seat]
                display_info = f"{client['name'][0]}{client['height']} ({client['sale_number']})"
                if client['is_disabled']:
                    display_info += "i"
                row_display += f"[{display_info}]"
            else:
                row_display += "[ ]"
        print(f"Ред {row + 1}: {row_display}")


def display_ticket_numbers(seating_chart, rows, seats_per_row):
    print("\nСхема на местата с номера на билетите:")
    for row in range(rows):
        row_display = ""
        for seat in range(seats_per_row):
            if seating_chart[row][seat]:
                client = seating_chart[row][seat]
                row_display += f"[{client['sale_number']}]"
            else:
                row_display += "[ ]"
        print(f"Ред {row + 1}: {row_display}")


def are_all_seats_sold(seating_chart, rows, seats_per_row):
    for row in range(rows):
        for seat in range(seats_per_row):
            if seating_chart[row][seat] is None:
                return False
    return True


def display_all_sales(seating_info, total_seats):
    print("\nСправка за продажбите:")
    for i in range(1, total_seats + 1):
        sale_number = f"x{i}"
        client = next((client for client in seating_info if client['sale_number'] == sale_number), None)
        if client:
            status = (
                f"Име: {client['name']}, "
                f"Билет: {client['ticket_number']}, "
                f"Ръст: {client['height']} см, "
                f"Ред: {client['row']}, "
                f"Място: {client['seat']}"
            )
        else:
            status = "Отказан билет"
        print(f"{sale_number}: {status}")


def main():
    start_date, end_date = get_dates()
    rows, seats_per_row = get_seat_info()
    total_seats = rows * seats_per_row

    seating_info = []
    used_ticket_numbers = set()
    sale_count = 1

    while True:
        print("\n1. Продажба на билет")
        print("2. Отмяна на билет")
        print("3. Преглед на заетите места")
        print("4. Преглед на местата с номера на билетите")
        print("5. Справка за продажбите")
        print("6. Изход")
        choice = input("Изберете опция: ")

        if choice == '1':
            if not is_sale_period_valid(start_date, end_date):
                print("Продажбата на билети е прекратена поради изтичане на периода.")
                break

            client = get_client_info(used_ticket_numbers, sale_count)
            seating_info.append(client)
            sale_count += 1

            seating_info = sort_clients(seating_info)
            seating_chart = arrange_seating(seating_info, rows, seats_per_row)

            print(
                f"Билет закупен успешно! Номер на билета: {client['ticket_number']} "
                f"(Продажба: {client['sale_number']})")

            if are_all_seats_sold(seating_chart, rows, seats_per_row):
                print("Всички места са продадени. Програмата приключва.")
                break

        elif choice == '2':
            name_to_cancel = input("Въведете име на клиента за отмяна на билета: ")
            found = False
            for client in seating_info:
                if client['name'] == name_to_cancel:
                    used_ticket_numbers.discard(client['ticket_number'])
                    seating_info.remove(client)
                    print(f"Билетът на {name_to_cancel} е отменен. (Продажба: {client['sale_number']})")
                    found = True
                    break
            if not found:
                print("Не е намерен клиент с това име.")
            else:
                seating_info = sort_clients(seating_info)
                seating_chart = arrange_seating(seating_info, rows, seats_per_row)

        elif choice == '3':
            seating_chart = arrange_seating(seating_info, rows, seats_per_row)
            display_seating_chart(seating_chart, rows, seats_per_row)

        elif choice == '4':
            seating_chart = arrange_seating(seating_info, rows, seats_per_row)
            display_ticket_numbers(seating_chart, rows, seats_per_row)

        elif choice == '5':
            display_all_sales(seating_info, total_seats)

        elif choice == '6':
            print("Програмата приключва.")
            break


if __name__ == "__main__":
    main()
