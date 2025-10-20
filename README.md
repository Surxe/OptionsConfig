# OptionsConfig
Configure options for your repository for environment variables, arguments, and documentation generation

<!-- BEGIN_GENERATED_OPTIONS -->
#### Parse

- **SHOULD_PARSE** - Whether to parse the game files after downloading.
  - Default: `"false"`
  - Command line: `--should-parse`

* **GAME_NAME** - Name of the game to download.
  - Default: `"WRFrontiers"`
  - Command line: `--game-name`
  - Depends on: `SHOULD_PARSE`

* **EXPORT_DIR** - Directory where the exported game JSON files are stored.
  - Default: None - required when SHOULD_PARSE is True
  - Command line: `--export-dir`
  - Depends on: `SHOULD_PARSE`


#### Push Data

- **SHOULD_PUSH_DATA** - Whether to push parsed data to the data repository.
  - Default: `"false"`
  - Command line: `--should-push-data`

* **GAME_VERSION** - Version of the game being processed, as its release date yyyy-mm-dd.
  - Default: None - required when SHOULD_PUSH_DATA is True
  - Command line: `--game-version`
  - Depends on: `SHOULD_PUSH_DATA`

* **CURRENT_IS_LATEST** - Whether to also push data to the 'current' directory (in addition to archive).
  - Default: `"true"`
  - Command line: `--current-is-latest`
  - Depends on: `SHOULD_PUSH_DATA`

* **TARGET_BRANCH** - Target branch to push data to in the data repository.
  - Default: `"testing-grounds"`
  - Command line: `--target-branch`
  - Depends on: `SHOULD_PUSH_DATA`

* **GH_DATA_REPO_PAT** - PAT token to the GitHub repository that stores the data.
  - Default: None - required when SHOULD_PUSH_DATA is True
  - Command line: `--gh-data-repo-pat`
  - Depends on: `SHOULD_PUSH_DATA`


#### Both

- **LOG_LEVEL** - Logging level. Must be one of: DEBUG, INFO, WARNING, ERROR, CRITICAL.
  - Default: `"DEBUG"`
  - Command line: `--log-level`

* **OUTPUT_DIR** - Directory where the parser will output files and where data is pushed from.
  - Default: None - required when SHOULD_PARSE or SHOULD_PUSH_DATA is True
  - Command line: `--output-dir`
  - Depends on: `SHOULD_PARSE`, `SHOULD_PUSH_DATA`


<!-- END_GENERATED_OPTIONS -->