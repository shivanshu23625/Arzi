// ARZI Civic RTI & Statutory Legal Intelligence Platform - Client Interaction Logic

const API_BASE = "/api/v1";
let currentCase = null;
let activePersona = "law_firm"; // 'law_firm' or 'gov_desk'
let currentDocTab = "rti"; // 'rti', 'appeal', 'notice', 'report'
let radarAnimationId = null;

function renderLucide() {
  if (window.lucide && typeof window.lucide.createIcons === "function") {
    window.lucide.createIcons();
  }
}

document.addEventListener("DOMContentLoaded", () => {
  setupNavigation();
  loadCaseQueue();
  loadRunLogs();
  initRadarAnimation();
  loadDirectoryInRadarTab();
  loadCustomActs();
  renderLucide();
});

// Persona Switcher (Law Firm vs Gov Desk)
function switchPersona(persona) {
  activePersona = persona;
  const btnLaw = document.getElementById("btnPersonaLaw");
  const btnGov = document.getElementById("btnPersonaGov");

  if (persona === "law_firm") {
    btnLaw.classList.add("active");
    btnGov.classList.remove("active");
    const revInput = document.getElementById("reviewerName");
    if (revInput) revInput.value = "Adv. S. Kalra (Advocate on Record / Legal NGO)";
  } else {
    btnGov.classList.add("active");
    btnLaw.classList.remove("active");
    const revInput = document.getElementById("reviewerName");
    if (revInput) revInput.value = "Shri R. P. Maurya, IAS (Designated Public Authority)";
  }

  if (currentCase) {
    updateWorkspacePersonaView(currentCase);
  }
  renderLucide();
}

// Top-Level Site Navigation Router (Home, About, Pillars, Dashboard)
function showPage(pageId) {
  document.querySelectorAll(".nav-link-btn").forEach(b => b.classList.remove("active"));
  const navDashBtn = document.getElementById("navDashboardBtn");
  if (navDashBtn) navDashBtn.classList.remove("active");
  document.querySelectorAll(".site-page").forEach(p => p.classList.remove("active"));

  const navMap = {
    home: "siteNavHome",
    about: "siteNavAbout",
    pillars: "siteNavPillars"
  };

  const navBtn = navMap[pageId] ? document.getElementById(navMap[pageId]) : null;
  const pageEl = document.getElementById(`page-${pageId}`);

  if (navBtn) navBtn.classList.add("active");
  if (pageId === "dashboard" && navDashBtn) navDashBtn.classList.add("active");
  if (pageEl) {
    pageEl.classList.add("active");
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  if (pageId === "dashboard") {
    loadCaseQueue();
    loadRunLogs();
    loadCustomActs();
  } else if (pageId === "home") {
    loadCaseQueue();
  }

  renderLucide();
}

// Dashboard Sub-Tab Switcher (Casework, Statutory, PIO, Compliance, RunLog)
function switchDashTab(tabId) {
  showPage("dashboard");
  document.querySelectorAll(".desk-subnav-btn").forEach(b => b.classList.remove("active"));
  document.querySelectorAll(".dash-module").forEach(m => m.classList.remove("active"));

  const subnavMap = {
    casework: "subnavCasework",
    statutory: "subnavStatutory",
    pio: "subnavPio",
    compliance: "subnavCompliance",
    runlog: "subnavRunlog"
  };

  const targetBtn = subnavMap[tabId] ? document.getElementById(subnavMap[tabId]) : null;
  const targetModule = document.getElementById(`dashtab-${tabId}`);

  if (targetBtn) targetBtn.classList.add("active");
  if (targetModule) targetModule.classList.add("active");

  if (tabId === "casework") loadCaseQueue();
  if (tabId === "statutory") loadCustomActs();
  if (tabId === "runlog") loadRunLogs();
  if (tabId === "pio" && currentCase) updateRadarTelemetry(currentCase);

  renderLucide();
}

// Backwards compatibility aliases
function switchMainModule(modName) {
  if (modName === "home" || modName === "about" || modName === "pillars") {
    showPage(modName);
  } else {
    switchDashTab(modName);
  }
}

function switchToTab(tabName) {
  if (tabName === "intake" || tabName === "queue" || tabName === "workspace") switchDashTab("casework");
  else if (tabName === "precedents") switchDashTab("statutory");
  else if (tabName === "radar") switchDashTab("pio");
  else if (tabName === "runlog") switchDashTab("runlog");
  else switchDashTab("casework");
}

function toggleIntakeForm() {
  const c = document.getElementById("intakeFormContainer");
  const t = document.getElementById("intakeToggleText");
  if (c) {
    if (c.style.display === "none") {
      c.style.display = "block";
      if (t) t.textContent = "Hide Form";
    } else {
      c.style.display = "none";
      if (t) t.textContent = "+ Expand Form";
    }
  }
}

function setupNavigation() {
  // Navigation setup
}

// Document Sub-Tabs in Legal Workspace
function switchDocTab(tabName) {
  currentDocTab = tabName;
  document.querySelectorAll(".doc-tab-btn").forEach(b => b.classList.remove("active"));
  document.querySelectorAll("[id^='docPanel']").forEach(p => p.classList.add("hidden"));

  const btn = Array.from(document.querySelectorAll(".doc-tab-btn")).find(b => 
    b.dataset.doctab === tabName || b.textContent.toLowerCase().includes(tabName)
  );
  if (btn) btn.classList.add("active");

  const panelMap = {
    rti: "docPanelRti",
    appeal: "docPanelAppeal",
    notice: "docPanelNotice",
    report: "docPanelReport"
  };

  const panel = document.getElementById(panelMap[tabName]);
  if (panel) panel.classList.remove("hidden");
}

// Submit Citizen / Advocate Intake
async function submitIntake(event) {
  event.preventDefault();

  const complainant = {
    name: document.getElementById("complainantName").value.trim(),
    contact: document.getElementById("complainantContact").value.trim(),
    address: document.getElementById("complainantAddr").value.trim(),
    language: document.getElementById("complainantLang").value
  };

  const raw_grievance = document.getElementById("rawGrievance").value.trim();
  const application_ref_no = document.getElementById("intakeRefNo").value.trim();
  const original_submission_date = document.getElementById("intakeSubDate").value.trim();

  try {
    const res = await fetch(`${API_BASE}/cases/intake`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ complainant, raw_grievance, application_ref_no, original_submission_date })
    });

    const data = await res.json();
    if (res.ok) {
      document.getElementById("intakeForm").reset();
      openCaseWorkspace(data.case);
      switchToTab("workspace");
    } else {
      alert(`Error: ${data.message || "Failed to create case"}`);
    }
  } catch (err) {
    console.error("Intake error:", err);
    alert("Connection error submitting intake.");
  }
}

