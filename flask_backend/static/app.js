// ARZI Civic RTI Legal Filing Desk - Frontend Interaction Logic

const API_BASE = "/api/v1";
let currentCase = null;

document.addEventListener("DOMContentLoaded", () => {
  setupNavigation();
  loadCaseQueue();
  loadRunLogs();
});

// Navigation Setup
function setupNavigation() {
  const tabs = document.querySelectorAll(".nav-tab");
  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      const targetTab = tab.dataset.tab;
      switchToTab(targetTab);
    });
  });
}

function switchToTab(tabName) {
  document.querySelectorAll(".nav-tab").forEach(t => t.classList.remove("active"));
  document.querySelectorAll(".tab-panel").forEach(p => p.classList.remove("active"));

  const targetTabBtn = document.querySelector(`.nav-tab[data-tab="${tabName}"]`);
  const targetPanel = document.getElementById(`tab-${tabName}`);

  if (targetTabBtn && targetPanel) {
    targetTabBtn.classList.add("active");
    targetPanel.classList.add("active");
  }

  if (tabName === "queue") loadCaseQueue();
  if (tabName === "runlog") loadRunLogs();
}

// Intake Submission (ML Automatically Predicts Department & Extracts Evidence Report)
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

    if (res.status === 503) {
      handleKillSwitchTriggered();
      return;
    }

    const data = await res.json();
    if (res.ok) {
      alert(`Case ingested! ML generated Legal Assessment Report for department: "${data.case.department}".`);
      document.getElementById("intakeForm").reset();
      openCaseWorkspace(data.case);
    } else {
      alert(`Error: ${data.message || "Failed to create case"}`);
    }
  } catch (err) {
    console.error("Intake submission error:", err);
    alert("Connection error while submitting intake.");
  }
}

