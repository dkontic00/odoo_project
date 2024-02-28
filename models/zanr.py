# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Zanr(models.Model):
    _name = "knjiznica.zanr"
    _description = "Žanr"
    _rec_name = "naziv"

    naziv = fields.Char(string='Žanr', required=True)
