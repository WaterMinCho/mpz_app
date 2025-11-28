import React from "react";
import { cn } from "@/lib/utils";

interface DotProgressBarProps {
  currentStep: number;
  totalSteps?: number;
  className?: string;
  size?: "sm" | "md" | "lg";
  labels?: string[];
}

const barStyles = {
  completed: "bg-brand border-brand",
  active: "bg-brand border-brand",
  inactive: "bg-lg",
  line: "border-bg",
  completedLine: "border-brand",
  text: "text-gr",
  activeText: "text-brand font-bold",
  completedText: "text",
};

const sizeStyles = {
  sm: {
    counter: "w-3 h-3",
    lineTop: 4.5,
    gap: "gap-2",
    text: "text-xs",
  },
  md: {
    counter: "w-3 h-3",
    lineTop: 4.5,
    gap: "gap-4",
    text: "text-xs",
  },
  lg: {
    counter: "w-3 h-3",
    lineTop: 4.5,
    gap: "gap-6",
    text: "text-xs",
  },
};

const defaultLabels = [
  "입양신청",
  "미팅",
  "계약서 작성",
  "입양 완료",
  "모니터링",
];

export function DotProgressBar({
  currentStep,
  totalSteps = 5,
  className,
  size = "sm",
  labels = defaultLabels,
}: DotProgressBarProps) {
  const sizeStyle = sizeStyles[size];

  return (
    <div className={cn("flex justify-between mb-5 w-full", className)}>
      {Array.from({ length: totalSteps }, (_, index) => {
        const stepNumber = index + 1;
        const isCompleted = stepNumber < currentStep;
        const isActive = stepNumber === currentStep;
        const label = labels[index] || defaultLabels[index];

        let stepClass = "";
        let counterClass = "";
        let textClass = "";

        if (isCompleted) {
          stepClass = "completed";
          counterClass = barStyles.completed;
          textClass = barStyles.completedText;
        } else if (isActive) {
          stepClass = "active";
          counterClass = barStyles.active;
          textClass = barStyles.activeText;
        } else {
          counterClass = barStyles.inactive;
          textClass = barStyles.text;
        }

        return (
          <div
            key={index}
            className={cn(
              "relative flex flex-col items-center flex-1",
              stepClass
            )}
          >
            {/* Before line */}
            {index > 0 && (
              <div
                className={cn(
                  "absolute content-[''] border-b-[3px] w-full",
                  index < currentStep
                    ? barStyles.completedLine
                    : barStyles.line,
                  "z-[2]"
                )}
                style={{ top: `${sizeStyle.lineTop}px`, left: "-50%" }}
              />
            )}

            {/* After line */}
            {index < totalSteps - 1 && (
              <div
                className={cn(
                  "absolute content-[''] border-b-[3px] w-full",
                  index < currentStep
                    ? barStyles.completedLine
                    : barStyles.line,
                  "z-[2]"
                )}
                style={{ top: `${sizeStyle.lineTop}px`, left: "50%" }}
              />
            )}

            {/* Step counter */}
            <div
              className={cn(
                "relative z-[5] flex justify-center items-center rounded-full mb-1.5",
                sizeStyle.counter,
                counterClass
              )}
            />

            {/* Step name */}
            <div className={cn("text-center text-xs text-gray-600", textClass)}>
              {label}
            </div>
          </div>
        );
      })}
    </div>
  );
}