// Preset Loader
function loadPreset(num) {
  if (num === 1) {
    document.getElementById("complainantName").value = "Sunita Devi";
    document.getElementById("complainantContact").value = "+91-9876543210";
    document.getElementById("complainantAddr").value = "House No. 45, BPL Cluster, Ward 4, New Delhi";
    document.getElementById("intakeRefNo").value = "RC-88492";
    document.getElementById("intakeSubDate").value = "15-Feb-2026";
    document.getElementById("rawGrievance").value = "My family's BPL ration card application (Ref No. RC-88492) was submitted on 15-Feb-2026 at Ward 4 supply office. We have not received the card or food grains. Staff keeps telling us to come back next week without giving any reason.";
  } else if (num === 2) {
    document.getElementById("complainantName").value = "Ramesh Chandra";
    document.getElementById("complainantContact").value = "+91-9123456789";
    document.getElementById("complainantAddr").value = "Street 7, Sector 12, Dwarka, New Delhi";
    document.getElementById("intakeRefNo").value = "MW-77401";
    document.getElementById("intakeSubDate").value = "3 weeks ago";
    document.getElementById("rawGrievance").value = "Severe monsoon waterlogging and open storm drain behind Market Road Sector 12. Multiple complaints (Ack MW-77401) filed 3 weeks ago to Zone 7 office, no response.";
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
}

// Queue Listing & Global Multi-Field Search
async function loadCaseQueue() {
  await filterCasesBySearch();
}

async function filterCasesBySearch() {
  const searchQuery = document.getElementById("caseSearchInput") ? document.getElementById("caseSearchInput").value.trim() : "";
  const filter = document.getElementById("queueFilter") ? document.getElementById("queueFilter").value : "";
  
  let url = `${API_BASE}/cases?`;
  if (filter) url += `status=${encodeURIComponent(filter)}&`;
  if (searchQuery) url += `search=${encodeURIComponent(searchQuery)}`;
  
  try {
    const res = await fetch(url);
    if (res.status === 503) {
      handleKillSwitchTriggered();
      return;
    }
    const data = await res.json();
    if (!res.ok) return;

    // Update Counts
    document.getElementById("statInbox").textContent = data.counts.inbox;
    document.getElementById("statApproved").textContent = data.counts.approved;
    document.getElementById("statAtRisk").textContent = data.counts.at_risk;
    document.getElementById("statTotal").textContent = data.counts.total;
    document.getElementById("inboxCount").textContent = data.counts.inbox;

    // Render Table
    const tbody = document.getElementById("caseQueueBody");
    tbody.innerHTML = "";

    if (data.cases.length === 0) {
      tbody.innerHTML = `<tr><td colspan="8" style="text-align: center; color: #757575; padding: 24px;">No matching cases found for search keyword "${searchQuery}".</td></tr>`;
      return;
    }

    data.cases.forEach(c => {
      const tr = document.createElement("tr");
      tr.style.cursor = "pointer";
      tr.onclick = () => openCaseById(c.case_id);
      tr.innerHTML = `
        <td><b>${c.case_id}</b></td>
        <td>${c.complainant.name}<br/><small class="text-mono" style="color: #616161;">${c.complainant.address || c.complainant.contact}</small></td>
        <td><b>${c.department}</b> <span class="badge" style="background:#E8F5E9; color:#1B5E20;">ML</span></td>
        <td><small class="text-mono">REF: ${c.application_ref_no || 'N/A'}<br/>SUBMITTED: ${c.original_submission_date || 'N/A'}</small></td>
        <td>${c.suggested_pio.pio_name}<br/><small class="text-mono">${c.suggested_pio.office_address}</small></td>
        <td><span class="badge">${c.confidence.overall}% Match</span></td>
        <td><span class="badge ${c.status === 'APPROVED' ? 'badge-live' : (c.status === 'MERGED_DUPLICATE' ? 'badge-risk' : '')}">${c.status}</span></td>
        <td><button class="btn btn-sm btn-primary" onclick="event.stopPropagation(); openCaseById('${c.case_id}')">REVIEW REPORT →</button></td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    console.error("Failed to load/filter queue:", err);
  }
}

async function openCaseById(caseId) {
  try {
    const res = await fetch(`${API_BASE}/cases/${caseId}`);
    if (res.status === 503) {
      handleKillSwitchTriggered();
      return;
    }
    const data = await res.json();
    if (res.ok) {
      openCaseWorkspace(data.case);
    }
  } catch (err) {
    console.error("Error loading case:", err);
  }
}

// Workspace Renderer
function openCaseWorkspace(c) {
  currentCase = c;
  document.getElementById("noCaseSelected").classList.add("hidden");
  document.getElementById("caseWorkspaceView").classList.remove("hidden");

  document.getElementById("viewCaseId").textContent = c.case_id;
  document.getElementById("viewCaseStatus").textContent = c.status;
  document.getElementById("viewRiskBadge").textContent = `${c.confidence.risk_level} RISK`;
  document.getElementById("viewSla").textContent = `${c.sla_days_remaining || 30} DAYS`;
  document.getElementById("viewComplainant").textContent = c.complainant.name;

  document.getElementById("viewRawGrievance").textContent = `"${c.raw_grievance}"`;
  document.getElementById("viewRefNo").textContent = c.application_ref_no || "Not Provided";
  document.getElementById("viewSubDate").textContent = c.original_submission_date || "Unconfirmed";

  // In-place edit input values
  document.getElementById("editComplainantName").value = c.complainant.name;
  document.getElementById("editComplainantContact").value = c.complainant.contact || "";
  document.getElementById("editComplainantAddr").value = c.complainant.address || "";

  document.getElementById("editRefNo").value = c.application_ref_no && c.application_ref_no !== "Not Provided" ? c.application_ref_no : "";
  document.getElementById("editSubDate").value = c.original_submission_date && c.original_submission_date !== "Unconfirmed" ? c.original_submission_date : "";

  document.getElementById("viewPioName").textContent = c.suggested_pio.pio_name;
  document.getElementById("viewPioDept").textContent = `${c.suggested_pio.department} (ML PREDICTED)`;
  document.getElementById("viewPioAddr").textContent = c.suggested_pio.office_address;

  if (c.confidence.ml_prediction_reason) {
    document.getElementById("viewMlReason").textContent = `Reason: ${c.confidence.ml_prediction_reason}`;
  } else {
    document.getElementById("viewMlReason").textContent = "";
  }

  document.getElementById("confOverall").textContent = `${c.confidence.overall}%`;
  document.getElementById("confJuris").textContent = `${c.confidence.jurisdiction_confidence}%`;

  // Evidence Gaps
  const gapsBox = document.getElementById("evidenceGapsBox");
  const gapsList = document.getElementById("evidenceGapsList");
  gapsList.innerHTML = "";
  if (c.confidence.evidence_gaps && c.confidence.evidence_gaps.length > 0) {
    gapsBox.classList.remove("hidden");
    c.confidence.evidence_gaps.forEach(g => {
      const li = document.createElement("li");
      li.textContent = g;
      gapsList.appendChild(li);
    });
  } else {
    gapsBox.classList.add("hidden");
  }

  // Draft RTI Form & ML Report Format
  document.getElementById("editDraftSubject").value = c.draft_rti.application_subject;
  document.getElementById("editDraftQuestions").value = c.draft_rti.questions.join("\n");
  document.getElementById("viewMlReportFormat").value = c.ml_report_format || generateClientReport(c);

  // Render Case Timeline & Audit History Table
  const timelineBox = document.getElementById("caseTimelineContainer");
  const historyTbody = document.getElementById("caseHistoryBody");

  if (timelineBox) timelineBox.innerHTML = "";
  if (historyTbody) historyTbody.innerHTML = "";

  if (c.update_history && c.update_history.length > 0) {
    // Render visual timeline steps
    if (timelineBox) {
      let timelineHtml = `<div style="font-weight: bold; font-family: var(--font-display); font-size: 13px; color: var(--accent-terracotta); margin-bottom: 10px;">TIMELINE AUDIT TRAIL FOR CASE ${c.case_id}:</div>`;
      timelineHtml += `<div style="display: flex; flex-direction: column; gap: 10px;">`;
      
      c.update_history.forEach((h, idx) => {
        timelineHtml += `
          <div style="display: flex; gap: 12px; align-items: flex-start; padding: 8px 12px; background: #FFF; border: 1px solid var(--border-color); border-left: 4px solid ${idx === c.update_history.length - 1 ? '#D94E28' : '#1E242B'}; border-radius: 4px;">
            <div style="font-family: var(--font-mono); font-size: 11px; min-width: 140px; color: #555;">${h.timestamp}</div>
            <div style="flex: 1;">
              <div style="font-weight: bold; font-size: 12px;">
                <span class="badge" style="background:#E3F2FD; color:#0D47A1; margin-right: 6px;">STEP 0${idx+1}</span>
                <span style="color: var(--text-color);">${h.update_type}</span> — <span style="color: #616161;">${h.actor}</span>
              </div>
              <div style="font-size: 11px; color: #424242; margin-top: 2px;">
                <b>Field Changed:</b> ${h.field_changed} &nbsp;|&nbsp; <b>Old:</b> <code>${h.old_value}</code> &rarr; <b>New:</b> <code>${h.new_value}</code>
              </div>
              ${h.remarks ? `<div style="font-size: 11px; color: #616161; font-style: italic; margin-top: 2px;">"${h.remarks}"</div>` : ''}
            </div>
          </div>
        `;
      });
      timelineHtml += `</div>`;
      timelineBox.innerHTML = timelineHtml;
    }

    c.update_history.forEach(h => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td class="text-mono">${h.timestamp}</td>
        <td><span class="badge" style="background:#FFF3E0; color:#E65100;">${h.update_type}</span></td>
        <td><b>${h.actor}</b></td>
        <td>${h.field_changed}</td>
        <td><small class="text-mono">Old: ${h.old_value}<br/>New: <b>${h.new_value}</b></small></td>
        <td><small style="color:#616161;">${h.remarks || 'No remarks logged'}</small></td>
      `;
      historyTbody.appendChild(tr);
    });
  } else {
    if (timelineBox) timelineBox.innerHTML = `<div class="text-mono">No update history recorded yet.</div>`;
    if (historyTbody) historyTbody.innerHTML = `<tr><td colspan="6" class="text-mono">No update history recorded yet.</td></tr>`;
  }

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
    document.getElementById("approveBtn").textContent = "CASE APPROVED & DISPATCHED ✓";
  } else {
    proofBox.classList.add("hidden");
    document.getElementById("approveBtn").disabled = false;
    document.getElementById("approveBtn").textContent = "APPROVE & RELEASE FINAL RTI DISPATCH →";
  }

  switchToTab("workspace");
}

