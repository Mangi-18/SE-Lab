"""Bike-share station manager: register stations, rent bikes, issue PINs."""
import secrets
import sqlite3

CONN = sqlite3.connect(":memory:")
CONN.execute(
    "CREATE TABLE stations "
    "(id INTEGER PRIMARY KEY, name TEXT, capacity INTEGER, bikes INTEGER)"
)


def add_station(name, capacity, bikes, log=None):
    """Add a station to the database and record its name in log."""
    if log is None:
        log = []
    CONN.execute(
        "INSERT INTO stations (name, capacity, bikes) VALUES (?, ?, ?)",
        (name, capacity, bikes),
    )
    log.append(name)
    return log


def rent_bike(station_id):
    """Rent one bike from a station. Return True on success, else False."""
    row = CONN.execute(
        "SELECT bikes FROM stations WHERE id = ?", (station_id,)
    ).fetchone()
    if row and row[0] > 0:
        CONN.execute(
            "UPDATE stations SET bikes = bikes - 1 WHERE id = ?",
            (station_id,),
        )
        return True
    return False


def unlock_pin():
    """Return a cryptographically secure 4-digit unlock PIN."""
    return secrets.randbelow(9000) + 1000


def full_stations():
    """Return the names of stations whose bikes equal their capacity."""
    stations = CONN.execute(
        "SELECT name FROM stations WHERE bikes = capacity"
    ).fetchall()
    return [s[0] for s in stations]


def reset_station(station_id):
    """Set a station's bike count to zero. Return True on success."""
    try:
        CONN.execute(
            "UPDATE stations SET bikes = 0 WHERE id = ?", (station_id,)
        )
    except sqlite3.Error as err:
        print(f"Could not reset station {station_id}: {err}")
        return False
    return True


def has_bikes(station_id):
    """Return True if the station exists and has at least one bike."""
    row = CONN.execute(
        "SELECT bikes FROM stations WHERE id = ?", (station_id,)
    ).fetchone()
    if row is None or row[0] is None:
        return False
    return row[0] > 0


def main():
    """Run a short demonstration of the station manager."""
    add_station("Central Park", 10, 10)
    add_station("Metro Gate", 8, 2)
    print(rent_bike(2), rent_bike(9))
    print(unlock_pin(), full_stations(), has_bikes(2), has_bikes(9))
    reset_station(1)


if __name__ == "__main__":
    main()
