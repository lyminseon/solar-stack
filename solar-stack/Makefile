# ===== Config =====
ENV ?= dev                          # dev | prod
PROJECT_NAME := hudius-solar-stack
COMPOSE_DIR := compose
COMPOSE_FILES := -f $(COMPOSE_DIR)/docker-compose.base.yml
ifeq ($(ENV),prod)
  COMPOSE_FILES += -f $(COMPOSE_DIR)/docker-compose.prod.yml
else
  COMPOSE_FILES += -f $(COMPOSE_DIR)/docker-compose.dev.yml
endif
C := docker compose -p $(PROJECT_NAME) $(COMPOSE_FILES)

# ===== Phony =====
.PHONY: help install init run stop down ps logs up restart exec renew-cert reload-nginx health seed feast apply grafana-init superset-init airflow-users prune

help: ## 명령어 목록
	@grep -E '^[a-zA-Z0-9_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "\033[36m%-16s\033[0m %s\n", $$1, $$2}'

install: ## 이미지 pull 및 초기 리소스 생성
	$(C) pull
	$(C) create

init: ## 1회 초기화(마이그/정적/Feast 등) - 컨테이너 up 이후 실행 권장
	# Portal DB 마이그/정적
	$(C) run --rm portal bash -lc 'pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput'
	# Feast repo 적용 (필요 시)
	$(C) run --rm portal bash -lc 'pip install -r requirements.txt && cd /srv/feast && feast apply || true'
	# (선택) Airflow 초기 사용자/권한 스크립트가 있다면 여기서 실행
	# $(C) run --rm airflow-init

run: ## 서비스 기동(up) 및 상태 출력
	$(C) up -d --remove-orphans --wait
	$(C) ps

up: ## up만 수행(대기 포함)
	$(C) up -d --remove-orphans --wait

stop: ## 서비스 중지
	$(C) stop

down: ## 서비스 종료 및 네트워크/익명볼륨 제거
	$(C) down -v

ps: ## 상태 확인
	$(C) ps

logs: ## 전체 로그 tail (svc=<서비스명> 지정 가능)
ifdef svc
	$(C) logs -f --tail=200 $(svc)
else
	$(C) logs -f --tail=200
endif

restart: ## 서비스 재시작 (svc=<서비스명> 없으면 전체)
ifdef svc
	$(C) restart $(svc)
else
	$(C) restart
endif

exec: ## 컨테이너 명령 실행 (svc=<서비스명> cmd="...") 
	$(C) exec $(svc) bash -lc $(cmd)

health: ## 핵심 엔드포인트 헬스 점검(nginx 내부에서)
	$(C) exec nginx sh -lc "\
	  set -e; \
	  for u in \
	    'http://portal:8001/healthz' \
	    'http://airflow-api-server:8080/health' \
	    'http://oauth2-proxy-mlflow:4180/oauth2/start' \
	    'http://keycloak:8080/realms/solar/.well-known/openid-configuration' \
	    'http://grafana:3000/api/health' \
	    'http://superset:8088/health' \
	    'http://prometheus:9090/-/ready' \
	    'http://loki:3100/ready' \
	    'http://minio:9001/minio/health/ready' \
	  ; do echo \"Checking $$u\"; curl -sf $$u > /dev/null || exit 1; done; echo OK \
	"

renew-cert: ## certbot 갱신 + nginx reload
	$(C) run --rm certbot renew --non-interactive --quiet || true
	$(C) exec nginx nginx -t
	$(C) exec nginx nginx -s reload

reload-nginx: ## nginx 설정 reload
	$(C) exec nginx nginx -t
	$(C) exec nginx nginx -s reload

prune: ## 쓰지 않는 리소스 정리
	docker system prune -f

