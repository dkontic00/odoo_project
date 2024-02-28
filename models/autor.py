# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Autor(models.Model):
    _name = "knjiznica.autor"
    _description = "Autor"
    _rec_name = "naziv"

    naziv = fields.Char(string='Naziv autora', required=True)