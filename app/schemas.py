from marshmallow import Schema, fields, validate, validates, ValidationError



# Plain task schema (used in task list when getting all tasks of a category)
class PlainTaskSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(max=100))
    completed = fields.Bool(dump_default=False)



# Plain category schema (used in category section of individual task)
class PlainCategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, unique=True, validate=validate.Length(max=50))
    color = fields.Str(validate=validate.Length(max=7))



# Schema for task response output (builds on plain task schema)
class TaskSchema(PlainTaskSchema):
    description = fields.Str(validate=validate.Length(max=500))
    due_date = fields.DateTime(format="iso")
    category_id = fields.Int()
    category = fields.Nested(PlainCategorySchema)
    created_at = fields.DateTime(format="iso")
    updated_at = fields.DateTime(format="iso")



# Schema for task creation input
class TaskCreateSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(max=100))
    description = fields.Str(validate=validate.Length(max=500))
    due_date = fields.DateTime(format="iso")
    category_id = fields.Int()



# Schema for task update input
class TaskUpdateSchema(Schema):
    title = fields.Str(validate=validate.Length(max=100))
    description = fields.Str(validate=validate.Length(max=500))
    completed = fields.Bool()
    due_date = fields.DateTime(format="iso")
    category_id = fields.Int()
    created_at = fields.DateTime(format="iso")
    updated_at = fields.DateTime(format="iso")



# Schema for category response output
class CategorySchema(PlainCategorySchema):
    tasks = fields.List(fields.Nested(PlainTaskSchema, many=True), dump_only=True)



# Schema for category creation input
class CategoryCreateSchema(Schema):
    name = fields.Str(required=True, unique=True, validate=validate.Length(min=1, max=50))
    color = fields.Str(validate=validate.Length(max=7))

    # Unique validator for color hexcode -- must be 7 characters (including #) with values between 0-F (uppercase only)
    @validates("color")
    def reject_invalid_hexcolor(self, value):
        if len(value) != 7:
            raise ValidationError("Valid hexcodes must be 7 characters long, including #.")
        elif value[0] != "#":
            raise ValidationError("The hexcode must start with #.")
        elif any([c not in "0123456789ABCDEF" for c in value[1:]]):
            raise ValidationError("Each character of a valid hexcode must be in the numeric range 0-9 or A-F.")