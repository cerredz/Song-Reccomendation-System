"use client";
import { useState } from "react";
import Navbar from "./components/Navbar";
import MainText from "./components/MainText";
import Image from "next/image";

export default function Home() {
  const [state, setState] = useState(false);

  return (
    <div className="min-h-screen relative overflow-hidden">
      <Navbar />

      {/* BACKGROUND IMAGE */}
      <Image src="/images/center-glow-pink.png" alt="Background" fill className="object-cover" quality={100} priority />

      {/* Main Content */}
      <MainText state={state} setState={setState} />
    </div>
  );
}
