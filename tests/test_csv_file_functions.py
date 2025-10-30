import os
os.environ["DATA_DIR"] = "test"
DATA_DIR = os.environ["DATA_DIR"]

import unittest
import os
from csv_file_functions import read_csv, write_to_csv, append_to_csv
from typing import List, Dict
import json


class TestCSVTools(unittest.TestCase):
    """Unit tests for CSV agent tools: read_csv, write_to_csv, and append_to_csv."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test directory from DATA_DIR environment variable."""
        data_dir = os.environ.get('DATA_DIR')
        if not data_dir:
            raise EnvironmentError("DATA_DIR environment variable must be set")
        
        cls.data_dir: str = data_dir
        
        # Create DATA_DIR if it doesn't exist
        os.makedirs(cls.data_dir, exist_ok=True)
    
    def setUp(self):
        """Set up test data before each test."""
        # self.test_file: str = os.path.join(self.data_dir, 'test.csv')
        self.test_file: str = 'test.csv'
        
        # Sample test data as list of dictionaries
        self.column_names: List[str] = ['Name', 'Age', 'City']
        self.test_data: List[Dict[str, str]] = [
            {'Name': 'Alice', 'Age': '30', 'City': 'New York'},
            {'Name': 'Bob', 'Age': '25', 'City': 'San Francisco'}
        ]
        
        self.append_data: List[Dict[str, str]] = [
            {'Name': 'Charlie', 'Age': '35', 'City': 'Chicago'}
        ]
    
    def tearDown(self):
        """Clean up test files after each test."""
        # Remove test file if it exists
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        
        # Clean up any other test files
        test_files = ['test2.csv', 'empty.csv', 'special.csv', 'test1.csv']
        for file in test_files:
            filepath: str = os.path.join(self.data_dir, file)
            if os.path.exists(filepath):
                os.remove(filepath)
    
    def test_write_creates_file(self):
        """Test that write_to_csv.invoke() creates a new CSV file."""
        write_to_csv.invoke({
            "path": self.test_file,
            "data": self.test_data,
            "column_names": self.column_names
        })
        self.assertTrue(os.path.exists(os.path.join(self.data_dir, 'test.csv')))
    
    def test_write_and_read_content(self):
        """Test that write_to_csv.invoke() writes correct content and read_csv.invoke() reads it."""
        write_to_csv.invoke({
            "path": self.test_file,
            "data": self.test_data,
            "column_names": self.column_names
        })
        
        result = json.loads(read_csv.invoke({"path": self.test_file}))
        self.assertEqual(result, self.test_data)
    
    def test_write_overwrites_existing(self):
        """Test that write_to_csv.invoke() overwrites existing file content."""
        # Write initial data
        write_to_csv.invoke({
            "path": self.test_file,
            "data": self.test_data,
            "column_names": self.column_names
        })
        
        # Overwrite with new data
        new_data: List[Dict[str, str]] = [{'X': '1', 'Y': '2'}]
        new_columns: List[str] = ['X', 'Y']
        write_to_csv.invoke({
            "path": self.test_file,
            "data": new_data,
            "column_names": new_columns
        })
        
        result = json.loads(read_csv.invoke({"path": self.test_file}))
        self.assertEqual(result, new_data)
        self.assertNotEqual(result, self.test_data)
    
    def test_read_nonexistent_file(self):
        """Test that read_csv.invoke() raises appropriate error for nonexistent file."""
        nonexistent: str = 'nonexistent.csv'
        self.assertEqual(f"Error encountered while reading from file ({nonexistent}): [Errno 2] No such file or directory: 'test/{nonexistent}'", read_csv.invoke({"path": nonexistent}))
    
    def test_read_empty_file(self):
        """Test that read_csv.invoke() handles empty CSV files."""
        empty_file: str = 'empty.csv'
        # Create empty file
        open(os.path.join(self.data_dir, empty_file), 'w').close()
        result = json.loads(read_csv.invoke({"path": empty_file}))
        self.assertEqual(result, [])
    
    def test_append_to_existing_file(self):
        """Test that append_to_csv.invoke() appends data to existing CSV file."""
        # Write initial data
        write_to_csv.invoke({
            "path": self.test_file,
            "data": self.test_data,
            "column_names": self.column_names
        })
        
        # Append new data
        append_to_csv.invoke({
            "path": self.test_file,
            "data": self.append_data,
            "column_names": self.column_names
        })
        
        # Verify both original and appended data exist
        result = json.loads(read_csv.invoke({"path": self.test_file}))
        expected: List[Dict[str, str]] = self.test_data + self.append_data
        self.assertEqual(result, expected)
    
    def test_append_to_nonexistent_file(self):
        """Test that append_to_csv.invoke() creates file if it doesn't exist."""
        append_to_csv.invoke({
            "path": self.test_file,
            "data": self.append_data,
            "column_names": self.column_names
        })
        
        self.assertTrue(os.path.exists(os.path.join(self.data_dir, self.test_file)))
        result = json.loads(read_csv.invoke({"path": self.test_file}))
        self.assertEqual(result, self.test_data + self.append_data + self.append_data)
    
    def test_append_multiple_times(self):
        """Test multiple append operations."""
        write_to_csv.invoke({
            "path": self.test_file,
            "data": self.test_data,
            "column_names": self.column_names
        })
        
        append_to_csv.invoke({
            "path": self.test_file,
            "data": self.append_data,
            "column_names": self.column_names
        })
        
        append_to_csv.invoke({
            "path": self.test_file,
            "data": [{'Name': 'David', 'Age': '40', 'City': 'Boston'}],
            "column_names": self.column_names
        })
        
        result = json.loads(read_csv.invoke({"path": self.test_file}))
        self.assertEqual(len(result), 4)  # 3 original + 1 appended
    
    def test_read_write_special_characters(self):
        """Test handling of special characters in CSV data."""
        special_file: str = 'special.csv'
        special_columns: List[str] = ['Name', 'Description']
        special_data: List[Dict[str, str]] = [
            {'Name': 'Item1', 'Description': 'Contains, comma'},
            {'Name': 'Item2', 'Description': 'Contains "quotes"'},
            {'Name': 'Item3', 'Description': 'Contains\nnewline'}
        ]
        
        write_to_csv.invoke({
            "path": special_file,
            "data": special_data,
            "column_names": special_columns
        })
        
        result = json.loads(read_csv.invoke({"path": special_file}))
        self.assertEqual(result, special_data)
    
    def test_write_empty_data(self):
        """Test writing empty data list."""
        write_to_csv.invoke({
            "path": self.test_file,
            "data": [],
            "column_names": self.column_names
        })
        
        result = json.loads(read_csv.invoke({"path": self.test_file}))
        self.assertEqual(result, [])
    
    def test_append_empty_data(self):
        """Test appending empty data list."""
        write_to_csv.invoke({
            "path": self.test_file,
            "data": self.test_data,
            "column_names": self.column_names
        })
        
        append_to_csv.invoke({
            "path": self.test_file,
            "data": [],
            "column_names": self.column_names
        })
        
        result = json.loads(read_csv.invoke({"path": self.test_file}))
        self.assertEqual(result, self.test_data)
    
    def test_multiple_files(self):
        """Test working with multiple CSV files."""
        file1: str = 'test1.csv'
        file2: str = 'test2.csv'
        
        data1: List[Dict[str, str]] = [{'A': '1', 'B': '2'}]
        data2: List[Dict[str, str]] = [{'X': '3', 'Y': '4'}]
        
        write_to_csv.invoke({
            "path": file1,
            "data": data1,
            "column_names": ['A', 'B']
        })
        
        write_to_csv.invoke({
            "path": file2,
            "data": data2,
            "column_names": ['X', 'Y']
        })
        
        result1 = json.loads(read_csv.invoke({"path": file1}))
        result2 = json.loads(read_csv.invoke({"path": file2}))
        
        self.assertEqual(result1, data1)
        self.assertEqual(result2, data2)
    
    def test_complete_workflow(self):
        """Test a complete workflow using all three tools."""
        # Write initial data
        write_to_csv.invoke({
            "path": self.test_file,
            "data": self.test_data,
            "column_names": self.column_names
        })
        
        # Read and verify
        data = json.loads(read_csv.invoke({"path": self.test_file}))
        self.assertEqual(len(data), 2)
        
        # Append more data
        append_to_csv.invoke({
            "path": self.test_file,
            "data": self.append_data,
            "column_names": self.column_names
        })
        
        # Read final result
        final_data = json.loads(read_csv.invoke({"path": self.test_file}))
        self.assertEqual(len(final_data), 3)
        self.assertEqual(final_data[0]['Name'], 'Alice')
        self.assertEqual(final_data[-1]['Name'], 'Charlie')
    
    def test_column_order_preserved(self):
        """Test that column order is preserved in write and append operations."""
        custom_order: List[str] = ['City', 'Name', 'Age']
        data: List[Dict[str, str]] = [{'City': 'New York', 'Name': 'Alice', 'Age': '30'}]
        
        write_to_csv.invoke({
            "path": self.test_file,
            "data": data,
            "column_names": custom_order
        })
        
        result = json.loads(read_csv.invoke({"path": self.test_file}))
        # Verify the data is correctly read back
        self.assertEqual(result[0]['City'], 'New York')
        self.assertEqual(result[0]['Name'], 'Alice')


if __name__ == '__main__':
    unittest.main()