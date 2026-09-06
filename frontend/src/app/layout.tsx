import type { Metadata } from "next";
import { AppShell } from "@/components/app-shell";
import { NotificationProvider } from "@/hooks/use-notification";
import "./globals.css";

export const metadata: Metadata = {
  title: "Trading Assistant",
  description: "Define and manage trading information, strategies, actions, and related data.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" dir="auto">
      <body>
        <NotificationProvider>
          <AppShell>{children}</AppShell>
        </NotificationProvider>
      </body>
    </html>
  );
}
