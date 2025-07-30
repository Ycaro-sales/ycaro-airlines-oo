from enum import Enum
from typing import Dict
from datetime import timedelta


class cities(Enum):
    Maceio = "Maceio"
    Recife = "Recife"
    Aracaju = "Aracaju"
    Joao_pessoa = "Joao Pessoa"

    @classmethod
    def distance(cls, city1: "cities", city2: "cities"):
        distances: Dict[cities, Dict[cities, timedelta]] = {
            cities.Maceio: {
                cities.Aracaju: timedelta(hours=1),
                cities.Recife: timedelta(hours=1),
                cities.Joao_pessoa: timedelta(hours=2),
            },
            cities.Aracaju: {
                cities.Maceio: timedelta(hours=1),
                cities.Recife: timedelta(hours=2),
                cities.Joao_pessoa: timedelta(hours=3),
            },
            cities.Recife: {
                cities.Maceio: timedelta(hours=1),
                cities.Joao_pessoa: timedelta(hours=1),
                cities.Aracaju: timedelta(hours=2),
            },
            cities.Joao_pessoa: {
                cities.Aracaju: timedelta(hours=3),
                cities.Maceio: timedelta(hours=2),
                cities.Recife: timedelta(hours=1),
            },
        }
        return distances[city1][city2]
