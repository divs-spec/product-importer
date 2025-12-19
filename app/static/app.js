async function upload() {
  const file = document.getElementById("file").files[0];
  const form = new FormData();
  form.append("file", file);

  const res = await fetch("/upload", { method: "POST", body: form });
  const { job_id } = await res.json();

  const interval = setInterval(async () => {
    const j = await fetch(`/jobs/${job_id}`).then(r => r.json());
    document.getElementById("status").innerText =
      `${j.status} ${j.processed}/${j.total}`;
    if (j.status === "completed" || j.status === "failed") clearInterval(interval);
  }, 1000);
}

