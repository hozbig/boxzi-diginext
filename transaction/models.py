from django.db import models
from utils.uuid_generator import random_uuid


class ProductWalletTransaction(models.Model):
    uuid = models.CharField(
        unique=True,
        max_length=5,
        blank=True,
        default=random_uuid,
        editable=False,
    )

    product_wallet = models.ForeignKey("plan.ProductWallet", related_name="product_wallet_of_transaction", verbose_name="کیف پول محصول", on_delete=models.CASCADE)
    investor_fund = models.ForeignKey("investor.InvestorFund", related_name="investor_fund_of_transaction", verbose_name="صندوق سرمایه گذار", on_delete=models.CASCADE)
    accelerator_fund = models.ForeignKey("investor.InvestorFund", related_name="accelerator_fund_of_transaction", verbose_name="صندوق شتابدهنده", on_delete=models.CASCADE, null=True, blank=True)
    amount = models.PositiveIntegerField(default=0, verbose_name="مقدار")

    class Meta:
        verbose_name = "تراکنش کیف پول محصول"
        verbose_name_plural = "تراکنش های کیف پول های محصول"

    def __str__(self) -> str:
        return f"{self.wallet} - {self.depositor} - {self.amount}"
    

class RoadFundTransaction(models.Model):
    uuid = models.CharField(
        unique=True,
        max_length=5,
        blank=True,
        default=random_uuid,
        editable=False,
    )

    wallet = models.ForeignKey("content.RoadFund", related_name="fund_of_transaction", verbose_name="صندوق شتابدهنده", on_delete=models.CASCADE)
    depositor = models.ForeignKey("account.User", verbose_name="فرستنده (سرمایه گذار)", on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0, verbose_name="مقدار")

    created_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "تراکنش صندوق شتابدهنده"
        verbose_name_plural = "تراکنش های صندوق های شتابدهنده"

    def __str__(self) -> str:
        return f"{self.wallet} - {self.depositor} - {self.amount}"
