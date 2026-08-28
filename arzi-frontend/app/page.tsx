"use client";

import React, { useState, useEffect } from "react";

export default function Home() {
  const [activeTab, setActiveTab] = useState("intake");
  const [killSwitchActive, setKillSwitchActive] = useState(false);
  const [killMessage, setKillMessage] = useState("");
  const [cases, setCases] = useState<any[]>([]);
  const [counts, setCounts] = useState({ inbox: 0, approved: 0, at_risk: 0, total: 0 });
  const [runLogs, setRunLogs] = useState<any[]>([]);
  const [selectedCase, setSelectedCase] = useState<any>(null);
  const [searchQuery, setSearchQuery] = useState("");

  // Form State
  const [name, setName] = useState("");
  const [contact, setContact] = useState("");
  const [address, setAddress] = useState("");
  const [dept, setDept] = useState("");
  const [grievance, setGrievance] = useState("");
  const [refNo, setRefNo] = useState("");
  const [subDate, setSubDate] = useState("");

  const API_BASE = "http://localhost:5000/api/v1";

  useEffect(() => {
    fetchQueue(searchQuery);
    fetchRunLogs();
  }, []);

  const fetchQueue = async (query = "") => {
    try {
      let url = `${API_BASE}/cases`;
      if (query.trim()) {
        url += `?search=${encodeURIComponent(query.trim())}`;
      }
      const res = await fetch(url);
      if (res.status === 503) {
        setKillSwitchActive(true);
        setKillMessage("GitHub Repository deletion detected (HTTP 503). Core repository binding revoked.");
        return;
      }
      const data = await res.json();
      if (res.ok) {
        setCases(data.cases || []);
        setCounts(data.counts || { inbox: 0, approved: 0, at_risk: 0, total: 0 });
        if (!selectedCase && data.cases && data.cases.length > 0) {
          setSelectedCase(data.cases[0]);
        }
      }
    } catch (e) {
      console.log("Flask backend offline or starting...");
    }
  };

  const fetchRunLogs = async () => {
    try {
      const res = await fetch(`${API_BASE}/run-log`);
      const data = await res.json();
      if (res.ok) {
        setRunLogs(data.run_logs || []);
      }
    } catch (e) {}
  };

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    fetchQueue(searchQuery);
  };

  const handleIntakeSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch(`${API_BASE}/cases/intake`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          complainant: { name, contact, address, language: "Hindi / English" },
          raw_grievance: grievance,
          department: dept,
          application_ref_no: refNo,
          original_submission_date: subDate
        })
      });

      if (res.status === 503) {
        setKillSwitchActive(true);
        return;
      }

      const data = await res.json();
      if (res.ok) {
        alert(`Case Created with Unique ID: ${data.case.case_id}\nAssigned PIO: ${data.case.suggested_pio.pio_name} (${data.case.suggested_pio.office_address})`);
        setName("");
        setContact("");
        setAddress("");
        setGrievance("");
        setDept("");
        setRefNo("");
        setSubDate("");
        setSelectedCase(data.case);
        setActiveTab("workspace");
        fetchQueue();
      }
    } catch (err) {
      alert("Error connecting to Flask backend.");
    }
  };

  const openCaseDetails = (c: any) => {
    setSelectedCase(c);
    setActiveTab("workspace");
  };

  const toggleKillSwitchSim = async (simulate: boolean) => {
    try {
      const res = await fetch(`${API_BASE}/system/kill-switch`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ simulate_deleted: simulate })
      });
      const data = await res.json();
      if (simulate) {
        setKillSwitchActive(true);
        setKillMessage(data.repository_validation.status_message);
      } else {
        setKillSwitchActive(false);
        fetchQueue();
      }
    } catch (e) {}
  };

  return (
    <div style={{ maxWidth: "1280px", margin: "0 auto", padding: "20px" }}>
      {killSwitchActive && (
        <div style={{
          position: "fixed", top: 0, left: 0, width: "100vw", height: "100vh",
          background: "rgba(30,36,43,0.95)", zIndex: 9999, display: "flex",
          alignItems: "center", justifyContent: "center", padding: "20px"
        }}>
          <div style={{
            background: "#FFF", border: "4px solid #D94E28", boxShadow: "8px 8px 0 #000",
            maxWidth: "600px", padding: "36px", textAlign: "center"
          }}>
            <div style={{ background: "#D94E28", color: "#FFF", padding: "4px 12px", fontFamily: "monospace" }}>
              CRITICAL SYSTEM INTEGRITY BREACH
            </div>
            <h1 style={{ margin: "16px 0" }}>CORE REPOSITORY BINDING REVOKED</h1>
            <p>{killMessage}</p>
            <button 
              onClick={() => toggleKillSwitchSim(false)}
              style={{
                marginTop: "20px", background: "#D94E28", color: "#FFF",
                padding: "12px 24px", border: "2px solid #1E242B", cursor: "pointer", fontWeight: "bold"
              }}
            >
              RESTORE SYSTEM INTEGRITY
            </button>
          </div>
        </div>
      )}

      {/* Header */}
      <header style={{
        background: "#FFF", border: "2px solid #1E242B", boxShadow: "4px 4px 0 #1E242B",
        padding: "16px 24px", display: "flex", justifyContent: "space-between", marginBottom: "20px"
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
          <div style={{ background: "#D94E28", color: "#FFF", fontWeight: "bold", fontSize: "24px", padding: "6px 16px", border: "2px solid #1E242B" }}>
            ARZI
          </div>
          <div>
            <div style={{ fontWeight: "bold", fontSize: "18px" }}>CIVIC RTI LEGAL FILING DESK</div>
            <div style={{ fontFamily: "monospace", fontSize: "12px", color: "#555" }}>Flask Engine + Banaras / Varanasi Multi-Domain Officer Routing</div>
          </div>
        </div>

        <button 
          onClick={() => toggleKillSwitchSim(true)}
          style={{ background: "#FFF", border: "2px solid #1E242B", padding: "8px 16px", cursor: "pointer", fontWeight: "bold" }}
        >
          SIMULATE REPO DELETION
        </button>
      </header>

      {/* Nav */}
      <nav style={{ display: "flex", gap: "12px", marginBottom: "24px" }}>
        {["intake", "queue", "workspace", "runlog"].map((t) => (
          <button
            key={t}
            onClick={() => setActiveTab(t)}
            style={{
              padding: "12px 20px", fontWeight: "bold", border: "2px solid #1E242B",
              background: activeTab === t ? "#1E242B" : "#FFF",
              color: activeTab === t ? "#FFF" : "#1E242B",
              boxShadow: activeTab === t ? "4px 4px 0 #1E242B" : "2px 2px 0 #1E242B",
              cursor: "pointer"
            }}
          >
            {t === "intake" && "01. INTAKE PORTAL"}
            {t === "queue" && `02. COMMAND CENTER (${counts.inbox})`}
            {t === "workspace" && `03. LEGAL WORKSPACE (${selectedCase ? selectedCase.case_id : 'SELECT'})`}
            {t === "runlog" && "04. PROOF RUN LOG"}
          </button>
        ))}
      </nav>

      {/* Content */}
      {activeTab === "intake" && (
        <div style={{ background: "#FFF", border: "2px solid #1E242B", boxShadow: "4px 4px 0 #1E242B", padding: "24px" }}>
          <h2 style={{ marginBottom: "16px" }}>INGEST CITIZEN GRIEVANCE</h2>
          <form onSubmit={handleIntakeSubmit}>
            <div style={{ marginBottom: "16px" }}>
              <label style={{ display: "block", fontFamily: "monospace", fontWeight: "bold" }}>COMPLAINANT NAME *</label>
              <input type="text" value={name} onChange={e => setName(e.target.value)} required style={{ width: "100%", padding: "10px", border: "2px solid #1E242B" }} placeholder="e.g. Shivanshu Pandey" />
            </div>

            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px", marginBottom: "16px" }}>
              <div>
                <label style={{ display: "block", fontFamily: "monospace", fontWeight: "bold" }}>PHONE / CONTACT *</label>
                <input type="text" value={contact} onChange={e => setContact(e.target.value)} required style={{ width: "100%", padding: "10px", border: "2px solid #1E242B" }} placeholder="+91-9988776655" />
              </div>
              <div>
                <label style={{ display: "block", fontFamily: "monospace", fontWeight: "bold" }}>POSTAL ADDRESS (e.g. Varanasi / Banaras) *</label>
                <input type="text" value={address} onChange={e => setAddress(e.target.value)} required style={{ width: "100%", padding: "10px", border: "2px solid #1E242B" }} placeholder="Assi Ghat, Varanasi / Banaras, UP" />
              </div>
            </div>

            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px", marginBottom: "16px" }}>
              <div>
                <label style={{ display: "block", fontFamily: "monospace", fontWeight: "bold" }}>REF / ACKNOWLEDGEMENT NO</label>
                <input type="text" value={refNo} onChange={e => setRefNo(e.target.value)} style={{ width: "100%", padding: "10px", border: "2px solid #1E242B" }} placeholder="e.g. VNS-99401" />
              </div>
              <div>
                <label style={{ display: "block", fontFamily: "monospace", fontWeight: "bold" }}>ORIGINAL FILING DATE</label>
                <input type="text" value={subDate} onChange={e => setSubDate(e.target.value)} style={{ width: "100%", padding: "10px", border: "2px solid #1E242B" }} placeholder="e.g. 10-Jan-2026" />
              </div>
            </div>

            <div style={{ marginBottom: "16px" }}>
              <label style={{ display: "block", fontFamily: "monospace", fontWeight: "bold" }}>RAW GRIEVANCE NARRATIVE *</label>
              <textarea value={grievance} onChange={e => setGrievance(e.target.value)} rows={4} required style={{ width: "100%", padding: "10px", border: "2px solid #1E242B" }} placeholder="My land mutation khasra application submitted at Varanasi / Banaras Tehsil is pending..."></textarea>
            </div>

            <button type="submit" style={{ background: "#D94E28", color: "#FFF", border: "2px solid #1E242B", padding: "12px 24px", fontWeight: "bold", cursor: "pointer", width: "100%" }}>
              INGEST & ASSIGN BANARAS / DIVISION PIO OFFICER →
            </button>
          </form>
        </div>
      )}

      {activeTab === "queue" && (
        <div style={{ background: "#FFF", border: "2px solid #1E242B", boxShadow: "4px 4px 0 #1E242B", padding: "24px" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px" }}>
            <h2>LAWYER DASHBOARD & COMMAND CENTER</h2>
            
            <form onSubmit={handleSearchSubmit} style={{ display: "flex", gap: "8px", alignItems: "center" }}>
              <label style={{ fontWeight: "bold", fontFamily: "monospace" }}>SEARCH KEYWORD:</label>
              <input
                type="text"
                placeholder="Unique ID, Name, Varanasi/Banaras, Address, Issue..."
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
                style={{ width: "320px", padding: "8px 12px", border: "2px solid #1E242B" }}
              />
              <button 
                type="submit" 
                style={{ background: "#D94E28", color: "#FFF", border: "2px solid #1E242B", padding: "8px 16px", fontWeight: "bold", cursor: "pointer" }}
              >
                SEARCH 🔍
              </button>
            </form>
          </div>

          <p style={{ fontFamily: "monospace", color: "#555", marginBottom: "16px" }}>
            Showing {cases.length} cases. Click on any row to open the RTI Legal Workspace with full updates & timeline.
          </p>

          <table style={{ width: "100%", borderCollapse: "collapse", marginTop: "8px" }}>
            <thead>
              <tr style={{ background: "#1E242B", color: "#FFF" }}>
                <th style={{ padding: "10px", border: "1px solid #1E242B" }}>UNIQUE CASE ID</th>
                <th style={{ padding: "10px", border: "1px solid #1E242B" }}>COMPLAINANT & ADDRESS</th>
                <th style={{ padding: "10px", border: "1px solid #1E242B" }}>DEPARTMENT</th>
                <th style={{ padding: "10px", border: "1px solid #1E242B" }}>ASSIGNED PUBLIC OFFICER</th>
                <th style={{ padding: "10px", border: "1px solid #1E242B" }}>STATUS</th>
                <th style={{ padding: "10px", border: "1px solid #1E242B" }}>ACTION</th>
              </tr>
            </thead>
            <tbody>
              {cases.length === 0 ? (
                <tr>
                  <td colSpan={6} style={{ textAlign: "center", padding: "20px", color: "#888" }}>
                    No matching cases found for search keyword "{searchQuery}".
                  </td>
                </tr>
              ) : (
                cases.map(c => (
                  <tr 
                    key={c.case_id}
                    onClick={() => openCaseDetails(c)}
                    style={{ cursor: "pointer", background: selectedCase?.case_id === c.case_id ? "#FFFDE7" : "#FFF" }}
                  >
                    <td style={{ padding: "10px", border: "1px solid #1E242B" }}><b>{c.case_id}</b></td>
                    <td style={{ padding: "10px", border: "1px solid #1E242B" }}>
                      <b>{c.complainant.name}</b><br/>
                      <small style={{ color: "#555" }}>{c.complainant.address}</small>
                    </td>
                    <td style={{ padding: "10px", border: "1px solid #1E242B" }}>{c.department}</td>
                    <td style={{ padding: "10px", border: "1px solid #1E242B" }}>
                      <b>{c.suggested_pio?.pio_name}</b><br/>
                      <small style={{ color: "#555" }}>{c.suggested_pio?.office_address}</small>
                    </td>
                    <td style={{ padding: "10px", border: "1px solid #1E242B" }}>
                      <span style={{
                        padding: "2px 8px", background: c.status === "APPROVED" ? "#C8E6C9" : "#FFE0B2",
                        border: "1px solid #1E242B", fontSize: "12px", fontWeight: "bold"
                      }}>
                        {c.status}
                      </span>
                    </td>
                    <td style={{ padding: "10px", border: "1px solid #1E242B" }}>
                      <button 
                        onClick={(e) => { e.stopPropagation(); openCaseDetails(c); }}
                        style={{ background: "#D94E28", color: "#FFF", border: "1px solid #1E242B", padding: "4px 10px", fontWeight: "bold", cursor: "pointer" }}
                      >
                        OPEN CASE →
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      )}

      {activeTab === "workspace" && (
        <div style={{ background: "#FFF", border: "2px solid #1E242B", boxShadow: "4px 4px 0 #1E242B", padding: "24px" }}>
          {selectedCase ? (
            <div>
              <div style={{ display: "flex", justifyContent: "space-between", borderBottom: "2px solid #1E242B", paddingBottom: "12px", marginBottom: "16px" }}>
                <div>
                  <span style={{ background: "#D94E28", color: "#FFF", padding: "4px 8px", fontWeight: "bold", marginRight: "8px" }}>
                    UNIQUE CASE ID: {selectedCase.case_id}
                  </span>
                  <span style={{ background: "#1E242B", color: "#FFF", padding: "4px 8px", fontWeight: "bold" }}>
                    {selectedCase.status}
                  </span>
                </div>
                <div style={{ fontFamily: "monospace", fontWeight: "bold" }}>
                  REF: {selectedCase.application_ref_no || "N/A"} | SUBMITTED: {selectedCase.original_submission_date || "N/A"}
                </div>
              </div>

              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "20px", marginBottom: "20px" }}>
                <div style={{ border: "2px solid #1E242B", padding: "16px" }}>
                  <h3 style={{ borderBottom: "1px solid #ccc", paddingBottom: "6px", marginBottom: "10px" }}>CITIZEN COMPLAINANT</h3>
                  <div><b>Name:</b> {selectedCase.complainant?.name}</div>
                  <div><b>Contact:</b> {selectedCase.complainant?.contact}</div>
                  <div><b>Address:</b> {selectedCase.complainant?.address}</div>
                  <div style={{ marginTop: "10px", fontStyle: "italic", background: "#f5f5f5", padding: "8px" }}>
                    "{selectedCase.raw_grievance}"
                  </div>
                </div>

                <div style={{ border: "2px solid #1E242B", padding: "16px", background: "#F1F8E9" }}>
                  <h3 style={{ borderBottom: "1px solid #ccc", paddingBottom: "6px", marginBottom: "10px", color: "#2E7D32" }}>
                    ASSIGNED PUBLIC OFFICER (PIO)
                  </h3>
                  <div><b>Department / Domain:</b> {selectedCase.department}</div>
                  <div><b>Officer Name:</b> {selectedCase.suggested_pio?.pio_name}</div>
                  <div><b>Designation:</b> {selectedCase.suggested_pio?.designation}</div>
                  <div><b>Office Address:</b> {selectedCase.suggested_pio?.office_address}</div>
                  <div><b>Email:</b> {selectedCase.suggested_pio?.email}</div>
                  <div><b>Phone:</b> {selectedCase.suggested_pio?.phone}</div>
                </div>
              </div>

              {/* TIMELINE & UPDATES AUDIT HISTORY TABLE */}
              <div style={{ border: "2px solid #1E242B", padding: "16px", marginBottom: "20px", background: "#FAF3E0" }}>
                <h3 style={{ borderBottom: "1px solid #ccc", paddingBottom: "6px", marginBottom: "12px", color: "#D94E28" }}>
                  ⏱️ CASE UPDATE TIMELINE & TABULAR AUDIT HISTORY
                </h3>
                
                {selectedCase.update_history && selectedCase.update_history.length > 0 ? (
                  <div>
                    {/* Visual Timeline Cards */}
                    <div style={{ display: "flex", flexDirection: "column", gap: "10px", marginBottom: "16px" }}>
                      {selectedCase.update_history.map((h: any, idx: number) => (
                        <div key={idx} style={{
                          display: "flex", gap: "12px", padding: "10px", background: "#FFF",
                          border: "1px solid #1E242B", borderLeft: `4px solid ${idx === selectedCase.update_history.length - 1 ? '#D94E28' : '#1E242B'}`
                        }}>
                          <div style={{ fontFamily: "monospace", fontSize: "11px", color: "#555", minWidth: "140px" }}>
                            {h.timestamp}
                          </div>
                          <div>
                            <div style={{ fontWeight: "bold", fontSize: "12px" }}>
                              <span style={{ background: "#E3F2FD", color: "#0D47A1", padding: "2px 6px", marginRight: "8px", fontSize: "10px" }}>
                                STEP 0{idx + 1}
                              </span>
                              {h.update_type} — {h.actor}
                            </div>
                            <div style={{ fontSize: "11px", color: "#333", marginTop: "2px" }}>
                              <b>Field Changed:</b> {h.field_changed} | <b>Old:</b> <code>{h.old_value}</code> &rarr; <b>New:</b> <code>{h.new_value}</code>
                            </div>
                            {h.remarks && (
                              <div style={{ fontSize: "11px", color: "#666", fontStyle: "italic", marginTop: "2px" }}>
                                "{h.remarks}"
                              </div>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>

                    {/* Tabular Form */}
                    <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "12px", background: "#FFF" }}>
                      <thead>
                        <tr style={{ background: "#1E242B", color: "#FFF" }}>
                          <th style={{ padding: "8px", border: "1px solid #1E242B" }}>TIMESTAMP</th>
                          <th style={{ padding: "8px", border: "1px solid #1E242B" }}>UPDATE TYPE</th>
                          <th style={{ padding: "8px", border: "1px solid #1E242B" }}>ACTOR</th>
                          <th style={{ padding: "8px", border: "1px solid #1E242B" }}>FIELD CHANGED</th>
                          <th style={{ padding: "8px", border: "1px solid #1E242B" }}>OLD vs NEW VALUE</th>
                          <th style={{ padding: "8px", border: "1px solid #1E242B" }}>REMARKS</th>
                        </tr>
                      </thead>
                      <tbody>
                        {selectedCase.update_history.map((h: any, idx: number) => (
                          <tr key={idx}>
                            <td style={{ padding: "8px", border: "1px solid #1E242B", fontFamily: "monospace" }}>{h.timestamp}</td>
                            <td style={{ padding: "8px", border: "1px solid #1E242B" }}><b>{h.update_type}</b></td>
                            <td style={{ padding: "8px", border: "1px solid #1E242B" }}>{h.actor}</td>
                            <td style={{ padding: "8px", border: "1px solid #1E242B" }}>{h.field_changed}</td>
                            <td style={{ padding: "8px", border: "1px solid #1E242B", fontFamily: "monospace" }}>
                              <small>Old: {h.old_value}<br/>New: <b>{h.new_value}</b></small>
                            </td>
                            <td style={{ padding: "8px", border: "1px solid #1E242B", color: "#555" }}>{h.remarks}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                ) : (
                  <p>No updates recorded yet.</p>
                )}
              </div>

              <div style={{ border: "2px solid #1E242B", padding: "16px", marginBottom: "20px" }}>
                <h3>DRAFT LEGAL RTI APPLICATION SUBJECT</h3>
                <p style={{ fontWeight: "bold", background: "#eee", padding: "8px" }}>
                  {selectedCase.draft_rti?.application_subject}
                </p>

                <h3 style={{ marginTop: "12px" }}>RECORD-BASED RTI QUESTIONS SOUGHT</h3>
                <ol style={{ paddingLeft: "20px" }}>
                  {selectedCase.draft_rti?.questions?.map((q: string, idx: number) => (
                    <li key={idx} style={{ marginBottom: "6px" }}>{q}</li>
                  ))}
                </ol>
              </div>

              <div style={{ border: "2px solid #1E242B", padding: "16px" }}>
                <h3>FULL LEGAL ASSESSMENT REPORT</h3>
                <pre style={{ background: "#1E242B", color: "#00FF66", padding: "16px", overflowX: "auto", fontSize: "12px" }}>
                  {selectedCase.ml_report_format}
                </pre>
              </div>
            </div>
          ) : (
            <p>No case selected. Please select a case from the Operational Command Center.</p>
          )}
        </div>
      )}

      {activeTab === "runlog" && (
        <div style={{ background: "#FFF", border: "2px solid #1E242B", boxShadow: "4px 4px 0 #1E242B", padding: "24px" }}>
          <h2>IMMUTABLE CODE-GENERATED RUN LOG</h2>
          <table style={{ width: "100%", borderCollapse: "collapse", marginTop: "16px" }}>
            <thead>
              <tr style={{ background: "#1E242B", color: "#FFF" }}>
                <th style={{ padding: "10px", border: "1px solid #1E242B" }}>TIMESTAMP</th>
                <th style={{ padding: "10px", border: "1px solid #1E242B" }}>EVENT</th>
                <th style={{ padding: "10px", border: "1px solid #1E242B" }}>CASE ID</th>
                <th style={{ padding: "10px", border: "1px solid #1E242B" }}>ACTION</th>
              </tr>
            </thead>
            <tbody>
              {runLogs.map((l, idx) => (
                <tr key={idx}>
                  <td style={{ padding: "10px", border: "1px solid #1E242B", fontFamily: "monospace" }}>{l.timestamp}</td>
                  <td style={{ padding: "10px", border: "1px solid #1E242B" }}>{l.event_type}</td>
                  <td style={{ padding: "10px", border: "1px solid #1E242B" }}><b>{l.case_id}</b></td>
                  <td style={{ padding: "10px", border: "1px solid #1E242B" }}>{l.action}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
