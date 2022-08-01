from odoo import fields, models


class Course(models.Model):
    _name = "course"
    _description = "Course"

    title = fields.Char(required=True)
    description = fields.Text()
    responsible_id = fields.Many2one("res.users", "Responsible")
    session_ids = fields.One2many("session", "course_id")

    def copy(self):
        default = {}
        default.update({
            "title": f"Copy of {self.title}"
        })

        return super(Course, self).copy(default)
