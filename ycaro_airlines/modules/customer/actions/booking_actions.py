import re
import questionary
from ycaro_airlines.models import Flight, Booking, Customer
from ycaro_airlines.menus import console
from rich.table import Table
from rich.console import Console

from ycaro_airlines.models.flight import SeatStatus


def book_flight_action(user: Customer):
    flight_id = questionary.autocomplete(
        "Type the id of the flight you want to book:(type q to go back)",
        choices=[str(k) for k, _ in Flight.flights.items()],
        validate=lambda x: True
        if x in {str(k) for k, _ in Flight.flights.items()} or x == "q"
        else False,
    ).ask()

    if flight_id == "q" or not flight_id:
        return

    flight = Flight.flights[int(flight_id)]
    flight.print_flight_table(console)

    wants_to_book = questionary.confirm(
        "Are you sure you want to book this flight?"
    ).ask()

    if not wants_to_book:
        return

    passenger_name = questionary.text("Type passenger name:").ask()
    passenger_cpf = questionary.text(
        "Type passenger cpf",
        validate=lambda x: True
        if re.fullmatch(r"^\d{3}\.\d{3}\.\d{3}\-\d{2}$", x)
        else False,
    ).ask()
    if not passenger_name or not passenger_cpf:
        print("Operation Cancelled")
        return

    # voce quer comprar essa passagem
    booking = Booking(flight, user.id, passenger_name, passenger_cpf)

    wants_to_spend_loyalty_points = questionary.confirm(
        f"Do you wish to spend loyalty points to get a discount?(you have: {user.loyalty_points} loyalty points)"
    ).ask()

    if wants_to_spend_loyalty_points:
        loyalty_points_spent = int(
            questionary.text(
                "how many loyalty points do you wish to spend?(1 Loyalty Point = R$1.00)",
                validate=lambda x: True
                if re.fullmatch("[0-9]+", x) and int(x) <= user.loyalty_points
                else False,
            ).ask()
        )

        if loyalty_points_spent > booking.price:
            loyalty_points_spent = int(booking.price)

        user.spend_loyalty_points(int(loyalty_points_spent))
        booking.price -= loyalty_points_spent

    wants_to_select_seat = questionary.confirm(
        "Do you want to choose this seat for R$40.00?"
    ).ask()

    if wants_to_select_seat:
        booking.price += 40
        select_seat_action(booking)

    print("Flight booked!")


def show_baggage_information(booking: Booking, console: Console):
    _ = booking
    table = Table(title="Baggage")
    table.add_column("Type")
    table.add_column("Description")
    table.add_column("Fee")

    table.add_row(
        "Additional Baggage", "Baggage above the limit", "R$149.99/Additional baggage"
    )
    table.add_row(
        "Overweight Baggage",
        "Hand baggage over 13kg e dispatched Baggage over 23kg",
        "R$19.99/per kg above the limit",
    )
    table.add_row(
        "Oversized Baggage",
        "Baggage with dimensions over 300 linear cm(height+width+length)",
        "R$10.00/per cm above the limit",
    )
    console.print(table)


def select_seat_action(booking: Booking):
    seat = questionary.autocomplete(
        "Which seat do you want?",
        choices=[
            str(k)
            for k, v in booking.flight.seats.items()
            if v.status is SeatStatus.open
        ],
        validate=lambda x: True
        if x
        in {
            str(k)
            for k, v in booking.flight.seats.items()
            if v.status is SeatStatus.open
        }
        else False,
    ).ask()

    if not seat:
        return False

    seat = int(seat)

    booking.reserve_seat(seat)


def cancel_booking_action(user: Customer, booking: Booking):
    confirmation = questionary.confirm(
        "Are you sure you want to cancel this booking?"
    ).ask()

    if not confirmation:
        return

    if booking.owner_id != user.id:
        print("You dont own this booking!")

    booking.cancel_booking()


def check_in_action(user: Customer, booking: Booking):
    if user.id != booking.owner_id:
        print("You arent the owner of this booking!")
        return

    name_confirmation = questionary.text(
        "Confirm passenger name:",
        validate=lambda x: True if re.fullmatch(r"^[a-zA-Z ]+$", x) else False,
    ).ask()

    if not name_confirmation:
        return

    if name_confirmation != booking.passenger_name:
        print("Incorrect name!")
        return

    cpf_confirmation = questionary.text(
        "Confirm passenger cpf:",
        validate=lambda x: True
        if re.fullmatch(r"^\d{3}\.\d{3}\.\d{3}\-\d{2}$", x)
        else False,
    ).ask()

    if cpf_confirmation != booking.passenger_cpf:
        print("incorrect cpf!")
        return

    confirm_check_in = questionary.confirm(
        "Are you sure you want to check-in this booking?"
    )

    if not confirm_check_in:
        return

    if booking.seat is None:
        select_seat_action(booking)

    confirm_change_seat = questionary.confirm("Do you want to change seats?")
    if confirm_change_seat:
        select_seat_action(booking)

    if not booking.check_in():
        print("Couldn't check-in booking")
        return

    user.gain_loyalty_points(int(booking.price // 10))

    see_baggage_information: bool = questionary.confirm(
        "Do you want to check baggage information and fees?"
    ).ask()

    if see_baggage_information:
        show_baggage_information(booking, console)
        questionary.press_any_key_to_continue()
