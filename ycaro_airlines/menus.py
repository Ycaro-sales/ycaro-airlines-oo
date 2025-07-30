from functools import partial
from datetime import datetime
from typing import Any, Callable, Tuple, Dict, Optional
from questionary import Choice, question
import questionary
from rich.console import Console
from rich.table import Table
from ycaro_airlines.models import BookingStatus, Flight, Customer, Booking


# ╭─ hello ─────────╮
# │ <1> - oi        │
# │ <2> - tchau     │
# ╰─────────────────╯

console = Console()


def menu_factory(title: str, options: list[Tuple[str, Callable]]):
    choices: list[Choice] = [Choice(c[0], c[1]) for c in options]
    choices.append(Choice("Go Back", value=""))

    def menu() -> Any:
        while True:
            selection = questionary.select(title, choices=choices).ask()
            match selection:
                case "":
                    break
                case _:
                    selection()

    return menu


def customer_menu(user: Customer):
    options: list[Tuple[str, Callable]] = [
        ("Ver Voos", partial(flights_menu, user=user)),
        ("Ver bilhetes", partial(bookings_menu, user=user)),
    ]

    menu_factory("Customer Menu", options)()


def select_seat_action(booking: Booking):
    seat = int(
        questionary.autocomplete(
            "Qual assento voce deseja?",
            choices=[str(i) for i, v in enumerate(booking.flight.seats) if v is None],
            validate=lambda x: True
            if x in {str(i) for i, v in enumerate(booking.flight.seats) if v is None}
            else False,
        ).ask()
    )
    booking.select_seat(seat)


def create_booking_action(user: Customer):
    flight_id = questionary.autocomplete(
        "Insira o id do voo que voce quer comprar a passagem:",
        choices=[str(k) for k, _ in Flight.flights.items()],
        validate=lambda x: True
        if x in {str(k) for k, _ in Flight.flights.items()}
        else False,
    ).ask()

    flight = Flight.flights[int(flight_id)]
    flight.print_flight_table(console)

    wants_to_book = questionary.confirm("Voce quer comprar essa passagem?").ask()
    if not wants_to_book:
        return

    # voce quer comprar essa passagem
    booking = Booking(flight, user)

    wants_to_select_seat = questionary.confirm("Voce quer escolher um assento?").ask()

    if wants_to_select_seat:
        select_seat_action(booking)

    # TODO: show flight id
    print("Flight booked")

    # see departure and arrival


def cancel_booking_action(user: Customer, booking: Booking):
    confirmation = questionary.confirm(
        "Voce tem certeza que voce quer cancelar essa passagem?"
    ).ask()

    if not confirmation or booking.owner.id != user.id:
        return

    booking.cancel_booking()


def show_baggage_information(booking: Booking, console: Console):
    _ = booking
    table = Table(title="Bagagem")
    table.add_column("Tipo")
    table.add_column("Descrição")
    table.add_column("Preço")

    table.add_row(
        "Peça Adicional", "Bagagem Extra Transportada", "R$149.99/Bagagem adicional"
    )
    table.add_row(
        "Excesso de peso",
        "Bagagem de mão acima de 13 kg e Bagagem despachada acima de 23 kg",
        "R$19.99/por kg acima do limite",
    )
    table.add_row(
        "Sobredimensão",
        "Bagagem com dimensões superiores a 300 cm lineares(altura+comprimento+largura)",
        "R$10.00/Centimetro acima do limite",
    )
    console.print(table)


# TODO: finish function
def check_in_action(booking: Booking):
    name_confirmation = questionary.text("Confirme o seu nome:").ask()
    if name_confirmation != booking.owner.username:
        print("Nome Incorreto!")

    confirm_check_in = questionary.confirm(
        "Voce tem certeza que quer fazer o check-in?"
    )

    if not confirm_check_in:
        return

    booking.check_in()

    if booking.seat is None:
        select_seat_action(booking)

    see_baggage_information: bool = questionary.confirm(
        "Voce quer ver informacoes sobre bagagens e taxas?"
    ).ask()

    if see_baggage_information:
        show_baggage_information(booking, console)
        questionary.press_any_key_to_continue()


def bookings_menu(user: Customer):
    Booking.print_bookings_table(user, console)

    booking_id = questionary.autocomplete(
        "Insira o id da passagem que voce deseja gerenciar: ",
        choices=[str(i.id) for i in Booking.list_bookings(user)],
        validate=lambda x: True
        if x in {str(i.id) for i in Booking.list_bookings(user)}
        else False,
    ).ask()

    booking = Booking.bookings[int(booking_id)]
    booking.print_booking_table(console)

    options: list[Tuple[str, Callable]] = [
        (
            "Cancelar Passagem",
            partial(cancel_booking_action, user=user, booking=booking),
        ),
        ("Modificar Assento", partial(select_seat_action, booking=booking)),
        ("Check-in Online", partial(check_in_action, booking=booking)),
    ]

    if booking.status != BookingStatus.booked:
        options = [
            (
                "Ver passagem",
                partial(booking.print_booking_table, console=console),
            )
        ]

    menu_factory("Booking management", options)()


def flight_search_action():
    options: list[str] = [
        "preço",
        "cidade",
        "data de saida",
        "data de chegada",
    ]

    selected = questionary.checkbox("Como voce quer filtrar?", choices=options).ask()

    filtered_list = Flight.list_flights()

    if "preço" in selected:
        filter_by_price(filtered_list)

    if "cidade" in selected:
        pass

    if "data de saida" in selected:
        pass

    if "data de chegad" in selected:
        pass


def flights_menu(user: Customer):
    options: list[Tuple[str, Callable]] = [
        ("Comprar Passagem", partial(create_booking_action, user=user)),
        ("Buscar Voo", flight_search_action),
    ]

    Flight.print_flights_table(console)

    menu_factory("Flights", options)()


def filter_by_city(
    flights: Dict[int, Flight], From: Optional[str] = None, To: Optional[str] = None
):
    filtered_list = flights.values()

    if From is not None:
        filtered_list = [x for x in filtered_list if x.From == From]

    if To is not None:
        filtered_list = [x for x in filtered_list if x.To == To]

    return filtered_list


def filter_by_date2(
    flights: Dict[int, Flight],
    date_lte: Optional[datetime] = None,
    date_gte: Optional[datetime] = None,
    departure: bool = False,
):
    filtered_list = flights.values()

    if departure:
        if date_lte is not None:
            filtered_list = [x for x in filtered_list if x.departure <= date_lte]

        if date_gte is not None:
            filtered_list = [x for x in filtered_list if x.departure >= date_gte]
    else:
        if date_lte is not None:
            filtered_list = [x for x in filtered_list if x.arrival <= date_lte]

        if date_gte is not None:
            filtered_list = [x for x in filtered_list if x.arrival >= date_gte]

    return filtered_list


def filter_by_price(
    flights: list[Flight],
    price_lte: Optional[float] = None,
    price_gte: Optional[float] = None,
):
    filtered_list = flights.values()

    if price_lte is not None:
        filtered_list = [x for x in filtered_list if x.price <= price_lte]

    if price_gte is not None:
        filtered_list = [x for x in filtered_list if x.price >= price_gte]

    return filtered_list
