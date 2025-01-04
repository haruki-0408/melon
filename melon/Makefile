################################
# 共通変数
################################
ENV_FILE = env.json
LOG_DIR = logs
EVENT_DIR = events

################################
# Lambda関数のリスト
################################
FUNCTIONS = \
	GetFakeThesisTitleCategoryFormat \
	GeneratePromptParameters \
	RequestGenerativeAiModelApi \
	FakeThesisDataValidation \
	FixFakeThesisData \
	SendWorkflowCallback \
	GenerateFakeFormula \
	GenerateFakeTable \
	GenerateFakeGraph \
	ConvertToPdf \
	WorkflowProgressRecorder

################################
# Lambda ローカル実行
################################
# ログディレクトリ作成
$(LOG_DIR):
	mkdir -p $(LOG_DIR)

# 各Lambda関数のローカル実行ルール
.PHONY: $(FUNCTIONS)
$(FUNCTIONS): $(LOG_DIR)
	@echo "Invoking $@..."
	sam local invoke $@ \
		--event $(EVENT_DIR)/$(shell echo $@ | tr '[:upper:]' '[:lower:]')/event.json \
		--env-vars $(ENV_FILE) \
		2> $(LOG_DIR)/$(shell echo $@ | tr '[:upper:]' '[:lower:]').log

################################
# テスト関連
################################
# テスト設定
TEST_DIR = tests/unit
PYTEST_FLAGS = -v -s

# 全単体テスト実行
.PHONY: test-unit
test-unit:
	pytest $(PYTEST_FLAGS) $(TEST_DIR)

# 特定関数の単体テスト実行
.PHONY: test-%
test-%:
	@echo "Running tests for $*..."
	pytest $(PYTEST_FLAGS) $(TEST_DIR)/test_$(shell echo $* | tr '[:upper:]' '[:lower:]').py

# テストカバレッジレポート生成
.PHONY: test-coverage
test-coverage:
	pytest --cov=functions --cov-report=html $(TEST_DIR)

################################
# ヘルプ
################################
.PHONY: help
help:
	@echo "Available targets:"
	@echo "\nLambda Local Invoke:"
	@echo "  make <function-name>     - Invoke specific Lambda function locally"
	@echo "\nTest Execution:"
	@echo "  make test-unit           - Run all unit tests"
	@echo "  make test-<function>     - Run tests for specific function"
	@echo "  make test-coverage       - Generate test coverage report"
	@echo "\nAvailable Lambda functions:"
	@echo "  $(FUNCTIONS)" | tr ' ' '\n' | sed 's/^/  /' 