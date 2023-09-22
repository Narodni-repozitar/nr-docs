black oarepo_vocabularies tests --target-version py310
autoflake --in-place --remove-all-unused-imports --recursive oarepo_vocabularies tests
isort oarepo_vocabularies tests  --profile black
