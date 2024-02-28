# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Nakladnik(models.Model):
    _name = "knjiznica.nakladnik"
    _description = "Nakladnik"
    _rec_name = "naziv"

    naziv = fields.Char(string='Nakladnik', required=True)
