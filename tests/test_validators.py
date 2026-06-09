"""Unit tests for validators."""

import unittest
from datetime import date, timedelta
from unittest.mock import MagicMock

from src.validators.form_validator import FormValidator, ValidationError
from src.validators.business_rules import BusinessRuleValidator


class TestFormValidator(unittest.TestCase):
    """Test form field validators."""

    def test_validate_name_valid(self):
        """Test valid name validation."""
        result = FormValidator.validate_name("John Doe")
        self.assertEqual(result, "John Doe")

    def test_validate_name_empty(self):
        """Test empty name raises error."""
        with self.assertRaises(ValidationError):
            FormValidator.validate_name("")

    def test_validate_name_too_short(self):
        """Test name too short raises error."""
        with self.assertRaises(ValidationError):
            FormValidator.validate_name("A")

    def test_validate_name_too_long(self):
        """Test name too long raises error."""
        with self.assertRaises(ValidationError):
            FormValidator.validate_name("A" * 101)

    def test_validate_name_invalid_characters(self):
        """Test name with invalid characters raises error."""
        with self.assertRaises(ValidationError):
            FormValidator.validate_name("John123")

    def test_validate_email_valid(self):
        """Test valid email validation."""
        result = FormValidator.validate_email("test@example.com")
        self.assertEqual(result, "test@example.com")

    def test_validate_email_empty(self):
        """Test empty email raises error."""
        with self.assertRaises(ValidationError):
            FormValidator.validate_email("")

    def test_validate_email_invalid_format(self):
        """Test invalid email format raises error."""
        with self.assertRaises(ValidationError):
            FormValidator.validate_email("invalid.email")

    def test_validate_phone_valid(self):
        """Test valid phone validation."""
        result = FormValidator.validate_phone("9876543210")
        self.assertEqual(result, "9876543210")

    def test_validate_phone_empty(self):
        """Test empty phone raises error."""
        with self.assertRaises(ValidationError):
            FormValidator.validate_phone("")

    def test_validate_phone_invalid_length(self):
        """Test phone with invalid length raises error."""
        with self.assertRaises(ValidationError):
            FormValidator.validate_phone("123456789")

    def test_validate_phone_non_numeric(self):
        """Test phone with non-numeric characters raises error."""
        with self.assertRaises(ValidationError):
            FormValidator.validate_phone("98765ABCD0")

    def test_validate_aadhaar_valid(self):
        """Test valid Aadhaar validation."""
        result = FormValidator.validate_aadhaar("123456789012")
        self.assertEqual(result, "123456789012")

    def test_validate_aadhaar_invalid_length(self):
        """Test Aadhaar with invalid length raises error."""
        with self.assertRaises(ValidationError):
            FormValidator.validate_aadhaar("12345678901")

    def test_validate_date_valid(self):
        """Test valid date validation."""
        result = FormValidator.validate_date("2000-01-15")
        self.assertEqual(result, date(2000, 1, 15))

    def test_validate_date_empty(self):
        """Test empty date raises error."""
        with self.assertRaises(ValidationError):
            FormValidator.validate_date("")

    def test_validate_date_invalid_format(self):
        """Test invalid date format raises error."""
        with self.assertRaises(ValidationError):
            FormValidator.validate_date("15-01-2000")

    def test_validate_dob_valid(self):
        """Test valid date of birth validation."""
        today = date.today()
        dob = date(today.year - 20, today.month, today.day)
        result = FormValidator.validate_dob(dob)
        self.assertEqual(result, dob)

    def test_validate_dob_too_young(self):
        """Test DOB too young raises error."""
        today = date.today()
        dob = date(today.year - 10, today.month, today.day)
        with self.assertRaises(ValidationError):
            FormValidator.validate_dob(dob, min_age=15)

    def test_validate_dob_too_old(self):
        """Test DOB too old raises error."""
        today = date.today()
        dob = date(today.year - 70, today.month, today.day)
        with self.assertRaises(ValidationError):
            FormValidator.validate_dob(dob, max_age=60)

    def test_validate_dob_future_date(self):
        """Test future DOB raises error."""
        future_dob = date.today() + timedelta(days=1)
        with self.assertRaises(ValidationError):
            FormValidator.validate_dob(future_dob)

    def test_validate_percentage_valid(self):
        """Test valid percentage validation."""
        result = FormValidator.validate_percentage("75.5")
        self.assertEqual(result, 75.5)

    def test_validate_percentage_zero(self):
        """Test zero percentage is valid."""
        result = FormValidator.validate_percentage("0")
        self.assertEqual(result, 0.0)

    def test_validate_percentage_hundred(self):
        """Test 100 percentage is valid."""
        result = FormValidator.validate_percentage("100")
        self.assertEqual(result, 100.0)

    def test_validate_percentage_invalid_range(self):
        """Test percentage outside range raises error."""
        with self.assertRaises(ValidationError):
            FormValidator.validate_percentage("101")

    def test_validate_percentage_negative(self):
        """Test negative percentage raises error."""
        with self.assertRaises(ValidationError):
            FormValidator.validate_percentage("-10")

    def test_validate_marks_valid(self):
        """Test valid marks validation."""
        result = FormValidator.validate_marks("85")
        self.assertEqual(result, 85.0)

    def test_validate_marks_invalid_range(self):
        """Test marks outside range raises error."""
        with self.assertRaises(ValidationError):
            FormValidator.validate_marks("105")

    def test_validate_gpa_valid(self):
        """Test valid GPA validation."""
        result = FormValidator.validate_gpa("3.5")
        self.assertEqual(result, 3.5)

    def test_validate_gpa_invalid_range(self):
        """Test GPA outside range raises error."""
        with self.assertRaises(ValidationError):
            FormValidator.validate_gpa("4.5")

    def test_validate_cgpa_valid(self):
        """Test valid CGPA validation."""
        result = FormValidator.validate_cgpa("3.8")
        self.assertEqual(result, 3.8)

    def test_validate_password_valid(self):
        """Test valid password validation."""
        result = FormValidator.validate_password("password123")
        self.assertEqual(result, "password123")

    def test_validate_password_too_short(self):
        """Test password too short raises error."""
        with self.assertRaises(ValidationError):
            FormValidator.validate_password("pass", min_length=6)

    def test_validate_required_field_valid(self):
        """Test valid required field."""
        result = FormValidator.validate_required_field("value", "Field")
        self.assertEqual(result, "value")

    def test_validate_required_field_empty(self):
        """Test empty required field raises error."""
        with self.assertRaises(ValidationError):
            FormValidator.validate_required_field("", "Field")

    def test_validate_dropdown_selection_valid(self):
        """Test valid dropdown selection."""
        result = FormValidator.validate_dropdown_selection("Male", "Gender")
        self.assertEqual(result, "Male")

    def test_validate_dropdown_selection_select(self):
        """Test 'Select' dropdown raises error."""
        with self.assertRaises(ValidationError):
            FormValidator.validate_dropdown_selection("Select", "Gender")

    def test_validate_text_area_valid(self):
        """Test valid text area content."""
        result = FormValidator.validate_text_area("This is a valid text")
        self.assertEqual(result, "This is a valid text")

    def test_validate_text_area_too_short(self):
        """Test text area too short raises error."""
        with self.assertRaises(ValidationError):
            FormValidator.validate_text_area("test")

    def test_validate_text_area_too_long(self):
        """Test text area too long raises error."""
        with self.assertRaises(ValidationError):
            FormValidator.validate_text_area("A" * 501)


