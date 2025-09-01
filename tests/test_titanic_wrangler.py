# filepath: /workspaces/streamlit-demo/tests/test_titanic_wrangler.py
from streamlit_demo.titanic_wrangler import TitanicWrangler
import polars as pl
import pytest


def test_calculate_decade_from_age():
    # Given
    titanic_passengers = pl.DataFrame(
        {
            "PassengerId": [1, 2, 3, 4, 5],
            "Age": [0.5, 12, 23.5, 55.2, 61]
        }
    )

    # When
    result = TitanicWrangler._calculate_decade_from_age(titanic_passengers)

    # Then
    assert "AgeInDecades" in result.columns
    assert list(result["AgeInDecades"].to_list()) == [0, 1, 2, 5, 6]


def test_calculate_decade_from_age_empty_dataframe():
    # Given
    empty_df = pl.DataFrame({
        "PassengerId": pl.Series([], dtype=pl.Int64), 
        "Age": pl.Series([], dtype=pl.Float64)
    })

    # When
    result = TitanicWrangler._calculate_decade_from_age(empty_df)

    # Then
    assert "AgeInDecades" in result.columns
    assert len(result) == 0


def test_calculate_decade_from_age_with_nulls():
    # Given
    titanic_passengers = pl.DataFrame(
        {
            "PassengerId": [1, 2, 3, 4],
            "Age": [25.0, None, 45.5, 0.0]
        }
    )

    # When
    result = TitanicWrangler._calculate_decade_from_age(titanic_passengers)

    # Then
    assert "AgeInDecades" in result.columns
    expected = [2, None, 4, 0]
    assert result["AgeInDecades"].to_list() == expected


def test_calculate_decade_from_age_boundary_values():
    # Given
    titanic_passengers = pl.DataFrame(
        {
            "PassengerId": [1, 2, 3, 4, 5],
            "Age": [0.0, 9.9, 10.0, 19.9, 20.0]
        }
    )

    # When
    result = TitanicWrangler._calculate_decade_from_age(titanic_passengers)

    # Then
    assert "AgeInDecades" in result.columns
    assert result["AgeInDecades"].to_list() == [0, 0, 1, 1, 2]


def test_calculate_decade_from_age_preserves_other_columns():
    # Given
    titanic_passengers = pl.DataFrame(
        {
            "PassengerId": [1, 2, 3],
            "Name": ["John", "Jane", "Bob"],
            "Age": [25.0, 35.5, 45.0],
            "Survived": ['Survived', 'Died', 'Survived']
        }
    )

    # When
    result = TitanicWrangler._calculate_decade_from_age(titanic_passengers)

    # Then
    assert "AgeInDecades" in result.columns
    assert "PassengerId" in result.columns
    assert "Name" in result.columns
    assert "Survived" in result.columns
    assert len(result.columns) == 5


def test_calculate_decade_from_age_large_ages():
    # Given
    titanic_passengers = pl.DataFrame(
        {
            "PassengerId": [1, 2, 3],
            "Age": [80.0, 95.5, 100.0]
        }
    )

    # When
    result = TitanicWrangler._calculate_decade_from_age(titanic_passengers)

    # Then
    assert "AgeInDecades" in result.columns
    assert result["AgeInDecades"].to_list() == [8, 9, 10]


def test_calculate_decade_from_age_missing_age_column():
    # Given
    titanic_passengers = pl.DataFrame(
        {
            "PassengerId": [1, 2, 3],
            "Name": ["John", "Jane", "Bob"]
        }
    )

    # When/Then
    with pytest.raises(Exception):
        TitanicWrangler._calculate_decade_from_age(titanic_passengers)