// Golden Path Preset Loader
function loadPreset(num) {
  switchMainModule("casework");
  const c = document.getElementById("intakeFormContainer");
  if (c) c.style.display = "block";

  if (num === 1) {
    document.getElementById("complainantName").value = "Sunita Devi";
    document.getElementById("complainantContact").value = "+91-9876543210";
    document.getElementById("complainantAddr").value = "House No. 45, BPL Cluster, Ward 4, New Delhi";
    document.getElementById("intakeRefNo").value = "RC-88492";
    document.getElementById("intakeSubDate").value = "15-Feb-2026";
    document.getElementById("rawGrievance").value = "My family's BPL ration card application (Ref No. RC-88492) was submitted on 15-Feb-2026 at Ward 4 supply office. We have not received the card or food grains. Staff refuses to disclose stock registers.";
  } else if (num === 2) {
    document.getElementById("complainantName").value = "Ramesh Chandra";
    document.getElementById("complainantContact").value = "+91-9123456789";
    document.getElementById("complainantAddr").value = "Street 7, Sector 12, Dwarka, New Delhi";
    document.getElementById("intakeRefNo").value = "MW-77401";
    document.getElementById("intakeSubDate").value = "3 weeks ago";
    document.getElementById("rawGrievance").value = "Severe monsoon waterlogging and open storm drain behind Market Road Sector 12. Multiple complaints (Ack MW-77401) filed to MCD Zone 7 office without response.";
  } else if (num === 3) {
    document.getElementById("complainantName").value = "Shivanshu Pandey";
    document.getElementById("complainantContact").value = "+91-9988776655";
    document.getElementById("complainantAddr").value = "Sector 4, Mehrauli, New Delhi";
    document.getElementById("intakeRefNo").value = "LND-88301";
    document.getElementById("intakeSubDate").value = "10-Jan-2026";
    document.getElementById("rawGrievance").value = "My land mutation khasra 45/12 application (Ref LND-88301) submitted on 10-Jan-2026 at Tehsil office Mehrauli is pending. Patwari is not updating land record registry.";
  } else if (num === 4) {
    document.getElementById("complainantName").value = "Shivanshu Pandey";
    document.getElementById("complainantContact").value = "+91-9988776655";
    document.getElementById("complainantAddr").value = "Assi Ghat, Varanasi / Banaras, Uttar Pradesh - 221005";
    document.getElementById("intakeRefNo").value = "VNS-99401";
    document.getElementById("intakeSubDate").value = "10-Jan-2026";
    document.getElementById("rawGrievance").value = "My land mutation khasra 88/14 application (Ref VNS-99401) submitted on 10-Jan-2026 at Tehsil Kachehri Varanasi / Banaras is pending beyond the 30-day statutory limit. Patwari is refusing to update the revenue registry.";
  }

  // Scroll to intake form smoothly
  const intakeForm = document.getElementById("intakeForm");
  if (intakeForm) intakeForm.scrollIntoView({ behavior: "smooth", block: "center" });
}

// Queue Listing & Global Multi-Field Search
async function loadCaseQueue() {
  const searchQuery = document.getElementById("caseSearchInput") ? document.getElementById("caseSearchInput").value.trim() : "";
  const filter = document.getElementById("queueFilter") ? document.getElementById("queueFilter").value : "";
  
  let url = `${API_BASE}/cases?`;
  if (filter) url += `status=${encodeURIComponent(filter)}&`;
  if (searchQuery) url += `search=${encodeURIComponent(searchQuery)}`;

  try {
    const res = await fetch(url);
    const data = await res.json();
    if (!res.ok) return;

    // Update Counts
    const statInbox = document.getElementById("statInbox");
    if (statInbox) statInbox.textContent = data.counts.inbox;
    const statApproved = document.getElementById("statApproved");
    if (statApproved) statApproved.textContent = data.counts.approved;
    const statAtRisk = document.getElementById("statAtRisk");
    if (statAtRisk) statAtRisk.textContent = data.counts.at_risk;
    const statTotal = document.getElementById("statTotal");
    if (statTotal) statTotal.textContent = data.counts.total;
    const inboxCount = document.getElementById("inboxCount");
    if (inboxCount) inboxCount.textContent = data.counts.inbox;
    const homeBadge = document.getElementById("homeQueueBadge");
    if (homeBadge) homeBadge.textContent = data.counts.inbox;
    const homeInboxEl = document.getElementById("homeStatInbox");
    if (homeInboxEl) homeInboxEl.textContent = data.counts.inbox;
    const homeTotalEl = document.getElementById("homeStatTotal");
    if (homeTotalEl) homeTotalEl.textContent = data.counts.total;

    const tbody = document.getElementById("caseQueueBody");
    tbody.innerHTML = "";

    if (data.cases.length === 0) {
      tbody.innerHTML = `<tr><td colspan="8" style="text-align: center; color: var(--text-muted); padding: 24px;">No matching cases found for keyword "${searchQuery}".</td></tr>`;
      return;
    }

    // Auto-select first case if none is selected yet
    if (!currentCase && data.cases.length > 0) {
      currentCase = data.cases[0];
      populateWorkspaceFields(data.cases[0]);
    }

    data.cases.forEach(c => {
      const tr = document.createElement("tr");
      tr.style.cursor = "pointer";
      tr.onclick = () => openCaseById(c.case_id);

      const pio = c.suggested_pio || {};
      const legal = c.statutory_legal_analysis || {};
      const ipcBrief = legal.ipc_sections ? legal.ipc_sections[0] : "IPC Sec 420";
      const bnsBrief = legal.bns_sections ? legal.bns_sections[0] : "BNS Sec 318(4)";
      tr.innerHTML = `
        <td><b style="font-family: var(--font-mono); color: var(--gov-navy); font-size: 11.5px;">${c.case_id}</b></td>
        <td><b>${c.complainant.name}</b><br/><span style="font-size: 10px; color: var(--ink-muted);">${c.complainant.address || 'Local'}</span></td>
        <td><b>${c.department}</b><br/><span style="font-size: 10px; color: var(--gov-copper);">${legal.statutory_infraction || 'Administrative Infraction'}</span></td>
        <td><span class="statutory-tag bns" style="font-size: 9.5px; padding: 1px 4px;">${bnsBrief}</span><br/><span class="statutory-tag ipc" style="font-size: 9.5px; padding: 1px 4px; margin-top: 2px;">${ipcBrief}</span></td>
        <td><b>${pio.pio_name || 'Designated PIO'}</b><br/><span style="font-size: 9.5px; color: var(--status-active); font-family: var(--font-mono);">${distLabel}</span></td>
        <td><span class="status-pill ${c.status === 'APPROVED' ? 'approved' : (c.status === 'TRANSFERRED_SEC_6_3' ? 'transferred' : 'under-review')}">● ${c.status}</span></td>
        <td><button class="btn-gov-outline" style="padding: 3px 8px; font-size: 10.5px;" onclick="event.stopPropagation(); openCaseById('${c.case_id}')">View</button></td>
      `;
      tbody.appendChild(tr);
    });
    renderLucide();
  } catch (err) {
    console.error("Queue load error:", err);
  }
}

