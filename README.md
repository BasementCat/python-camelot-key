# camelot_key

Python library to parse and format musical key notation and convert between
Camelot key notation.

## Usage

The `camelot_key` package provides a `parse()` method that takes a value
representing a musical or camelot key, and returns a `Key` instance that
contains the parsed data.  `Key` instances can be compared and sorted, shifted
to adjacent keys, and contain details on the musical key and camelot key.  For
more detailed information, see the `docs/` folder.

## Development

For local development, run `pipenv install`, which will install development
dependencies as well.

### Testing

Run `pipenv run python -m unittest`

### Documentation Generation

Run `pipenv run pdoc --html --output-dir docs camelot_key --force`

### Deployment

  1. Ensure tests pass
  2. Ensure latest documentation is generated
  3. Update the version in `src/camelot_key/__init__.py`
  4. Build the packages: `pipenv run python -m build`
  5. Upload the packages: `pipenv run python -m twine upload dist/*`