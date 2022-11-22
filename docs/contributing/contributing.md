## Contribution Guidelines

### LinkML Testing Framework

* The LinkML test suite can be found in the [tests](../../tests/) folder. The tests are written under specific subfolders within the main aggregated [tests](../../tests/) suite. 
* If you want to formalize your test case into a unit test, you should decide the scope of your test and find the subfolder that the test might best fit under. For example, if your test is related to one of the LinkML generators, then you would create it under the [test_generators](../../tests/test_generators/) subfolder.
* There are a few model LinkML schemas within the test suite that you can use while creating your unit tests. You will ideally find them in an `input` directory within the scoped tests folder you are looking at. For example, the [input](../../tests/test_generators/input/) directory under the [test_generators](../../tests/test_generators/) subfolder. One of the main test schemas that most LinkML generator related unit tests use is the [kitchen_sink.yaml](../../tests/test_generators/input/kitchen_sink.yaml).
* Outside of generators, users will want to create issue specific unit tests. For that, you need to turn your attention to the [test_issues](../../tests/test_issues/) folder. 
  * The current direction is to first make an issue with specific instructions to reproduce the bug under the [issues](https://github.com/linkml/linkml/issues) tab on the main [linkml](https://github.com/linkml/linkml/) GitHub repo.
  * Then, create a test case for the above issue, with an minimal test LinkML schema in the input folder of the [test_issues](../../tests/test_issues/) suite. A minimal test case entails that you only use the elements you need in the schema for your unit test and not bloat the test schema with more elements that necessary.
  * Ideally, it is also advised not to bloat the output folders under each sub test suites with large autogenerated outputs. You can use the Python standard [tempfile](https://docs.python.org/3/library/tempfile.html) module to create temporary files where you can direct the output to and then load in the temporary file however for your test case assertions. See an example [here](../../tests/test_generators/test_excelgen.py).

#### Directions for creating a unit test

There are two cases you need to consider while writing your unit test. The first one is when you are writing a test for bugs in the LinkML library and the second is for enhancements. For bugs you would typically create your test case in the [test_issues](../../tests/test_issues/) folder, whereas for enhancements, you would typically create it in the [test_generators](../../tests/test_generators/), [test_utils](../../tests/test_utils/), etc. subfolder.
* While creating a test for a bug, you can should make a file called `test_linkml_issue_NNN.py`. After that it is perhaps easiest to just copy over a test from an existing issue test case and modify it.
  * As discussed above, ideally, all your test issues will have an accompanying minimal test schema. One pattern is that you include the schema in your Python unit test file as strings. Another pattern is to include them as separate YAML files in the `input` folder.
* As for new functionality, as directed above, create a test case under any of the existing Python test files if there are tests already scoped with respect to your enhancement. Or if not, then create a new Python test file with your unit test.
* All tests within this repo are Python [unittest](https://docs.python.org/3/library/unittest.html) tests. The unittest module is bundled natively with the latest versions of Python. The tests can be run using either the unittest module, or using the [pytest](https://docs.pytest.org/en/6.2.x/) library.
* If you have already activated the poetry virtual environment, then there is no need to use the `poetry run` prefix.
* If you want to isolate specific test methods from within your Python unit test file, then you can use the `-k` option for the unittest module. Refer to [unittest](https://docs.python.org/3.3/library/unittest.html) module docs for more information on its usage.


To run your  test using `unittest`:

```python
poetry run python -m unittest tests/test_issues/test_linkml_issue_NNN.py
```

To run your test using `pytest`:

```python
poetry run pytest tests/test_issues/test_linkml_issue_NNN.py
```
You can run the full test suite in the following way:

```
poetry run python -m unittest discover
```

* When you create a Pull Request with your unit test on the linkml repo, the a GitHub Action run will be set off which runs the entire test suite with the new test case that you added, on that test case branch too.

Note: You will see a number of issues which are named `test_issue_NNN.py`. The numbers and convention for those issues are with reference to the old *biolinkml* issue numbering convention.

#### General Tips

* Always make sure to use `assert` statements to compare the expected value with the actual value, rather than simply printing or logging the expected and actual values.
* Avoid using `print` statements for logging purposes. Use the `logging` module natively provided by Python approporiately with it's various logging levels like `DEBUG`, `INFO`, `ERROR`, etc.
* You can create a config file by copying the [test_config.ini.example](https://github.com/linkml/linkml/blob/main/tests/test_config.ini.example) to a `test_config.ini` file and making changes, for example, to the logging levels:

```
[test.settings]
DEFAULT_LOG_LEVEL: logging.ERROR
DEFAULT_LOG_LEVEL_TEXT: ERROR
```

* Never hardcode any file paths. Always use import variables such as `INPUT_DIR`, `OUTPUT_DIR` and use `os.path.join()` to make file paths. This ensures that the tests will run independent of the OS they are running on.
* Running the test suite may change many files in the `output` folders accompanying the sub test suites which overloads the `git status` lists with unnecessary file changes. This should be avoided by not adding the output files changed to `git status`, removing them if they got added automatically, or implement the temporary file solution discussed previously.
* To ignore the changed files run the shell script `hide_test_changes.sh`.
* To reset all test output files back to original state use the shell script `checkout_outputs.sh`.


#### IDE Tips
PyCharm, IntelliJ:

To run a single test:
* Open to Run/Debug
* `+` to add test
* Choose Python "tests > unittests"
* In dialog:
  * Target: Select Script path, browse to test script
  * Choose Python interpreter
  * Click ‘OK’ to save
* Run or debug the test from the configurations menu

To run all tests:
* Open to Run/Debug
* `+` to add test
* Choose “Python tests > unittests”

### Release to PyPI

A Github action is set up to automatically release the package to PyPI. When it is ready for a new release, create a [Github release](https://github.com/linkml/releases). The version should be in the vX.X.X format following [the semantic versioning specification](https://semver.org/).

Release notes should always be autogenerated (just click the "generate release notes" button) - these can be tweaked but the emphasis should be on making sure PR titles and githu issue titles are clear and concise. Note we don't keep a separate CHANGELOG file, it all goes in the release notes.

After the release is created, the GitHub action will be triggered to publish to PyPI. The release version will be used to create the PyPI package.

If the PyPI release failed, make fixes, [delete](https://docs.github.com/en/enterprise/2.16/user/github/administering-a-repository/editing-and-deleting-releases#deleting-a-release) the GitHub release, and recreate a release with the same version again.