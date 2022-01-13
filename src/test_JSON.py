# Code developed by Lina Rietuma and Ryan Farish 

import JSON
import unittest

class test_JSON(unittest.TestCase):
    def test_incorrect_file_path(self):
        path = 'src/nonexistant path'
        with self.assertRaises(ValueError):
            JSON.JSON(path)
        
    def test_corrupted_file(self):
        path = 'test_data/corrupted_test_file.json'
        with self.assertRaises(ValueError):
            JSON.JSON(path)
    
    def test_find_browser(self):
        browser_list = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36']
        path = 'test_data/browser_test_data.json'
        expected_results = ['Mozilla - Chrome']
        json = JSON.JSON(path)
        self.assertEqual(json.find_browser(browser_list), expected_results)
    
    def test_top_reader(self):
        path = 'test_data/browser_test_data.json'
        expected_results = 'ade7e1f63bc83c66 - 0.0 hours'
        json = JSON.JSON(path)
        top_readers = json.top_readers()
        self.assertEqual(top_readers, expected_results)
    
    def test_get_unique(self):
        path = 'test_data/unique_test_data.json'
        expected_results = ['ade7e1f63bc83c66']
        json = JSON.JSON(path)
        doc_uuid = '140222143932-91796b01f94327ee809bd759fd0f6c76'
        unique = json.get_unique(doc_uuid, json.data)
        self.assertEqual(unique, expected_results)
        
if __name__ == '__main__':
    unittest.main()