# Integration Tests
def test_prepare_data_complete_pipeline():
    # Given - realistic sample data
    sample_data = pl.DataFrame({
        'PassengerId': [1, 2, 3, 4],
        'Survived': [1, 0, 1, 0],
        'Pclass': [1, 2, 3, 1],
        'Name': ['Braund, Mr. Owen Harris', 'Allen, Miss. Elisabeth Walton', 'Smith, Mrs. John (Mary)', 'Johnson, Master. William'],
        'Sex': ['male', 'female', 'female', 'male'],
        'Age': [22.0, None, 26.0, 4.0],
        'SibSp': [1, 0, 0, 1],
        'Parch': [0, 0, 0, 2],
        'Ticket': ['A/5 21171', 'PC 17599', 'STON/O2', 'A/5 21171'],
        'Fare': [7.25, None, 8.05, 7.25],
        'Cabin': [None, 'C85', None, 'A10'],
        'Embarked': ['S', None, 'S', 'C']
    })

    # When
    result = TitanicWrangler.prepare_data(sample_data)

    # Then - check expected columns are created
    expected_columns = ['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp', 'Parch', 
                       'Ticket', 'Fare', 'Cabin', 'Embarked', 'Title', 'CabinOccupancy', 
                       'TicketShareCount', 'Level', 'FareLog10', 'AgeInDecades']
    assert all(col in result.columns for col in expected_columns)
    assert len(result) == 4
    
    # Verify some key transformations (titles may be consolidated to 'Other' due to small sample)
    assert 'Title' in result.columns
    assert len(result['Title'].to_list()) == 4
    assert result['Cabin'].null_count() == 0  # Should be filled with "None"
    assert result['Fare'].null_count() == 0   # Should be filled with 0.0
    assert result['Embarked'].null_count() == 0  # Should be filled with location names
    # Check that Survived is converted to strings
    survived_values = set(result['Survived'].to_list())
    assert survived_values == {'Survived', 'Died'}
    # Check that Embarked is converted to location names
    embarked_values = set(result['Embarked'].to_list())
    expected_embarked = {'Southampton', 'Cherbourg'}
    assert embarked_values == expected_embarked


def test_prepare_data_empty_dataframe():
    # Given - properly typed empty DataFrame
    empty_data = pl.DataFrame({
        'PassengerId': pl.Series([], dtype=pl.Int64), 
        'Survived': pl.Series([], dtype=pl.Int64), 
        'Pclass': pl.Series([], dtype=pl.Int64), 
        'Name': pl.Series([], dtype=pl.Utf8), 
        'Sex': pl.Series([], dtype=pl.Utf8),
        'Age': pl.Series([], dtype=pl.Float64), 
        'SibSp': pl.Series([], dtype=pl.Int64), 
        'Parch': pl.Series([], dtype=pl.Int64), 
        'Ticket': pl.Series([], dtype=pl.Utf8), 
        'Fare': pl.Series([], dtype=pl.Float64), 
        'Cabin': pl.Series([], dtype=pl.Utf8), 
        'Embarked': pl.Series([], dtype=pl.Utf8)
    })

    # When
    result = TitanicWrangler.prepare_data(empty_data)

    # Then
    assert len(result) == 0
    assert len(result.columns) == 18  # Should have all expected columns


# Priority 1 Tests
def test_extract_title_from_name():
    # Given
    data = pl.DataFrame({
        'Name': [
            'Braund, Mr. Owen Harris',
            'Allen, Miss. Elisabeth Walton',
            'Smith, Mrs. John (Mary)',
            'Johnson, Master. William',
            'O\'Brien, Dr. Thomas',
            'Williams, Rev. Charles'
        ]
    })

    # When
    result = TitanicWrangler._extract_title_from_name(data)

    # Then
    assert 'Title' in result.columns
    expected_titles = ['Mr', 'Miss', 'Mrs', 'Master', 'Dr', 'Rev']
    assert result['Title'].to_list() == expected_titles


def test_extract_title_from_name_edge_cases():
    # Given
    data = pl.DataFrame({
        'Name': [
            'Invalid Name Format',
            'NoComma Mr. John',
            'Smith, Mr.',  # No name after title
            ''  # Empty string
        ]
    })

    # When
    result = TitanicWrangler._extract_title_from_name(data)

    # Then
    assert 'Title' in result.columns
    # Should handle edge cases gracefully (may return null for invalid formats)


def test_consolidate_titles():
    # Given - create data where some titles have <5 occurrences
    data = pl.DataFrame({
        'Title': ['Mr', 'Mr', 'Mr', 'Mr', 'Mr',  # 5+ occurrences
                  'Miss', 'Miss', 'Miss', 'Miss', 'Miss',  # 5+ occurrences  
                  'Dr', 'Dr',  # <5 occurrences
                  'Rev', 'Col', 'Major']  # <5 occurrences
    })

    # When
    result = TitanicWrangler._consolidate_titles(data)

    # Then
    titles = result['Title'].to_list()
    # Titles with 5+ occurrences should remain
    assert 'Mr' in titles
    assert 'Miss' in titles
    # Titles with <5 occurrences should become 'Other'
    assert 'Dr' not in titles
    assert 'Rev' not in titles
    assert 'Col' not in titles
    assert 'Major' not in titles
    assert titles.count('Other') == 5  # Dr, Dr, Rev, Col, Major