async function openCaseById(caseId) {
  try {
    const res = await fetch(`${API_BASE}/cases/${caseId}`);
    const data = await res.json();
    if (res.ok) {
      openCaseWorkspace(data.case);
      switchMainModule("casework");
    }
  } catch (err) {
    console.error("Open case error:", err);
  }
}

// Workspace Renderer
function openCaseWorkspace(c) {
  currentCase = c;
  populateWorkspaceFields(c);
  switchMainModule("casework");
}

function populateWorkspaceFields(c) {
  const emptyState = document.getElementById("noCaseSelected");
  const workspaceView = document.getElementById("caseWorkspaceView");
  if (emptyState) emptyState.classList.add("hidden");
  if (workspaceView) workspaceView.classList.remove("hidden");

  document.getElementById("viewCaseId").textContent = c.case_id;
  
  const statusEl = document.getElementById("viewCaseStatus");
  if (statusEl) {
    statusEl.textContent = `● ${c.status}`;
    statusEl.className = `status-pill ${c.status === 'APPROVED' ? 'approved' : (c.status === 'TRANSFERRED_SEC_6_3' ? 'transferred' : 'under-review')}`;
  }

  document.getElementById("viewComplainant").textContent = c.complainant.name;
  document.getElementById("viewRawGrievance").textContent = `"${c.raw_grievance}"`;

  const legal = c.statutory_legal_analysis || {};
  document.getElementById("viewMeritBadge").textContent = `${legal.case_merit_score || 92}/100 Merit (${legal.win_probability || 'High'})`;
  
  const pen = legal.section_20_penalty_liability_inr || 0;
  document.getElementById("viewPenaltyBadge").textContent = `Section 20(1) Penalty Liability: ₹${pen} (Mandatory ₹250/day deduction applicable on delinquent PIO)`;
  document.getElementById("viewSla").textContent = `${c.sla_days_remaining || 30} Days Remaining`;

  document.getElementById("viewRefNo").textContent = c.application_ref_no || "Not Provided";
  document.getElementById("viewSubDate").textContent = c.original_submission_date || "Unconfirmed";

  // PIO & FAA Block
  const pio = c.suggested_pio || {};
  const faa = c.suggested_faa || pio.faa || {};

  document.getElementById("viewDistanceLabel").textContent = pio.distance_label || "1.5 km away";
  document.getElementById("viewPioName").textContent = pio.pio_name || "Designated PIO";
  document.getElementById("viewPioDept").textContent = pio.department || c.department;
  document.getElementById("viewPioAddr").textContent = pio.office_address || "District Kachehri";
  document.getElementById("viewPioRoom").textContent = `Room: ${pio.room_no || 'Room 101, Ground Floor'} &middot; Email: ${pio.email || 'N/A'}`;

  document.getElementById("viewFaaName").textContent = faa.faa_name || "Additional District Magistrate (Revenue)";

  // Statutory Pills (IPC & BNS)
  const ipcPillsBox = document.getElementById("viewIpcPills");
  const bnsPillsBox = document.getElementById("viewBnsPills");
  ipcPillsBox.innerHTML = "";
  bnsPillsBox.innerHTML = "";

  (legal.ipc_sections || ["IPC Section 420 (Cheating)", "IPC Section 166 (Disobedience of Law)"]).forEach(s => {
    const span = document.createElement("span");
    span.className = "statutory-tag ipc";
    span.style.cssText = "margin-right: 4px; margin-bottom: 4px; display: inline-block;";
    span.textContent = s;
    ipcPillsBox.appendChild(span);
  });

  (legal.bns_sections || ["BNS Section 318(4) (Cheating)", "BNS Section 198 (Public Servant Disobedience)"]).forEach(s => {
    const span = document.createElement("span");
    span.className = "statutory-tag bns";
    span.style.cssText = "margin-right: 4px; margin-bottom: 4px; display: inline-block;";
    span.textContent = s;
    bnsPillsBox.appendChild(span);
  });

  const ipcCountEl = document.getElementById("viewIpcCount");
  const bnsCountEl = document.getElementById("viewBnsCount");
  if (ipcCountEl) ipcCountEl.textContent = `${(legal.ipc_sections || []).length} Sections`;
  if (bnsCountEl) bnsCountEl.textContent = `${(legal.bns_sections || []).length} Sections`;
  const maxPunEl = document.getElementById("viewMaxPunishment");
  if (maxPunEl) maxPunEl.textContent = legal.maximum_punishment || "Rigorous Imprisonment + Fine";

  const groundsList = document.getElementById("viewLegalGrounds");
  groundsList.innerHTML = "";
  (legal.legal_grounds || ["Statutory failure under Citizen Charter"]).forEach(g => {
    const li = document.createElement("li");
    li.textContent = g;
    groundsList.appendChild(li);
  });

  // Draft RTI Inputs
  document.getElementById("editDraftSubject").value = c.draft_rti?.application_subject || "";
  document.getElementById("editDraftQuestions").value = (c.draft_rti?.questions || []).join("\n");
  document.getElementById("editDraftFees").value = c.draft_rti?.fees_paid || "Rs. 10 IPO under Rule 3 Central RTI Rules 2012";

  // First Appeal Panel
  const appeal = c.first_appeal_draft || {};
  document.getElementById("viewAppealSubject").value = appeal.subject || `FIRST APPEAL UNDER SECTION 19(1) IN CASE ${c.case_id}`;
  document.getElementById("viewAppealGrounds").value = (appeal.grounds_of_appeal || []).join("\n\n");
  document.getElementById("viewAppealPrayers").value = (appeal.prayers_sought || []).join("\n");

  // Legal Notice Panel
  const notice = c.legal_notice_draft || {};
  document.getElementById("viewLegalNoticeText").value = notice.notice_text || "";

  // ML Dossier
  document.getElementById("viewMlReportFormat").value = c.ml_report_format || "";

  // Timeline
  renderCaseTimeline(c);

  // Dispatch Proof
  const proofBox = document.getElementById("dispatchProofBox");
  if (c.dispatch_info) {
    proofBox.classList.remove("hidden");
    document.getElementById("proofDetails").innerHTML = `
      <div>DISPATCH ID: <b>${c.dispatch_info.dispatch_id}</b></div>
      <div>TRACKING ID: <b>${c.dispatch_info.tracking_id}</b></div>
      <div>DISPATCHED AT: <b>${c.dispatch_info.dispatched_at}</b></div>
      <div>RECIPIENT: <b>${c.dispatch_info.recipient_name} (${c.dispatch_info.recipient_email})</b></div>
    `;
    document.getElementById("approveBtn").disabled = true;
    document.getElementById("approveBtn").textContent = "CASE DISPATCHED & SEALED ✓";
  } else {
    proofBox.classList.add("hidden");
    document.getElementById("approveBtn").disabled = false;
    document.getElementById("approveBtn").textContent = "⚖️ APPROVE & EXECUTE DISPATCH →";
  }

  updateRadarTelemetry(c);
  updateWorkspacePersonaView(c);
}

