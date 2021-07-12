from django.db import models

class BacktestResults(models.Model):
    fiat_balance = models.FloatField()
    coin_balance = models.FloatField()
    win_rate = models.FloatField()

    def __str__(self):
        return str(self.win_rate)