function generateClientReport(c) {
  return `================================================================================
           ARZI ML LEGAL RTI INTELLIGENCE & ASSESSMENT REPORT
================================================================================
[CASE ID]: ${c.case_id}
[COMPLAINANT]: ${c.complainant.name}
[DEPARTMENT]: ${c.department}
[PIO]: ${c.suggested_pio.pio_name} (${c.suggested_pio.office_address})

SUBJECT:
${c.draft_rti.application_subject}

QUESTIONS SOUGHT:
${c.draft_rti.questions.join("\n")}
================================================================================`;
}

function copyMlReport() {
  const reportBox = document.getElementById("viewMlReportFormat");
  reportBox.select();
  navigator.clipboard.writeText(reportBox.value);
  alert("Full ML Legal RTI Assessment Report copied to clipboard!");
}

// In-Place Complainant Correction Fix
async function submitInplaceComplainantFix() {
  if (!currentCase) return;

  const newName = document.getElementById("editComplainantName").value.trim();
  const newContact = document.getElementById("editComplainantContact").value.trim();
  const newAddress = document.getElementById("editComplainantAddr").value.trim();
  const reviewer = document.getElementById("reviewerName").value.trim();

  if (!newName) {
    alert("Complainant name cannot be empty.");
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/cases/${currentCase.case_id}/update-complainant`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        complainant_name: newName,
        complainant_contact: newContact,
        complainant_address: newAddress,
        reviewer: reviewer || "Adv. S. Kalra (Legal NGO)"
      })
    });

    if (res.status === 503) {
      handleKillSwitchTriggered();
      return;
    }

    const data = await res.json();
    if (res.ok) {
      alert(`In-place update success! Complainant name corrected to "${newName}" on Master Case ${currentCase.case_id}. No duplicate case spawned.`);
      openCaseWorkspace(data.case);
      loadRunLogs();
    } else {
      alert(`Error: ${data.message}`);
    }
  } catch (err) {
    console.error("In-place fix error:", err);
  }
}

// Merge Duplicate Cases
async function mergeDuplicateCase() {
  if (!currentCase) return;
  const duplicateId = document.getElementById("duplicateCaseIdInput").value.trim();
  const reviewer = document.getElementById("reviewerName").value.trim();

  if (!duplicateId) {
    alert("Please enter the duplicate case ID to merge.");
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/cases/merge-duplicates`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        master_case_id: currentCase.case_id,
        duplicate_case_id: duplicateId,
        reviewer: reviewer || "Adv. S. Kalra (Legal NGO)"
      })
    });

    if (res.status === 503) {
      handleKillSwitchTriggered();
      return;
    }

    const data = await res.json();
    if (res.ok) {
      alert(`Duplicate case ${duplicateId} successfully merged into Master Case ${currentCase.case_id}!`);
      openCaseWorkspace(data.master_case);
      loadCaseQueue();
      loadRunLogs();
    } else {
      alert(`Error: ${data.message}`);
    }
  } catch (err) {
    console.error("Merge error:", err);
  }
}

