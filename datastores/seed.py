from datastores.database import SessionLocal, engine, Base
from datastores.models import Driver

Base.metadata.create_all(bind=engine)

db = SessionLocal()

drivers = [
    Driver(name="John Mwangi", age=34, city="Nairobi", rating=4.5),
    Driver(name="Amina Hassan", age=29, city="Mombasa", rating=4.7),
    Driver(name="Peter Otieno", age=41, city="Kisumu", rating=4.2),
    Driver(name="Grace Wanjiku", age=26, city="Nakuru", rating=4.8),
    Driver(name="David Kamau", age=38, city="Eldoret", rating=4.3),
]

db.add_all(drivers)
db.commit()
db.close()

print("Database seeded successfully!")