"use client";
import { useState } from "react";
import Navbar from "./components/Navbar";
import MainText from "./components/MainText";
import Image from "next/image";
import SongForm from "./components/SongForm";
import { motion } from "framer-motion";
import RecommendedSongs from "./components/RecommendedSongs";

export default function Home() {
  const [state, setState] = useState(false);

  return (
    <motion.div layout className="relative min-h-screen overflow-y-auto overflow-x-hidden">
      <Navbar />
      {/* BACKGROUND IMAGE */}
      <div className="fixed top-0 left-0 w-screen h-screen">
        <Image src="/images/center-glow-pink.png" alt="Background" fill className="object-cover" quality={100} priority />
      </div>
      {/* Conditional rendering based on state */}
      {!state.finished ? (
        // Show main text and form when not finished
        <div className="flex flex-col items-center justify-center min-h-screen">
          <MainText state={state} setState={setState} />
          <SongForm state={state} setState={setState} />
        </div>
      ) : (
        // Show recommendations when finished - starts from top
        <div className="pt-20">
          <RecommendedSongs state={state} />
        </div>
      )}
    </motion.div>
  );
}
