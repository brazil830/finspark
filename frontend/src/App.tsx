import React from "react";
import { HashRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";

// Page Imports
import Landing from "./pages/Landing";
import About from "./pages/About";
import Architecture from "./pages/Architecture";
import Dashboard from "./pages/Dashboard";
import Simulation from "./pages/Simulation";
import Assistant from "./pages/Assistant";
import TokenGen from "./pages/TokenGen";
import HoneyTable from "./pages/HoneyTable";
import Analytics from "./pages/Analytics";
import Documentation from "./pages/Documentation";
import Team from "./pages/Team";

export default function App() {
  return (
    <Router>
      <div className="flex flex-col min-h-screen bg-[#050816] text-white selection:bg-cyan-500/30 selection:text-white">
        {/* Top Sticky Header */}
        <Navbar />

        {/* Dynamic Route Pages */}
        <main className="flex-grow">
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/about" element={<About />} />
            <Route path="/architecture" element={<Architecture />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/simulation" element={<Simulation />} />
            <Route path="/assistant" element={<Assistant />} />
            <Route path="/token" element={<TokenGen />} />
            <Route path="/honey-table" element={<HoneyTable />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/documentation" element={<Documentation />} />
            <Route path="/team" element={<Team />} />
          </Routes>
        </main>

        {/* Global Footer */}
        <Footer />
      </div>
    </Router>
  );
}
