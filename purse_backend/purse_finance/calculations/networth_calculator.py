from purse_core.base_task import BaseTask
from purse_finance.calculations.base_calculation import BaseCalculation
from purse_finance.models.networth import NetWorth


class NetWorthCreator(BaseCalculation, BaseTask):

    def run(self, *args, **kwargs):
        networth = self.user.get_networth()
        NetWorth.objects.create(
            user_id=self.user_id, 
            networth=networth
        )
        return {
            "networth": networth
        }