// On-Demand Dispatch Report for Lawyer
async function dispatchUpdateReport() {
  if (!currentCase) return;
  const reviewer = document.getElementById("reviewerName").value.trim();

  try {
    const res = await fetch(`${API_BASE}/cases/${currentCase.case_id}/dispatch-update-report`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ reviewer: reviewer || "Adv. S. Kalra (Legal NGO)" })
    });

    if (res.status === 503) {
      handleKillSwitchTriggered();
      return;
    }

    const data = await res.json();
    if (res.ok) {
      alert(`On-demand dispatch report generated & dispatched for victim: ${currentCase.complainant.name}! Dispatch ID: ${data.dispatch_info.dispatch_id}`);
      openCaseWorkspace(data.case);
      loadRunLogs();
    } else {
      alert(`Error: ${data.message}`);
    }
  } catch (err) {
    console.error("Dispatch update report error:", err);
  }
}

// Legal Approval
async function approveCurrentCase() {
  if (!currentCase) return;

  const reviewer = document.getElementById("reviewerName").value.trim();
  const notes = document.getElementById("reviewerNotes").value.trim();
  const subject = document.getElementById("editDraftSubject").value.trim();
  const questionsRaw = document.getElementById("editDraftQuestions").value.trim();
  const refNo = document.getElementById("editRefNo").value.trim();
  const subDate = document.getElementById("editSubDate").value.trim();

  const questions = questionsRaw.split("\n").filter(q => q.trim().length > 0);

  const payload = {
    reviewer: reviewer || "Adv. NGO Reviewer",
    notes: notes || "Approved for filing",
    application_ref_no: refNo,
    original_submission_date: subDate,
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

    if (res.status === 503) {
      handleKillSwitchTriggered();
      return;
    }

    const data = await res.json();
    if (res.ok) {
      alert(`Case ${currentCase.case_id} approved and dispatched!`);
      openCaseWorkspace(data.case);
      loadRunLogs();
    } else {
      alert(`Error: ${data.message}`);
    }
  } catch (err) {
    console.error("Approval error:", err);
  }
}

