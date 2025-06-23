"""
Data utilities for downloading and managing datasets.

Downloaded ONLY "age" and "net worth" columns from CPS data 
"""

import pandas as pd
from pathlib import Path
from huggingface_hub import hf_hub_download
from typing import Union, List
import h5py


chosen_columns = ["household_id/2024", "age/2024", "net_worth/2024", "household_weight/2024"]  # Columns to be used from the dataset
'''
📊 Available columns:
  • aca_take_up_seed/2024
  • age/2024
  • alimony_expense/2024
  • alimony_income/2024
  • american_opportunity_credit/2024
  • amt_foreign_tax_credit/2024
  • auto_loan_balance/2024
  • auto_loan_interest/2024
  • business_is_sstb/2024
  • casualty_loss/2024
  • cdcc_relevant_expenses/2024
  • charitable_cash_donations/2024
  • charitable_non_cash_donations/2024
  • child_support_expense/2024
  • child_support_received/2024
  • county_fips/2024
  • cps_race/2024
  • deductible_mortgage_interest/2024
  • detailed_occupation_recode/2024
  • disability_benefits/2024
  • domestic_production_ald/2024
  • early_withdrawal_penalty/2024
  • educator_expense/2024
  • employment_income_before_lsr/2024
  • employment_income_last_year/2024
  • energy_efficient_home_improvement_credit/2024
  • estate_income/2024
  • estate_income_would_be_qualified/2024
  • excess_withheld_payroll_tax/2024
  • family_id/2024
  • farm_income/2024
  • farm_operations_income/2024
  • farm_operations_income_would_be_qualified/2024
  • farm_rent_income/2024
  • farm_rent_income_would_be_qualified/2024
  • foreign_tax_credit/2024
  • free_school_meals_reported/2024
  • general_business_credit/2024
  • has_esi/2024
  • has_marketplace_health_coverage/2024
  • has_never_worked/2024
  • health_insurance_premiums_without_medicare_part_b/2024
  • health_savings_account_ald/2024
  • hours_worked_last_week/2024
  • household_id/2024
  • household_weight/2024
  • housing_assistance/2024
  • in_nyc/2024
  • interest_deduction/2024
  • investment_income_elected_form_4952/2024
  • is_blind/2024
  • is_computer_scientist/2024
  • is_disabled/2024
  • is_executive_administrative_professional/2024
  • is_farmer_fisher/2024
  • is_female/2024
  • is_full_time_college_student/2024
  • is_hispanic/2024
  • is_household_head/ETERNITY
  • is_military/2024
  • is_separated/2024
  • keogh_distributions/2024
  • long_term_capital_gains_before_response/2024
  • long_term_capital_gains_on_collectibles/2024
  • marital_unit_id/2024
  • medicaid_take_up_seed/2024
  • medicare_part_b_premiums/2024
  • miscellaneous_income/2024
  • net_worth/2024
  • non_qualified_dividend_income/2024
  • non_sch_d_capital_gains/2024
  • other_credits/2024
  • other_medical_expenses/2024
  • over_the_counter_health_expenses/2024
  • own_children_in_household/2024
  • partnership_s_corp_income/2024
  • partnership_s_corp_income_would_be_qualified/2024
  • person_family_id/2024
  • person_household_id/2024
  • person_id/2024
  • person_marital_unit_id/2024
  • person_spm_unit_id/2024
  • person_tax_unit_id/2024
  • person_weight/2024
  • pre_subsidy_rent/2024
  • pre_tax_contributions/2024
  • previous_year_income_available/2024
  • prior_year_minimum_tax_credit/2024
  • qualified_bdc_income/2024
  • qualified_dividend_income/2024
  • qualified_reit_and_ptp_income/2024
  • qualified_tuition_expenses/2024
  • real_estate_taxes/2024
  • recapture_of_investment_credit/2024
  • receives_wic/2024
  • rent/2024
  • rental_income/2024
  • rental_income_would_be_qualified/2024
  • roth_401k_contributions/2024
  • roth_ira_contributions/2024
  • salt_refund_income/2024
  • savers_credit/2024
  • self_employed_health_insurance_ald/2024
  • self_employed_pension_contribution_ald/2024
  • self_employed_pension_contributions/2024
  • self_employment_income_before_lsr/2024
  • self_employment_income_last_year/2024
  • self_employment_income_would_be_qualified/2024
  • short_term_capital_gains/2024
  • snap_reported/2024
  • snap_take_up_seed/2024
  • social_security/2024
  • social_security_dependents/2024
  • social_security_disability/2024
  • social_security_retirement/2024
  • social_security_survivors/2024
  • spm_unit_broadband_subsidy_reported/2024
  • spm_unit_capped_housing_subsidy_reported/2024
  • spm_unit_capped_work_childcare_expenses/2024
  • spm_unit_energy_subsidy_reported/2024
  • spm_unit_federal_tax_reported/2024
  • spm_unit_id/2024
  • spm_unit_net_income_reported/2024
  • spm_unit_payroll_tax_reported/2024
  • spm_unit_pre_subsidy_childcare_expenses/2024
  • spm_unit_spm_threshold/2024
  • spm_unit_state_tax_reported/2024
  • spm_unit_total_income_reported/2024
  • spm_unit_wic_reported/2024
  • ssi_reported/2024
  • ssn_card_type/2024
  • state_fips/2024
  • strike_benefits/2024
  • student_loan_interest/2024
  • takes_up_dc_ptc/2024
  • takes_up_eitc/2024
  • tanf_reported/2024
  • tax_exempt_401k_distributions/2024
  • tax_exempt_403b_distributions/2024
  • tax_exempt_interest_income/2024
  • tax_exempt_ira_distributions/2024
  • tax_exempt_pension_income/2024
  • tax_exempt_private_pension_income/2024
  • tax_exempt_sep_distributions/2024
  • tax_unit_id/2024
  • taxable_401k_distributions/2024
  • taxable_403b_distributions/2024
  • taxable_interest_income/2024
  • taxable_ira_distributions/2024
  • taxable_pension_income/2024
  • taxable_private_pension_income/2024
  • taxable_sep_distributions/2024
  • taxable_unemployment_compensation/2024
  • tenure_type/2024
  • tip_income/2024
  • traditional_401k_contributions/2024
  • traditional_ira_contributions/2024
  • unadjusted_basis_qualified_property/2024
  • unemployment_compensation/2024
  • unrecaptured_section_1250_gain/2024
  • unreimbursed_business_employee_expenses/2024
  • unreported_payroll_tax/2024
  • veterans_benefits/2024
  • w2_wages_from_qualified_business/2024
  • weekly_hours_worked_before_lsr/2024
  • workers_compensation/2024

'''

