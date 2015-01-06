# encoding: utf-8

import unittest
from tests import MOCKUPS_PATH
from static_bundle import (CssBundle, JsBundle,
                           OtherFilesBundle, FilePath,
                           DirectoryPath, BuilderConfig,
                           Asset, StandardBuilder)


class BundlesTest(unittest.TestCase):

    def test_adding_file(self):
        bundle = JsBundle('js')
        bundle.add_file('include/app.js')
        bundle.add_files([
            ['vendors', 'example1.js'],
            'vendors/example2.js'
        ])

        bundle.add_path_object(FilePath('include/modules/module1.js'))

        self.assertEqual(len(bundle.files), 4)
        self.assertIsInstance(bundle.files[0], FilePath)
        self.assertIsInstance(bundle.files[1], FilePath)
        self.assertIsInstance(bundle.files[2], FilePath)
        self.assertIsInstance(bundle.files[3], FilePath)
        self.assertEqual(bundle.files[0].bundle, bundle)
        self.assertEqual(bundle.files[1].bundle, bundle)
        self.assertEqual(bundle.files[2].bundle, bundle)
        self.assertEqual(bundle.files[3].bundle, bundle)
        self.assertEqual(bundle.files[0].file_path, 'include/app.js')
        self.assertEqual(bundle.files[1].file_path, 'vendors/example1.js')
        self.assertEqual(bundle.files[2].file_path, 'vendors/example2.js')
        self.assertEqual(bundle.files[3].file_path, 'include/modules/module1.js')

    def test_adding_directories(self):
        bundle = JsBundle('js')
        bundle.add_directory('include/modules')
        bundle.add_directory('vendors')

        self.assertEqual(len(bundle.files), 2)
        self.assertIsInstance(bundle.files[0], DirectoryPath)
        self.assertIsInstance(bundle.files[1], DirectoryPath)
        self.assertEqual(bundle.files[0].directory_path, 'include/modules')
        self.assertEqual(bundle.files[1].directory_path, 'vendors')

    def test_input_dir(self):
        bundle = JsBundle('js')
        bc = BuilderConfig('tests/mockups/src', 'tests/mockups/out')
        builder = StandardBuilder(bc)
        asset = builder.create_asset("test-example")
        asset.add_bundle(bundle)
        asset.collect_files()
        self.assertEquals(len(asset.files), 6)
        self.assertTrue(bundle.abs_path)
        self.assertEqual(bundle.abs_bundle_path, MOCKUPS_PATH + '/src/js')
        self.assertEqual(bundle.input_dir, bc.input_dir)