// Lawyer Override Metadata & Department
async function submitOverride() {
  if (!currentCase) return;
  const dept = document.getElementById("overrideDeptSelect").value;
  const refNo = document.getElementById("editRefNo").value.trim();
  const subDate = document.getElementById("editSubDate").value.trim();
  const reviewer = document.getElementById("reviewerName").value.trim();

  try {
    const res = await fetch(`${API_BASE}/cases/${currentCase.case_id}/override`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ department: dept, application_ref_no: refNo, original_submission_date: subDate, reviewer: reviewer || "Legal Reviewer" })
    });

    if (res.status === 503) {
      handleKillSwitchTriggered();
      return;
    }

    const data = await res.json();
    if (res.ok) {
      alert(`Lawyer updated metadata & regenerated report for: ${dept}`);
      openCaseWorkspace(data.case);
      loadRunLogs();
    }
  } catch (err) {
    console.error("Override error:", err);
  }
}

function viewPdf() {
  if (!currentCase) return;
  window.open(`${API_BASE}/cases/${currentCase.case_id}/pdf`, "_blank");
}

// Run Log
async function loadRunLogs() {
  try {
    const res = await fetch(`${API_BASE}/run-log`);
    if (res.status === 503) {
      handleKillSwitchTriggered();
      return;
    }
    const data = await res.json();
    if (!res.ok) return;

    const tbody = document.getElementById("runLogBody");
    tbody.innerHTML = "";

    data.run_logs.forEach(log => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td class="text-mono">${log.timestamp}</td>
        <td><span class="badge">${log.event_type}</span></td>
        <td><b>${log.case_id}</b></td>
        <td>${log.actor}</td>
        <td>${log.action}<br/><small class="text-mono">Result: ${log.result}</small></td>
        <td class="text-mono">${log.correlation_id}</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    console.error("Run log load error:", err);
  }
}

// ML Model Pipeline Inference
async function runMlInference(event) {
  event.preventDefault();

  const reqId = document.getElementById("mlReqId").value.trim();
  const rawText = document.getElementById("mlText").value.trim();

  try {
    const res = await fetch(`${API_BASE}/process`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ request_id: reqId, raw_text: rawText })
    });

    if (res.status === 503) {
      handleKillSwitchTriggered();
      return;
    }

    let data;
    if (res.status === 400) {
      data = { status: "REJECTED_INPUT", rejection_reason: "Malformed or suspicious payload characters detected." };
    } else {
      data = await res.json();
    }

    const box = document.getElementById("mlResultBox");
    const content = document.getElementById("mlResultContent");
    box.classList.remove("hidden");

    content.innerHTML = `
      <div>STATUS: <b>${data.status}</b></div>
      <div>REQUEST ID: <b>${reqId}</b></div>
      <div>CONFIDENCE SCORE: <b>${data.confidence ? data.confidence.confidence_score : '0.00'} (${data.confidence ? data.confidence.confidence_level : 'N/A'})</b></div>
      <div>LATENCY: <b>${data.execution_time_ms || 0} ms</b></div>
      ${data.output ? `<div>GENERATED GROUNDED ANSWER: <i>"${data.output.generation}"</i></div>` : ''}
    `;
  } catch (err) {
    console.error("ML Inference error:", err);
  }
}

