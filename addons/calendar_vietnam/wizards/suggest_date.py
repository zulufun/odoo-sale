from odoo import models, fields
from datetime import datetime, timedelta

print("Loading x_suggest_date_wizard model")  # Debug để kiểm tra

class SuggestDateWizard(models.TransientModel):
    _name = 'x_suggest_date_wizard'
    _description = 'Đề xuất ngày không phải ngày lễ'

    event_id = fields.Many2one('calendar.event', string='Sự kiện')
    suggested_date = fields.Date('Ngày đề xuất', compute='_compute_suggested_date')
    message = fields.Char('Thông báo', compute='_compute_suggested_date')

    def _compute_suggested_date(self):
        holiday_obj = self.env['hr.public.holiday']
        vn_country = self.env.ref('base.vn')
        for wizard in self:
            if wizard.event_id and wizard.event_id.start:
                current_date = wizard.event_id.start.date()
                max_attempts = 30  # Ngăn vòng lặp vô hạn
                attempts = 0
                while attempts < max_attempts:
                    current_date += timedelta(days=1)
                    if current_date.weekday() >= 5:  # Bỏ qua cuối tuần
                        continue
                    holiday = holiday_obj.search([
                        ('date', '=', current_date),
                        ('country_id', '=', vn_country.id)
                    ], limit=1)
                    if not holiday:
                        wizard.suggested_date = current_date
                        wizard.message = f"Ngày khả dụng tiếp theo: {current_date}"
                        return
                    attempts += 1
                wizard.suggested_date = False
                wizard.message = "Không tìm thấy ngày khả dụng trong 30 ngày tới."
            else:
                wizard.suggested_date = False
                wizard.message = "Không có ngày sự kiện được cung cấp."

    def apply_suggested_date(self):
        self.ensure_one()
        if self.suggested_date and self.event_id:
            self.event_id.write({
                'start': datetime.combine(self.suggested_date, self.event_id.start.time()),
                'stop': datetime.combine(self.suggested_date, self.event_id.stop.time()),
            })
        return {'type': 'ir.actions.act_window_close'}