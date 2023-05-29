from policyengine_us.model_api import *


class ga_cdcc(Variable):
    value_type = float
    entity = TaxUnit
    label = "Georgia dependent care credit"
    unit = USD
    definition_period = YEAR
    defined_for = StateCode.GA

    def formula(tax_unit, period, parameters):
        expenses = tax_unit("cdcc", period)
        rate = parameters(
            period
        ).gov.states.ga.tax.income.credits.qualified_child.rate
        return expenses * rate
