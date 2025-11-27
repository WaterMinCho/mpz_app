import { cn } from "@/lib/utils";

interface IconButtonProps {
  icon: React.ComponentType<{
    size?: number | string;
    className?: string;
  }>;
  size?: "iconM" | "iconS" | "iconL";
  label?: string;
  className?: string;
  onClick?: (e: React.MouseEvent<HTMLButtonElement>) => void;
  disabled?: boolean;
}

const sizeMap = {
  iconM: 20,
  iconS: 16,
  iconL: 24,
};

const sizeClassMap = {
  iconM: "h-5 w-5", // 20px
  iconS: "h-4 w-4", // 16px
  iconL: "h-7 w-7", // 28px
};

export function IconButton({
  icon: Icon,
  size = "iconM",
  label,
  className,
  onClick,
  disabled = false,
}: IconButtonProps) {
  return (
    <button
      className={cn(
        "inline-flex items-center justify-center rounded-full focus:outline-none transition-all cursor-pointer text-gr p-0",
        sizeClassMap[size],
        disabled && "opacity-50 cursor-not-allowed",
        className
      )}
      aria-label={label}
      type="button"
      onClick={onClick}
      disabled={disabled}
    >
      <Icon size={sizeMap[size]} className="" />
    </button>
  );
}
