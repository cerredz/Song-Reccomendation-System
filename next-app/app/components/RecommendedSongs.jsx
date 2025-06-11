"use client";
import { AnimatePresence, motion } from "framer-motion";
import { useState } from "react";

export default function RecommendedSongs({ state }) {
  const [hoveredIndex, setHoveredIndex] = useState(null);

  // Array of gradient colors for the icons
  const iconColors = [
    "bg-gradient-to-br from-pink-500 to-pink-700",
    "bg-gradient-to-br from-purple-500 to-purple-700",
    "bg-gradient-to-br from-blue-500 to-blue-700",
    "bg-gradient-to-br from-pink-400 to-purple-500",
    "bg-gradient-to-br from-purple-400 to-blue-500",
    "bg-gradient-to-br from-blue-400 to-pink-500",
    "bg-gradient-to-br from-pink-500 to-purple-600",
    "bg-gradient-to-br from-purple-500 to-blue-600",
    "bg-gradient-to-br from-blue-500 to-pink-600",
    "bg-gradient-to-br from-pink-600 to-purple-700",
  ];

  // Function to get initials from song name
  const getInitials = (songName) => {
    return songName
      .split(" ")
      .map((word) => word[0])
      .join("")
      .toUpperCase()
      .slice(0, 2);
  };

  // Function to format similarity score as percentage
  const formatScore = (score) => {
    return `${(score * 100).toFixed(1)}%`;
  };

  // Function to format genre
  const formatGenre = (genre) => {
    return genre.split(",")[0].trim(); // Take first genre if multiple
  };

  const recommendations = state.recommendations?.data || [];

  return (
    <AnimatePresence>
      {state.finished && recommendations.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -50 }}
          transition={{ duration: 0.5 }}
          layout
          className="flex justify-center px-4 sm:px-8 relative z-10 py-8"
        >
          <div className="w-full max-w-7xl bg-black/20 backdrop-blur-sm rounded-2xl p-4 sm:p-8 border border-white/10">
            {/* Header */}
            <div className="text-center mb-8">
              <h1 className="font-primary text-3xl sm:text-4xl md:text-5xl font-bold text-white leading-tight mb-3">Your Music Recommendations</h1>
              <p className="text-white/50 text-sm tracking-wider">Found {recommendations.length} songs that match your taste</p>
            </div>

            {/* Song List - 2 Column Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
              {recommendations.map((recommendation, index) => {
                const { metadata, score } = recommendation;
                const iconColor = iconColors[index % iconColors.length];
                const isHovered = hoveredIndex === index;

                return (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -50 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.3, delay: index * 0.05 }}
                    layout
                    onHoverStart={() => setHoveredIndex(index)}
                    onHoverEnd={() => setHoveredIndex(null)}
                    className="bg-white/5 shadow-[inset_0_0_4px_rgba(255,255,255,.2),inset_0_0_12px_rgba(255,255,255,.1)] rounded-xl py-4 px-4 sm:px-6 cursor-pointer overflow-hidden"
                    whileHover={{
                      backgroundColor: "rgba(255, 255, 255, 0.1)",
                      borderColor: "rgba(255, 255, 255, 0.2)",
                      transition: { duration: 0.2 },
                    }}
                  >
                    <div className="flex items-center justify-between">
                      {/* Left side: Icon + Song Info */}
                      <div className="flex items-center space-x-3 flex-1 min-w-0">
                        {/* Colored Icon */}
                        <motion.div
                          className={`w-10 h-10 sm:w-12 sm:h-12 ${iconColor} rounded-full flex items-center justify-center text-white font-bold text-xs sm:text-sm shadow-lg flex-shrink-0`}
                          whileHover={{
                            scale: 1.1,
                            rotate: 5,
                            transition: { duration: 0.2 },
                          }}
                        >
                          {getInitials(metadata.song)}
                        </motion.div>

                        {/* Song Details */}
                        <div className="flex-1 min-w-0">
                          <motion.h3 className="text-white font-bold text-base sm:text-lg transition-colors duration-200 truncate">
                            {metadata.song}
                          </motion.h3>
                          <div className="flex items-center space-x-2 text-white/60 text-xs">
                            <span className="font-medium tracking-wider truncate">{metadata.artist}</span>
                            <span className="w-1 h-1 bg-white/40 rounded-full flex-shrink-0"></span>
                            <span className="tracking-wider truncate">{formatGenre(metadata.genre)}</span>
                            <span className="w-1 h-1 bg-white/40 rounded-full flex-shrink-0"></span>
                            <span className="flex-shrink-0">{metadata.length}</span>
                          </div>
                          <div className="text-white/40 text-xs mt-1 truncate">
                            {metadata.album} • {metadata.release_date}
                          </div>
                        </div>
                      </div>

                      {/* Right side: Match Score */}
                      <div className="flex-shrink-0 ml-2">
                        <div className="text-right">
                          <motion.div
                            className="text-white font-bold text-sm sm:text-lg"
                            whileHover={{
                              scale: 1.1,
                              color: "#f9a8d4",
                              transition: { duration: 0.2 },
                            }}
                          >
                            {formatScore(score)}
                          </motion.div>
                          <div className="text-white/40 text-xs tracking-wider">MATCH</div>
                        </div>
                      </div>
                    </div>

                    {/* Similar Songs Info (smooth expand/collapse) */}
                    <AnimatePresence>
                      {isHovered && (
                        <motion.div
                          initial={{
                            height: 0,
                            opacity: 0,
                            marginTop: 0,
                            paddingTop: 0,
                          }}
                          animate={{
                            height: "auto",
                            opacity: 1,
                            marginTop: 12,
                            paddingTop: 12,
                          }}
                          exit={{
                            height: 0,
                            opacity: 0,
                            marginTop: 0,
                            paddingTop: 0,
                          }}
                          transition={{
                            duration: 0.3,
                            ease: "easeInOut",
                          }}
                          layout
                          className="border-t border-white/10 tracking-wider overflow-hidden"
                        >
                          <motion.div
                            className="text-xs text-white/50"
                            initial={{ y: 10 }}
                            animate={{ y: 0 }}
                            exit={{ y: 10 }}
                            transition={{ duration: 0.2, delay: 0.1 }}
                          >
                            <span className="font-medium text-white/70 tracking-wider">Similar Songs:</span>
                            <div className="mt-1 line-clamp-3">
                              <span>{metadata.similar_song_1}</span>
                              {metadata.similar_song_2 && (
                                <>
                                  <span className="text-white/30">, </span>
                                  <span>{metadata.similar_song_2}</span>
                                </>
                              )}
                              {metadata.similar_song_3 && (
                                <>
                                  <span className="text-white/30">, </span>
                                  <span>{metadata.similar_song_3}</span>
                                </>
                              )}
                            </div>
                          </motion.div>
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </motion.div>
                );
              })}
            </div>

            {/* Footer */}
            <div className="mt-8 text-center">
              <motion.button
                whileHover={{ opacity: 0.7 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => window.location.reload()}
                className="mb-8 cursor-pointer flex items-center justify-center gap-2 mx-auto py-3 px-6 font-bold text-white tracking-wide bg-gradient-to-br from-pink-500 to-pink-800 rounded-2xl shadow-[inset_0_0_4px_rgba(255,255,255,.4),inset_0_0_12px_rgba(255,255,255,.2)]"
              >
                <span>Get New Recommendations</span>
              </motion.button>
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
