"use client";

import { MiniButton } from "@/components/ui/MiniButton";

interface MultiSelectFilterProps {
  title: string;
  options: (string | { label: string; value: string })[];
  selectedValues: string[];
  onSelectionChange: (values: string[]) => void;
  layout?: "flex" | "grid";
  gridCols?: number;
  className?: string;
}

export default function MultiSelectFilter({
  title,
  options,
  selectedValues,
  onSelectionChange,
  layout = "flex",
  gridCols = 4,
  className = "",
}: MultiSelectFilterProps) {
  const handleMultiSelect = (value: string) => {
    if (selectedValues.includes(value)) {
      onSelectionChange(selectedValues.filter((item) => item !== value));
    } else {
      onSelectionChange([...selectedValues, value]);
    }
  };

  // 타입 가드 함수들
  const getOptionValue = (
    option: string | { label: string; value: string }
  ): string => {
    return typeof option === "object" ? option.value : option;
  };

  const getOptionLabel = (
    option: string | { label: string; value: string }
  ): string => {
    return typeof option === "object" ? option.label : option;
  };

  const getGridClassName = (cols: number) => {
    switch (cols) {
      case 2:
        return "grid grid-cols-2 gap-1";
      case 3:
        return "grid grid-cols-3 gap-1";
      case 4:
        return "grid grid-cols-3 gap-1";
      case 5:
        return "grid grid-cols-5 gap-1";
      case 6:
        return "grid grid-cols-6 gap-1";
      default:
        return "grid grid-cols-4 gap-1";
    }
  };

  const containerClassName =
    layout === "grid" ? getGridClassName(gridCols) : "flex flex-wrap gap-1";

  return (
    <div className="flex flex-col gap-1">
      <h5 className="text-dg">
        {title}{" "}
        {selectedValues.length > 0 && (
          <span className="text-brand">{selectedValues.length}</span>
        )}
      </h5>
      <div className={containerClassName}>
        {options.map((option) => (
          <MiniButton
            key={getOptionValue(option)}
            text={getOptionLabel(option)}
            variant={
              selectedValues.includes(getOptionValue(option))
                ? "filterOn"
                : "filterOff"
            }
            onClick={() => handleMultiSelect(getOptionValue(option))}
            className={className}
          />
        ))}
      </div>
    </div>
  );
}