def get_data_directory() -> Path:
    """
    Get the data directory path.
    Creates the directory if it doesn't exist.
    """
    data_dir = Path.home() / ".microcalibrate" / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


class Dataset:
    """
    Dataset class for loading data from HDF5 files.
    """
    
    @staticmethod
    def from_file(file_path: Union[str, Path], 
                  time_period: int = 2024, 
                  columns: List[str] = chosen_columns) -> pd.DataFrame:
        """
        Load dataset from HDF5 file.
        
        Args:
            file_path: Path to the HDF5 file
            time_period: Time period for the dataset
            columns: List of columns to load from the dataset
            
        Returns:
            DataFrame containing the dataset
        """
        with h5py.File(file_path, "r") as f:
                        # Print all available dataset paths (leaves only)
            # Load all columns
            raw_data = {key: f[key][()] for key in columns}

            # Find the minimum length
            min_len = min(len(arr) for arr in raw_data.values())

            # Truncate all arrays to the minimum length
            data = {key: arr[:min_len] for key, arr in raw_data.items()}
            
        return pd.DataFrame(data)


def get_dataset(dataset: str = "small_enhanced_cps_2024", 
                time_period: int = 2024,
                columns: List[str] = chosen_columns) -> pd.DataFrame:
    """
    Get the dataset from the huggingface hub.
    
    Args:
        dataset: Dataset name to download
        time_period: Time period for the dataset
        
    Returns:
        DataFrame containing the dataset
    """
    dataset_path = hf_hub_download(
        repo_id="policyengine/policyengine-us-data",
        filename=f"{dataset}.h5",
        local_dir=get_data_directory() / "input" / "cps",
    )


    return Dataset.from_file(dataset_path, time_period=time_period, columns=columns)