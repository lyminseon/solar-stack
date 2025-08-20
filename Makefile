# ===== Config =====
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


# ===== Solar cert workflow =====
acme: cert-issue ## 1) .26:80 임시 오픈 → 발급 → 종료(한 번에)


cert-open: ## (임시) .26:80만 오픈 (acme-nginx up)
$(S) --profile acme up -d acme-nginx
@echo ">> .26:80 opened (acme-nginx)."


cert-issue: cert-open ## 인증서 발급(webroot)
$(S) run --rm certbot-init
$(S) --profile acme down
@$(MAKE) cert-check


cert-clean: ## (필요시) acme 리소스 종료
$(S) --profile acme down


cert-check: ## 인증서 존재 확인
@docker run --rm -v $(CERT_VOL):/etc/letsencrypt alpine:3.20 \
sh -lc 'set -e; ls -l /etc/letsencrypt/live/$(CERT_DOMAIN)/fullchain.pem /etc/letsencrypt/live/$(CERT_DOMAIN)/privkey.pem >/dev/null && echo "✅ cert OK: $(CERT_DOMAIN)"' \
|| (echo "❌ cert not found: $(CERT_DOMAIN)"; exit 1)


deploy-solar: ## 3) 운영 전환 (nginx 80/443 + 내부 스택, certbot-renew 포함)
$(S) --profile prod up -d --remove-orphans --wait
$(S) ps


renew-solar: ## 수동 갱신 + nginx reload (프로필 prod 사용 중일 때)
$(S) run --rm certbot renew --webroot -w /var/www/certbot --quiet || true
$(S) exec nginx nginx -t
$(S) exec nginx nginx -s reload


enable-https-conf: ## (선택) HTTPS conf 전환
@test -f git/nginx/conf.d/solar-https.conf.off && mv git/nginx/conf.d/solar-https.conf.off git/nginx/conf.d/solar-https.conf || true