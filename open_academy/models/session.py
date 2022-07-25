from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class Session(models.Model):
    _name = "session"
    _description = "Session"

    name = fields.Char(required=True)
    start_date = fields.Date(default=lambda self: fields.Date.today(self))
    duration = fields.Float()
    seats = fields.Integer(string="Number of seats")
    percent_seats = fields.Integer(string="Taken seats %", compute="_compute_seats")
    attendee_count = fields.Integer(compute="_compute_seats", store=True)
    active = fields.Boolean(default=True)
    instructor_id = fields.Many2one("res.partner", domain="[('instructor', '=', True)]")
    course_id = fields.Many2one("course")
    attendee_ids = fields.Many2many("res.partner")

    @api.depends("seats", "attendee_ids")
    def _compute_seats(self):
        for record in self:
            if record.seats > 0 and record.seats >= len(record.attendee_ids):
                record.percent_seats = round(len(record.attendee_ids) / record.seats * 100)
                record.attendee_count = len(record.attendee_ids)
            else:
                record.percent_seats = 0

    @api.onchange("seats", "attendee_ids")
    def _onchange_percent_seats(self):
        if len(self.attendee_ids) > self.seats or self.seats < 0:
            self.seats = self._origin.seats
            self.attendee_ids = self._origin.attendee_ids

            return {
                "warning": {
                    "title": _("Invalid Values"),
                    "message": _("Cannot have a negative number of seats or more seats taken than the total number "
                                 "of seats."),
                }
            }

    @api.constrains("instructor_id", "attendee_ids")
    def _check_instructor_in_attendees(self):
        for record in self:
            if record.instructor_id in record.attendee_ids:
                raise ValidationError(_("Instructor present in the attendees of his/her own session"))
