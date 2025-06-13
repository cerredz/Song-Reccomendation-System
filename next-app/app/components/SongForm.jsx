"use client";
import { motion, AnimatePresence } from "framer-motion";
import { useState, useEffect } from "react";

export default function SongForm({ state, setState }) {
  const defaultFormData = {
    // Text inputs
    artist: "",
    genre: "",
    emotion: "",

    // Sliders (0-100)
    popularity: 50,
    energy: 50,
    danceability: 50,
    positiveness: 50,
    speechiness: 50,
    liveness: 50,
    acousticness: 50,
    instrumentalness: 50,

    // Tempo slider (50-200)
    tempo: 120,

    // Good for checkboxes (true/false)
    good_for_party: false,
    good_for_work_study: false,
    good_for_exercise: false,
    good_for_running: false,
    good_for_driving: false,
    good_for_social_gatherings: false,
    good_for_morning_routine: false,
    good_for_meditation_stretching: false,
  };

  const [formData, setFormData] = useState(defaultFormData);

  // Load data from localStorage on component mount
  useEffect(() => {
    try {
      const savedData = localStorage.getItem("songFormData");
      if (savedData) {
        const parsedData = JSON.parse(savedData);
        // Merge with default values to ensure all fields exist
        setFormData((prev) => ({
          ...defaultFormData,
          ...parsedData,
        }));
      }
    } catch (error) {
      console.error("Error loading data from localStorage:", error);
      // If there's an error, stick with default values
    }
  }, []);

  // Save data to localStorage whenever formData changes
  useEffect(() => {
    try {
      localStorage.setItem("songFormData", JSON.stringify(formData));
    } catch (error) {
      console.error("Error saving data to localStorage:", error);
    }
  }, [formData]);

  const handleInputChange = (field, value) => {
    setFormData((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const baseUrl = process.env.NODE_ENV === "development" ? "http://localhost:5000" : "https://song-reccomendation-system.onrender.com";

    // Debug logging
    console.log("Form submitted with data:", formData);
    console.log("Making POST request to:", `${baseUrl}/recommend`);

    setState({ ...state, loading: true });
    try {
      const response = await fetch(`${baseUrl}/recommend`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ ...formData, n: 20 }),
      });

      if (response.ok) {
        const recommendations = await response.json();
        setState({ ...state, loading: false, finished: true, recommendations: recommendations });
      }
    } catch (error) {
      console.error("Error getting recommendations:", error);
    }
  };

  // Optional: Function to clear saved data
  const clearSavedData = () => {
    try {
      localStorage.removeItem("songFormData");
      setFormData(defaultFormData);
    } catch (error) {
      console.error("Error clearing localStorage:", error);
    }
  };

  return (
    <AnimatePresence>
      {state.started && !state.finished && (
        <motion.div
          initial={{ opacity: 0, y: 100, display: "none" }}
          animate={{ opacity: 1, y: 0, display: "block" }}
          exit={{ opacity: 0, y: -100, display: "none" }}
          layout
          transition={{ duration: 0.5, delay: 0.4 }}
          className="flex items-center justify-center px-8 relative z-10  py-8 mb-16"
        >
          <form onSubmit={handleSubmit} className="w-full max-w-4xl bg-black/20 backdrop-blur-sm rounded-2xl p-8 border border-white/10 mt-32 ">
            <div className="text-center mb-8">
              <h1 className="font-primary text-4xl md:text-5xl font-bold text-white leading-tight mb-3">Find My Music</h1>
              <p className="text-white/50 text-sm tracking-wider">Tell us about your music preferences</p>
              {/* Optional: Clear button */}
              <button type="button" onClick={clearSavedData} className="mt-2 text-xs text-white/40 hover:text-white/60 underline">
                Clear saved preferences
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              {/* Basic Preferences */}
              <div className="space-y-6">
                <h3 className="text-xl font-semibold text-white mb-4 tracking-wider">Basic Preferences</h3>

                <div>
                  <label className="block text-white mb-2 text-white/60 text-sm tracking-wider font-bold">Favorite Artist</label>
                  <input
                    type="text"
                    value={formData.artist}
                    onChange={(e) => handleInputChange("artist", e.target.value)}
                    className="w-full px-4 py-3 shadow-[inset_0_0_4px_rgba(255,255,255,.4),inset_0_0_12px_rgba(255,255,255,.2)] bg-white/5 border-white/20 rounded-2xl font-bold tracking-wider text-white placeholder-white/50 focus:outline-none focus:border-white/40"
                    placeholder="e.g., Drake, Taylor Swift"
                  />
                </div>

                <div>
                  <label className="block text-white mb-2 text-white/60 text-sm tracking-wider font-bold">Genre</label>
                  <input
                    type="text"
                    value={formData.genre}
                    onChange={(e) => handleInputChange("genre", e.target.value)}
                    className="w-full px-4 py-3 shadow-[inset_0_0_4px_rgba(255,255,255,.4),inset_0_0_12px_rgba(255,255,255,.2)] bg-white/5 border-white/20 rounded-2xl font-bold tracking-wider text-white placeholder-white/50 focus:outline-none focus:border-white/40"
                    placeholder="e.g., pop, hip hop, rock"
                  />
                </div>

                <div>
                  <label className="block text-white mb-2 text-white/60 text-sm tracking-wider font-bold">Emotion/Mood</label>
                  <input
                    type="text"
                    value={formData.emotion}
                    onChange={(e) => handleInputChange("emotion", e.target.value)}
                    className="w-full px-4 py-3 shadow-[inset_0_0_4px_rgba(255,255,255,.4),inset_0_0_12px_rgba(255,255,255,.2)] bg-white/5 border-white/20 rounded-2xl font-bold tracking-wider text-white placeholder-white/50 focus:outline-none focus:border-white/40"
                    placeholder="e.g., happy, sad, energetic"
                  />
                </div>
              </div>

              {/* Music Characteristics */}
              <div className="space-y-6">
                <h3 className="text-xl font-semibold text-white mb-4 tracking-wider">Music Characteristics</h3>

                {/* Tempo Slider (50-200) */}
                <div>
                  <label className="block text-white mb-2 text-white/60 text-sm tracking-wider font-bold">Tempo: {formData.tempo} BPM</label>
                  <input
                    type="range"
                    min="50"
                    max="200"
                    value={formData.tempo}
                    onChange={(e) => handleInputChange("tempo", parseInt(e.target.value))}
                    className="w-full h-2 bg-white/10 rounded-lg appearance-none cursor-pointer slider"
                  />
                </div>

                {/* Regular Sliders (0-100) */}
                {[
                  { key: "popularity", label: "Popularity" },
                  { key: "energy", label: "Energy" },
                  { key: "danceability", label: "Danceability" },
                  { key: "positiveness", label: "Positiveness" },
                  { key: "speechiness", label: "Speechiness" },
                  { key: "liveness", label: "Liveness" },
                  { key: "acousticness", label: "Acousticness" },
                  { key: "instrumentalness", label: "Instrumentalness" },
                ].map(({ key, label }) => (
                  <div key={key}>
                    <label className="block text-white mb-2 text-white/60 text-sm tracking-wider font-bold">
                      {label}: {formData[key]}
                    </label>
                    <input
                      type="range"
                      min="0"
                      max="100"
                      value={formData[key]}
                      onChange={(e) => handleInputChange(key, parseInt(e.target.value))}
                      className="w-full h-2 bg-white/10 rounded-lg appearance-none cursor-pointer"
                    />
                  </div>
                ))}
              </div>
            </div>

            {/* Good For Custom Toggles */}
            <div className="mt-8">
              <h3 className="text-xl font-semibold text-white mb-4 tracking-wider">Good For</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                {[
                  { key: "good_for_party", label: "Party" },
                  { key: "good_for_work_study", label: "Work/Study" },
                  { key: "good_for_exercise", label: "Exercise" },
                  { key: "good_for_running", label: "Running" },
                  { key: "good_for_driving", label: "Driving" },
                  { key: "good_for_social_gatherings", label: "Social Gatherings" },
                  { key: "good_for_morning_routine", label: "Morning Routine" },
                  { key: "good_for_meditation_stretching", label: "Meditation" },
                ].map(({ key, label }) => (
                  <div
                    key={key}
                    onClick={() => handleInputChange(key, !formData[key])}
                    className={`
                      relative cursor-pointer p-3 rounded-xl transition-all duration-300 transform 
                      ${
                        formData[key]
                          ? "shadow-[inset_0_0_12px_rgba(236,72,153,0.5)] bg-gradient-to-r from-pink-500/20 to-purple-500/20 "
                          : "shadow-[inset_0_0_4px_rgba(255,255,255,.4),inset_0_0_12px_rgba(255,255,255,.2)]"
                      }
                    `}
                  >
                    {/* Custom checkbox indicator */}
                    <div className="flex items-center space-x-2">
                      <div
                        className={`
                        w-5 h-5 rounded-full  transition-all duration-300 flex items-center justify-center
                        ${
                          formData[key]
                            ? "bg-gradient-to-r from-pink-500 to-purple-500  shadow-lg shadow-pink-500/50"
                            : "border-white/40 bg-transparent bg-gradient-to-r from-white/20 to-white/10"
                        }
                      `}
                      ></div>
                      <span
                        className={`
                        text-sm font-bold tracking-wider transition-colors duration-300
                        ${formData[key] ? "text-white" : "text-white/60"}
                      `}
                      >
                        {label}
                      </span>
                    </div>

                    {/* Glow effect when selected */}
                    {formData[key] && (
                      <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="absolute inset-0 rounded-xl bg-gradient-to-r from-pink-500/10 to-purple-500/10 pointer-events-none"
                      />
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* Submit Button */}
            <div className="mt-8 text-center">
              <motion.button
                type="submit"
                disabled={state.loading}
                whileHover={!state.loading ? { opacity: 0.7 } : {}}
                whileTap={!state.loading ? { scale: 0.98 } : {}}
                className={`cursor-pointer flex items-center justify-center gap-2 mx-auto py-3 px-6 font-bold text-white tracking-wide bg-gradient-to-br from-pink-500 to-pink-800 rounded-2xl shadow-[inset_0_0_4px_rgba(255,255,255,.4),inset_0_0_12px_rgba(255,255,255,.2)] ${
                  state.loading ? "opacity-70 cursor-not-allowed" : ""
                }`}
              >
                <AnimatePresence mode="wait">
                  {state.loading ? (
                    <motion.div
                      key="loading"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      exit={{ opacity: 0 }}
                      className="flex items-center gap-2"
                    >
                      <motion.div
                        animate={{ rotate: 360 }}
                        transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                        className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full"
                      />
                      <span>Getting Recommendations...</span>
                    </motion.div>
                  ) : (
                    <motion.span key="default" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
                      Get My Recommendations
                    </motion.span>
                  )}
                </AnimatePresence>
              </motion.button>
            </div>
          </form>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
