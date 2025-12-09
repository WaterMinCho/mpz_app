"use client";

import { useEffect, useState } from "react";
import { Container } from "@/components/common/Container";
import { Capacitor } from "@capacitor/core";

export default function DebugFCMPage() {
  const [fcmToken, setFcmToken] = useState<string>("");
  const [platform, setPlatform] = useState<string>("");
  const [logs, setLogs] = useState<string[]>([]);

  const addLog = (message: string) => {
    const timestamp = new Date().toLocaleTimeString();
    setLogs((prev) => [`[${timestamp}] ${message}`, ...prev]);
    console.log(`[FCM Debug] ${message}`);
  };

  useEffect(() => {
    // 플랫폼 확인
    const detectedPlatform = Capacitor.getPlatform();
    setPlatform(detectedPlatform);
    addLog(`플랫폼 감지: ${detectedPlatform}`);

    // localStorage에서 토큰 확인
    const savedToken = localStorage.getItem("fcm_token_debug");
    if (savedToken) {
      setFcmToken(savedToken);
      addLog(`localStorage에서 토큰 발견: ${savedToken.substring(0, 20)}...`);
    } else {
      addLog("저장된 토큰이 없습니다.");
    }

    // FCM 토큰 이벤트 리스너
    const handleFcmToken = (event: Event) => {
      const token = (event as CustomEvent).detail;
      addLog(`FCM 토큰 수신: ${token.substring(0, 20)}...`);
      setFcmToken(token);
      localStorage.setItem("fcm_token_debug", token);
    };

    window.addEventListener("fcmToken", handleFcmToken);
    addLog("FCM 토큰 이벤트 리스너 등록 완료");

    // Notification API 권한 확인
    if ("Notification" in window) {
      addLog(`알림 권한 상태: ${Notification.permission}`);
    } else {
      addLog("이 브라우저는 알림 API를 지원하지 않습니다.");
    }

    return () => {
      window.removeEventListener("fcmToken", handleFcmToken);
    };
  }, []);

  const requestNotificationPermission = async () => {
    if (!("Notification" in window)) {
      addLog("이 브라우저는 알림을 지원하지 않습니다.");
      return;
    }

    try {
      const permission = await Notification.requestPermission();
      addLog(`알림 권한 요청 결과: ${permission}`);
    } catch (error) {
      addLog(`알림 권한 요청 실패: ${error}`);
    }
  };

  const copyToken = () => {
    if (fcmToken) {
      navigator.clipboard.writeText(fcmToken);
      addLog("토큰이 클립보드에 복사되었습니다.");
    }
  };

  const sendTestNotification = () => {
    if ("Notification" in window && Notification.permission === "granted") {
      new Notification("테스트 알림", {
        body: "이것은 테스트 알림입니다.",
        icon: "/img/op-image.png",
      });
      addLog("브라우저 알림 전송 완료");
    } else {
      addLog("알림 권한이 없습니다. 먼저 권한을 요청해주세요.");
    }
  };

  return (
    <Container>
      <div className="p-4 space-y-6">
        <div className="bg-white rounded-lg shadow p-4">
          <h1 className="text-xl font-bold mb-4">FCM 디버깅 페이지</h1>

          <div className="space-y-4">
            {/* 플랫폼 정보 */}
            <div>
              <h3 className="font-semibold text-sm text-gray-700 mb-1">
                플랫폼
              </h3>
              <p className="text-sm bg-gray-100 p-2 rounded">
                {platform || "감지 중..."}
              </p>
            </div>

            {/* FCM 토큰 */}
            <div>
              <h3 className="font-semibold text-sm text-gray-700 mb-1">
                FCM 토큰
              </h3>
              {fcmToken ? (
                <div className="space-y-2">
                  <textarea
                    readOnly
                    value={fcmToken}
                    className="w-full text-xs bg-gray-100 p-2 rounded h-24 font-mono"
                  />
                  <button
                    onClick={copyToken}
                    className="w-full bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600"
                  >
                    토큰 복사
                  </button>
                </div>
              ) : (
                <p className="text-sm bg-yellow-100 p-2 rounded text-yellow-800">
                  토큰을 받는 중... 앱을 재시작해보세요.
                </p>
              )}
            </div>

            {/* 버튼들 */}
            <div className="space-y-2">
              <button
                onClick={requestNotificationPermission}
                className="w-full bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600"
              >
                알림 권한 요청
              </button>
              <button
                onClick={sendTestNotification}
                className="w-full bg-purple-500 text-white py-2 px-4 rounded hover:bg-purple-600"
              >
                테스트 알림 보내기
              </button>
            </div>

            {/* 로그 */}
            <div>
              <h3 className="font-semibold text-sm text-gray-700 mb-1">
                디버그 로그
              </h3>
              <div className="bg-black text-green-400 p-3 rounded h-64 overflow-y-auto font-mono text-xs">
                {logs.length > 0 ? (
                  logs.map((log, index) => (
                    <div key={index} className="mb-1">
                      {log}
                    </div>
                  ))
                ) : (
                  <div className="text-gray-500">로그가 없습니다.</div>
                )}
              </div>
            </div>

            {/* 사용 안내 */}
            <div className="bg-blue-50 p-3 rounded">
              <h3 className="font-semibold text-sm text-blue-900 mb-2">
                사용 방법
              </h3>
              <ol className="text-xs text-blue-800 space-y-1 list-decimal list-inside">
                <li>앱을 실행하고 이 페이지에 접속합니다.</li>
                <li>FCM 토큰이 자동으로 표시됩니다.</li>
                <li>&ldquo;토큰 복사&rdquo; 버튼으로 토큰을 복사합니다.</li>
                <li>
                  Firebase Console에서 &ldquo;테스트 메시지 전송&rdquo;에 토큰을
                  붙여넣습니다.
                </li>
                <li>알림이 수신되는지 확인합니다.</li>
              </ol>
            </div>

            {/* Firebase Console 링크 */}
            <a
              href="https://console.firebase.google.com/"
              target="_blank"
              rel="noopener noreferrer"
              className="block w-full bg-orange-500 text-white text-center py-2 px-4 rounded hover:bg-orange-600"
            >
              Firebase Console 열기
            </a>
          </div>
        </div>
      </div>
    </Container>
  );
}
