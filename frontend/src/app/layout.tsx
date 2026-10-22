import type { Metadata } from "next";
import { SessionProvider } from "@/components/Session";
import { Header } from "@/components/Header";
import "./globals.css";
export const metadata: Metadata = {
  title: {
    default: "Dark Imperium | Personnel Archive",
    template: "%s | Dark Imperium",
  },
  description: "A private tabletop character archive for Dark Imperium.",
};
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <SessionProvider>
          <a href="#main" className="skip-link">
            Skip to content
          </a>
          <Header />
          <main id="main">{children}</main>
          <footer>
            <span>
              Dark Imperium <span aria-hidden="true">/</span> Private campaign
              archive
            </span>
            <span>Foundation edition · 0.1</span>
          </footer>
        </SessionProvider>
      </body>
    </html>
  );
}
