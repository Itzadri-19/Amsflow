const grid = document.getElementById("grid");

const squareSize = 70;
const squareGap = 5;
const cols = Math.floor(window.innerWidth / (squareSize + squareGap));
const rows = Math.floor(window.innerHeight / (squareSize + squareGap));

const squares = [];

for (let r = 0; r < rows; r++) {
  for (let c = 0; c < cols; c++) {
    const square = document.createElement("div");
    square.classList.add("square");
    square.dataset.row = r;
    square.dataset.col = c;
    grid.appendChild(square);
    squares.push(square);
  }
}

squares.forEach((square) => {
  square.addEventListener("mouseenter", () => {
    square.classList.add("active");
    setTimeout(() => square.classList.remove("active"), 650);
  });
});

document.getElementById("login-form").addEventListener("submit", function (e) {
  e.preventDefault();

  const correo = document.getElementById("correo").value;
  const contraseña = document.getElementById("contrasegna").value;

  fetch("/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ correo, contrasegna: contraseña })
  })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        localStorage.setItem("nombreUsuario", data.nombre); // Guarda el nombre del usuario
        window.location.href = "/inicio";
      } else {
        document.getElementById("error-message").style.display = "block";
      }
    })
    .catch(err => console.error("Error al hacer login:", err));
});
