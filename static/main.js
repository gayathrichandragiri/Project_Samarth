async function ask(){
  const q = document.getElementById('q').value;
  const res = await fetch('/api/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:q})});
  const j = await res.json();
  document.getElementById('out').textContent = JSON.stringify(j, null, 2);
}
