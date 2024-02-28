# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime, timedelta


class Knjiga(models.Model):

    _name = "knjiznica.knjiga"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Knjiga"
    _rec_name = "naziv"

    naziv = fields.Char(string='Naziv', required=True)
    autor = fields.Many2one('knjiznica.autor', string='Autor', required=True)
    nakladnik = fields.Many2one('knjiznica.nakladnik', string='Nakladnik', required=True)
    zanr = fields.Many2one('knjiznica.zanr', string='Žanr', required=True)
    zaduzena_datuma = fields.Char(string="Zadužena datuma:")
    zaduzena_do = fields.Char(string="Zadužena do:")
    state = fields.Selection([('nije_zaduzena', 'Nije zadužena'), ('zaduzena', 'Zadužena'), ('uredi', 'Uredi')],
                             default='uredi', string="Stanje")
    zaduzio = fields.Char(string="Zadužio")
    zakasnina = fields.Float(string="Zakasnina", default=0.0)

    def button_zaduzi(self):
        dat1 = datetime.today()
        dat2 = datetime.today() + timedelta(days=21)
        datum_vracanja = dat2.strftime("%d-%m-%Y")
        self.state = 'zaduzena'
        self.zaduzena_datuma = dat1.strftime("%d-%m-%Y")
        self.zaduzena_do = datum_vracanja
        self.zaduzio = self.env.user.name
        return {"type": "ir.actions.server", "id": 213}

    def button_vraceno(self):
        if self.zaduzena_do:
            self.state = 'nije_zaduzena'
            datum1_s = self.zaduzena_do
            datum1 = datetime.strptime(datum1_s, "%d-%m-%Y")
            datum2 = datetime.today()
            razlika = datum2 - datum1
            if razlika.days > 0:
                zakasnina = razlika.days * 0.75
                self.zaduzena_do = ''
                self.zaduzena_datuma = ''
                self.zaduzio = ''
                obavijest = {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Warning!',
                        'message': f'Zakasnina za knjigu iznosi : {zakasnina}kn',
                        'sticky': False
                        }
                    }
                self.zakasnina = 0.0
                return obavijest
            else:
                self.zaduzena_do = ''
                self.zaduzena_datuma = ''
                self.zaduzio = ''
        else:
            self.state = 'nije_zaduzena'
            self.zaduzena_do = ''
            self.zaduzena_datuma = ''
            self.zaduzio = ''

    def button_uredi(self):
        self.state = 'uredi'

    def button_zakasnina(self):
        if self.zaduzena_do:
            datum1_s = self.zaduzena_do
            datum1 = datetime.strptime(datum1_s, "%d-%m-%Y")
            datum2 = datetime.today()
            razlika = datum2 - datum1
            if razlika.days > 0:
                platiti = razlika.days * 0.75
                self.zakasnina = platiti
                obavijest = {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Warning!',
                        'message': f'Zakasnina iznosi: {platiti}kn',
                        'sticky': False
                    }
                }
                return obavijest
            else:
                self.zakasnina = 0.0
                obavijest = {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Warning!',
                        'message': 'Rok posudbe nije istekao, nemate zakasninu',
                        'sticky': False
                    }
                }
                return obavijest
        else:
            self.zakasnina = 0.0
            obavijest = {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Warning!',
                    'message': 'Rok posudbe nije istekao, nemate zakasninu',
                    'sticky': False
                }
            }
            return obavijest

    def button_ukupna_zakasnina(self):
        korisnik = self.env.user.name
        ukupno = 0.0
        knjige = self.env['knjiznica.knjiga'].search([])
        for knjiga in knjige:
            if knjiga.zaduzio == korisnik:
                datum1_s = knjiga.zaduzena_do
                datum1 = datetime.strptime(datum1_s, "%d-%m-%Y")
                datum2 = datetime.today()
                razlika = datum2 - datum1
                if razlika.days > 0:
                    platiti = razlika.days * 0.75
                    knjiga.zakasnina = platiti
                ukupno += knjiga.zakasnina
        obavijest = {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Warning!',
                'message': f'Zakasnina iznosi {ukupno}kn',
                'sticky': False
            }
        }
        return obavijest
