from odoo import models, fields, api
from datetime import datetime

class HrPublicHoliday(models.Model):
    _name = 'hr.public.holiday'
    _description = 'Public Holidays'
    _order = 'date'
    
    name = fields.Char('Holiday Name', required=True)
    date = fields.Date('Date', required=True, index=True)
    country_id = fields.Many2one('res.country', string='Country', default=lambda self: self.env.company.country_id.id)
    year = fields.Integer(string='Year', compute='_compute_year', store=True)
    description = fields.Text(string='Mô tả', help='Mô tả chi tiết về ngày nghỉ lễ')
    
    @api.depends('date')
    def _compute_year(self):
        for holiday in self:
            holiday.year = holiday.date.year if holiday.date else False
    
    @api.model
    def create_default_vietnam_holidays(self, year=None):
        """Tạo các ngày nghỉ lễ cố định theo Luật Lao động Việt Nam"""
        if not year:
            year = fields.Date.today().year
        
        # Thêm các ngày lễ cố định
        holidays = [
            {'name': 'Tết Dương lịch', 'date': f'{year}-01-01'},
            {'name': 'Ngày Giải phóng miền Nam', 'date': f'{year}-04-30'},
            {'name': 'Quốc tế Lao động', 'date': f'{year}-05-01'},
            {'name': 'Quốc khánh', 'date': f'{year}-09-02'},
        ]
        
        # Thêm ngày lễ thứ 2 nếu Quốc khánh rơi vào cuối tuần (thứ 7, CN)
        qk_date = datetime.strptime(f'{year}-09-02', '%Y-%m-%d')
        if qk_date.weekday() == 5:  # Thứ 7
            holidays.append({'name': 'Quốc khánh (bù)', 'date': f'{year}-09-04'})
        elif qk_date.weekday() == 6:  # Chủ nhật
            holidays.append({'name': 'Quốc khánh (bù)', 'date': f'{year}-09-03'})
        
        # Chúng ta sẽ cần thêm các ngày lễ Âm lịch riêng (cần cập nhật hàng năm)
        
        # Kiểm tra và thêm vào cơ sở dữ liệu
        vn_country = self.env.ref('base.vn')
        for holiday in holidays:
            existing = self.search([
                ('name', '=', holiday['name']),
                ('date', '=', holiday['date']),
                ('country_id', '=', vn_country.id)
            ])
            if not existing:
                self.create({
                    'name': holiday['name'],
                    'date': holiday['date'],
                    'country_id': vn_country.id,
                })
        return True
    
    @api.model
    def update_lunar_holidays(self, year, holiday_data):
        """Cập nhật ngày nghỉ Tết Âm lịch và các ngày lễ theo lịch Âm"""
        vn_country = self.env.ref('base.vn')
        
        # Xóa ngày Tết Âm lịch cũ nếu có
        old_lunar_holidays = self.search([
            ('name', 'like', 'Tết Âm lịch'),
            ('year', '=', year),
            ('country_id', '=', vn_country.id)
        ])
        old_lunar_holidays.unlink()
        
        # Xóa ngày Giỗ Tổ Hùng Vương cũ
        old_gt_holidays = self.search([
            ('name', '=', 'Giỗ Tổ Hùng Vương'),
            ('year', '=', year),
            ('country_id', '=', vn_country.id)
        ])
        old_gt_holidays.unlink()
        
        # Thêm ngày nghỉ lễ mới
        for holiday in holiday_data:
            self.create({
                'name': holiday['name'],
                'date': holiday['date'],
                'country_id': vn_country.id,
            })
        return True