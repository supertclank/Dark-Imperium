import { AuthGate } from "@/components/Session";
export default function ArchiveLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <AuthGate>{children}</AuthGate>;
}
