from odoo import fields, models


class Attendee(models.TransientModel):
    _name = "attendee"
    _description = "Attendee"

    def _default_session(self):
        return self.env['session'].browse(self._context.get('active_ids'))

    session_ids = fields.Many2many("session", required=True, default=_default_session)
    attendee_ids = fields.Many2many("res.partner")

    def add_attendees(self):
        for session in self.session_ids:
            session.attendee_ids |= self.attendee_ids
