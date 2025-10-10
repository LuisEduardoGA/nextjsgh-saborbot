const API_URL = "http://localhost:8000"; // cambia por tu API Gateway

async function login(email, password) {
  const response = await fetch(`${API_URL}/auth`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password })
  });

  if (!response.ok) {
    throw new Error("Credenciales inválidas");
  }

  const data = await response.json();
  localStorage.setItem("token", data.access_token);
  return data;
}

function getToken() {
  return localStorage.getItem("token");
}

function logout() {
  localStorage.removeItem("token");
  window.location.href = "index.html";
}
