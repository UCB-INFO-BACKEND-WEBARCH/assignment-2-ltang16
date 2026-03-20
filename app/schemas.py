from marshmallow import Schema, fields, validate, validates, ValidationError



# Schema for category response output
class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, unique=True, validate=validate.Length(max=50))
    color = fields.Str(validate=validate.Length(max=7))
    tasks = fields.List(fields.Nested(TaskSchema, many=True), dump_only=True) #TODO: HOW TO RESOLVE SCHEMAS NEEDING EACH OTHER IN DEFINITION?



# Schema for category creation input
class CategoryCreateSchema(Schema):
    name = fields.Str(required=True, unique=True, validate=validate.Length(min=1, max=50))
    color = fields.Str(validate=validate.Length(max=7))

    # Unique validator for color hexcode -- must be 7 characters (including #) with values between 0-F (uppercase only)
    @validates("color")
    def reject_invalid_hexcolor(self, value, **kwargs):
        if len(value) != 7:
            raise ValidationError("Valid hexcodes must be 7 characters long, including #.")
        elif value[0] != "#":
            raise ValidationError("The hexcode must start with #.")
        elif not any([c in "0123456789ABCDEF" for c in value[1:]]):
            raise ValidationError("Each character of a valid hexcode must be in the numeric range 0-9 or A-F.")



# Schema for task response output
class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(max=100))
    description = fields.Str(validate=validate.Length(max=500))
    completed = fields.Bool(dump_default=False)
    due_date = fields.DateTime()
    category_id = fields.Int()
    category = fields.Nested(CategorySchema)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()



# Schema for task creation input
class TaskCreateSchema(Schema):
    