import { useState } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import "./App.css";

function App() {
  const [company, setCompany] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState("report");

  const runAnalysis = async () => {
    if (!company.trim()) return;
    setLoading(true);
    setResult(null);
    setError(null);

    try {
      const response = await axios.post("http://127.0.0.1:8000/analyse", {
        company_name: company,
      });
      setResult(response.data);
    } catch (err) {
      setError("Analysis failed. Make sure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") runAnalysis();
  };

  return (
    <div className="app">
      <header className="header">
        <div className="header-inner">
          <h1 className="logo">AgentFlow</h1>
          <p className="tagline">
            Local-first multi-agent financial due diligence
          </p>
        </div>
      </header>

      <main className="main">
        <div className="search-section">
          <div className="search-box">
            <input
              type="text"
              className="search-input"
              placeholder="Enter company name (e.g. Tesla, Apple, Amazon)"
              value={company}
              onChange={(e) => setCompany(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={loading}
            />
            <button
              className="search-btn"
              onClick={runAnalysis}
              disabled={loading || !company.trim()}
            >
              {loading ? "Analysing..." : "Run Analysis"}
            </button>
          </div>
          {loading && (
            <div className="loading-state">
              <div className="spinner"></div>
              <div className="loading-steps">
                <p>Three agents are running locally on your machine</p>
                <p className="loading-sub">
                  Research → Risk Analysis → Report Generation
                </p>
              </div>
            </div>
          )}
        </div>

        {error && <div className="error-box">{error}</div>}

        {result && (
          <div className="results-section">
            <div className="results-header">
              <h2 className="results-title">
                Due Diligence Report: {result.company}
              </h2>
              <div className="badge">Zero Data Egress</div>
            </div>

            <div className="tabs">
              <button
                className={`tab ${activeTab === "report" ? "active" : ""}`}
                onClick={() => setActiveTab("report")}
              >
                Full Report
              </button>
              <button
                className={`tab ${activeTab === "research" ? "active" : ""}`}
                onClick={() => setActiveTab("research")}
              >
                Research
              </button>
              <button
                className={`tab ${activeTab === "analysis" ? "active" : ""}`}
                onClick={() => setActiveTab("analysis")}
              >
                Risk Analysis
              </button>
            </div>

            <div className="tab-content">
              {activeTab === "report" && (
                <div className="report-content">
                  <ReactMarkdown>{result.report}</ReactMarkdown>
                </div>
              )}
              {activeTab === "research" && (
                <div className="report-content">
                  <ReactMarkdown>{result.research}</ReactMarkdown>
                </div>
              )}
              {activeTab === "analysis" && (
                <div className="report-content">
                  <ReactMarkdown>{result.analysis}</ReactMarkdown>
                </div>
              )}
            </div>
          </div>
        )}
      </main>

      <footer className="footer">
        <p>All processing runs locally. No data leaves your machine.</p>
      </footer>
    </div>
  );
}

export default App;