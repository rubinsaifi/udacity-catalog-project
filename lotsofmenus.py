from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Sport, Base, MenuItem, User

engine = create_engine('sqlite:///sportitemwithusers.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create dummy user
User1 = User(
  name="Robo Barista", email="tinnyTim@udacity.com",
  picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829e\
    d78203a5a36dd364160_400x400.png'
)
session.add(User1)
session.commit()

sport1 = Sport(user_id=1, name="Soccer")

session.add(sport1)
session.commit()

menuItem1 = MenuItem(
  user_id=1,
  name="Soccer Shoes & Cleats",
  description=(
    "Firm Ground cleats are defined as cleats that are made "
    "typicallyfor use on natural surfaces such as dirt and grass. These "
    "cleats are equipped with large studs on the bottom of the "
    "shoe to assist in gripping the surface and preventing sliding and "
    "assisting in rapid directional changes."
  ),
  price="$22.50",
  sport_item="shoe",
  sport=sport1)

session.add(menuItem1)
session.commit()


menuItem2 = MenuItem(
  user_id=1,
  name="Soccer Balls",
  description=(
    "The standard soccer ball is made of synthetic leather, usually "
    "polyurethane or polyvinyl chloride, stitched around an inflated rubber or"
    " rubber-like bladder. Few of the manufacturers are Adidas, Nike, Puma, "
    "Mitre, etc."
  ),
  price="$15.49",
  sport_item="ball",
  sport=sport1)

session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(
  user_id=1,
  name="Soccer Shin Guards",
  description=(
    "Shin guards are one of the suggested preventive methods. "
    "Their main function is to protect the soft tissues and bones in the "
    "lower extremities from external impact. Shin guards provide shock "
    "absorption and facilitate energy dissipation, thereby decreasing the "
    "risk of serious injuries."
  ),
  price="$7.49",
  sport_item="guard",
  sport=sport1)

session.add(menuItem3)
session.commit()

menuItem4 = MenuItem(
  user_id=1,
  name="Soccer Goals, Nets & Rebounders",
  description=(
    "Based on FIFA guidelines, the posts must be round, "
    "rectangular, elliptical or square in shape and should pose no harm "
    "to players. The posts should sit in 8 yards (7.32 meters) from each "
    "other. The lower crossbar edge should sit 8 feet (2.44 meters) "
    "above the ground."
  ),
  price="$49.65",
  sport_item="net",
  sport=sport1)

session.add(menuItem4)
session.commit()

menuItem5 = MenuItem(
  user_id=1,
  name="Goalkeeper Gloves",
  description=(
    "Most goalkeepers wear gloves to protect their hands "
    "and enhance their grip of the ball. Like every player on the pitch, "
    "they are required to wear shin guards. The goalkeeper is allowed to "
    "catch the ball, and is also allowed to punch or deflect the ball "
    "away from the goal."
  ),
  price="$25.00",
  sport_item="glove",
  sport=sport1)

session.add(menuItem5)
session.commit()


# Menu for Cricket
sport2 = Sport(user_id=1, name="Cricket")

session.add(sport2)
session.commit()

menuItem1 = MenuItem(
  user_id=1,
  name="Ball",
  description=(
    "A red, white or pink ball with a cork base, wrapped in "
    "twine covered with leather. The ball should have a circumference of "
    "9.1 in (23 centimetres) unless it is a children's size."
  ),
  price="$11.99",
  sport_item="ball",
  sport=sport2)

session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(
  user_id=1,
  name="Bat",
  description=(
    "A wooden bat is used. The wood used is from the Kashmir or "
    "English willow tree. The bat cannot be more than 38 inches (96.5 cm) "
    "long and 4.25 inches (10.8 cm) wide. Aluminum bats are not allowed. "
    "The bat has a long handle and one side has a smooth face."
  ),
  price="$212.12",
  sport_item="bat",
  sport=sport2)

session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(
  user_id=1,
  name="Stumps",
  description=(
   "three upright wooden poles that, together with the bails, "
    "form the wicket."
  ),
  price="$16.99",
  sport_item="stump",
  sport=sport2)

session.add(menuItem3)
session.commit()

menuItem4 = MenuItem(
  user_id=1,
  name="Stumps",
  description=(
    "three upright wooden poles that, together with the bails, "
    "form the wicket."
  ),
  price="$16.99",
  sport_item="stump",
  sport=sport2)

session.add(menuItem4)
session.commit()


# Tennis items
sport3 = Sport(user_id=1, name="Tennis")

session.add(sport3)
session.commit()

menuItem1 = MenuItem(
  user_id=1,
  name="Tennis Strings",
  description=(
    "There are so many different types of tennis strings, it is "
    "impossible to keep track of the developments! At the pro level strings "
    "can play a big role and Luxilon strings have certainly had an influence "
    "on how the professional game is played these days!. It is important to "
    "remember though that for most recreational players the type of string "
    "does not matter nearly as much as most people believe!"
  ),
  price="$150.99",
  sport_item="string",
  sport=sport3)

session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(
  user_id=1,
  name="Tennis Balls",
  description=(
    "Tennis players are already confused with choosing rackets "
    "and strings but nowadays there is also a big variety on tennis balls "
    "available. Balls usually vary in pressure and the amount of felt that "
    "surrounds the core. I have no particular recommendation as for which "
    "balls to play with. Use a ball that you are comfortable playing with!"
  ),
  price="$10.39",
  sport_item="ball",
  sport=sport3)

session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(
  user_id=1,
  name="Tennis Grips",
  description=(
    "The grip on a tennis racket also comes in different forms. "
    "You can either use a leather grip, like the ones that are usually on "
    "the racket when you buy it or you can put a grip on top, which is called "
    "an overgrip. The leather ones are more expensive to replace but they "
    "also last a lot longer. If you use a leather grip or an overgrip is "
    "simply a matter of feel and preference."
  ),
  price="$10.39",
  sport_item="grip",
  sport=sport3)

session.add(menuItem3)
session.commit()

menuItem4 = MenuItem(
  user_id=1,
  name="Sweat bands",
  description=(
    "In hotter climates sweat bands can be very important for "
    "tennis players. Getting sweat on your grip can be really annoying!"
  ),
  price="$5.49",
  sport_item="band",
  sport=sport3)

session.add(menuItem4)
session.commit()

# Swimming item
sport4 = Sport(user_id=1, name="Swimming")

session.add(sport4)
session.commit()

menuItem1 = MenuItem(
  user_id=1,
  name="Kickboard",
  description="Boards to Surf on water",
  price="$15.99",
  sport_item="board",
  sport=sport4)

session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(
  user_id=1,
  name="Towel",
  description="Towels to dry and wrap body after swimming.",
  price="$10.00",
  sport_item="towel",
  sport=sport4)

session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(
  user_id=1,
  name="Swim Cap",
  description="Swiming Caps to cover face while resting near water.",
  price="$25.10",
  sport_item="cap",
  sport=sport4)

session.add(menuItem3)
session.commit()