function updateWorkspacePersonaView(c) {
  if (activePersona === "gov_desk") {
    document.getElementById("approveBtn").innerHTML = `<i data-lucide="check-check"></i> <span>Dispose / Approve on Gov Desk</span>`;
  } else {
    document.getElementById("approveBtn").innerHTML = `<i data-lucide="send"></i> <span>Advocate Approve & Release Dispatch</span>`;
  }
  renderLucide();
}

function renderCaseTimeline(c) {
  const container = document.getElementById("caseTimelineContainer");
  const tbody = document.getElementById("caseHistoryBody");
  container.innerHTML = "";
  tbody.innerHTML = "";

  if (c.update_history && c.update_history.length > 0) {
    c.update_history.forEach((h, idx) => {
      const isLatest = idx === c.update_history.length - 1;
      const card = document.createElement("div");
      card.style.cssText = `display: flex; gap: 12px; padding: 8px 12px; background: var(--bg-primary); border: 1px solid var(--border-color); border-left: 3px solid ${isLatest ? 'var(--accent-gold)' : 'var(--text-muted)'}; border-radius: 4px; margin-bottom: 6px; font-size: 11px;`;
      card.innerHTML = `
        <div class="text-mono" style="min-width: 130px; color: var(--text-muted);">${h.timestamp}</div>
        <div>
          <b>${h.update_type}</b> — <span style="color: var(--text-secondary);">${h.actor}</span>
          <div style="color: var(--text-secondary); margin-top: 2px;">Field: <b>${h.field_changed}</b> &nbsp;|&nbsp; <code>${h.old_value}</code> &rarr; <code>${h.new_value}</code></div>
          ${h.remarks ? `<div style="color: var(--text-muted); font-style: italic; margin-top: 2px;">"${h.remarks}"</div>` : ''}
        </div>
      `;
      container.appendChild(card);

      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td class="text-mono">${h.timestamp}</td>
        <td><span class="badge badge-gold">${h.update_type}</span></td>
        <td><b>${h.actor}</b></td>
        <td>${h.field_changed}</td>
        <td><small class="text-mono">Old: ${h.old_value}<br/>New: <b>${h.new_value}</b></small></td>
      `;
      tbody.appendChild(tr);
    });
  } else {
    container.innerHTML = `<div class="text-mono" style="font-size: 11px; color: var(--text-muted);">No prior timeline events.</div>`;
  }
}

// Section 6(3) Transfer Modal & Execution
function openTransferModal() {
  if (!currentCase) return;
  document.getElementById("transferModal").classList.remove("hidden");
}

function closeTransferModal() {
  document.getElementById("transferModal").classList.add("hidden");
}

async function submitTransferSec6_3() {
  if (!currentCase) return;
  const targetDept = document.getElementById("transferDeptSelect").value;
  const reason = document.getElementById("transferReason").value.trim();
  const reviewer = document.getElementById("reviewerName").value.trim();

  try {
    const res = await fetch(`${API_BASE}/cases/${currentCase.case_id}/transfer-sec6-3`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ target_department: targetDept, transfer_reason: reason, reviewer })
    });

    const data = await res.json();
    if (res.ok) {
      alert(`Section 6(3) 5-Day Mandatory Transfer Executed!\n\n• Transferred to: ${targetDept}\n• Transferee PIO: ${data.case.suggested_pio?.pio_name}\n• Transfer ID: ${data.case.section_6_3_transfer?.transfer_id}`);
      closeTransferModal();
      openCaseWorkspace(data.case);
      loadRunLogs();
    } else {
      alert(`Error: ${data.message}`);
    }
  } catch (err) {
    console.error("Transfer error:", err);
  }
}

// Approve & Dispatch
async function approveCurrentCase() {
  if (!currentCase) return;

  const reviewer = document.getElementById("reviewerName").value.trim();
  const action = document.getElementById("reviewActionSelect").value;
  const subject = document.getElementById("editDraftSubject").value.trim();
  const questions = document.getElementById("editDraftQuestions").value.trim().split("\n").filter(q => q.trim());

  const payload = {
    reviewer: reviewer || "Adv. S. Kalra",
    notes: `Approved under action: ${action}`,
    draft_rti: {
      application_subject: subject,
      questions: questions
    }
  };

  try {
    const res = await fetch(`${API_BASE}/cases/${currentCase.case_id}/approve`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (res.ok) {
      alert(`Case ${currentCase.case_id} approved and dispatched!\n\n• Dispatch Tracking ID: ${data.case.dispatch_info?.tracking_id}\n• Status: APPROVED & DISPATCHED`);
      openCaseWorkspace(data.case);
      loadRunLogs();
    } else {
      alert(`Error: ${data.message}`);
    }
  } catch (err) {
    console.error("Approval error:", err);
  }
}

// View / Download PDF
function viewPdf(type = "rti") {
  if (!currentCase) {
    alert("Please select a case first.");
    return;
  }
  window.open(`${API_BASE}/cases/${currentCase.case_id}/pdf?type=${type}`, "_blank");
}

// Immutable Run Logs & Multi-Field Search Cache
let allRunLogsCache = [];
let allCasesCache = [];

async function loadRunLogs() {
  try {
    const res = await fetch(`${API_BASE}/run-log`);
    const data = await res.json();
    if (!res.ok) return;

    allRunLogsCache = data.run_logs || [];

    // Also load cases to cross-reference keywords across Name, Place, Subject, Address, Officer
    try {
      const caseRes = await fetch(`${API_BASE}/cases`);
      const caseData = await caseRes.json();
      if (caseRes.ok) {
        allCasesCache = caseData.cases || [];
      }
    } catch (e) {
      console.warn("Could not preload cases for run log search:", e);
    }

    const searchInput = document.getElementById("runLogSearchInput");
    if (searchInput && searchInput.value.trim()) {
      handleRunLogSearch(searchInput.value.trim());
    } else {
      renderRunLogsTable(allRunLogsCache);
      const countBadge = document.getElementById("runLogCountBadge");
      if (countBadge) countBadge.textContent = allRunLogsCache.length;
      const matchedCasesPanel = document.getElementById("matchedCasesPanel");
      if (matchedCasesPanel) matchedCasesPanel.style.display = "none";
      const filterBadge = document.getElementById("runLogFilterBadge");
      if (filterBadge) {
        filterBadge.textContent = "All Events";
        filterBadge.className = "status-pill approved";
      }
      const searchStatus = document.getElementById("runLogSearchStatus");
      if (searchStatus) {
        searchStatus.textContent = "All Logs Active";
        searchStatus.className = "status-pill approved";
      }
    }
  } catch (err) {
    console.error("Run log error:", err);
  }
}

function renderRunLogsTable(logs) {
  const tbody = document.getElementById("runLogBody");
  if (!tbody) return;
  tbody.innerHTML = "";

  if (!logs || logs.length === 0) {
    tbody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: var(--ink-muted); padding: 24px;">No execution run logs match the active query.</td></tr>`;
    return;
  }

  logs.forEach(log => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td style="font-family: var(--font-mono); font-size: 11px;">${log.timestamp}</td>
      <td><span class="statutory-tag" style="font-size: 10px;">${log.event_type}</span></td>
      <td>
        <a href="#" style="font-family: var(--font-mono); color: var(--gov-navy); font-weight: 700; font-size: 11.5px; text-decoration: underline;" onclick="event.preventDefault(); inspectCaseFromRunLog('${log.case_id}')">
          ${log.case_id}
        </a>
      </td>
      <td><b>${log.actor}</b></td>
      <td>${log.action}<br/><span style="font-family: var(--font-mono); font-size: 10px; color: var(--status-active);">Result: ${log.result}</span></td>
      <td style="font-family: var(--font-mono); font-size: 10.5px; color: var(--ink-muted);">${log.correlation_id}</td>
    `;
    tbody.appendChild(tr);
  });
  renderLucide();
}

function handleRunLogSearch(rawQuery) {
  const query = (rawQuery || "").trim().toLowerCase();
  const matchedCasesContainer = document.getElementById("matchedCasesContainer");
  const matchedCasesPanel = document.getElementById("matchedCasesPanel");
  const matchedCasesCount = document.getElementById("matchedCasesCount");
  const runLogFilterBadge = document.getElementById("runLogFilterBadge");
  const runLogSearchStatus = document.getElementById("runLogSearchStatus");
  const countBadge = document.getElementById("runLogCountBadge");

  if (!query) {
    if (matchedCasesPanel) matchedCasesPanel.style.display = "none";
    if (runLogFilterBadge) {
      runLogFilterBadge.textContent = "All Events";
      runLogFilterBadge.className = "status-pill approved";
    }
    if (runLogSearchStatus) {
      runLogSearchStatus.textContent = "All Logs Active";
      runLogSearchStatus.className = "status-pill approved";
    }
    renderRunLogsTable(allRunLogsCache);
    if (countBadge) countBadge.textContent = allRunLogsCache.length;
    return;
  }

  // Synonym expansions (Varanasi / Banaras / Kashi)
  const synonyms = query.includes("varanasi") || query.includes("banaras") || query.includes("kashi")
    ? ["varanasi", "banaras", "kashi"]
    : [query];

  // 1. Search cases across: Complainant Name, Place/Address, Subject/Grievance/Department, Officer Name
  const matchedCases = allCasesCache.filter(c => {
    const complainantName = (c.complainant?.name || "").toLowerCase();
    const complainantAddr = (c.complainant?.address || "").toLowerCase();
    const userLocality = (c.confidence?.user_locality || "").toLowerCase();
    const department = (c.department || c.category || "").toLowerCase();
    const rawGrievance = (c.raw_grievance || "").toLowerCase();
    const draftSubject = (c.draft_rti?.application_subject || "").toLowerCase();
    const refNo = (c.application_ref_no || "").toLowerCase();
    const pioName = (c.suggested_pio?.pio_name || "").toLowerCase();
    const pioAddr = (c.suggested_pio?.office_address || "").toLowerCase();
    const pioDesig = (c.suggested_pio?.designation || "").toLowerCase();
    const caseId = (c.case_id || "").toLowerCase();

    const fullSearchText = `${caseId} ${complainantName} ${complainantAddr} ${userLocality} ${department} ${rawGrievance} ${draftSubject} ${refNo} ${pioName} ${pioAddr} ${pioDesig}`;

    return synonyms.some(term => fullSearchText.includes(term));
  });

  const matchedCaseIds = new Set(matchedCases.map(c => c.case_id.toUpperCase()));

  // 2. Render Matched Case Dockets
  if (matchedCasesPanel && matchedCasesContainer) {
    matchedCasesPanel.style.display = "block";
    if (matchedCasesCount) matchedCasesCount.textContent = matchedCases.length;

    if (matchedCases.length === 0) {
      matchedCasesContainer.innerHTML = `
        <div style="grid-column: 1 / -1; padding: 18px; text-align: center; color: var(--ink-muted); font-size: 12px; background: var(--bg-surface); border: 1px dashed var(--border-medium); border-radius: 4px;">
          <i data-lucide="info" style="width: 16px; height: 16px; display: inline-block; vertical-align: middle; margin-right: 4px; color: var(--gov-copper);"></i>
          No case dockets matched the keyword "<b>${rawQuery}</b>". Checking audit event trail below...
        </div>
      `;
    } else {
      matchedCasesContainer.innerHTML = matchedCases.map(c => {
        const pio = c.suggested_pio || {};
        const pioOfficer = pio.pio_name ? `${pio.pio_name} (${pio.designation || 'PIO'})` : 'Designation Pending';
        const locality = c.confidence?.user_locality || c.complainant?.address?.split(',').slice(-2).join(',').trim() || 'Jurisdiction Assigned';
        const subjectBrief = c.draft_rti?.application_subject || c.raw_grievance || 'Public Record Inquiry';
        const truncatedSubject = subjectBrief.length > 95 ? subjectBrief.substring(0, 92) + '...' : subjectBrief;
        const statusClass = c.status === 'APPROVED' ? 'approved' : (c.status === 'TRANSFERRED_SEC_6_3' ? 'neutral' : 'under-review');

        return `
          <div class="matched-case-card">
            <div>
              <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px;">
                <div style="display: flex; align-items: center; gap: 6px;">
                  <b style="font-family: var(--font-mono); color: var(--gov-navy); font-size: 12.5px;">${c.case_id}</b>
                  <span class="status-pill ${statusClass}" style="font-size: 9.5px;">${c.status.replace(/_/g, ' ')}</span>
                </div>
                <span style="font-family: var(--font-mono); font-size: 10.5px; color: var(--gov-copper); font-weight: 700;">SLA: ${c.sla_days_remaining ?? 14}d</span>
              </div>
              
              <div style="font-size: 12px; font-weight: 700; color: var(--ink-primary); margin-bottom: 3px; display: flex; align-items: center; gap: 4px;">
                <i data-lucide="user" style="width: 12px; height: 12px; color: var(--gov-navy);"></i>
                <span>${c.complainant?.name || 'Anonymous Citizen'}</span>
                <span style="font-weight: 400; color: var(--ink-muted); font-size: 11px;">&bull; ${locality}</span>
              </div>

              <div style="font-size: 11px; color: var(--ink-secondary); margin-bottom: 6px; line-height: 1.35;">
                <b>Subject:</b> ${truncatedSubject}
              </div>

              <div style="font-size: 10.5px; color: var(--ink-secondary); background: var(--bg-subtle); padding: 6px 8px; border-radius: 2px; margin-bottom: 8px;">
                <div style="display: flex; align-items: center; gap: 4px; color: var(--gov-navy); font-weight: 600;">
                  <i data-lucide="building-2" style="width: 11px; height: 11px;"></i>
                  <span>${c.department || 'Public Authority'}</span>
                </div>
                <div style="margin-top: 2px; color: var(--ink-muted);">
                  <b>Officer:</b> ${pioOfficer}
                </div>
                <div style="margin-top: 1px; color: var(--ink-muted);">
                  <b>Address:</b> ${pio.office_address || c.complainant?.address || 'Designated Administrative Complex'}
                </div>
              </div>
            </div>

            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 4px; padding-top: 6px; border-top: 1px dashed var(--border-subtle);">
              <span style="font-size: 10.5px; color: var(--ink-muted);">Ref: <b>${c.application_ref_no || 'Standard Docket'}</b></span>
              <button class="btn-gov-outline" style="font-size: 11px; padding: 3px 8px; background: #FFFFFF;" onclick="inspectCaseFromRunLog('${c.case_id}')">
                <span>Inspect Dossier &rarr;</span>
              </button>
            </div>
          </div>
        `;
      }).join("");
    }
  }

  // 3. Filter Run Log table rows: match log directly OR match case ID of matched cases
  const filteredLogs = allRunLogsCache.filter(log => {
    const caseId = (log.case_id || "").toUpperCase();
    if (matchedCaseIds.has(caseId)) return true;

    const actor = (log.actor || "").toLowerCase();
    const action = (log.action || "").toLowerCase();
    const eventType = (log.event_type || "").toLowerCase();
    const result = (log.result || "").toLowerCase();
    const correlationId = (log.correlation_id || "").toLowerCase();
    const logCaseId = (log.case_id || "").toLowerCase();

    const logText = `${logCaseId} ${actor} ${action} ${eventType} ${result} ${correlationId}`;
    return synonyms.some(term => logText.includes(term));
  });

  renderRunLogsTable(filteredLogs);

  if (runLogFilterBadge) {
    runLogFilterBadge.textContent = `Filtered: ${filteredLogs.length} Rows (${matchedCases.length} Cases)`;
    runLogFilterBadge.className = "status-pill under-review";
  }
  if (runLogSearchStatus) {
    runLogSearchStatus.textContent = `${matchedCases.length} Cases Matched`;
    runLogSearchStatus.className = matchedCases.length > 0 ? "status-pill approved" : "status-pill under-review";
  }
  if (countBadge) {
    countBadge.textContent = filteredLogs.length;
  }
  renderLucide();
}

function inspectCaseFromRunLog(caseId) {
  openCaseById(caseId);
  switchDashTab("casework");
}

function clearRunLogSearch() {
  const input = document.getElementById("runLogSearchInput");
  if (input) input.value = "";
  handleRunLogSearch("");
}

function setRunLogSearchQuery(term) {
  const input = document.getElementById("runLogSearchInput");
  if (input) {
    input.value = term;
    handleRunLogSearch(term);
  }
}

// Live Canvas Radar Animation
let sweepAngle = 0;
function initRadarAnimation() {
  const canvas = document.getElementById("radarCanvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const cx = canvas.width / 2;
  const cy = canvas.height / 2;
  const radius = cx - 15;

  function draw() {
    ctx.fillStyle = "#F8FAFC";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Outer Circle
    ctx.beginPath();
    ctx.arc(cx, cy, radius, 0, Math.PI * 2);
    ctx.strokeStyle = "#CBD5E1";
    ctx.lineWidth = 2;
    ctx.stroke();

    // Concentric Range Rings (1km, 5km, 10km, 15km)
    const rings = [0.25, 0.5, 0.75, 1.0];
    rings.forEach((r, idx) => {
      ctx.beginPath();
      ctx.arc(cx, cy, radius * r, 0, Math.PI * 2);
      ctx.strokeStyle = "#E2E8F0";
      ctx.lineWidth = 1;
      ctx.stroke();

      ctx.fillStyle = "#64748B";
      ctx.font = "10px Segoe UI, Arial, sans-serif";
      ctx.fillText(`${(idx + 1) * 3.75}km`, cx + 6, cy - radius * r + 14);
    });

    // Crosshairs
    ctx.beginPath();
    ctx.moveTo(cx, cy - radius);
    ctx.lineTo(cx, cy + radius);
    ctx.moveTo(cx - radius, cy);
    ctx.lineTo(cx + radius, cy);
    ctx.strokeStyle = "#E2E8F0";
    ctx.stroke();

    // Rotating Sweep Line
    sweepAngle += 0.03;
    const sweepX = cx + Math.cos(sweepAngle) * radius;
    const sweepY = cy + Math.sin(sweepAngle) * radius;

    // Sweep gradient
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.arc(cx, cy, radius, sweepAngle - 0.4, sweepAngle);
    ctx.closePath();
    const grad = ctx.createRadialGradient(cx, cy, 0, cx, cy, radius);
    grad.addColorStop(0, "rgba(37, 99, 235, 0)");
    grad.addColorStop(1, "rgba(37, 99, 235, 0.15)");
    ctx.fillStyle = grad;
    ctx.fill();

    // Sweep leading edge
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.lineTo(sweepX, sweepY);
    ctx.strokeStyle = "rgba(37, 99, 235, 0.6)";
    ctx.lineWidth = 1.5;
    ctx.stroke();

    // Center Blip: Citizen Complainant Location
    ctx.beginPath();
    ctx.arc(cx, cy, 6, 0, Math.PI * 2);
    ctx.fillStyle = "#D97706";
    ctx.fill();

    // Target Blip: Nearest PIO Office
    let pioOffsetX = 45;
    let pioOffsetY = -35;
    if (currentCase?.geospatial_meta?.distance_km) {
      const d = currentCase.geospatial_meta.distance_km;
      pioOffsetX = Math.min(radius - 20, (d / 15) * radius * 0.8 + 25);
      pioOffsetY = -pioOffsetX * 0.7;
    }

    ctx.beginPath();
    ctx.arc(cx + pioOffsetX, cy + pioOffsetY, 7, 0, Math.PI * 2);
    ctx.fillStyle = "#1D4ED8";
    ctx.fill();

    ctx.fillStyle = "#0F172A";
    ctx.font = "bold 11px Segoe UI, Arial, sans-serif";
    ctx.fillText("YOU (CITIZEN)", cx - 28, cy + 20);
    ctx.fillStyle = "#1D4ED8";
    ctx.fillText("PIO (NEAREST)", cx + pioOffsetX - 30, cy + pioOffsetY - 10);

    radarAnimationId = requestAnimationFrame(draw);
  }

  draw();
}

function updateRadarTelemetry(c) {
  const geo = c.geospatial_meta || {};
  const pio = c.suggested_pio || {};

  const uCoords = geo.user_coords || pio.user_coordinates || { latitude: 25.2905, longitude: 82.9995 };
  const pCoords = geo.pio_coords || pio.pio_coordinates || { latitude: 25.3340, longitude: 82.9860 };

  const uEl = document.getElementById("radarUserCoords");
  const pEl = document.getElementById("radarPioCoords");
  const dEl = document.getElementById("radarDistance");

  if (uEl) uEl.textContent = `${uCoords.latitude?.toFixed(4)}° N, ${uCoords.longitude?.toFixed(4)}° E`;
  if (pEl) pEl.textContent = `${pCoords.latitude?.toFixed(4)}° N, ${pCoords.longitude?.toFixed(4)}° E`;
  if (dEl) dEl.textContent = geo.distance_label || pio.distance_label || "1.42 km away";
}

function loadDirectoryInRadarTab() {
  const list = document.getElementById("radarDirectoryList");
  if (!list) return;

  const hubs = [
    { city: "Varanasi / Banaras", dept: "Revenue & Land Records", name: "Shri A. K. Rai (Tehsildar Sadar)", coords: "25.3340, 82.9860", addr: "Tehsil Sadar Kachehri Complex" },
    { city: "Varanasi / Banaras", dept: "Food & Civil Supplies", name: "Shri V. P. Singh (DSO)", coords: "25.3375, 82.9810", addr: "Nadesar DSO Complex" },
    { city: "Varanasi / Banaras", dept: "Police Commissionerate", name: "Shri R. K. Singh (DCP)", coords: "25.3420, 82.9830", addr: "Police Line Headquarters" },
    { city: "New Delhi", dept: "Revenue (South Delhi)", name: "Shri N. Goyal (Tehsildar)", coords: "28.5180, 77.1850", addr: "Mehrauli Revenue Circle 2" },
    { city: "New Delhi", dept: "Food Supplies (Central)", name: "Shri R. K. Sharma (Asst Comm)", coords: "28.6750, 77.2250", addr: "Ward 4 Civil Lines" },
    { city: "New Delhi", dept: "Municipal Works (Dwarka)", name: "Er. S. K. Kalra (Executive Eng)", coords: "28.5920, 77.0460", addr: "Zone 7 Sector 12 Dwarka" }
  ];

  list.innerHTML = "";
  hubs.forEach(h => {
    const div = document.createElement("div");
    div.className = "pio-box";
    div.innerHTML = `
      <div style="display: flex; justify-content: space-between;">
        <b>${h.dept}</b>
        <span class="badge badge-blue">${h.city}</span>
      </div>
      <div style="font-size: 11px; color: var(--accent-gold);">${h.name}</div>
      <div style="font-size: 10.5px; color: var(--text-secondary);">${h.addr}</div>
      <div class="text-mono" style="font-size: 10px; color: var(--text-muted); margin-top: 2px;">GPS: ${h.coords}</div>
    `;
    list.appendChild(div);
  });
  renderLucide();
}

// ----------------------------------------------------
// LAWYER CUSTOM ACTS & STATUTORY INGESTION METHODS
// ----------------------------------------------------

async function loadCustomActs() {
  const container = document.getElementById("customActsContainer");
  const countEl = document.getElementById("customActsCount");
  if (!container) return;

  try {
    const res = await fetch(`${API_BASE}/cases/custom-acts`);
    const data = await res.json();
    if (!res.ok) return;

    const acts = data.custom_acts || [];
    if (countEl) countEl.textContent = acts.length;

    container.innerHTML = "";
    if (acts.length === 0) {
      container.innerHTML = `<div style="grid-column: 1 / -1; color: var(--text-muted); font-size: 12px; padding: 16px;">No custom acts registered yet. Use the form above to add an Act.</div>`;
      return;
    }

    acts.forEach(act => {
      const card = document.createElement("div");
      card.className = "statutory-card";
      card.style.cssText = "display: flex; flex-direction: column; justify-content: space-between; border-left: 3px solid var(--accent-gold);";
      
      card.innerHTML = `
        <div>
          <div class="statutory-card-header">
            <span>${act.act_title}</span>
            <span class="badge badge-gold">${act.act_id}</span>
          </div>
          <div style="font-family: var(--font-mono); font-size: 11px; color: var(--accent-cyan); margin-bottom: 6px;">
            <b>${act.section}</b>
          </div>
          <div style="margin-bottom: 6px;">
            <span class="badge badge-blue">${act.domain}</span>
          </div>
          <p style="font-size: 12px; color: var(--text-secondary); margin-bottom: 8px;">
            ${act.statutory_grounds}
          </p>
          ${act.punishment_or_relief ? `<div class="text-mono" style="font-size: 10.5px; color: var(--accent-terracotta); margin-bottom: 8px;"><b>Scope:</b> ${act.punishment_or_relief}</div>` : ''}
          <div class="text-mono" style="font-size: 10px; color: var(--text-muted); margin-bottom: 12px;">
            Registered by: <b>${act.added_by}</b> &middot; ${act.created_at}
          </div>
        </div>

        <div style="display: flex; gap: 8px; border-top: 1px solid var(--border-color); padding-top: 10px;">
          <button class="btn btn-sm btn-primary framer-button" style="flex: 1;" onclick="applyCustomActToActiveCase('${act.act_id}')">
            <i data-lucide="link"></i>
            <span>Link to Case</span>
          </button>
          <button class="btn btn-sm btn-outline framer-button" style="color: var(--color-rose); border-color: #FECDD3;" onclick="deleteCustomAct('${act.act_id}')">
            <i data-lucide="trash-2"></i>
          </button>
        </div>
      `;
      container.appendChild(card);
    });
    renderLucide();
  } catch (err) {
    console.error("Error loading custom acts:", err);
  }
}

async function submitCustomAct(event) {
  event.preventDefault();

  const actTitle = document.getElementById("customActTitle").value.trim();
  const section = document.getElementById("customActSection").value.trim();
  const domain = document.getElementById("customActDomain").value;
  const author = document.getElementById("customActAuthor").value.trim();
  const grounds = document.getElementById("customActGrounds").value.trim();
  const relief = document.getElementById("customActRelief").value.trim();
  const linkActive = document.getElementById("customActLinkActive").checked;

  const payload = {
    act_title: actTitle,
    section: section,
    domain: domain,
    added_by: author || "Advocate Legal Counsel",
    statutory_grounds: grounds,
    punishment_or_relief: relief,
    linked_case_id: linkActive && currentCase ? currentCase.case_id : null
  };

  try {
    const res = await fetch(`${API_BASE}/cases/custom-acts`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (res.ok) {
      alert(`Custom Act Registered into Legal Codex!\n\n• Act ID: ${data.custom_act.act_id}\n• Act: ${data.custom_act.act_title}\n• Section: ${data.custom_act.section}\n${linkActive && currentCase ? `• Linked to Active Case: ${currentCase.case_id}` : ''}`);
      document.getElementById("customActForm").reset();
      loadCustomActs();
      loadRunLogs();

      if (linkActive && currentCase) {
        openCaseById(currentCase.case_id);
      }
    } else {
      alert(`Error: ${data.message || "Failed to register custom act."}`);
    }
  } catch (err) {
    console.error("Custom act submit error:", err);
    alert("Connection error registering custom act.");
  }
}

async function deleteCustomAct(actId) {
  if (!confirm(`Are you sure you want to remove custom act ${actId} from the legal library?`)) {
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/cases/custom-acts/${actId}`, {
      method: "DELETE"
    });

    const data = await res.json();
    if (res.ok) {
      loadCustomActs();
      loadRunLogs();
    } else {
      alert(`Error: ${data.message}`);
    }
  } catch (err) {
    console.error("Delete custom act error:", err);
  }
}

async function applyCustomActToActiveCase(actId) {
  if (!currentCase) {
    alert("Please select or open an active case docket first from Command Center.");
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/cases/${currentCase.case_id}/apply-custom-act`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ act_id: actId, reviewer: "Adv. S. Kalra" })
    });

    const data = await res.json();
    if (res.ok) {
      alert(`Custom Act ${actId} successfully linked to active case ${currentCase.case_id}!\n\nCheck '03. LEGAL & COMPLIANCE WORKSPACE' to see the added statutory section and grounds.`);
      openCaseWorkspace(data.case);
      loadRunLogs();
    } else {
      alert(`Error: ${data.message}`);
    }
  } catch (err) {
    console.error("Apply custom act error:", err);
  }
}


