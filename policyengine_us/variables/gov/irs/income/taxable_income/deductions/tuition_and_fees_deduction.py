from policyengine_us.model_api import *


class tuition_and_fees_deduction(Variable):
    value_type = float
    entity = TaxUnit
    label = "Tuition and fees deduction"
    unit = USD
    definition_period = YEAR
    reference = (
        "https://www.irs.gov/pub/irs-pdf/f8917.pdf#page=2"
        # Law was repealed in 2021
        "https://irc.bloombergtax.com/public/uscode/doc/irc/section_222"
    )

    def formula(tax_unit, period, parameters):
        qualified_tuition_expenses = add(
            tax_unit, period, ["qualified_tuition_expenses"]
        )
        adjusted_gross_income = tax_unit("adjusted_gross_income", period)
        # married filing separatly are not eligible for this deduction
        filing_status = tax_unit("filing_status", period)
        separate = filing_status == filing_status.possible_values.SEPARATE
        # can't caim this deduction if the household has American oppportunity or lifetime learning credit
        american_opportunity_credit = tax_unit(
            "american_opportunity_credit", period
        )
        lifetime_learning_credit = tax_unit("lifetime_learning_credit", period)
        has_take_the_american_opp_or_life_learn_credits = (
            american_opportunity_credit + lifetime_learning_credit
        ) > 0
        p = parameters(period).gov.irs.deductions.tuition_and_fees
        joint = filing_status == filing_status.possible_values.JOINT
        cap = where(
            joint,
            p.joint.calc(adjusted_gross_income),
            p.non_joint.calc(adjusted_gross_income),
        )
        capped_expenses = min_(qualified_tuition_expenses, cap)
        return (
            capped_expenses
            * ~has_take_the_american_opp_or_life_learn_credits
            * ~separate
        )
