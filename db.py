import peewee as pw

db = pw.SqliteDatabase("data.sqlite3")


class Ship(pw.Model):
    name = pw.CharField()
    imo = pw.IntegerField(unique=True)

    class Meta:
        database = db


class TrackPoint(pw.Model):
    lng = pw.FloatField()
    lat = pw.FloatField()
    stamp = pw.DateTimeField()
    ship = pw.ForeignKeyField(Ship)

    class Meta:
        database = db


db.connect()
db.create_tables([Ship, TrackPoint])

if __name__ == "__main__":
    import pandas as pd
    import argparse
    import arrow

    parser = argparse.ArgumentParser()
    parser.add_argument("csv", help="Load data from this CSV")
    args = parser.parse_args()

    df = pd.read_csv(args.csv, header=None)
    df.columns = ["imo", "stamp", "lat", "lng"]

    Ship.insert_many(
        [
            {"imo": 9632179, "name": "Mathilde Maersk"},
            {"imo": 9247455, "name": "Australian Spirit"},
            {"imo": 9595321, "name": "MSC Preziosa"},
        ]
    ).execute()
    print(Ship.select().count(), "ships inserted")
    ships = {s.imo: s for s in Ship.select()}
    with db.atomic():
        for batch in pw.chunked(
            [
                {
                    "ship": ships[i],
                    "stamp": arrow.get(date).datetime,
                    "lat": lat,
                    "lng": lng,
                }
                for _, (i, date, lat, lng) in df.iterrows()
            ],
            100,
        ):
            TrackPoint.insert_many(batch).execute()
    print(TrackPoint.select().count(), "track points inserted")
