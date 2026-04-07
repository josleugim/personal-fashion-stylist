import enum

class WardrobeCategory(enum.Enum):
    TOP = "top"
    BOTTOM = "bottom"
    SHOES = "shoes"
    OUTERWEAR = "outerwear"
    ACCESSORY = "accessory"
    BAG = "bag"
    DRESS = "dress"
    ACTIVEWEAR = "activewear"
    UNDERWEAR = "underwear"

class WardrobeSubcategory(enum.Enum):
    # Tops
    T_SHIRT = "t-shirt"
    SHIRT = "shirt"
    BLOUSE = "blouse"
    SWEATER = "sweater"
    HOODIE = "hoodie"
    TANK_TOP = "tank-top"
    # Bottoms
    JEANS = "jeans"
    TROUSERS = "trousers"
    SHORTS = "shorts"
    SKIRT = "skirt"
    LEGGINGS = "leggings"
    # Shoes
    SNEAKERS = "sneakers"
    BOOTS = "boots"
    HEELS = "heels"
    SANDALS = "sandals"
    LOAFERS = "loafers"
    FLATS = "flats"
    # Outerwear
    JACKET = "jacket"
    COAT = "coat"
    BLAZER = "blazer"
    # Accessories
    HAT = "hat"
    BELT = "belt"
    SCARF = "scarf"
    SUNGLASSES = "sunglasses"
    JEWELRY = "jewelry"
    # Bags
    TOTE = "tote"
    BACKPACK = "backpack"
    CROSSBODY = "crossbody"
    CLUTCH = "clutch"