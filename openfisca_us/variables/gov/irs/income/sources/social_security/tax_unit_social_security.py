from openfisca_us.model_api import *

class tax_unit_social_security(Variable):
    value_type = float
    entity = TaxUnit
    label = "Tax unit social security"
    unit = USD
    definition_period = YEAR

    formula = sum_of_variables(["social_security"])