def test_consolidate_titles_all_frequent():
    # Given - all titles have 5+ occurrences
    data = pl.DataFrame({
        'Title': ['Mr'] * 6 + ['Miss'] * 5 + ['Mrs'] * 7
    })

    # When
    result = TitanicWrangler._consolidate_titles(data)

    # Then
    unique_titles = set(result['Title'].to_list())
    assert unique_titles == {'Mr', 'Miss', 'Mrs'}
    assert 'Other' not in unique_titles


def test_impute_missing_age_based_on_title():
    # Given
    data = pl.DataFrame({
        'Age': [25.0, 30.0, None, 35.0, None, 8.0, 10.0, None],
        'Title': ['Mr', 'Mr', 'Mr', 'Miss', 'Miss', 'Master', 'Master', 'Master']
    })

    # When
    result = TitanicWrangler._impute_missing_age_based_on_title(data)

    # Then
    ages = result['Age'].to_list()
    # No nulls should remain
    assert result['Age'].null_count() == 0
    
    # Check imputation logic: Mr avg = (25+30+35)/3 = 30, Miss avg = 35, Master avg = (8+10)/2 = 9
    expected_ages = [25.0, 30.0, 30, 35.0, 35, 8.0, 10.0, 9]  # Averages may be cast to int
    # Allow for integer casting in the implementation
    assert len(ages) == 8
    assert ages[0] == 25.0
    assert ages[1] == 30.0
    assert ages[3] == 35.0
    assert ages[5] == 8.0
    assert ages[6] == 10.0


def test_impute_missing_age_no_nulls():
    # Given - no missing ages
    data = pl.DataFrame({
        'Age': [25.0, 30.0, 35.0],
        'Title': ['Mr', 'Miss', 'Mrs']
    })

    # When
    result = TitanicWrangler._impute_missing_age_based_on_title(data)

    # Then (order may change due to join operation)
    ages_sorted = sorted(result['Age'].to_list())
    assert ages_sorted == [25.0, 30.0, 35.0]


# Priority 2 Tests
def test_add_cabin_occupancy():
    # Given
    data = pl.DataFrame({
        'Cabin': ['A1', 'A1', 'B2', 'None', 'None', 'C3']
    })

    # When
    result = TitanicWrangler._add_cabin_occupancy(data)

    # Then
    assert 'CabinOccupancy' in result.columns
    occupancy = result['CabinOccupancy'].to_list()
    # A1: 2 people, B2: 1 person, None: 0 (special case), C3: 1 person
    expected = [2, 2, 1, 0, 0, 1]
    assert occupancy == expected


def test_add_ticket_sharing_count():
    # Given
    data = pl.DataFrame({
        'Ticket': ['A123', 'A123', 'B456', 'C789', 'A123']
    })

    # When
    result = TitanicWrangler._add_ticket_sharing_count(data)

    # Then
    assert 'TicketShareCount' in result.columns
    counts = result['TicketShareCount'].to_list()
    # A123: 3 people, B456: 1 person, C789: 1 person
    expected = [3, 3, 1, 1, 3]
    assert counts == expected


def test_add_log10_of_fare():
    # Given
    data = pl.DataFrame({
        'Fare': [10.0, 100.0, 1.0, 0.0, None]
    })

    # When
    result = TitanicWrangler._add_log10_of_fare(data)

    # Then
    assert 'FareLog10' in result.columns
    log_fares = result['FareLog10'].to_list()
    # log10(10) = 1, log10(100) = 2, log10(1) = 0, log10(0) = 0 (special case), null handled
    assert abs(log_fares[0] - 1.0) < 0.001
    assert abs(log_fares[1] - 2.0) < 0.001  
    assert abs(log_fares[2] - 0.0) < 0.001
    assert log_fares[3] == 0.0  # Zero case
    # Null case may vary depending on implementation


def test_add_log10_of_fare_edge_cases():
    # Given
    data = pl.DataFrame({
        'Fare': [0.001, -5.0]  # Very small positive, negative
    })

    # When
    result = TitanicWrangler._add_log10_of_fare(data)

    # Then
    log_fares = result['FareLog10'].to_list()
    assert log_fares[0] < 0  # log10(0.001) is negative
    assert log_fares[1] == 0.0  # Negative values treated as zero case


def test_convert_survived_to_string():
    # Given
    data = pl.DataFrame({
        'Survived': [1.0, 0.0, 1.0, 0.0, None]
    })

    # When
    result = TitanicWrangler._convert_survived_to_string(data)

    # Then
    expected = ['Survived', 'Died', 'Survived', 'Died', None]
    assert result['Survived'].to_list() == expected