// Run Full Dataset Test Suite
async function runDatasetTestSuite() {
  const dataset = [
    { id: "test-001", text: "Can you provide a summary of project status?", expected: "PROCESS_EXECUTION_SUCCESS" },
    { id: "test-002", text: "CLAIM YOUR FREE MONEY WINNER", expected: "REJECTED_SPAM" },
    { id: "test-003", text: "Can you provide a summary of project status?", expected: "SHORT_CIRCUIT_DUPLICATE" },
    { id: "test-004", text: "drop table users;", expected: "REJECTED_INPUT" }
  ];

  let passed = 0;
  const container = document.getElementById("datasetResultsBox");
  container.innerHTML = "";

  for (let item of dataset) {
    let actual = "";
    try {
      const res = await fetch(`${API_BASE}/process`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ request_id: item.id, raw_text: item.text })
      });

      if (res.status === 400) {
        actual = "REJECTED_INPUT";
      } else {
        const data = await res.json();
        actual = data.status;
      }
    } catch (e) {
      actual = "CONNECTION_ERROR";
    }

    const isPass = actual === item.expected;
    if (isPass) passed++;

    const div = document.createElement("div");
    div.className = "preset-box";
    div.innerHTML = `
      <div class="preset-title">${item.id}: ${item.text}</div>
      <div class="preset-text">Expected: <code>${item.expected}</code> &nbsp;|&nbsp; Actual: <code>${actual}</code> &nbsp; <b style="color: ${isPass ? '#2E7D32' : '#C62828'}">${isPass ? '[PASS]' : '[FAIL]'}</b></div>
    `;
    container.appendChild(div);
  }

  const badge = document.getElementById("accuracyBadge");
  badge.classList.remove("hidden");
  const pct = ((passed / dataset.length) * 100).toFixed(1);
  document.getElementById("accuracyScore").textContent = `${pct}% ACCURACY`;
  document.getElementById("accuracyDetails").textContent = `${passed}/${dataset.length} Test Cases Passed`;
}

// Kill Switch System Controls
async function toggleKillSwitch(simulate) {
  try {
    const res = await fetch(`${API_BASE}/system/kill-switch`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ simulate_deleted: simulate })
    });

    const data = await res.json();
    if (simulate) {
      handleKillSwitchTriggered(data.repository_validation.status_message);
    } else {
      document.getElementById("killSwitchBanner").classList.add("hidden");
      document.getElementById("repoStatusText").textContent = "GITHUB REPO: LIVE";
      alert("System integrity restored. Kill-switch disengaged.");
      loadCaseQueue();
    }
  } catch (err) {
    console.error("Kill switch error:", err);
  }
}

function handleKillSwitchTriggered(msg) {
  document.getElementById("killSwitchBanner").classList.remove("hidden");
  document.getElementById("repoStatusText").textContent = "GITHUB REPO: DELETED (503)";
  if (msg) {
    document.getElementById("killSwitchMessage").textContent = msg;
  }
}
