#!/bin/zsh
set -e

echo "🚀 iOS 패키징 시작 (Capacitor + Next.js)..."

FRONTEND_DIR="/Users/jhy20/mpz_fullstack/frontend"
IOS_DIR="$FRONTEND_DIR/ios"
WEB_BUILD_DIR="$FRONTEND_DIR/.next"

cd "$FRONTEND_DIR"

# 의존성 설치 (node_modules가 없을 때만)
if [ ! -d "node_modules" ]; then
	echo "📦 의존성 설치 (node_modules 없음)"
	if command -v npm >/dev/null 2>&1; then
		npm install
	else
		echo "❌ npm을 찾을 수 없습니다. Node.js/npm 설치 후 다시 시도하세요."
		exit 1
	fi
else
	echo "⏭️  의존성 설치 스킵 (node_modules 존재)"
fi

export NEXT_TELEMETRY_DISABLED=1
export NEXT_DISABLE_SOURCEMAP="${NEXT_DISABLE_SOURCEMAP:-1}"

echo "🧱 Next.js 프로덕션 빌드 (next build)"
rm -rf "$WEB_BUILD_DIR"
if npm run -s build; then
	echo "✅ Next.js 빌드 완료"
else
	echo "❌ Next.js 빌드 실패"
	exit 1
fi

if [ "$NEXT_DISABLE_SOURCEMAP" = "1" ]; then
	echo "🧹 소스맵 제거 (앱 용량 최적화)"
	find "$WEB_BUILD_DIR" -name "*.map" -delete || true
fi

echo "🔗 Capacitor 동기화 (iOS)"
if ! command -v npx >/dev/null 2>&1; then
	echo "❌ npx를 찾을 수 없습니다. Node.js/npm 설치 후 다시 시도하세요."
	exit 1
fi

if [ ! -d "$IOS_DIR" ]; then
	echo "📁 iOS 플랫폼 초기화 (npx cap add ios)"
	npx cap add ios
fi

echo "🔄 npx cap sync ios"
npx cap sync ios

echo "📱 CocoaPods 의존성 설치"
cd "$IOS_DIR/App"
if command -v pod >/dev/null 2>&1; then
	pod install
	echo "✅ CocoaPods 설치 완료"
else
	echo "⚠️  CocoaPods가 설치되어 있지 않습니다."
	echo "   설치: sudo gem install cocoapods"
	echo "   또는: brew install cocoapods"
fi

echo ""
echo "🎉 완료!"
echo ""
echo "📲 다음 단계:"
echo "   1. Xcode에서 프로젝트 열기:"
echo "      open $IOS_DIR/App/App.xcworkspace"
echo ""
echo "   2. Xcode에서:"
echo "      - Signing & Capabilities에서 Team 선택"
echo "      - 실제 iOS 기기 연결 (시뮬레이터는 푸시 알림 불가)"
echo "      - Run 버튼 클릭"
echo ""
echo "   3. 앱에서 /debug-fcm 페이지로 이동하여 FCM 토큰 확인"
echo ""