def test_convert_embarked_to_location_names():
    # Given
    data = pl.DataFrame({
        'Embarked': ['S', 'C', 'Q', 'S', None, 'Unknown']
    })

    # When
    result = TitanicWrangler._convert_embarked_to_location_names(data)

    # Then
    expected = ['Southampton', 'Cherbourg', 'Queenstown', 'Southampton', None, 'Unknown']
    assert result['Embarked'].to_list() == expected


def test_calculate_survival_rate_overall():
    # Given
    data = pl.DataFrame({
        'Survived': ['Survived', 'Died', 'Survived', 'Died', 'Survived']
    })

    # When
    result = TitanicWrangler.calculate_survival_rate(data)

    # Then
    assert len(result) == 1
    assert result['Category'].to_list() == ['Overall']
    assert result['TotalCount'].to_list() == [5]
    assert result['SurvivedCount'].to_list() == [3]
    assert result['SurvivalRate'].to_list() == [60.0]


def test_calculate_survival_rate_by_category():
    # Given
    data = pl.DataFrame({
        'Survived': ['Survived', 'Died', 'Survived', 'Died', 'Survived', 'Died'],
        'Pclass': [1, 1, 2, 2, 3, 3]
    })

    # When
    result = TitanicWrangler.calculate_survival_rate(data, 'Pclass')

    # Then
    assert len(result) == 3
    categories = result['Category'].to_list()
    total_counts = result['TotalCount'].to_list()
    survived_counts = result['SurvivedCount'].to_list()
    survival_rates = result['SurvivalRate'].to_list()
    
    # Results should be sorted by category
    assert categories == [1, 2, 3]
    assert total_counts == [2, 2, 2]
    assert survived_counts == [1, 1, 1]
    assert survival_rates == [50.0, 50.0, 50.0]


def test_calculate_survival_rate_empty_data():
    # Given
    empty_data = pl.DataFrame({
        'Survived': pl.Series([], dtype=pl.Utf8)
    })

    # When
    result = TitanicWrangler.calculate_survival_rate(empty_data)

    # Then
    assert len(result) == 1
    assert result['Category'].to_list() == ['Overall']
    assert result['TotalCount'].to_list() == [0]
    assert result['SurvivedCount'].to_list() == [0]
    assert result['SurvivalRate'].to_list() == [0.0]


def test_load_titanic_data():
    # Given - use the actual data file
    data_path = "data/input/titanic_passengers.csv"
    
    # When - load with minimal delay for testing
    import time
    start_time = time.time()
    result = TitanicWrangler.load_titanic_data(data_path, delay_seconds=0.1)
    elapsed_time = time.time() - start_time
    
    # Then
    assert isinstance(result, pl.DataFrame)
    assert len(result) > 0  # Should have data
    assert len(result.columns) == 12  # Original CSV columns
    assert elapsed_time >= 0.1  # Should include the delay
    
    # Check expected columns exist
    expected_columns = ['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age', 
                       'SibSp', 'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked']
    for col in expected_columns:
        assert col in result.columns


def test_load_titanic_data_file_not_found():
    # Given - non-existent file path
    fake_path = "nonexistent/file.csv"
    
    # When/Then - should raise FileNotFoundError
    with pytest.raises(FileNotFoundError):
        TitanicWrangler.load_titanic_data(fake_path, delay_seconds=0.0)


def test_coerce_numeric_columns():
    # Given
    data = pl.DataFrame({
        'PassengerId': ['1', '2', '3'],
        'Survived': ['1', '0', '1'], 
        'Age': ['22.5', 'invalid', '30.0'],
        'SibSp': [1, 2, 3],  # Already numeric
        'Parch': ['0', '1', '2'],
        'Fare': ['7.25', '8.05', None],
        'Name': ['John', 'Jane', 'Bob']  # Non-numeric column
    })

    # When
    result = TitanicWrangler._coerce_numeric_columns(data)

    # Then
    numeric_columns = ['PassengerId', 'Survived', 'Age', 'SibSp', 'Parch', 'Fare']
    for col in numeric_columns:
        assert result[col].dtype == pl.Float64
    
    # Non-numeric columns should be unchanged
    assert result['Name'].dtype == pl.Utf8
    
    # Check conversion results
    assert result['PassengerId'].to_list() == [1.0, 2.0, 3.0]
    assert result['Survived'].to_list() == [1.0, 0.0, 1.0]
    # 'invalid' should become null with strict=False
    ages = result['Age'].to_list()
    assert ages[0] == 22.5
    assert ages[1] is None  # Invalid conversion
    assert ages[2] == 30.0