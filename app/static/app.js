async function upload(event) {
  if (event) event.preventDefault();

  const status = document.getElementById("status");
  const input = document.getElementById("file_url");
  const fileUrl = input.value.trim();

  if (!fileUrl) {
    status.innerText = "Please provide a CSV URL.";
    return;
  }

  status.innerText = "Queuing import...";

  const res = await fetch("/upload", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ file_url: fileUrl }),
  });

  if (!res.ok) {
    status.innerText = "Failed to queue job.";
    return;
  }

  const { job_id } = await res.json();
  status.innerText = "Import started...";

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
