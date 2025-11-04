const backendURL = "http://127.0.0.1:8000";
const analyzeBtn = document.getElementById("analyzeBtn");
const resultDiv = document.getElementById("result");

let uploadedId = null;

analyzeBtn.addEventListener("click", async () => {
  const fileInput = document.getElementById("resumeFile");
  const jobDesc = document.getElementById("jobDescription").value;

  if (!fileInput.files[0]) return alert("Please upload a resume first!");
  if (!jobDesc.trim()) return alert("Please enter a job description!");

  // Step 1: Upload resume
  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  resultDiv.innerHTML = "<p>Uploading and analyzing... </p>";

  try {
    const uploadRes = await fetch(`${backendURL}/api/v1/resumes/upload`, {
      method: "POST",
      body: formData,
    });

    const uploadData = await uploadRes.json();
    uploadedId = uploadData.id;

    if (!uploadedId) throw new Error("Upload failed");

    // Step 2: Match with job description
    const matchForm = new FormData();
    matchForm.append("job_description", jobDesc);

    const matchRes = await fetch(`${backendURL}/api/v1/resumes/${uploadedId}/match`, {
      method: "POST",
      body: matchForm,
    });

    const matchData = await matchRes.json();

    // Step 3: Display result
    // Step 3: Display result
resultDiv.innerHTML = `
  <h3> Resume Analysis Complete</h3>
  <p><strong>File:</strong> ${matchData.file}</p>
  <p><strong>Match Score:</strong> ${matchData.match_score}%</p>
  <p><strong>Matching Skills:</strong> ${matchData.matching_skills?.length > 0 ? matchData.matching_skills.join(", ") : "None"}</p>
  <p><strong>Skills Found in Resume:</strong> ${matchData.skills_found?.join(", ")}</p>
  <p><strong>Suggestion:</strong> ${matchData.suggestion}</p>
`;

  } catch (err) {
    console.error(err);
    resultDiv.innerHTML = `<p> Error: ${err.message}</p>`;
  }
});
