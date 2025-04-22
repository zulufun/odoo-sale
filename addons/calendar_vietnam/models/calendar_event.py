from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime

class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    is_holiday = fields.Boolean('Là ngày lễ', compute='_compute_is_holiday', store=True)

    @api.depends('start')
    def _compute_is_holiday(self):
        holiday_obj = self.env['hr.public.holiday']
        vn_country = self.env.ref('base.vn')
        for event in self:
            if event.start:
                holiday = holiday_obj.search([
                    ('date', '=', event.start.date()),
                    ('country_id', '=', vn_country.id)
                ], limit=1)
                event.is_holiday = bool(holiday)
            else:
                event.is_holiday = False

    @api.constrains('start')
    def _check_holiday_conflict(self):
        for event in self:
            if event.is_holiday:
                raise ValidationError(
                    _("Không thể lên lịch sự kiện vào %s do là ngày lễ: %s") % (
                        event.start.date(), event._get_holiday_name()
                    )
                )

    def _get_holiday_name(self):
        holiday = self.env['hr.public.holiday'].search([
            ('date', '=', self.start.date()),
            ('country_id', '=', self.env.ref('base.vn').id)
        ], limit=1)
        return holiday.name if holiday else "Ngày lễ không xác định"

    def action_suggest_date(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'x_suggest_date_wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_event_id': self.id},
        }