"use client";
import Link from "next/link";
import { motion } from "framer-motion";

export default function Navbar({ state, setState }) {
  const links = [
    {
      name: "LinkedIn",
      redirect: "https://www.linkedin.com/in/michael-cerreto-b3348524b/",
    },
    {
      name: "Docs",
      redirect: "https://github.com/cerredz/Song-Reccomendation-System/blob/main/README.md",
    },
  ];
  return (
    <nav className="fixed top-0 left-0 w-screen flex items-center justify-between px-12 py-8 backdrop-blur-md z-50 ">
      <div className="flex items-end space-x-8 justify-end ">
        <div className="hidden md:flex space-x-7 text-sm items-end justify-end h-full">
          <p className="tracking-wider font-bold text-xl translate-y-[2px]">Harmony AI</p>
          {/* Links */}
          {links &&
            links.map((link) => (
              <Link href={link.redirect} key={link.name} target="_blank">
                <p className="text-white/50 tracking-wider hover:text-white/80 transition duration-300 font-bold text-sm">{link.name}</p>
              </Link>
            ))}
        </div>
      </div>
      {/* Github Button */}
      <Link href="https://github.com/cerredz/Song-Reccomendation-System" target="_blank">
        <motion.button
          whileHover={{ opacity: 0.7 }}
          whileTap={{ scale: 0.98 }}
          className="cursor-pointer flex items-center justify-center gap-2 mx-auto py-2 px-4 text-sm font-bold text-white tracking-wide bg-gradient-to-br from-pink-500 to-pink-800 rounded-2xl shadow-[inset_0_0_4px_rgba(255,255,255,.4),inset_0_0_12px_rgba(255,255,255,.2)]"
        >
          Star on Github
        </motion.button>
      </Link>
    </nav>
  );
}
