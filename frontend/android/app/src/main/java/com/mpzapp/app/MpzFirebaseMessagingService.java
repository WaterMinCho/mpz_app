package com.mpzapp.app;

import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Intent;
import android.os.Build;
import android.util.Log;
import androidx.annotation.NonNull;
import androidx.core.app.NotificationCompat;
import com.google.firebase.messaging.FirebaseMessagingService;
import com.google.firebase.messaging.RemoteMessage;
import java.util.Map;

/**
 * Firebase Cloud Messaging 서비스
 * 푸시 알림을 받고 FCM 토큰을 관리합니다.
 */
public class MpzFirebaseMessagingService extends FirebaseMessagingService {
    
    private static final String TAG = "MpzFCMService";
    private static final String CHANNEL_ID = "mpz_default_channel";
    private static final String CHANNEL_NAME = "MPZ 알림";
    private static final String CHANNEL_DESCRIPTION = "마펫쯔 앱의 기본 알림 채널입니다.";

    @Override
    public void onCreate() {
        super.onCreate();
        createNotificationChannel();
    }

    /**
     * FCM 토큰이 생성되거나 갱신될 때 호출됩니다.
     * 이 토큰을 백엔드 서버로 전송해야 합니다.
     */
    @Override
    public void onNewToken(@NonNull String token) {
        super.onNewToken(token);
        Log.d(TAG, "\n========================================");
        Log.d(TAG, "🔥 FCM 토큰 수신!");
        Log.d(TAG, "========================================");
        Log.d(TAG, token);
        Log.d(TAG, "========================================");
        Log.d(TAG, "👆 이 토큰을 복사해서 Firebase Console에 붙여넣으세요");
        Log.d(TAG, "========================================\n");
        
        // TODO: 백엔드 서버로 토큰 전송
        // 예: sendTokenToServer(token);
        
        // Capacitor 플러그인을 통해 JavaScript로 토큰 전달
        sendTokenToCapacitor(token);
    }

    /**
     * 푸시 알림을 받았을 때 호출됩니다.
     */
    @Override
    public void onMessageReceived(@NonNull RemoteMessage remoteMessage) {
        super.onMessageReceived(remoteMessage);
        
        Log.d(TAG, "푸시 알림 수신");
        Log.d(TAG, "From: " + remoteMessage.getFrom());
        
        createNotificationChannel();

        // 알림 데이터 확인
        if (remoteMessage.getNotification() != null) {
            String title = remoteMessage.getNotification().getTitle();
            String body = remoteMessage.getNotification().getBody();
            Log.d(TAG, "알림 제목: " + title);
            Log.d(TAG, "알림 내용: " + body);
        }
        
        // 커스텀 데이터 확인
        Map<String, String> data = remoteMessage.getData();
        if (data.size() > 0) {
            Log.d(TAG, "커스텀 데이터: " + data);
        }
        
        // 알림 표시
        showNotification(remoteMessage);
        sendMessageToCapacitor(remoteMessage);
    }

    /**
     * 알림 채널 생성 (Android 8.0 이상 필수)
     */
    private void createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            NotificationChannel channel = new NotificationChannel(
                CHANNEL_ID,
                CHANNEL_NAME,
                NotificationManager.IMPORTANCE_HIGH
            );
            channel.setDescription(CHANNEL_DESCRIPTION);
            channel.enableLights(true);
            channel.enableVibration(true);
            
            NotificationManager notificationManager = getSystemService(NotificationManager.class);
            if (notificationManager != null) {
                notificationManager.createNotificationChannel(channel);
                Log.d(TAG, "알림 채널 생성 완료: " + CHANNEL_ID);
            }
        }
    }

    /**
     * 알림을 생성해 표시합니다. data-only 메시지도 표시되도록 처리.
     */
    private void showNotification(RemoteMessage remoteMessage) {
        NotificationManager notificationManager = (NotificationManager) getSystemService(NOTIFICATION_SERVICE);
        if (notificationManager == null) {
            Log.w(TAG, "NotificationManager null");
            return;
        }

        String title = null;
        String body = null;

        if (remoteMessage.getNotification() != null) {
            title = remoteMessage.getNotification().getTitle();
            body = remoteMessage.getNotification().getBody();
        }

        Map<String, String> data = remoteMessage.getData();
        if (data != null) {
            if (title == null) title = data.get("title");
            if (body == null) body = data.get("body");
        }

        if (title == null) title = "MPZ";
        if (body == null) body = "새 알림이 도착했습니다.";

        Intent intent = new Intent(this, MainActivity.class);
        intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP | Intent.FLAG_ACTIVITY_SINGLE_TOP);
        PendingIntent pendingIntent = PendingIntent.getActivity(
            this,
            0,
            intent,
            PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE
        );

        NotificationCompat.Builder notificationBuilder =
            new NotificationCompat.Builder(this, CHANNEL_ID)
                .setSmallIcon(R.mipmap.ic_launcher)
                .setContentTitle(title)
                .setContentText(body)
                .setAutoCancel(true)
                .setPriority(NotificationCompat.PRIORITY_HIGH)
                .setContentIntent(pendingIntent);

        // 메시지마다 다른 ID로 여러 개 표시
        int notificationId = (int) System.currentTimeMillis();
        notificationManager.notify(notificationId, notificationBuilder.build());
    }

    /**
     * FCM 토큰을 Capacitor로 전달
     * JavaScript에서 이 토큰을 받아 백엔드로 전송할 수 있습니다.
     */
    private void sendTokenToCapacitor(String token) {
        // Capacitor 플러그인을 통해 JavaScript로 토큰 전달
        // 이 부분은 Capacitor Push Notifications 플러그인을 사용하거나
        // 커스텀 플러그인을 만들어서 구현할 수 있습니다.
        Log.d(TAG, "토큰을 Capacitor로 전달: " + token);
        
        // TODO: Capacitor 플러그인을 통해 JavaScript로 이벤트 전송
        // 예: Bridge.getInstance().triggerJSEvent("fcmTokenReceived", "{token: '" + token + "'}");
    }

    /**
     * 푸시 알림 메시지를 Capacitor로 전달
     */
    private void sendMessageToCapacitor(RemoteMessage remoteMessage) {
        Log.d(TAG, "푸시 알림을 Capacitor로 전달");
        
        // TODO: Capacitor 플러그인을 통해 JavaScript로 이벤트 전송
        // 예: Bridge.getInstance().triggerJSEvent("pushNotificationReceived", messageData);
    }
}
