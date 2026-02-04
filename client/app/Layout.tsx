/**
 * REALM FORGE: TITAN LAYOUT v60.5 (PRODUCTION HARDENED)
 * STYLE: CAFFEINE-NEON / SOVEREIGN RECONSTRUCTION
 * ARCHITECT: LEAD SWARM ENGINEER (MASTERMIND v31.4)
 * PATH: F:/agentic_workforce/client/app/layout.tsx
 */

import "./globals.css";
import type { Metadata, Viewport } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";

// Correct variable names to match globals.css
const inter = Inter({ subsets: ["latin"], variable: "--font-sans" });
const jetbrains = JetBrains_Mono({ subsets: ["latin"], variable: "--font-mono" });

export const metadata: Metadata = {
  title: "REALM FORGE | SOVEREIGN COMMAND v60.5",
  description:
    "Industrial Agentic Software Engineering Platform — 13,472 Node Neural Lattice",
  icons: { icon: "/favicon.ico" },
};

export const viewport: Viewport = {
  themeColor: "#050505",
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html
      lang="en"
      className={`${inter.variable} ${jetbrains.variable} dark`}
      suppressHydrationWarning
    >
      <body className="bg-[#050505] text-[#f0f0f0] antialiased selection:bg-[#00f2ff] selection:text-black font-sans overflow-hidden h-screen w-screen">

        {/* INFINITE NEON CANVAS BACKGROUND */}
        <div className="fixed inset-0 z-[-1] pointer-events-none select-none overflow-hidden">

          {/* Base Layer */}
          <div className="absolute inset-0 bg-[#050505]" />

          {/* Ambient Mesh */}
          <div className="absolute inset-0 bg-mesh opacity-10 blur-[100px]" />

          {/* Dot Grid */}
          <div className="absolute inset-0 bg-dot-grid opacity-[0.03]" />

          {/* CRT Scanlines */}
          <div className="absolute inset-0 pointer-events-none bg-scanlines opacity-[0.02]" />

          {/* Central Vignette */}
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_transparent_20%,_#050505_100%)]" />

          {/* Ambient Glows */}
          <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-[#00f2ff] opacity-[0.05] blur-[120px] rounded-full" />
          <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-[#ff80bf] opacity-[0.05] blur-[120px] rounded-full" />
        </div>

        {/* TITAN HUD CHASSIS */}
        <div className="relative flex h-full w-full flex-col overflow-hidden">

          {/* Top Rail Glow */}
          <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-[#00f2ff]/30 to-transparent z-[9999]" />

          {children}
        </div>

      </body>
    </html>
  );
}