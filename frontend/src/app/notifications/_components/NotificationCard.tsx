import { Bell, ChatCircle, PawPrint, HeartStraight, Eye } from "@phosphor-icons/react";
import { cn } from "@/lib/utils";

interface NotificationCardProps {
  variant?: "primary" | "pressed";
  message: string;
  date: string;
  type?: string;
  isRead?: boolean;
  onClick?: () => void;
}

const getTimeAgo = (dateString: string): string => {
  const createdAt = new Date(dateString);
  const now = new Date();
  const diffMs = now.getTime() - createdAt.getTime();
  const diffMin = Math.floor(diffMs / (1000 * 60));

  if (diffMin < 1) return "방금 전";
  if (diffMin < 60) return `${diffMin}분 전`;

  const diffHours = Math.floor(diffMin / 60);
  if (diffHours < 24) return `${diffHours}시간 전`;

  const diffDays = Math.floor(diffHours / 24);
  if (diffDays < 30) return `${diffDays}일 전`;

  return createdAt.toLocaleDateString("ko-KR", { month: "long", day: "numeric" });
};

const getTypeInfo = (type: string) => {
  if (type?.includes("monitoring")) {
    return { label: "모니터링", icon: Eye, color: "text-red" };
  }
  if (type?.includes("adoption")) {
    return { label: "입양", icon: PawPrint, color: "text-brand" };
  }
  if (type?.includes("comment") || type?.includes("reply") || type?.includes("community")) {
    return { label: "커뮤니티", icon: ChatCircle, color: "text-yellow" };
  }
  if (type?.includes("like")) {
    return { label: "좋아요", icon: HeartStraight, color: "text-red" };
  }
  return { label: "알림", icon: Bell, color: "text-brand" };
};

function NotificationCard({
  variant = "primary",
  message,
  date,
  type,
  isRead = true,
  onClick,
}: NotificationCardProps) {
  const isPressed = variant === "pressed";
  const { label, icon: Icon, color } = getTypeInfo(type || "");

  return (
    <div
      className={cn(
        "flex items-start w-full border-b border-bg cursor-pointer active:bg-bg transition-colors px-4 py-3",
        isPressed && "shadow-md",
        !isRead && "bg-brand/[0.04]"
      )}
      onClick={onClick}
    >
      {/* 아이콘 */}
      <div className={cn("flex-shrink-0 mt-0.5 mr-3", color)}>
        <Icon size={20} weight="fill" />
      </div>

      {/* 내용 */}
      <div className="flex-1 min-w-0">
        <p className="text-[11px] font-medium text-gr mb-0.5">{label}</p>
        <p className="text-[14px] text-bk leading-[20px] line-clamp-2">{message}</p>
        <p className="text-[11px] text-gr mt-1">{getTimeAgo(date)}</p>
      </div>

      {/* 읽지 않은 표시 */}
      {!isRead && (
        <div className="flex-shrink-0 ml-2 mt-2">
          <div className="w-2 h-2 rounded-full bg-brand" />
        </div>
      )}
    </div>
  );
}

export { NotificationCard };
