from marshmallow import Schema, fields, validate

class CropDataSchema(Schema):
    """
    Schema for incoming Crop Data.
    
    It is needed for validating incoming data before passing them to
    the Crop Yield prediction model.
    """

    area = fields.String(validate=validate.OneOf([
        "albania", "algeria", "angola", "argentina", "armenia",
        "australia", "austria", "azerbaijan", "bahamas", "bahrain",
        "bangladesh", "belarus", "belgium", "botswana", "brazil",
        "bulgaria", "burkina_faso", "burundi", "cameroon", "canada",
        "central_african_republic", "chile", "colombia", "croatia",
        "denmark", "dominican_republic", "ecuador", "egypt", "el_salvador",
        "eritrea", "estonia", "finland", "france", "germany", "ghana",
        "greece", "guatemala", "guinea", "guyana", "haiti", "honduras",
        "hungary", "india", "indonesia", "iraq", "ireland", "italy",
        "jamaica", "japan", "kazakhstan", "kenya", "latvia", "lebanon",
        "lesotho", "libya", "lithuania", "madagascar", "malawi",
        "malaysia", "mali", "mauritania", "mauritius", "mexico",
        "montenegro", "morocco", "mozambique", "namibia", "nepal",
        "netherlands", "new_zealand", "nicaragua", "niger", "norway",
        "pakistan", "papua_new_guinea", "peru", "poland", "portugal",
        "qatar", "romania", "rwanda", "saudi_arabia", "senegal",
        "slovenia", "south_africa", "spain", "sri_lanka", "sudan",
        "suriname", "sweden", "switzerland", "tajikistan", "thailand",
        "tunisia", "turkey", "uganda", "ukraine", "united_kingdom",
        "uruguay", "zambia", "zimbabwe"
    ]))
    item = fields.String(validate=validate.OneOf([
        "maize", "potatoes", "rice_paddy", "sorghum", "soybeans", "wheat",
        "cassava", "sweet_potatoes", "plantains_and_others", "yams"
    ]))
    year = fields.Integer()
    average_rain_fall_mm_per_year = fields.Float()
    pesticides_tonnes = fields.Float()
    avg_temp = fields.Float()
