from marshmallow import Schema, fields

# User schema
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(load_only=True, required=True)



# Trip schema
class TripSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    start_date = fields.Date()
    end_date = fields.Date()
    user_id = fields.Int(dump_only=True)



# Country schema
class CountrySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    budget = fields.Float()
    trip_id = fields.Int(dump_only=True)


# Expense schema
class ExpenseSchema(Schema):
    id = fields.Int(dump_only=True)
    description = fields.Str(required=True)
    amount = fields.Float(required=True)
    country_id = fields.Int(dump_only=True)
    

user_schema = UserSchema()
users_schema = UserSchema(many=True)

trip_schema = TripSchema()
trips_schema = TripSchema(many=True)

country_schema = CountrySchema()
countries_schema = CountrySchema(many=True)

expense_schema = ExpenseSchema()
expenses_schema = ExpenseSchema(many=True)
