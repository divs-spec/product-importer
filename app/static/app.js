async function upload() {
  const file = document.getElementById("file").files[0];
  const status = document.getElementById("status");

  const form = new FormData();
  form.append("file", file);

  // Start upload
  const res = await fetch("/upload", {
    method: "POST",
    body: form,
  });

  const { job_id } = await res.json();

  // ----------------------------
  // REPLACE POLLING WITH SSE
  // ----------------------------
  const es = new EventSource(`/jobs/${job_id}/events`);

  es.onmessage = (e) => {
    const j = JSON.parse(e.data);
    status.innerText = `${j.status}: ${j.processed}/${j.total}`;

    if (j.status === "completed" || j.status === "failed") {
      es.close();
    }
  };

  es.onerror = () => {
    status.innerText = "Connection lost. Please refresh.";
    es.close();
  };
}