class TestBusinessRuleValidator(unittest.TestCase):
    """Test business rule validators."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_queries = MagicMock()
        self.validator = BusinessRuleValidator(self.mock_queries)

    def test_validate_student_id_unique_valid(self):
        """Test valid unique student ID."""
        self.mock_queries.get_student_by_id.return_value = None
        result = self.validator.validate_student_id_unique("STU001")
        self.assertEqual(result, "STU001")

    def test_validate_student_id_unique_duplicate(self):
        """Test duplicate student ID raises error."""
        mock_student = MagicMock()
        mock_student.student_id = "STU001"
        self.mock_queries.get_student_by_id.return_value = mock_student

        with self.assertRaises(ValidationError):
            self.validator.validate_student_id_unique("STU001")

    def test_validate_student_age_range_valid(self):
        """Test valid student age."""
        today = date.today()
        dob = date(today.year - 20, today.month, today.day)
        result = self.validator.validate_student_age_range(dob)
        self.assertEqual(result, dob)

    def test_validate_student_age_range_too_young(self):
        """Test student too young raises error."""
        today = date.today()
        dob = date(today.year - 10, today.month, today.day)

        with self.assertRaises(ValidationError):
            self.validator.validate_student_age_range(dob, min_age=15)

    def test_validate_marks_range_valid(self):
        """Test valid marks range."""
        result = self.validator.validate_marks_range(85.5)
        self.assertEqual(result, 85.5)

    def test_validate_marks_range_invalid(self):
        """Test invalid marks range raises error."""
        with self.assertRaises(ValidationError):
            self.validator.validate_marks_range(105)

    def test_validate_cgpa_calculation_valid(self):
        """Test valid CGPA calculation."""
        cgpa = self.validator.validate_cgpa_calculation(
            total_marks=300, total_subjects=4
        )
        self.assertGreater(cgpa, 0)
        self.assertLessEqual(cgpa, 4.0)

    def test_validate_cgpa_calculation_invalid_subjects(self):
        """Test invalid subjects count raises error."""
        with self.assertRaises(ValidationError):
            self.validator.validate_cgpa_calculation(
                total_marks=300, total_subjects=0
            )

    def test_validate_gpa_from_percentage_valid(self):
        """Test valid GPA conversion."""
        gpa = self.validator.validate_gpa_from_percentage(80)
        self.assertEqual(gpa, 3.2)

    def test_validate_disability_percentage_with_disability(self):
        """Test disability percentage with disability marked."""
        result = self.validator.validate_disability_percentage(
            "yes", "50"
        )
        self.assertEqual(result, 50.0)

    def test_validate_disability_percentage_without_disability(self):
        """Test disability percentage without disability."""
        result = self.validator.validate_disability_percentage(
            "no", ""
        )
        self.assertEqual(result, 0.0)

    def test_validate_disability_percentage_required_but_missing(self):
        """Test disability percentage required but missing raises error."""
        with self.assertRaises(ValidationError):
            self.validator.validate_disability_percentage("yes", "")

    def test_validate_nationality_country_indian(self):
        """Test Indian nationality with India country."""
        result = self.validator.validate_nationality_country(
            "Indian", "India"
        )
        self.assertEqual(result, "India")

    def test_validate_nationality_country_mismatch(self):
        """Test nationality country mismatch raises error."""
        with self.assertRaises(ValidationError):
            self.validator.validate_nationality_country(
                "Indian", "USA"
            )

    def test_validate_address_fields_same_address(self):
        """Test address validation with same address."""
        result = self.validator.validate_address_fields(
            "yes", "Any Address"
        )
        self.assertEqual(result, "")

    def test_validate_address_fields_different_address(self):
        """Test address validation with different address."""
        result = self.validator.validate_address_fields(
            "no", "123 Main Street, City, State"
        )
        self.assertEqual(result, "123 Main Street, City, State")

    def test_validate_address_fields_missing(self):
        """Test missing address raises error."""
        with self.assertRaises(ValidationError):
            self.validator.validate_address_fields("no", "")

    def test_validate_marks_prerequisites_valid(self):
        """Test valid marks prerequisites."""
        result = self.validator.validate_marks_prerequisites(
            "Mathematics", 85
        )
        self.assertEqual(result, 85)

    def test_validate_marks_prerequisites_invalid_subject(self):
        """Test invalid subject raises error."""
        with self.assertRaises(ValidationError):
            self.validator.validate_marks_prerequisites("", 85)


if __name__ == "__main__":
    unittest.main()
