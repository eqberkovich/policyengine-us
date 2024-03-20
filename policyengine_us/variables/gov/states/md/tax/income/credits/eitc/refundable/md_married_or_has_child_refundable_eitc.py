from policyengine_us.model_api import *


class md_married_or_has_child_refundable_eitc(Variable):
    value_type = float
    entity = TaxUnit
    label = "MD refundable EITC for filers who are married or have qualifying child"
    unit = USD
    definition_period = YEAR
    reference = "https://www.marylandtaxes.gov/forms/21_forms/Resident_Booklet.pdf#page=23"
    defined_for = StateCode.MD

    def formula(tax_unit, period, parameters):
        # Limited to filers who are married or have child
        married_or_has_child = ~tax_unit(
            "md_qualifies_for_unmarried_childless_eitc", period
        )

        federal_eitc = tax_unit("eitc", period)
        md_tax = tax_unit("md_income_tax_before_credits", period)
        p = parameters(
            period
        ).gov.states.md.tax.income.credits.eitc.refundable.married_or_has_child
        md_refundable_eitc_allowed = max_(federal_eitc * p.match - md_tax, 0)

        return married_or_has_child * md_refundable_eitc_allowed
