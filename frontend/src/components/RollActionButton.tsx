"use client";
import type { RollOption } from "@/lib/rolls";
export function RollActionButton({
  option,
  disabled,
  onRoll,
}: {
  option: RollOption;
  disabled: boolean;
  onRoll: () => void;
}) {
  const name = option.consumes
    ? `Use ${option.label.replace(/ damage$/, "")} and roll damage`
    : `Roll ${option.label}`;
  return (
    <button
      type="button"
      disabled={disabled || !option.available}
      onClick={onRoll}
      aria-label={name}
    >
      {name}
    </button>
  );
}
