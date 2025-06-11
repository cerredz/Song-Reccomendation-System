"use client";
import { motion, AnimatePresence } from "framer-motion";
import Link from "next/link";
import Image from "next/image";

export default function MainText({ state, setState }) {
  return (
    <AnimatePresence>
      {!state.started && (
        <main className="flex items-center justify-center px-8 relative z-10 h-screen">
          <motion.div
            animate={{ translateY: state.started ? 0 : 100 }}
            layout
            transition={{ duration: 0.5 }}
            exit={{ opacity: 0, y: -100 }}
            className="text-center max-w-2xl"
          >
            {/* CHECK OUT VIDBYTE LABEL */}
            <Link href="https://www.vidbyte.pro" target="_blank">
              <div className="hover:scale-105 transition-all duration-300 px-6 py-4 rounded-3xl bg-gradient-to-br from-pink-500/20 to-pink-700/50 w-fit mx-auto mb-10 z-10 flex flex-row items-center justify-center gap-4 shadow-[inset_0_0_4px_rgba(236,72,153,.6),inset_0_0_12px_rgba(236,72,153,.4)]">
                <h1 className="z-10 text-white tracking-wider font-bold whitespace-nowrap ">Check out Vidbyte</h1>
                <Image src="/images/vidbyte.png" alt="Vidbyte Logo" width={80} height={60} priority quality={100} className="rounded-xl" />
              </div>
            </Link>

            <h1 className="font-primary text-5xl md:text-6xl lg:text-7xl font-bold text-white leading-tight mb-3">
              Discover music,
              <br />
              love every beat.
            </h1>

            <p className="tracking-wider text-sm text-white/50 tracking-wide font-semibold max-w-lg mb-5">
              AI-powered song recommendations tailored to your favorite artists, genres, and exact preferences for the perfect soundtrack.
            </p>

            <motion.button
              whileHover={{ opacity: 0.7 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => setState({ ...state, started: !state.started })}
              className="cursor-pointer flex items-center justify-center gap-2 mx-auto py-3 px-6 font-bold text-white tracking-wide bg-gradient-to-br from-pink-500 to-pink-800 rounded-2xl shadow-[inset_0_0_4px_rgba(255,255,255,.4),inset_0_0_12px_rgba(255,255,255,.2)]"
            >
              {state.started ? <span>Reset</span> : <span>Find My Music</span>}
            </motion.button>
          </motion.div>
        </main>
      )}
    </AnimatePresence>
  );
}
