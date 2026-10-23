"use client";
import type { RollOption } from "@/lib/rolls";
import type { ReactNode } from "react";
export function RollActionButton({
  option,
  disabled,
  onRoll,
  children,
}: {
  option: RollOption;
  disabled: boolean;
  onRoll: () => void;
  children?: ReactNode;
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
      {children ?? name}
    </button>
  );
}
