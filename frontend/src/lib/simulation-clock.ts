/** Fixed simulation budget, independent of display refresh rate. Discard excessive wall time. */
export function simulationClock(timestep: number, maxCatchup: number) {
  let accumulator = 0;
  const maximum = Math.floor(maxCatchup / timestep);
  return (elapsedSeconds: number) => {
    const elapsed = Number.isFinite(elapsedSeconds)
      ? Math.max(0, elapsedSeconds)
      : 0;
    accumulator += Math.min(elapsed, maxCatchup);
    const count = Math.min(
      maximum,
      Math.floor((accumulator + 1e-12) / timestep),
    );
    accumulator = Math.max(0, accumulator - count * timestep);
    return count;
  };
}
