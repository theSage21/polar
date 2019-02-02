import bottle
from bottle_tools import fill_args
from db import Ship, TrackPoint


app = bottle.Bottle()


@app.get("/")
def home():
    return bottle.template("index.html")


@app.get("/api/ships")
@fill_args
def ship_items(offset=0, limit=10):
    total = Ship.select().count()
    return {
        "ships": list(Ship.select().offset(offset).limit(limit).dicts()),
        "total": total,
    }


@app.get("/api/positions/<imo>")
def ship_positions(imo):
    data = {
        "positions": list(
            TrackPoint.select(TrackPoint.lat.alias('latitute'), TrackPoint.lng.alias('longitude'))
            .join(Ship)
            .where(TrackPoint.ship.imo == int(imo))
            .dicts()
        )
    }
    return data


if __name__ == "__main__":
    app.run(port=8000, reloader=True)
