# テスト設定
TEST_DIR = tests/unit
TEST_LOG_DIR = tests/logs
PYTEST_FLAGS = -v -s --capture=tee-sys
LAMBDA_DOCKER_IMAGE = public.ecr.aws/sam/build-python3.12:latest

# Dockerボリュームマウントのパス設定（テスト用）
MOUNT_PATHS = \
	-v $(PWD)/functions:/var/task/functions \
	-v $(PWD)/layers/common:/opt/python \
	-v $(PWD)/tests:/var/task/tests \
	-v $(PWD)/pytest.ini:/var/task/pytest.ini

# テスト実行用の共通Docker実行コマンド
DOCKER_TEST_CMD = docker run --rm \
	-w /var/task \
	$(MOUNT_PATHS) \
	-e PYTHONPATH=/opt/python \
	-e PYTHONDONTWRITEBYTECODE=1 \
	-e AWS_DEFAULT_REGION=ap-northeast-1 \
	-e WORKFLOW_EVENT_BUS_NAME=test-bus \
	-e DYNAMO_DB_WORKFLOW_PROGRESS_TABLE=test-progress-table \
	-e DYNAMO_DB_CATEGORY_MASTER_TABLE=test-category-table \
	-e S3_BUCKET=test-bucket \
	$(LAMBDA_DOCKER_IMAGE)

# テストコマンド
.PHONY: test-unit test-success test-failed test-validation-failed

$(TEST_LOG_DIR):
	@mkdir -p $(TEST_LOG_DIR)

test-unit: $(TEST_LOG_DIR)
	@$(DOCKER_TEST_CMD) /bin/bash -c "\
		pip install -r tests/requirements.txt > /dev/null 2>&1 && \
		python -m pytest $(PYTEST_FLAGS) $(TEST_DIR)" \
		2>&1 | tee $(TEST_LOG_DIR)/test-unit-$$(date +%Y%m%d-%H%M%S).log

# 正常系テスト実行
test-success: $(TEST_LOG_DIR)
	@if [ -n "$(filter-out test-success,$(MAKECMDGOALS))" ]; then \
		TEST_FILE=$$(echo $(filter-out test-success,$(MAKECMDGOALS)) | tr '[:upper:]' '[:lower:]'); \
		$(DOCKER_TEST_CMD) /bin/bash -c "\
			pip install -r tests/requirements.txt > /dev/null 2>&1 && \
			python -m pytest $(PYTEST_FLAGS) -m 'success' $(TEST_DIR)/$${TEST_FILE}.py" \
			2>&1 | tee $(TEST_LOG_DIR)/$${TEST_FILE}-success.log; \
	else \
		echo "Please specify a test file name"; \
		exit 1; \
	fi

# エラー系テスト実行
test-failed: $(TEST_LOG_DIR)
	@if [ -n "$(filter-out test-failed,$(MAKECMDGOALS))" ]; then \
		TEST_FILE=$$(echo $(filter-out test-failed,$(MAKECMDGOALS)) | tr '[:upper:]' '[:lower:]'); \
		$(DOCKER_TEST_CMD) /bin/bash -c "\
			pip install -r tests/requirements.txt > /dev/null 2>&1 && \
			python -m pytest $(PYTEST_FLAGS) -m 'failed' $(TEST_DIR)/$${TEST_FILE}.py" \
			2>&1 | tee $(TEST_LOG_DIR)/$${TEST_FILE}-failed.log; \
	else \
		echo "Please specify a test file name"; \
		exit 1; \
	fi

# バリデーションエラー系テスト実行
test-validation-failed: $(TEST_LOG_DIR)
	@if [ -n "$(filter-out test-validation-failed,$(MAKECMDGOALS))" ]; then \
		TEST_FILE=$$(echo $(filter-out test-validation-failed,$(MAKECMDGOALS)) | tr '[:upper:]' '[:lower:]'); \
		$(DOCKER_TEST_CMD) /bin/bash -c "\
			pip install -r tests/requirements.txt > /dev/null 2>&1 && \
			python -m pytest $(PYTEST_FLAGS) -m 'validation_failed' $(TEST_DIR)/$${TEST_FILE}.py" \
			2>&1 | tee $(TEST_LOG_DIR)/$${TEST_FILE}-validation-failed.log; \
	else \
		echo "Please specify a test file name"; \
		exit 1; \
	fi

# 未定義のターゲットを許容するためのパターンルール
%:
	@:

# ヘルプ
.PHONY: help
help:
	@echo "Test Commands:"
	@echo "  make test-unit                        - Run all unit tests"
	@echo "  make test-success <filename>          - Run success case tests"
	@echo "  make test-failed <filename>           - Run error case tests"
	@echo "  make test-validation-failed <filename>- Run validation error tests"
	@echo "\nExample:"
	@echo "  make test-success test_fake_thesis_data_validation" 